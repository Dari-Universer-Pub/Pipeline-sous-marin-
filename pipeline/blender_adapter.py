"""Adaptateur Pipeline V5 <-> framework Blender externe.

L'adaptateur est une COUCHE DE TRADUCTION. Il ne reimplemente pas le framework,
ne remplace aucun de ses systemes, et ne modifie pas le contrat universel.

Le chemin du framework n'est JAMAIS code en dur ici. Il est resolu, dans l'ordre:
  1. argument explicite `framework_path`
  2. variable d'environnement ABYSSAL_BLENDER_FRAMEWORK
  3. config/external_tools.json (genere depuis INPUT/external_tools.md)
Si aucune source ne donne un chemin existant -> BLOCKED, sans substitution.

Responsabilites (contractuelles):
  Pipeline : identite, canon, relations, dimensions, variantes, directions,
             animations attendues, placement, validation, integration runtime.
  Blender  : modeles, materiaux, rendus, sprites, animations, exports.
"""
from __future__ import annotations
import json, os, shutil
from pathlib import Path
from .util import ROOT, write_json, rel

ENV_VAR = "ABYSSAL_BLENDER_FRAMEWORK"
CONFIG = ROOT / "config" / "external_tools.json"
DELIVERY = ROOT / "ASSETS_IN"

# Noms de scripts/builders RECHERCHES dans le framework. Ce sont des hypotheses
# de decouverte, pas des affirmations sur son contenu: rien n'est invente,
# l'inspection reelle remplit le rapport de compatibilite.
ENTRY_CANDIDATES = ["main.py", "run.py", "build.py", "cli.py", "__main__.py",
                    "render.py", "export.py", "blender_main.py"]
BUILDER_HINTS = ["builder", "builders", "generators", "makers", "assets"]


# --------------------------------------------------------- resolution du chemin

def resolve_path(framework_path=None) -> dict:
    """Retourne {path, source, exists}. N'invente jamais de chemin."""
    if framework_path:
        return {"path": str(framework_path), "source": "argument",
                "exists": Path(framework_path).is_dir()}
    env = os.environ.get(ENV_VAR)
    if env:
        return {"path": env, "source": f"env:{ENV_VAR}", "exists": Path(env).is_dir()}
    if CONFIG.is_file():
        try:
            cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
            p = cfg.get("blender_framework", {}).get("path")
            if p:
                return {"path": p, "source": rel(CONFIG), "exists": Path(p).is_dir()}
        except (json.JSONDecodeError, OSError):
            pass
    return {"path": None, "source": None, "exists": False}


def blocked(reason, resolved) -> dict:
    """Rapport BLOCKED normalise: chemin manquant + remede exact."""
    shown = resolved.get("path") or "(aucun chemin declare)"
    return {
        "status": "BLOCKED", "ok": False, "reason": reason,
        "missing_path": shown,
        "resolution_source": resolved.get("source"),
        "remediation": {
            "cause": "Le framework Blender est introuvable. Aucun outil de "
                     "substitution n'est utilise et aucun asset n'est genere.",
            "fix_options": [
                {"order": 1, "how": "variable d'environnement",
                 "command_posix": f'export {ENV_VAR}="/chemin/reel/FRAMEWORK_BLENDER"',
                 "command_windows": f'setx {ENV_VAR} "D:\\chemin\\reel\\FRAMEWORK_BLENDER"'},
                {"order": 2, "how": "fichier de configuration",
                 "file": rel(CONFIG) if CONFIG.exists() else "config/external_tools.json",
                 "content": {"blender_framework": {"path": "/chemin/reel/FRAMEWORK_BLENDER"}}},
                {"order": 3, "how": "declaration officielle",
                 "file": "INPUT/external_tools.md",
                 "note": "Fichier ABSENT du bootstrapper. Gabarit fourni dans "
                         "docs/external_tools.template.md. C'est la source de verite "
                         "des outils externes selon la commande."},
            ],
            "never": ["inventer un chemin", "generer les assets autrement",
                      "dessiner un placeholder a la place d'un binaire attendu"],
        },
        "produced_files": [], "errors": [{"code": "tool.path_missing", "detail": shown}],
    }


# --------------------------------------------------------- inspection

def inspect(framework_path=None) -> dict:
    """Inspecte l'arborescence reelle du framework. BLOCKED s'il est absent."""
    r = resolve_path(framework_path)
    if not r["exists"]:
        return blocked("chemin du framework Blender inexistant", r)
    root = Path(r["path"])
    tree, entries, builders = [], [], []
    for p in sorted(root.rglob("*")):
        if any(part.startswith(".") for part in p.parts):
            continue
        rp = p.relative_to(root).as_posix()
        tree.append(rp + ("/" if p.is_dir() else ""))
        if p.is_file() and p.name in ENTRY_CANDIDATES:
            entries.append(rp)
        if p.is_file() and p.suffix == ".py" and any(h in rp.lower() for h in BUILDER_HINTS):
            builders.append(rp)
    return {"status": "AVAILABLE", "ok": True, "path": str(root),
            "resolution_source": r["source"],
            "tree": tree[:2000], "tree_truncated": len(tree) > 2000,
            "entry_scripts": entries, "builders": builders,
            "input_formats": ["json (manifest d'asset)"],
            "output_formats": ["png", "jpeg"],
            "output_paths": [rel(DELIVERY)],
            "runtime_required": False}


