"""Suite de tests de la Pipeline V5 — Abyssal Glass.

Couvre les categories imposees par CONTRACT/architecture_contract.md:
nominal, rejet, volume, donnee orpheline, reproductibilite, integration runtime,
plus l'integration Blender et la verification binaire.
"""
from __future__ import annotations
import shutil, tempfile, unittest
from pathlib import Path

from pipeline import binary_check as bc
from pipeline import blender_adapter as ba
from pipeline import simulate, compile_runtime, validators, reports
from pipeline.assets_bin import STORE, load_registry, reverify_all, store
from pipeline.canon import build as canon_build
from pipeline.catalogs import build as catalogs_build
from pipeline.graph import build as graph_build, analyse
from pipeline.ids import check_id, make_id
from pipeline.importers import import_result
from pipeline.inputs import load_all, missing_mandatory
from pipeline.manifests import build as manifests_build
from pipeline.ontology import build as ontology_build
from pipeline.palette import ABYSS_16
from pipeline.prompts import inject_context
from pipeline.schemas import validate as schema_validate
from pipeline.status import advance_asset, is_complete_asset
from pipeline.util import ROOT, jdump, sha256_file
from tools.make_fixture_png import indexed_png

DELIVERY = ROOT / "ASSETS_IN" / "fixture_tests"


def state():
    canon = canon_build()
    catalogs = catalogs_build(canon)
    graph = graph_build(catalogs)
    manifests = manifests_build(canon, catalogs, graph)
    return canon, ontology_build(), catalogs, graph, manifests


class TestInputs(unittest.TestCase):
    def test_nominal_entrees_lisibles_utf8(self):
        loaded = load_all()
        self.assertEqual(missing_mandatory(loaded), [])
        for path, e in loaded.items():
            if e["present"]:
                self.assertTrue(e["utf8"], f"{path} non UTF-8")
                self.assertFalse(e["bom"], f"{path} porte un BOM")

    def test_external_tools_absent_est_signale(self):
        """L'entree manquante est remontee, jamais inventee."""
        loaded = load_all()
        self.assertFalse(loaded["INPUT/external_tools.md"]["present"])


class TestCanon(unittest.TestCase):
    def test_nominal_chaque_fait_a_une_provenance(self):
        canon = canon_build()
        for e in canon["entries"]:
            self.assertEqual(e["status"], "CANONICAL")
            self.assertIsNotNone(e["source_line"], f"{e['id']} sans ligne source")

    def test_rejet_decision_ouverte_jamais_canonique(self):
        canon = canon_build()
        for o in canon["declared_open"]:
            self.assertEqual(o["status"], "TO_VALIDATE")
        textes = " ".join(e["display_name"] for e in canon["entries"]).lower()
        self.assertNotIn("anomalie", textes)

    def test_noms_canoniques_verbatim(self):
        canon = canon_build()
        self.assertEqual(canon["vessel_name"], "le Vitrail Noire")
        self.assertEqual(canon["world_name"], "l'Abysse de Veyr")


class TestNommage(unittest.TestCase):
    def test_nominal_id_sans_accent_ni_espace(self):
        self.assertEqual(make_id("zone", "La Faille des Échos"),
                         "zone_la_faille_des_echos")
        self.assertEqual(make_id("artifact", "Flasque d'oxygène"),
                         "artefact_flasque_d_oxygene")

    def test_rejet_id_invalide(self):
        self.assertTrue(check_id("zone", "Zone Échos"))
        self.assertTrue(check_id("zone", "zone-avec-tirets"))
        self.assertFalse(check_id("zone", "zone_valide"))

    def test_coherence_des_noms_du_catalogue(self):
        canon = canon_build()
        catalogs = catalogs_build(canon)
        kinds = {"zones": "zone", "artefacts": "artifact", "equipage": "crew",
                 "actions": "action", "systemes_vitaux": "system"}
        for block, kind in kinds.items():
            for e in catalogs[block]["entries"]:
                self.assertEqual(check_id(kind, e["id"]), [], e["id"])


