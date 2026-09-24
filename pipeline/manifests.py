"""Generateur de manifests. Un manifest DECRIT une production attendue.

Aucun asset n'est genere ici. Tout asset naît au statut PLANNED.
"""
from __future__ import annotations
from .ids import make_id
from .palette import colors
from .schemas import TILE
from .util import ROOT, write_json

DIMS = {"readout": (32, 32), "overlay": (160, 64), "panel": (160, 64),
        "silhouette": (96, 96), "tile": (TILE, TILE), "frame": (320, 192),
        "sprite": (32, 32)}
STYLE = ("pixel art 2D, mise a l'echelle entiere, sombre / oppressant / "
         "atmospherique, vue unique depuis l'interieur du sous-marin")


def _asset(entity_id, family, atype, suffix, *, variants=None, directions=None,
           animations=None, blocking=None):
    w, h = DIMS[atype]
    aid = make_id("asset", f"{entity_id}_{suffix}")
    return {
        "id": aid, "entity_id": entity_id, "family": family, "asset_type": atype,
        "width": w, "height": h, "resolution": f"{w}x{h}@1x", "style": STYLE,
        "format": "png", "palette": colors(),
        "variants": variants or [], "directions": directions or ["none"],
        "animations": animations or [],
        "output_rules": {
            "dir": f"ASSETS_IN/{family}", "filename": f"{aid}.png",
            "indexed": True, "max_bytes": 8 * 1024 * 1024,
            "no_resize_after_delivery": True,
            "must_declare": ["file", "file_sha256"]},
        "validations": [
            "binaire: octets magiques PNG + IHDR",
            "binaire: CRC valide sur chaque chunk",
            "binaire: SHA-256 reel == SHA-256 declare",
            f"binaire: dimensions reelles == {w}x{h}",
            "binaire: PLTE inclus dans palette_abysse_16",
            "binaire: taille <= 8 Mio",
            "reference: entity_id present dans le graphe",
        ],
        "status": "BLOCKED" if blocking else "PLANNED",
        "blocked_by": blocking,
        "producer": "framework_blender",
    }


def _anim(entity_id, state_or_action, assets, *, frames, fps, loop, effect,
          transitions=None, blocking=None):
    aid = make_id("animation", f"{entity_id}_{state_or_action}")
    return {
        "id": aid, "entity_id": entity_id, "state_or_action": state_or_action,
        "direction": "none", "frames": frames, "fps": fps, "loop": loop,
        "impact_frame": max(0, frames - 1) if not loop else 0,
        "logical_effect": effect, "transitions": transitions or [],
        "assets": assets,
        "tests": [f"test_{aid}_synchro_etat", f"test_{aid}_effet_logique_applique"],
        "status": "BLOCKED" if blocking else "PLANNED",
        "blocked_by": blocking, "producer": "framework_blender",
    }


