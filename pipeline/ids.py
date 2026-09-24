"""Regles de nommage. ID interne stable vs nom affiche."""
from __future__ import annotations
import re
from .util import ascii_fold

ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")

# Prefixes de type -> imposes par l'ontologie.
PREFIXES = {
    "system": "systeme", "zone": "zone", "anomaly": "anomalie",
    "artifact": "artefact", "trace": "trace", "crew": "equipage",
    "event": "evenement", "action": "action", "state": "etat",
    "asset": "asset", "animation": "anim", "resource": "ressource",
    "placement": "placement", "family": "famille",
}


def is_valid_id(value: str) -> bool:
    return bool(isinstance(value, str) and ID_RE.match(value) and len(value) <= 64)


def slug(display: str) -> str:
    """Nom affiche -> fragment d'ID sur: minuscule, sans accent, underscores."""
    s = ascii_fold(display).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return re.sub(r"_+", "_", s)


def make_id(kind: str, display: str) -> str:
    """make_id('artifact', 'Lampe de secours') -> 'artefact_lampe_de_secours'."""
    if kind not in PREFIXES:
        raise ValueError(f"unknown kind: {kind}")
    return f"{PREFIXES[kind]}_{slug(display)}"


def check_id(kind: str, value: str) -> list[str]:
    """Retourne la liste des violations de nommage (vide si conforme)."""
    errs = []
    if not is_valid_id(value):
        errs.append(f"id.malformed:{value!r} (attendu ^[a-z][a-z0-9_]*$, <=64)")
        return errs
    expected = PREFIXES.get(kind)
    if expected and not value.startswith(expected + "_"):
        errs.append(f"id.prefix:{value!r} devrait commencer par {expected}_")
    return errs