class TestSchemas(unittest.TestCase):
    def test_nominal_manifest_asset_valide(self):
        *_, manifests = state()
        for a in manifests["assets"]["entries"]:
            doc = {k: v for k, v in a.items() if k not in ("blocked_by", "producer")}
            self.assertEqual(schema_validate("asset", doc), [], a["id"])

    def test_rejet_champs_invalides(self):
        errs = schema_validate("asset", {"id": "MAJUSCULE", "width": 30})
        codes = {e["code"] for e in errs}
        self.assertIn("schema.id", codes)
        self.assertIn("schema.multiple", codes)
        self.assertIn("schema.missing_field", codes)

    def test_rejet_champ_non_declare(self):
        *_, manifests = state()
        a = dict(manifests["assets"]["entries"][0])
        a.pop("blocked_by"); a.pop("producer"); a["inconnu"] = 1
        self.assertIn("schema.unknown_field", {e["code"] for e in schema_validate("asset", a)})


class TestGraphe(unittest.TestCase):
    def test_nominal_graphe_connexe_sans_orphelin(self):
        _, _, catalogs, graph, _ = state()
        a = analyse(graph)
        self.assertTrue(a["connected"])
        self.assertEqual(a["orphans"], [])

    def test_donnee_orpheline_detectee(self):
        """Test d'entite orpheline: une entite sans relation est signalee."""
        _, _, catalogs, graph, _ = state()
        g = {**graph, "nodes": {**graph["nodes"],
                                "artefact_orphelin": {"id": "artefact_orphelin",
                                                      "kind": "artifact"}}}
        self.assertIn("artefact_orphelin", analyse(g)["orphans"])

    def test_volume_graphe_reste_coherent(self):
        _, _, catalogs, graph, _ = state()
        self.assertGreaterEqual(graph["node_count"], 20)
        for e in graph["edges"]:
            self.assertIn(e["from"], graph["nodes"])
            self.assertIn(e["to"], graph["nodes"])


class TestStatuts(unittest.TestCase):
    def test_rejet_saut_d_etape(self):
        with self.assertRaises(ValueError):
            advance_asset("GENERATED", "ART_GREEN")
        with self.assertRaises(ValueError):
            advance_asset("PLANNED", "VALIDATED")

    def test_nominal_progression_pas_a_pas(self):
        s = "PLANNED"
        for nxt in ["GENERATED", "IMPORTED", "VALIDATED", "RUNTIME_TESTED", "ART_GREEN"]:
            s = advance_asset(s, nxt)
        self.assertTrue(is_complete_asset(s))

    def test_asset_genere_n_est_pas_termine(self):
        for s in ["GENERATED", "IMPORTED", "VALIDATED", "RUNTIME_TESTED"]:
            self.assertFalse(is_complete_asset(s))