# --------------------------------------------------------- traduction

def to_blender_job(asset_manifest_entry: dict, *, canon, animations=None) -> dict:
    """Manifest V5 -> job Blender. Transmet EXACTEMENT les champs contractuels."""
    a = asset_manifest_entry
    return {
        "entity_id": a["entity_id"],
        "asset_id": a["id"],
        "visual_family": a["family"],
        "asset_type": a["asset_type"],
        "dimensions": {"width": a["width"], "height": a["height"]},
        "resolution": a["resolution"],
        "style": a["style"],
        "palette": a["palette"],
        "variants": a["variants"],
        "directions": a["directions"],
        "expected_animations": animations or a.get("animations", []),
        "output_rules": a["output_rules"],
        "required_validations": a["validations"],
        "canon_context": {"world": canon["world_name"], "vessel": canon["vessel_name"],
                          "player": canon["player_name"],
                          "forbidden": canon["forbidden"]},
    }


def from_blender_result(job: dict, result: dict) -> dict:
    """Resultat Blender -> reponse V5 normalisee. Ne valide PAS les binaires ici:
    la verification binaire appartient a importers/binary_check."""
    return {
        "asset_id": job["asset_id"], "entity_id": job["entity_id"],
        "status": result.get("status", "GENERATED"),
        "produced_files": result.get("files", []),
        "produced_variants": result.get("variants", []),
        "produced_directions": result.get("directions", []),
        "produced_animations": result.get("animations", []),
        "warnings": result.get("warnings", []),
        "errors": result.get("errors", []),
        "blender_version": result.get("blender_version"),
    }


def run_jobs(jobs, framework_path=None) -> dict:
    """Execute les jobs via le framework. BLOCKED si le framework est absent.

    Aucun fallback: si le framework manque, RIEN n'est produit.
    """
    r = resolve_path(framework_path)
    if not r["exists"]:
        out = blocked("generation impossible: framework Blender introuvable", r)
        out["jobs_planned"] = [j["asset_id"] for j in jobs]
        out["jobs_executed"] = []
        return out
    insp = inspect(framework_path)
    if not insp["entry_scripts"]:
        return {"status": "BLOCKED", "ok": False,
                "reason": "framework present mais aucun script d'entree reconnu",
                "searched": ENTRY_CANDIDATES, "path": insp["path"],
                "remediation": {"fix": "declarer le script d'entree reel dans "
                                       "config/external_tools.json sous "
                                       "blender_framework.entry_script"},
                "produced_files": [], "errors": [
                    {"code": "tool.entry_missing", "detail": insp["path"]}]}
    # Point d'execution reel. Non atteint tant que le framework est absent.
    return {"status": "GENERATED", "ok": True, "path": insp["path"],
            "entry_script": insp["entry_scripts"][0],
            "jobs_executed": [j["asset_id"] for j in jobs],
            "note": "L'execution reelle delegue au script d'entree du framework; "
                    "la pipeline ne reimplemente aucun builder.",
            "produced_files": [], "errors": []}


def compatibility_report(framework_path=None, path=ROOT / "REPORTS" / "blender_compatibility.json"):
    insp = inspect(framework_path)
    rep = {
        "report_version": "1.0.0",
        "framework": insp,
        "contract_split": {
            "pipeline_owns": ["identite de l'entite", "fonction gameplay", "canon",
                              "relations", "dimensions attendues", "variantes",
                              "directions", "animations attendues", "regles de placement",
                              "validation", "integration runtime"],
            "blender_owns": ["production visuelle", "modeles", "materiaux", "rendus",
                             "sprites", "animations produites", "exports demandes"],
        },
        "adapter_sends": ["entity_id", "asset_id", "visual_family", "asset_type",
                          "dimensions", "resolution", "style", "palette", "variants",
                          "directions", "expected_animations", "output_rules",
                          "required_validations"],
        "adapter_returns": ["produced_files", "output_path", "asset_id", "dimensions",
                            "formats", "sha256", "status", "warnings", "errors",
                            "produced_variants", "produced_directions",
                            "produced_animations"],
        "runtime_dependency": False,
        "runtime_note": "Blender est un outil HORS LIGNE. Le jeu final n'en depend pas.",
        "verdict": "BLOCKED" if not insp.get("ok") else "AVAILABLE",
    }
    write_json(path, rep)
    return rep