def build(canon, catalogs, graph) -> dict:
    assets, anims = [], []

    # --- famille cockpit: un cadran par systeme vital (justifie par dec_systemes_vitaux)
    for s in catalogs["systemes_vitaux"]["entries"]:
        a = _asset(s["id"], "famille_cockpit", "readout", "cadran",
                   variants=["nominal", "alerte", "critique"])
        assets.append(a)
        anims.append(_anim(s["id"], "etat_alerte", [a["id"]], frames=4, fps=6, loop=True,
                           effect={"target": f"{s['id']}.alarm", "op": "set", "value": True},
                           transitions=["etat_nominal", "etat_critique"]))
        anims.append(_anim(s["id"], "etat_critique", [a["id"]], frames=6, fps=10, loop=True,
                           effect={"target": s["failure_state"], "op": "set", "value": True},
                           transitions=["etat_alerte"]))

    # --- famille artefacts: une icone par objet canonique
    for art in catalogs["artefacts"]["entries"]:
        assets.append(_asset(art["id"], "famille_artefacts", "sprite", "icone"))

    # --- famille fond: une tuile de fond par zone d'exploration
    for z in catalogs["zones"]["entries"]:
        if z["role"] != "exploration":
            continue
        assets.append(_asset(z["id"], "famille_fond_abyssal", "tile", "fond",
                             variants=["proche", "moyen", "lointain"]))

    # --- familles bloquees: decrites, jamais remplies
    blocked_families = {
        "famille_anomalies": {
            "status": "BLOCKED", "blocked_by": "dec_nature_formes",
            "reason": "La nature des formes terrifiantes est declaree OUVERTE dans "
                      "canon_initial.md. Aucun asset d'anomalie ne peut etre specifie "
                      "sans inventer le coeur creatif du jeu.",
            "unblocks_when": "le proprietaire tranche dec_nature_formes et dec_nb_anomalies",
            "would_require": ["silhouette 96x96 par anomalie",
                              "sequence animee de presence par anomalie",
                              "prompt PAR FAMILLE (les anomalies sont visuellement "
                              "interdependantes: meme grammaire d'ombre)"]},
        "famille_traces": {
            "status": "BLOCKED", "blocked_by": "dec_nb_artefacts",
            "reason": "Les messages et archives des ruines sont declares OUVERTS.",
            "unblocks_when": "le proprietaire definit le contenu des archives",
            "would_require": ["panel 160x64 par trace lisible"]},
    }

    manifests = {
        "manifest_version": "1.0.0",
        "seed": 20260924,
        "assets": {"entries": sorted(assets, key=lambda a: a["id"]), "count": len(assets)},
        "animations": {"entries": sorted(anims, key=lambda a: a["id"]), "count": len(anims)},
        "blocked_families": blocked_families,
        "objets": {"entries": [
            {"id": a["id"], "display_name": a["display_name"], "category": a["category"],
             "function": a["function"], "gameplay_verb": a["gameplay_verb"],
             "obtained_by": ["trouve dans les abysses"], "loop_position": a["loop_position"],
             "used_by": ["equipage_pilote"], "progression": a["loop_position"],
             "assets": [x["id"] for x in assets if x["entity_id"] == a["id"]],
             "animations": [], "tests": [f"test_{a['id']}_usage_reel"],
             "status": "CANONICAL"}
            for a in catalogs["artefacts"]["entries"]], "count": 5},
        "maps": {"entries": [_map(z) for z in catalogs["zones"]["entries"]
                             if z["role"] == "exploration"], "count": 3},
        "placement": {"entries": _placement(), "count": 2},
        "transitions_terrain": {"entries": _transitions(), "count": 2},
        "effets_particules": {"status": "BLOCKED", "blocked_by": "dec_nature_formes",
                              "entries": [], "count": 0,
                              "reason": "Les effets de presence dependent de la nature "
                                        "des formes, declaree OUVERTE."},
        "ressources": {"status": "BLOCKED", "blocked_by": "dec_importance_maintenance",
                       "entries": [], "count": 0},
        "evenements": {"status": "BLOCKED", "blocked_by": "dec_nb_evenements",
                       "entries": [], "count": 0},
        "pnj": {"entries": [
            {"id": c["id"], "display_name": c["display_name"], "function": c["function"],
             "status": "CANONICAL",
             "routines": {"status": "TO_VALIDATE",
                          "reason": "Aucune routine horaire n'est specifiee dans le canon."},
             "knows": ["systeme_*"] if c["id"] == "equipage_mara" else [],
             "forbidden_knowledge": ["anomalie_*", "trace_*"],
             "note": "Un dialogue ne doit jamais reveler un fait que le PNJ ne connait pas."}
            for c in catalogs["equipage"]["entries"]], "count": 4},
        "non_applicables": {
            k: {"status": "NOT_APPLICABLE", "contradiction": "contra_vocabulaire_agricole"}
            for k in ["cultures", "machines", "recettes", "quetes", "creatures"]},
    }
    return manifests


