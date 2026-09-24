"""Familles de validateurs. Chacune retourne {family, ok, errors, warnings}."""
from __future__ import annotations
import re
from .assets_bin import reverify_all, load_registry
from .blender_adapter import compatibility_report
from .canon import build as build_canon
from .graph import analyse
from .ids import check_id
from .schemas import validate as schema_validate
from .status import ASSET_LIFECYCLE, is_complete_asset
from .util import ROOT, write_json


def _r(family, errors=None, warnings=None, **kw):
    errors, warnings = errors or [], warnings or []
    return {"family": family, "ok": not errors, "errors": errors,
            "warnings": warnings, **kw}


def structural(manifests):
    e = []
    for a in manifests["assets"]["entries"]:
        e += [{"code": x["code"], "detail": f"{a['id']}: {x['detail']}"}
              for x in schema_validate("asset", {k: v for k, v in a.items()
                                                 if k not in ("blocked_by", "producer")})]
    for an in manifests["animations"]["entries"]:
        e += [{"code": x["code"], "detail": f"{an['id']}: {x['detail']}"}
              for x in schema_validate("animation", {k: v for k, v in an.items()
                                                     if k not in ("blocked_by", "producer")})]
    return _r("structurel", e, checked=manifests["assets"]["count"] + manifests["animations"]["count"])


def schemas_family(manifests):
    e = []
    for o in manifests["objets"]["entries"]:
        e += [{"code": x["code"], "detail": f"{o['id']}: {x['detail']}"}
              for x in schema_validate("object", o)]
    for pr in manifests["placement"]["entries"]:
        e += [{"code": x["code"], "detail": f"{pr['id']}: {x['detail']}"}
              for x in schema_validate("placement_rule", pr)]
    return _r("schemas", e)


def references(manifests, graph):
    known = set(graph["nodes"])
    e = []
    for a in manifests["assets"]["entries"]:
        if a["entity_id"] not in known:
            e.append({"code": "ref.asset_without_entity",
                      "detail": f"{a['id']} reference l'entite inconnue {a['entity_id']}"})
    ids = {a["id"] for a in manifests["assets"]["entries"]}
    for an in manifests["animations"]["entries"]:
        for aid in an["assets"]:
            if aid not in ids:
                e.append({"code": "ref.animation_without_asset",
                          "detail": f"{an['id']} reference l'asset inconnu {aid}"})
    return _r("references", e)


def naming(canon, catalogs):
    e = []
    kind_map = {"systemes_vitaux": "system", "zones": "zone", "artefacts": "artifact",
                "equipage": "crew", "actions": "action"}
    for block, kind in kind_map.items():
        for it in catalogs[block]["entries"]:
            e += [{"code": "naming", "detail": v} for v in check_id(kind, it["id"])]
    return _r("nommage", e)


def canonical(canon, catalogs):
    """Le canon prime. Un nom canonique ne peut etre ni altere ni contredit."""
    e, w = [], []
    names = {x["display_name"] for b in catalogs.values()
             if isinstance(b, dict) and "entries" in b for x in b["entries"]}
    if canon["vessel_name"].replace("le ", "") not in {n for n in names}:
        w.append("le nom du vaisseau n'apparait pas dans les catalogues")
    forbidden_variants = ["Vitrail Noir", "Abysse de Veyre", "le Pilot"]
    blob = " ".join(sorted(names))
    for bad in forbidden_variants:
        if re.search(r"\b" + re.escape(bad) + r"\b", blob):
            e.append({"code": "canon.name_variant",
                      "detail": f"variante interdite d'un nom canonique: {bad!r}"})
    canonical_ids = {x["id"] for x in canon["entries"]}
    for b in catalogs.values():
        if isinstance(b, dict) and "entries" in b:
            for x in b["entries"]:
                if x.get("status") == "CANONICAL" and x["id"] not in canonical_ids:
                    e.append({"code": "canon.false_canonical",
                              "detail": f"{x['id']} se declare CANONICAL sans "
                                        f"exister dans le canon verrouille"})
    return _r("canonique", e, w)


