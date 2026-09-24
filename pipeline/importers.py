"""Importateurs. Point d'entree des resultats produits par Blender ou une autre IA.

Regle centrale: IMPORTED n'est accorde a un asset AVEC binaire que si la
verification binaire a reussi. Un asset GENERATED non verifie est INCOMPLET.
Rien n'est jamais repare silencieusement.
"""
from __future__ import annotations
from pathlib import Path
from .assets_bin import store
from .binary_check import verify
from .schemas import validate
from .status import advance_asset
from .util import ROOT, write_json

DELIVERY = ROOT / "ASSETS_IN"


def _spec_of(manifest_assets, asset_id):
    for a in manifest_assets:
        if a["id"] == asset_id:
            return a
    return None


def import_result(response: dict, manifest_assets: list, *, known_ids=None) -> dict:
    """Importe UNE reponse de generation (Blender ou autre IA).

    response: {asset_id, entity_id, status, width, height, format, variants,
               directions, [file], [file_sha256], [warnings], [errors]}
    """
    out = {"asset_id": response.get("asset_id"), "ok": False, "status": "BLOCKED",
           "errors": [], "warnings": list(response.get("warnings", [])),
           "stored_path": None, "sha256": None,
           "produced_variants": response.get("variants", []),
           "produced_directions": response.get("directions", []),
           "produced_animations": response.get("animations", [])}

    asset_id = response.get("asset_id")
    spec = _spec_of(manifest_assets, asset_id) if asset_id else None
    if spec is None:
        out["errors"].append({"code": "import.unknown_asset",
                              "detail": f"asset_id absent du manifest: {asset_id!r}"})
        return out

    if response.get("status") == "BLOCKED":
        out["status"] = "BLOCKED"
        out["errors"].append({"code": "import.generator_blocked",
                              "detail": f"le generateur a retourne BLOCKED: "
                                        f"{response.get('missing', [])}"})
        return out

    # 1) conformite de la reponse au manifest (hors binaire)
    for field, expected in (("width", spec["width"]), ("height", spec["height"]),
                            ("format", spec["format"])):
        if field in response and response[field] != expected:
            out["errors"].append({
                "code": "import.manifest_mismatch",
                "detail": f"{field} declare {response[field]!r}, manifest {expected!r}"})
    for v in response.get("variants", []):
        if spec["variants"] and v not in spec["variants"]:
            out["errors"].append({"code": "import.unknown_variant",
                                  "detail": f"variante hors manifest: {v!r}"})
    for d in response.get("directions", []):
        if d not in spec["directions"]:
            out["errors"].append({"code": "import.unknown_direction",
                                  "detail": f"direction hors manifest: {d!r}"})
    if out["errors"]:
        return out

    has_file = "file" in response and "file_sha256" in response
    if not has_file:
        if "file" in response or "file_sha256" in response:
            out["errors"].append({
                "code": "import.partial_binary_declaration",
                "detail": "'file' et 'file_sha256' doivent etre fournis ensemble"})
            return out
        # Specification valide sans binaire: l'asset reste PLANNED.
        out.update(ok=True, status="PLANNED",
                   warnings=out["warnings"] + [
                       "specification acceptee sans binaire; l'asset reste PLANNED "
                       "jusqu'a livraison et verification du fichier"])
        return out

    # 2) verification BINAIRE reelle
    src = Path(response["file"])
    if not src.is_absolute():
        src = ROOT / src
    res = verify(src, expected_sha256=response["file_sha256"],
                 expected_width=spec["width"], expected_height=spec["height"],
                 allowed_palette=spec["palette"], expected_format=spec["format"],
                 delivery_dir=DELIVERY)
    if not res["ok"]:
        out["errors"].extend(res["errors"])
        out["status"] = "BLOCKED"
        return out

    # 3) stockage INTACT dans ASSETS_BIN
    st = store(asset_id, spec["family"], src, spec=spec,
               declared_sha256=response["file_sha256"], delivery_dir=DELIVERY)
    if not st["ok"]:
        out["errors"].extend(st["errors"])
        out["status"] = "BLOCKED"
        return out

    # 4) transition de statut: GENERATED -> IMPORTED (jamais de saut)
    try:
        status = advance_asset("GENERATED", "IMPORTED")
    except ValueError as e:
        out["errors"].append({"code": "import.status", "detail": str(e)})
        return out

    out.update(ok=True, status=status, stored_path=st["stored_path"],
               sha256=st["sha256"], width=st["width"], height=st["height"],
               format=st["format"])
    return out


def import_batch(responses, manifest_assets, *, report_path=ROOT / "REPORTS" / "import_report.json"):
    results = [import_result(r, manifest_assets) for r in responses]
    rep = {
        "total": len(results),
        "imported": sum(1 for r in results if r["status"] == "IMPORTED"),
        "planned": sum(1 for r in results if r["status"] == "PLANNED"),
        "blocked": sum(1 for r in results if r["status"] == "BLOCKED"),
        "error_codes": sorted({e["code"] for r in results for e in r["errors"]}),
        "results": sorted(results, key=lambda r: str(r["asset_id"])),
    }
    write_json(report_path, rep)
    return rep
