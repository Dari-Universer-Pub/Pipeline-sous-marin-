"""Chargement et empreinte des entrees officielles. Aucune invention."""
from __future__ import annotations
from pathlib import Path
from .util import ROOT, sha256_bytes

INPUT_DIR = ROOT / "INPUT"
CONTRACT_DIR = ROOT / "CONTRACT"

REQUIRED = [
    ("INPUT/game_brief.md", True),
    ("INPUT/canon_initial.md", True),
    ("INPUT/constraints.md", True),
    ("INPUT/open_decisions.md", True),
    ("INPUT/external_tools.md", False),   # absent du bootstrapper livre
    ("CONTRACT/architecture_contract.md", True),
]


def load_all() -> dict:
    """Retourne {path: {present, utf8, bom, bytes, sha256, lines, text}}."""
    out = {}
    for relpath, mandatory in REQUIRED:
        p = ROOT / relpath
        entry = {"path": relpath, "mandatory": mandatory, "present": p.is_file()}
        if not entry["present"]:
            entry.update(utf8=False, bom=False, bytes=0, sha256=None, lines=0, text=None,
                         status="MISSING")
            out[relpath] = entry
            continue
        raw = p.read_bytes()
        bom = raw[:3] == b"\xef\xbb\xbf"
        try:
            text = raw.decode("utf-8")
            utf8 = True
        except UnicodeDecodeError:
            text, utf8 = None, False
        entry.update(utf8=utf8, bom=bom, bytes=len(raw), sha256=sha256_bytes(raw),
                     lines=text.count("\n") + 1 if text else 0, text=text,
                     status="LOADED" if utf8 else "ENCODING_ERROR")
        out[relpath] = entry
    return out


def missing_mandatory(loaded) -> list[str]:
    return [k for k, v in loaded.items() if v["mandatory"] and not v["present"]]


def missing_optional(loaded) -> list[str]:
    return [k for k, v in loaded.items() if not v["mandatory"] and not v["present"]]