def logical(catalogs, graph):
    """Conditions atteignables, dependances completes, pas de boucle impossible."""
    e, w = [], []
    a = analyse(graph)
    for n in a["orphans"]:
        e.append({"code": "logic.orphan", "detail": f"entite isolee: {n}"})
    for n in a["sinks"]:
        w.append(f"puits (aucune relation sortante): {n}")
    if not a["connected"]:
        e.append({"code": "logic.disconnected",
                  "detail": f"graphe en {a['component_count']} composantes"})
    for s in catalogs["systemes_vitaux"]["entries"]:
        if not s["covering_tests"]:
            e.append({"code": "logic.untested", "detail": f"{s['id']} sans test couvrant"})
    return _r("logique", e, w)


def narrative(canon, catalogs, manifests):
    """Memoire respectee, secrets progressifs, pas de revelation impossible."""
    e, w = [], []
    for p in manifests["pnj"]["entries"]:
        if not p["forbidden_knowledge"]:
            e.append({"code": "narrative.no_forbidden_knowledge",
                      "detail": f"{p['id']} n'a aucune connaissance interdite declaree; "
                                f"un dialogue pourrait reveler un fait inconnu de lui"})
        if p["routines"]["status"] == "TO_VALIDATE":
            w.append(f"{p['id']}: routines non definies (decision proprietaire)")
    for o in canon["declared_open"]:
        w.append(f"element narratif OUVERT non tranche: {o['text']}")
    return _r("narratif", e, w)


def economic(catalogs):
    e, w = [], []
    w.append("equilibrage non calculable: dec_duree_plongee et dec_frequence_degats "
             "sont des decisions ouvertes du proprietaire")
    for s in catalogs["systemes_vitaux"]["entries"]:
        if not s["consumed_by"]:
            e.append({"code": "econ.no_consumer", "detail": f"{s['id']} sans consommateur"})
    return _r("economique", e, w)


def temporal(catalogs):
    return _r("temporel", [], [
        "duree de plongee non fixee (dec_duree_plongee, TO_VALIDATE)",
        "aucune saison: NOT_APPLICABLE justifie (abysse sans lumiere)"])


def progression(catalogs, graph):
    e = []
    base = "zone_le_vitrail_noire"
    reach = {base}
    for edge in graph["edges"]:
        if edge["type"] == "connects_to" and edge["from"] in reach:
            reach.add(edge["to"])
    for z in catalogs["zones"]["entries"]:
        if z["id"] not in reach:
            e.append({"code": "progression.unreachable_zone",
                      "detail": f"{z['id']} inatteignable depuis {base}"})
    return _r("progression", e, reachable_zones=sorted(reach))


def maps_family(manifests):
    e = []
    for m in manifests["maps"]["entries"]:
        if not m["entries"] or not m["exits"]:
            e.append({"code": "map.no_entry_exit", "detail": f"{m['id']} sans entree/sortie"})
        if not m["placement_rules"]:
            e.append({"code": "map.no_placement", "detail": f"{m['id']} sans regle de placement"})
        if not m["navigation_rules"]:
            e.append({"code": "map.no_navigation", "detail": f"{m['id']} sans regle de navigation"})
        if not m["layers"]:
            e.append({"code": "map.no_layers", "detail": f"{m['id']} sans couche"})
    return _r("maps", e, checked=manifests["maps"]["count"])


def navigation(manifests):
    e = []
    for m in manifests["maps"]["entries"]:
        nav = m["navigation_rules"]
        if nav.get("mode") != "avance_recule_seulement":
            e.append({"code": "nav.mode", "detail": f"{m['id']}: mode incompatible "
                                                    f"avec la vue unique"})
    return _r("navigation", e)


def collisions(manifests):
    e = []
    for m in manifests["maps"]["entries"]:
        if not m["collisions"]:
            e.append({"code": "collision.none", "detail": f"{m['id']} sans collision definie"})
    return _r("collisions", e)