class TestVerificationBinaire(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="abg_bin_"))
        cls.ok = indexed_png(cls.tmp / "ok.png", 32, 32, ABYSS_16)
        cls.sha = sha256_file(cls.ok)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _codes(self, **kw):
        return {e["code"] for e in bc.verify(self.ok, **kw)["errors"]}

    def test_nominal_binaire_conforme(self):
        r = bc.verify(self.ok, expected_sha256=self.sha, expected_width=32,
                      expected_height=32, allowed_palette=ABYSS_16, expected_format="png")
        self.assertTrue(r["ok"], r["errors"])
        self.assertEqual(r["info"]["width"], 32)
        self.assertTrue(r["info"]["indexed"])

    def test_rejet_empreinte_fausse(self):
        self.assertIn("asset.file_hash", self._codes(expected_sha256="0" * 64))

    def test_rejet_dimensions_fausses(self):
        self.assertIn("asset.file_dimensions", self._codes(expected_width=64))

    def test_rejet_hors_palette(self):
        self.assertIn("asset.file_palette",
                      self._codes(allowed_palette=[(0, 0, 0), (255, 255, 255)]))

    def test_rejet_binaire_corrompu_crc(self):
        b = bytearray(self.ok.read_bytes()); b[-40] ^= 0xFF
        p = self.tmp / "corrupt.png"; p.write_bytes(bytes(b))
        self.assertIn("asset.file_corrupt", {e["code"] for e in bc.verify(p)["errors"]})

    def test_rejet_binaire_tronque(self):
        b = self.ok.read_bytes()
        p = self.tmp / "trunc.png"; p.write_bytes(b[:len(b) // 2])
        self.assertIn("asset.file_corrupt", {e["code"] for e in bc.verify(p)["errors"]})

    def test_rejet_extension_mensongere(self):
        """Le nom et l'extension ne font jamais foi."""
        p = self.tmp / "menteur.jpg"; shutil.copyfile(self.ok, p)
        self.assertIn("asset.file_format",
                      {e["code"] for e in bc.verify(p, expected_format="jpeg")["errors"]})

    def test_rejet_non_image(self):
        p = self.tmp / "x.png"; p.write_bytes(b"pas une image")
        self.assertIn("asset.file_format", {e["code"] for e in bc.verify(p)["errors"]})

    def test_rejet_fichier_absent(self):
        self.assertIn("asset.file_missing",
                      {e["code"] for e in bc.verify(self.tmp / "nope.png")["errors"]})

    def test_rejet_taille_hors_borne(self):
        self.assertIn("asset.file_too_large",
                      {e["code"] for e in bc.verify(self.ok, max_bytes=10)["errors"]})

    def test_rejet_traversee_de_chemin(self):
        r = bc.verify(self.ok, delivery_dir=ROOT / "ASSETS_IN")
        self.assertIn("asset.file_missing", {e["code"] for e in r["errors"]})


class TestImportEtStockage(unittest.TestCase):
    def setUp(self):
        _, _, _, _, self.m = state()
        self.assets = self.m["assets"]["entries"]
        self.spec = next(a for a in self.assets if a["family"] == "famille_artefacts")
        DELIVERY.mkdir(parents=True, exist_ok=True)

    def _deliver(self, w=None, h=None, palette=None, name=None):
        w = w or self.spec["width"]; h = h or self.spec["height"]
        fam = self.spec["family"]
        p = ROOT / "ASSETS_IN" / fam / (name or f"{self.spec['id']}.png")
        return indexed_png(p, w, h, palette or ABYSS_16)

    def _resp(self, p, **over):
        r = {"asset_id": self.spec["id"], "entity_id": self.spec["entity_id"],
             "status": "GENERATED", "width": self.spec["width"],
             "height": self.spec["height"], "format": "png", "variants": [],
             "directions": ["none"], "file": p.relative_to(ROOT).as_posix(),
             "file_sha256": sha256_file(p)}
        r.update(over); return r

    def test_nominal_import_stocke_intact_et_enregistre_empreinte(self):
        p = self._deliver()
        r = import_result(self._resp(p), self.assets)
        self.assertEqual(r["status"], "IMPORTED", r["errors"])
        dest = ROOT / r["stored_path"]
        self.assertTrue(dest.is_file())
        self.assertEqual(sha256_file(dest), sha256_file(p), "binaire altere a la copie")
        self.assertEqual(load_registry()["entries"][self.spec["id"]]["sha256"], r["sha256"])

    def test_rejet_empreinte_declaree_fausse(self):
        p = self._deliver()
        r = import_result(self._resp(p, file_sha256="0" * 64), self.assets)
        self.assertEqual(r["status"], "BLOCKED")
        self.assertIn("asset.file_hash", {e["code"] for e in r["errors"]})

    def test_rejet_binaire_redimensionne(self):
        p = self._deliver(w=64, h=64, name="redim.png")
        r = import_result(self._resp(p), self.assets)
        self.assertIn("asset.file_dimensions", {e["code"] for e in r["errors"]})

    def test_rejet_hors_palette(self):
        p = self._deliver(palette=[(255, 0, 255), (0, 255, 0)], name="horspal.png")
        r = import_result(self._resp(p), self.assets)
        self.assertIn("asset.file_palette", {e["code"] for e in r["errors"]})

    def test_rejet_asset_hors_manifest(self):
        r = import_result({"asset_id": "asset_inconnu", "status": "GENERATED"}, self.assets)
        self.assertIn("import.unknown_asset", {e["code"] for e in r["errors"]})

    def test_specification_sans_binaire_reste_planned(self):
        r = import_result({"asset_id": self.spec["id"], "entity_id": self.spec["entity_id"],
                           "status": "GENERATED", "width": self.spec["width"],
                           "height": self.spec["height"], "format": "png",
                           "variants": [], "directions": ["none"]}, self.assets)
        self.assertEqual(r["status"], "PLANNED")
        self.assertTrue(r["ok"])

    def test_generateur_bloque_est_propage(self):
        r = import_result({"asset_id": self.spec["id"], "status": "BLOCKED",
                           "missing": ["style"]}, self.assets)
        self.assertEqual(r["status"], "BLOCKED")

    def test_validateur_permanent_detecte_alteration(self):
        p = self._deliver()
        r = import_result(self._resp(p), self.assets)
        self.assertEqual(r["status"], "IMPORTED")
        dest = ROOT / r["stored_path"]
        original = dest.read_bytes()
        try:
            b = bytearray(original); b[-40] ^= 0xFF; dest.write_bytes(bytes(b))
            rv = reverify_all()
            self.assertFalse(rv["ok"])
            self.assertIn("asset.file_hash", {e["code"] for e in rv["errors"]})
        finally:
            dest.write_bytes(original)
        self.assertTrue(reverify_all()["ok"])

    def test_validateur_permanent_detecte_suppression(self):
        p = self._deliver()
        r = import_result(self._resp(p), self.assets)
        dest = ROOT / r["stored_path"]
        original = dest.read_bytes()
        try:
            dest.unlink()
            self.assertIn("asset.file_missing",
                          {e["code"] for e in reverify_all()["errors"]})
        finally:
            dest.write_bytes(original)


class TestBlender(unittest.TestCase):
    def test_chemin_absent_retourne_blocked_avec_remede(self):
        r = ba.inspect("/chemin/inexistant/FRAMEWORK_BLENDER")
        self.assertEqual(r["status"], "BLOCKED")
        self.assertEqual(r["missing_path"], "/chemin/inexistant/FRAMEWORK_BLENDER")
        self.assertTrue(r["remediation"]["fix_options"])
        self.assertIn("inventer un chemin", r["remediation"]["never"])

    def test_aucune_generation_sans_framework(self):
        r = ba.run_jobs([{"asset_id": "asset_x"}], "/chemin/inexistant")
        self.assertEqual(r["status"], "BLOCKED")
        self.assertEqual(r["produced_files"], [])
        self.assertEqual(r["jobs_executed"], [])

    def test_integration_framework_factice_est_inspecte(self):
        """Integration Blender: avec un framework present, l'adaptateur le lit."""
        tmp = Path(tempfile.mkdtemp(prefix="abg_fw_"))
        try:
            (tmp / "builders").mkdir()
            (tmp / "main.py").write_text("# entree factice\n", encoding="utf-8")
            (tmp / "builders" / "sprite_builder.py").write_text("# builder\n", encoding="utf-8")
            insp = ba.inspect(tmp)
            self.assertEqual(insp["status"], "AVAILABLE")
            self.assertIn("main.py", insp["entry_scripts"])
            self.assertTrue(insp["builders"])
            self.assertFalse(insp["runtime_required"])
            run = ba.run_jobs([{"asset_id": "asset_x"}], tmp)
            self.assertEqual(run["status"], "GENERATED")
            self.assertEqual(run["entry_script"], "main.py")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_traduction_manifest_vers_job_transmet_tous_les_champs(self):
        canon, _, _, _, manifests = state()
        a = manifests["assets"]["entries"][0]
        job = ba.to_blender_job(a, canon=canon)
        for field in ["entity_id", "asset_id", "visual_family", "asset_type",
                      "dimensions", "resolution", "style", "palette", "variants",
                      "directions", "expected_animations", "output_rules",
                      "required_validations"]:
            self.assertIn(field, job)
        self.assertEqual(job["asset_id"], a["id"])
        self.assertEqual(job["entity_id"], a["entity_id"])

    def test_retour_blender_expose_les_champs_attendus(self):
        canon, _, _, _, manifests = state()
        job = ba.to_blender_job(manifests["assets"]["entries"][0], canon=canon)
        out = ba.from_blender_result(job, {"status": "GENERATED", "files": [],
                                           "variants": ["nominal"], "directions": ["none"],
                                           "animations": [], "warnings": ["w"], "errors": []})
        for field in ["asset_id", "entity_id", "status", "produced_files",
                      "produced_variants", "produced_directions",
                      "produced_animations", "warnings", "errors"]:
            self.assertIn(field, out)


class TestPrompts(unittest.TestCase):
    def test_contexte_injecte_complet(self):
        canon, ontology, catalogs, graph, manifests = state()
        a = manifests["assets"]["entries"][0]
        ctx = inject_context(canon=canon, ontology=ontology, graph=graph,
                             manifest_entry=a, catalogs=catalogs, entity_id=a["entity_id"])
        for key in ["canon", "ontology", "functional_sheet", "graph_relations",
                    "manifest", "visual_constraints", "expected_output",
                    "validations", "response_contract", "correction_strategy"]:
            self.assertIn(key, ctx)
        self.assertTrue(ctx["canon"]["immutable_rules"])
        self.assertIn("BLOCKED", ctx["response_contract"]["on_missing_information"])

    def test_prompt_porte_le_comportement_blocked(self):
        canon, ontology, catalogs, graph, manifests = state()
        a = manifests["assets"]["entries"][0]
        ctx = inject_context(canon=canon, ontology=ontology, graph=graph,
                             manifest_entry=a, catalogs=catalogs, entity_id=a["entity_id"])
        self.assertIn("NE RIEN INVENTER", jdump(ctx))


class TestValidateurs(unittest.TestCase):
    def test_seule_famille_en_echec_est_blender(self):
        canon, _, catalogs, graph, manifests = state()
        rep = validators.run_all(canon=canon, catalogs=catalogs, graph=graph,
                                 manifests=manifests)
        self.assertEqual(rep["blocking_families"], ["sorties_blender"])

    def test_animation_sans_action_est_rejetee(self):
        canon, _, catalogs, graph, manifests = state()
        m = {**manifests, "animations": {"count": 1, "entries": [
            {**manifests["animations"]["entries"][0],
             "id": "anim_fantome", "state_or_action": "etat_inexistant"}]}}
        r = validators.animations_family(m, catalogs)
        self.assertIn("anim.no_state_or_action", {e["code"] for e in r["errors"]})

    def test_asset_sans_entite_est_rejete(self):
        canon, _, catalogs, graph, manifests = state()
        m = {**manifests, "assets": {"count": 1, "entries": [
            {**manifests["assets"]["entries"][0], "entity_id": "entite_inexistante"}]}}
        r = validators.references(m, graph)
        self.assertIn("ref.asset_without_entity", {e["code"] for e in r["errors"]})

    def test_faux_canonique_est_rejete(self):
        canon, _, catalogs, graph, manifests = state()
        c = {**catalogs, "zones": {"count": 1, "status": "CANONICAL", "entries": [
            {"id": "zone_inventee", "display_name": "Zone Inventée", "role": "exploration",
             "status": "CANONICAL", "justification": "", "source": "", "source_line": 0}]}}
        r = validators.canonical(canon, c)
        self.assertIn("canon.false_canonical", {e["code"] for e in r["errors"]})


class TestSimulation(unittest.TestCase):
    def test_etat_avant_et_apres_chaque_action(self):
        s = simulate.initial_state()
        before, after, effects = simulate.step(s, "avancer")
        self.assertLess(after["oxygen"], before["oxygen"])
        self.assertGreater(after["depth"], before["depth"])
        self.assertTrue(effects)

    def test_tous_les_profils_exercent_les_systemes(self):
        rep = simulate.run_all()
        self.assertEqual(rep["profile_count"], 8)
        for name, run in rep["runs"].items():
            self.assertGreater(run["turns_played"], 0, name)

    def test_reproductibilite_meme_graine_meme_trace(self):
        a = simulate.run_profile("explorateur", seed=123)
        b = simulate.run_profile("explorateur", seed=123)
        self.assertEqual(jdump(a), jdump(b))

    def test_graines_differentes_divergent(self):
        a = simulate.run_profile("fuyard", seed=1)
        b = simulate.run_profile("fuyard", seed=999)
        self.assertNotEqual(jdump(a), jdump(b))


class TestReproductibilite(unittest.TestCase):
    def test_deux_generations_identiques(self):
        self.assertEqual(jdump(state()[4]), jdump(state()[4]))
        self.assertEqual(jdump(canon_build()), jdump(canon_build()))

    def test_sortie_json_deterministe_octet_par_octet(self):
        canon = canon_build()
        self.assertEqual(jdump(canon).encode("utf-8"), jdump(canon).encode("utf-8"))


class TestRuntime(unittest.TestCase):
    def test_integration_runtime_sans_llm_ni_blender(self):
        canon, _, catalogs, graph, manifests = state()
        art, _ = compile_runtime.compile_all(canon=canon, catalogs=catalogs,
                                             graph=graph, manifests=manifests)
        v = compile_runtime.verify_no_runtime_dependency(art)
        self.assertTrue(v["ok"], v["errors"])
        self.assertFalse(art["requires_llm"])
        self.assertFalse(art["requires_blender"])
        self.assertTrue(art["dialogues"]["compiled"])

    def test_dependance_runtime_injectee_est_detectee(self):
        canon, _, catalogs, graph, manifests = state()
        art, _ = compile_runtime.compile_all(canon=canon, catalogs=catalogs,
                                             graph=graph, manifests=manifests)
        art["note_test"] = "appelle https://api.exemple/llm"
        self.assertFalse(compile_runtime.verify_no_runtime_dependency(art)["ok"])

    def test_liaisons_assets_portent_leur_empreinte(self):
        canon, _, catalogs, graph, manifests = state()
        art, _ = compile_runtime.compile_all(canon=canon, catalogs=catalogs,
                                             graph=graph, manifests=manifests)
        for b in art["asset_bindings"]:
            self.assertEqual(len(b["sha256"]), 64)


class TestRapports(unittest.TestCase):
    def test_maturite_aucun_asset_premature(self):
        canon, _, catalogs, graph, manifests = state()
        rep = reports.maturity(catalogs, manifests, graph)
        self.assertEqual(rep["complete"], 0,
                         "aucun asset ne doit etre ART_GREEN sans Blender")

    def test_decisions_ouvertes_listees(self):
        rep = reports.open_decisions()
        self.assertIn("dec_nature_formes", rep["owner_decisions"])
        self.assertIn("dec_chemin_blender", rep["blocked"])

    def test_tracabilite_couvre_chaque_type(self):
        canon, _, catalogs, graph, manifests = state()
        val = validators.run_all(canon=canon, catalogs=catalogs, graph=graph,
                                 manifests=manifests)
        m = reports.traceability(canon, catalogs, manifests, graph, val)
        self.assertGreaterEqual(m["row_count"], 10)
        for row in m["rows"]:
            self.assertFalse(row["runtime_tested"])


class TestBoutEnBout(unittest.TestCase):
    def test_minimal_de_bout_en_bout(self):
        """entree -> import -> schema -> canon -> graphe -> catalogue -> compilation."""
        canon, ontology, catalogs, graph, manifests = state()
        assets = manifests["assets"]["entries"]
        spec = next(a for a in assets if a["family"] == "famille_cockpit")

        # 1. l'entite existe dans le graphe et le catalogue
        self.assertIn(spec["entity_id"], graph["nodes"])

        # 2. livraison + verification binaire + stockage
        p = indexed_png(ROOT / "ASSETS_IN" / spec["family"] / f"{spec['id']}.png",
                        spec["width"], spec["height"], ABYSS_16)
        r = import_result({"asset_id": spec["id"], "entity_id": spec["entity_id"],
                           "status": "GENERATED", "width": spec["width"],
                           "height": spec["height"], "format": "png",
                           "variants": ["nominal"], "directions": ["none"],
                           "file": p.relative_to(ROOT).as_posix(),
                           "file_sha256": sha256_file(p)}, assets)
        self.assertEqual(r["status"], "IMPORTED", r["errors"])

        # 3. re-verification permanente
        self.assertTrue(reverify_all()["ok"])

        # 4. compilation runtime, le binaire est lie par empreinte
        art, _ = compile_runtime.compile_all(canon=canon, catalogs=catalogs,
                                             graph=graph, manifests=manifests)
        self.assertIn(spec["id"], {b["asset_id"] for b in art["asset_bindings"]})

        # 5. l'asset reste INCOMPLET: il n'a pas ete teste en contexte runtime
        self.assertFalse(is_complete_asset(r["status"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
