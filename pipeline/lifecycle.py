"""Magasin PERSISTANT du cycle de vie par asset.

Comble le trou signale a l'usage: `manifests.py` reconstruit les entrees de
maniere deterministe depuis canon+catalogues+graphe, et n'a donc aucune memoire
de ce qui a ete reellement produit. Sans ce magasin, un asset reellement
IMPORTED redevenait PLANNED a chaque execution et `cli report` restait
bloque a 0/23 ART_GREEN.

Le determinisme est preserve: la sortie reste une fonction pure des entrees,
le magasin faisant desormais partie des entrees (il est versionne et inspectable).
"""
from __future__ import annotations
import os
from pathlib import Path

from .status import ASSET_LIFECYCLE, BLOCKED, advance_asset
from .util import ROOT, read_json, write_json

STORE = ROOT / "STATE" / "lifecycle.json"
ENV_VAR = "ABYSSAL_LIFECYCLE_STORE"


def store_path() -> Path:
    """Chemin du magasin. Surchargeable pour isoler les tests de l'etat reel."""
    override = os.environ.get(ENV_VAR)
    return Path(override) if override else STORE


def load() -> dict:
    p = store_path()
    if p.is_file():
        return read_json(p)
    return {"version": 1, "assets": {}}


def _save(db) -> None:
    write_json(store_path(), db)


def get(asset_id: str):
    """Statut enregistre, ou None si l'asset n'a jamais ete produit."""
    e = load()["assets"].get(asset_id)
    return e["status"] if e else None


def entry(asset_id: str):
    return load()["assets"].get(asset_id)


def record(asset_id: str, status: str, *, sha256=None, note=None,
           allow_initial=False) -> dict:
    """Enregistre une transition. Refuse tout saut d'etape.

    `allow_initial=True` autorise l'entree directe a `status` pour un asset
    inconnu (utilise par l'import, qui arrive avec un binaire deja GENERATED).
    """
    if status != BLOCKED and status not in ASSET_LIFECYCLE:
        raise ValueError(f"lifecycle.unknown_status: {status!r}")
    db = load()
    prev = db["assets"].get(asset_id)
    current = prev["status"] if prev else "PLANNED"

    history = (prev or {}).get("history", [])

    if status == BLOCKED:
        new = BLOCKED
        history = history + [{"from": current, "to": new, "note": note}]
    elif status == current:
        # Idempotence: relivrer le meme etat n'est pas une transition.
        new = current
        history = history + [{"from": current, "to": new,
                              "note": f"idempotent: {note}" if note else "idempotent"}]
    elif allow_initial:
        # L'import traverse legitimement plusieurs crans (Blender a GENERE,
        # la pipeline a VERIFIE). Chaque cran est enregistre un par un:
        # le parcours est explicite, aucun saut n'est masque.
        new = current
        while new != status:
            nxt = ASSET_LIFECYCLE[ASSET_LIFECYCLE.index(new) + 1]
            new = advance_asset(new, nxt)   # leve ValueError si hors cycle
            history = history + [{"from": history[-1]["to"] if history else current,
                                  "to": new, "note": note}]
    else:
        new = advance_asset(current, status)  # leve ValueError sur un saut
        history = history + [{"from": current, "to": new, "note": note}]
    db["assets"][asset_id] = {"asset_id": asset_id, "status": new,
                              "sha256": sha256 or (prev or {}).get("sha256"),
                              "history": history}
    _save(db)
    return db["assets"][asset_id]


def unblock(asset_id: str, to: str = "PLANNED", note=None) -> dict:
    """Leve explicitement un BLOCKED. Jamais automatique."""
    db = load()
    e = db["assets"].get(asset_id)
    if not e or e["status"] != BLOCKED:
        raise ValueError(f"lifecycle.not_blocked: {asset_id}")
    e["history"] = e["history"] + [{"from": BLOCKED, "to": to, "note": note}]
    e["status"] = to
    _save(db)
    return e


def overlay(entries: list) -> list:
    """Applique les statuts reels enregistres sur des entrees de manifest.

    Une entree BLOCKED par decision ouverte le reste: le magasin ne peut pas
    debloquer ce que le canon n'a pas tranche.
    """
    db = load()["assets"]
    out = []
    for e in entries:
        rec = db.get(e["id"])
        if rec and e.get("status") != BLOCKED:
            e = {**e, "status": rec["status"], "produced_sha256": rec["sha256"]}
        out.append(e)
    return out


def summary() -> dict:
    db = load()["assets"]
    dist = {}
    for e in db.values():
        dist[e["status"]] = dist.get(e["status"], 0) + 1
    return {"tracked": len(db), "distribution": dict(sorted(dist.items())),
            "art_green": sorted(k for k, v in db.items() if v["status"] == "ART_GREEN")}