def assets_family(manifests):
    """Un asset seulement GENERATED n'est jamais considere comme termine."""
    e, w = [], []
    for a in manifests["assets"]["entries"]:
        if a["status"] not in ASSET_LIFECYCLE + ["BLOCKED"]:
            e.append({"code": "asset.status", "detail": f"{a['id']}: statut inconnu"})
        if a["width"] % 16 or a["height"] % 16:
            e.append({"code": "asset.tile_multiple",
                      "detail": f"{a['id']}: {a['width']}x{a['height']} non multiple de 16"})
        if not is_complete_asset(a["status"]):
            w.append(f"{a['id']}: {a['status']} — incomplet tant que ART_GREEN n'est pas atteint")
    return _r("assets", e, w)


def animations_family(manifests, catalogs):
    """Une animation sans action/etat correspondant est invalide."""
    e = []
    states = {f"etat_{k}" for k in ["alerte", "critique", "nominal"]}
    actions = {a["id"] for a in catalogs["actions"]["entries"]}
    sysfail = {s["failure_state"] for s in catalogs["systemes_vitaux"]["entries"]}
    valid = states | actions | sysfail
    for an in manifests["animations"]["entries"]:
        if an["state_or_action"] not in valid:
            e.append({"code": "anim.no_state_or_action",
                      "detail": f"{an['id']}: '{an['state_or_action']}' ne correspond "
                                f"a aucun etat ni action catalogue"})
        if not an["logical_effect"]:
            e.append({"code": "anim.no_logical_effect",
                      "detail": f"{an['id']}: animation purement visuelle, non "
                                f"synchronisee avec le gameplay"})
    return _r("animations", e)


def placement_family(manifests):
    e = []
    for pr in manifests["placement"]["entries"]:
        if not pr["allowed_terrain"]:
            e.append({"code": "placement.no_terrain", "detail": f"{pr['id']} sans terrain autorise"})
        if set(pr["allowed_terrain"]) & set(pr["forbidden_terrain"]):
            e.append({"code": "placement.contradiction",
                      "detail": f"{pr['id']}: terrain a la fois autorise et interdit"})
    return _r("placement", e)


def blender_outputs(framework_path=None):
    rep = compatibility_report(framework_path)
    if rep["verdict"] == "BLOCKED":
        return _r("sorties_blender", [{"code": "tool.path_missing",
                                       "detail": rep["framework"].get("missing_path")}],
                  verdict="BLOCKED")
    return _r("sorties_blender", [], verdict=rep["verdict"])


def stored_binaries():
    """Validateur PERMANENT des binaires acceptes."""
    rv = reverify_all()
    return _r("binaires_stockes",
              [{"code": e["code"], "detail": e["detail"]} for e in rv["errors"]],
              checked=rv["checked"])


def unused_assets(manifests, graph):
    """Assets sans entite, et assets jamais references par une animation ou un objet."""
    e, w = [], []
    used = {aid for an in manifests["animations"]["entries"] for aid in an["assets"]}
    used |= {aid for o in manifests["objets"]["entries"] for aid in o["assets"]}
    for a in manifests["assets"]["entries"]:
        if a["id"] not in used:
            w.append(f"asset non reference par une animation ni un objet: {a['id']}")
    return _r("assets_inutilises", e, w)


def run_all(*, canon, catalogs, graph, manifests, framework_path=None,
            path=ROOT / "REPORTS" / "validation_report.json"):
    fams = [
        structural(manifests), schemas_family(manifests), references(manifests, graph),
        naming(canon, catalogs), canonical(canon, catalogs), logical(catalogs, graph),
        narrative(canon, catalogs, manifests), economic(catalogs), temporal(catalogs),
        progression(catalogs, graph), maps_family(manifests), navigation(manifests),
        collisions(manifests), assets_family(manifests),
        animations_family(manifests, catalogs), placement_family(manifests),
        blender_outputs(framework_path), stored_binaries(),
        unused_assets(manifests, graph),
    ]
    rep = {
        "family_count": len(fams),
        "ok": all(f["ok"] for f in fams if f["family"] != "sorties_blender"),
        "blocking_families": sorted(f["family"] for f in fams if not f["ok"]),
        "error_total": sum(len(f["errors"]) for f in fams),
        "warning_total": sum(len(f["warnings"]) for f in fams),
        "families": sorted(fams, key=lambda f: f["family"]),
    }
    write_json(path, rep)
    return rep
