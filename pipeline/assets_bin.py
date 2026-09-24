"""ASSETS_BIN — stockage de reference des binaires acceptes.

Invariants:
  - un binaire accepte est copie INTACT (octet pour octet);
  - la pipeline ne modifie JAMAIS un binaire stocke;
  - toute alteration ou suppression est une ERREUR bloquante, jamais reparee.
"""
from __future__ import annotations
import shutil
from pathlib import Path
from .util import ROOT, sha256_file, read_json, write_json, rel
from .binary_check import verify, probe, BinaryError

STORE = ROOT / "ASSETS_BIN"
REGISTRY = STORE / "registry.json"
EXT = {"png": "png", "jpeg": "jpg"}


def load_registry() -> dict:
    if REGISTRY.is_file():
        return read_json(REGISTRY)
    return {"version": 1, "entries": {}}


def _save(reg) -> None:
    write_json(REGISTRY, reg)


def store(asset_id: str, family: str, src, *, spec: dict, declared_sha256: str,
          delivery_dir=None) -> dict:
    """Verifie puis archive un binaire livre. Aucune ecriture si la verif echoue.

    `spec` provient du manifest d'asset: width, height, palette, format.
    """
    res = verify(src,
                 expected_sha256=declared_sha256,
                 expected_width=spec.get("width"),
                 expected_height=spec.get("height"),
                 allowed_palette=spec.get("palette"),
                 expected_format=spec.get("format"),
                 delivery_dir=delivery_dir)
    if not res["ok"]:
        return {"ok": False, "asset_id": asset_id, "status": "BLOCKED",
                "errors": res["errors"], "stored_path": None}

    info = res["info"]
    dest = STORE / family / f"{asset_id}.{EXT[info['format']]}"
    reg = load_registry()
    prev = reg["entries"].get(asset_id)
    if prev and prev["sha256"] != info["sha256"]:
        # Ne jamais ecraser silencieusement un binaire deja accepte.
        return {"ok": False, "asset_id": asset_id, "status": "BLOCKED",
                "stored_path": prev["path"],
                "errors": [{"code": "asset.file_hash",
                            "detail": f"un binaire different est deja accepte pour "
                                      f"{asset_id} (stocke {prev['sha256']}, "
                                      f"livre {info['sha256']}); remplacement refuse"}]}

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)  # copie INTACTE, aucune reecriture d'image
    if sha256_file(dest) != info["sha256"]:
        dest.unlink(missing_ok=True)
        return {"ok": False, "asset_id": asset_id, "status": "BLOCKED",
                "errors": [{"code": "asset.file_corrupt",
                            "detail": "la copie vers ASSETS_BIN a altere le binaire"}],
                "stored_path": None}

    reg["entries"][asset_id] = {
        "asset_id": asset_id, "family": family, "path": rel(dest),
        "sha256": info["sha256"], "format": info["format"],
        "width": info["width"], "height": info["height"],
        "size_bytes": info["size_bytes"],
        "indexed": info["indexed"],
        "palette_size": len(info["palette"]) if info["palette"] else 0,
        "source_delivery": str(src),
    }
    _save(reg)
    return {"ok": True, "asset_id": asset_id, "status": "IMPORTED",
            "stored_path": rel(dest), "sha256": info["sha256"],
            "width": info["width"], "height": info["height"],
            "format": info["format"], "errors": []}


def reverify_all() -> dict:
    """Validateur PERMANENT: re-verifie chaque binaire accepte a chaque execution.

    Detecte suppression, alteration d'octets, et divergence de dimensions.
    Ne repare rien: remonte des erreurs bloquantes.
    """
    reg = load_registry()
    errors, checked = [], 0
    for asset_id, e in sorted(reg["entries"].items()):
        p = ROOT / e["path"]
        checked += 1
        if not p.is_file():
            errors.append({"asset_id": asset_id, "code": "asset.file_missing",
                           "detail": f"binaire accepte disparu: {e['path']}"})
            continue
        actual = sha256_file(p)
        if actual != e["sha256"]:
            errors.append({"asset_id": asset_id, "code": "asset.file_hash",
                           "detail": f"binaire altere: {e['path']} "
                                     f"(enregistre {e['sha256']}, actuel {actual})"})
            continue
        try:
            info = probe(p)
        except BinaryError as ex:
            errors.append({"asset_id": asset_id, "code": ex.code, "detail": ex.detail})
            continue
        if (info["width"], info["height"]) != (e["width"], e["height"]):
            errors.append({"asset_id": asset_id, "code": "asset.file_dimensions",
                           "detail": f"dimensions divergentes: "
                                     f"{info['width']}x{info['height']} vs "
                                     f"{e['width']}x{e['height']}"})
    return {"ok": not errors, "checked": checked, "errors": errors}
