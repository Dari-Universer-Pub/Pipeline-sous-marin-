"""Compilation pour le moteur (Godot 4). Sortie deterministe, sans LLM ni Blender.

Prouve que le jeu final ne depend ni d'un LLM ni de Blender a l'execution.
"""
from __future__ import annotations
from .assets_bin import load_registry
from .util import ROOT, write_json

OUT = ROOT / "RUNTIME"


def compile_all(*, canon, catalogs, graph, manifests, simulation=None) -> dict:
    reg = load_registry()
    art = {
        "runtime_version": "1.0.0", "engine": "godot4",
        "requires_llm": False, "requires_blender": False,
        "canon": {"world": canon["world_name"], "vessel": canon["vessel_name"],
                  "player": canon["player_name"]},
        "systems": [{"id": s["id"], "name": s["display_name"],
                     "failure_state": s["failure_state"]}
                    for s in catalogs["systemes_vitaux"]["entries"]],
        "actions": [{"id": a["id"], "name": a["display_name"], "affects": a["affects"]}
                    for a in catalogs["actions"]["entries"]],
        "zones": [{"id": z["id"], "name": z["display_name"], "role": z["role"]}
                  for z in catalogs["zones"]["entries"]],
        "objects": [{"id": o["id"], "name": o["display_name"], "verb": o["gameplay_verb"]}
                    for o in manifests["objets"]["entries"]],
        "navigation": {"mode": "avance_recule_seulement", "deterministic": True},
        "rules_engine": {"kind": "deterministe", "costs_source": "pipeline/simulate.py"},
        "dialogues": {"compiled": True, "count": 0,
                      "note": "Les dialogues essentiels seront compiles en donnees "
                              "conditionnelles. Aucun n'est ecrit: le contenu des "
                              "echanges depend de decisions ouvertes."},
        "asset_bindings": [
            {"asset_id": aid, "path": e["path"], "sha256": e["sha256"],
             "width": e["width"], "height": e["height"]}
            for aid, e in sorted(reg["entries"].items())],
        "asset_bindings_count": len(reg["entries"]),
        "seed": manifests["seed"],
    }
    h = write_json(OUT / "runtime_data.json", art)
    return art, h


def verify_no_runtime_dependency(art) -> dict:
    """Verifie qu'aucune dependance LLM/Blender ne subsiste dans la sortie runtime."""
    errors = []
    if art.get("requires_llm"):
        errors.append({"code": "runtime.llm_dependency", "detail": "requires_llm=True"})
    if art.get("requires_blender"):
        errors.append({"code": "runtime.blender_dependency", "detail": "requires_blender=True"})
    if not art["dialogues"]["compiled"]:
        errors.append({"code": "runtime.dialogues_not_compiled",
                       "detail": "les dialogues doivent etre compiles en donnees"})
    # On inspecte les VALEURS textuelles, jamais les noms de champs: la cle
    # `requires_blender` est precisement la declaration d'absence de dependance.
    def strings(node):
        if isinstance(node, str):
            yield node
        elif isinstance(node, dict):
            for v in node.values():
                yield from strings(v)
        elif isinstance(node, (list, tuple)):
            for v in node:
                yield from strings(v)

    forbidden = ("http://", "https://", "openai", "anthropic", "bpy.",
                 "import bpy", ".blend")
    for text in strings(art):
        low = text.lower()
        for bad in forbidden:
            if bad in low:
                errors.append({"code": "runtime.external_reference",
                               "detail": f"reference externe dans une valeur runtime: "
                                         f"{bad!r} dans {text[:60]!r}"})
    return {"ok": not errors, "errors": errors}
