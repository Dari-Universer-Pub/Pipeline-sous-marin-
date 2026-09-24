"""Palette de production. Decision PROPOSED (dec_palette), non canonique.

Modifiable sans toucher au canon narratif. 16 teintes, sombre et froid,
conforme a 'sombre, oppressant, atmospherique' (constraints.md).
"""
from __future__ import annotations
from .util import ROOT, write_json

ABYSS_16 = [
    (3, 5, 8), (8, 12, 18), (14, 22, 30), (20, 34, 44),
    (28, 50, 60), (38, 70, 78), (52, 94, 98), (72, 120, 118),
    (98, 148, 140), (140, 180, 172), (186, 210, 200), (232, 238, 230),
    (86, 28, 32), (140, 52, 44), (196, 126, 58), (58, 24, 66),
]


def build() -> dict:
    return {
        "palette_id": "palette_abysse_16", "status": "PROPOSED",
        "decision": "dec_palette", "source": "pipeline",
        "justification": "Aucune palette n'est specifiee dans les entrees; valeur "
                         "technique par defaut, modulaire et versionnee.",
        "size": len(ABYSS_16),
        "colors_rgb": [list(c) for c in ABYSS_16],
        "colors_hex": ["#%02x%02x%02x" % c for c in ABYSS_16],
    }


def colors():
    return [list(c) for c in ABYSS_16]


def write(path=ROOT / "CANON" / "palette.json"):
    p = build()
    return p, write_json(path, p)