def _map(z):
    return {
        "id": z["id"].replace("zone_", "map_"), "display_name": z["display_name"],
        "source_zone": z["id"],
        "size": {"window_w": 320, "window_h": 192, "unit": "px", "tile": TILE},
        "depth_band": {"min_m": 400, "max_m": 1200, "status": "PROPOSED"},
        "layers": [{"name": "vitre", "z": 0}, {"name": "proche", "z": 1},
                   {"name": "moyen", "z": 2}, {"name": "lointain", "z": 3}],
        "entries": ["zone_le_vitrail_noire"], "exits": ["zone_le_vitrail_noire"],
        "collisions": [{"layer": "proche", "kind": "relief", "blocks_propulsion": True}],
        "height_levels": [0, 1, 2, 3],
        "terrains": ["terrain_vase", "terrain_roche"],
        "transitions": [{"from": "terrain_vase", "to": "terrain_roche",
                         "rule": "bord dithered 16px"}],
        "points_of_interest": [], "structures": [], "secret_zones": [],
        "resources": [],
        "placement_rules": ["placement_relief_proche", "placement_artefact"],
        "navigation_rules": {"mode": "avance_recule_seulement",
                             "justification": "vue unique fixe (dec_vue_unique)",
                             "blocked_by_collision": True},
        "spawn_rules": [{"what": "anomalie_*", "status": "BLOCKED",
                         "blocked_by": "dec_nature_formes"}],
        "seasonal_conditions": {"status": "NOT_APPLICABLE",
                                "reason": "Aucune saison dans un abysse sans lumiere."},
        "relations": [{"connects_to": "zone_le_vitrail_noire", "bidirectional": True}],
        "seed": 20260924, "status": "PLANNED",
    }


def _placement():
    return [
        {"id": "placement_relief_proche", "applies_to": "terrain_roche",
         "allowed_terrain": ["terrain_roche"], "forbidden_terrain": ["terrain_vase"],
         "density": {"per_window": [2, 5]}, "min_distance": 32,
         "clustering": {"mode": "disperse"}, "season": "none", "weather": "none",
         "accessibility": "non_bloquant_pour_le_retour",
         "discovery_conditions": [], "poi_relations": []},
        {"id": "placement_artefact", "applies_to": "artefact_*",
         "allowed_terrain": ["terrain_vase", "terrain_roche"], "forbidden_terrain": [],
         "density": {"per_window": [0, 1]}, "min_distance": 64,
         "clustering": {"mode": "isole"}, "season": "none", "weather": "none",
         "accessibility": "atteignable_avec_propulsion_nominale",
         "discovery_conditions": [{"subject": "systeme_projecteur.on", "op": "eq",
                                   "value": True}],
         "poi_relations": []},
    ]


def _transitions():
    return [
        {"id": "transition_vase_roche", "from": "terrain_vase", "to": "terrain_roche",
         "family": "famille_fond_abyssal", "tiles_required": 4, "status": "PLANNED"},
        {"id": "transition_roche_vide", "from": "terrain_roche", "to": "terrain_vide",
         "family": "famille_fond_abyssal", "tiles_required": 4, "status": "PLANNED"},
    ]


def write(canon, catalogs, graph, outdir=ROOT / "MANIFESTS"):
    m = build(canon, catalogs, graph)
    hashes = {}
    for key in ["assets", "animations", "objets", "maps", "placement",
                "transitions_terrain", "pnj"]:
        hashes[key] = write_json(outdir / f"manifest_{key}.json", m[key])
    hashes["_index"] = write_json(outdir / "manifest_index.json", {
        "manifest_version": m["manifest_version"], "seed": m["seed"],
        "counts": {k: v.get("count") for k, v in m.items() if isinstance(v, dict) and "count" in v},
        "blocked_families": m["blocked_families"],
        "non_applicables": m["non_applicables"],
        "effets_particules": m["effets_particules"],
        "ressources": m["ressources"], "evenements": m["evenements"]})
    return m, hashes
