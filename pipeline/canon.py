"""Canon central verrouille — Abyssal Glass.

Chaque fait CANONICAL est extrait litteralement de INPUT/canon_initial.md et
porte sa ligne source. Aucun fait narratif n'est ajoute ici.
Les elements DERIVED/PROPOSED/TO_VALIDATE vivent dans decisions.py, pas ici.
"""
from __future__ import annotations
import re
from . import CANON_VERSION
from .ids import make_id
from .inputs import load_all
from .util import ROOT, ascii_fold, write_json

SRC = "INPUT/canon_initial.md"

# (kind, nom affiche, role) — chaque entree DOIT apparaitre litteralement dans SRC.
WORLD_NAME = "l'Abysse de Veyr"
PLAYER_NAME = "le Pilote"
VESSEL_NAME = "le Vitrail Noire"

PLACES = [
    ("Le Vitrail Noire", "sous-marin de depart et point d'observation principal"),
    ("La Faille des Échos", "zone d'exploration sombre et instable"),
    ("Le Corridor des Yeux", "couloir profond ou l'ombre parait vivante"),
    ("Les Ruines du Son", "vestiges de structures anciennes et de materiel perdu"),
]
CREW = [
    ("Mara", "ingenieure de bord, responsable des systemes du sous-marin"),
    ("Ilyan", "navigateur, qui refuse de regarder directement la vitre pendant les plongees"),
    ("Sorel", "chercheur de terrain, fascine par les traces anciennes et jamais totalement serein"),
]
ARTIFACTS = [
    ("Lampe de secours",), ("Carte des profondeurs",), ("Flasque d'oxygène",),
    ("Fragment d'archive abyssale",), ("Outil de réparation de coque",),
]
IMMUTABLE_RULES = [
    "La profondeur contient des traces d'une intelligence ancienne.",
    "Les objets trouves dans les abysses ne sont jamais entierement rassurants.",
    "Le jeu repose sur la survie, l'observation et la peur, pas sur un combat de style heroique.",
]
NAMING_RULE = ("Les noms doivent etre simples, claquants, sinistres, precis. "
               "Eviter toute surenchere fantasy, toute langue trop ornate, et toute "
               "reference trop explicite au surnaturel sans mystere.")
# Textuellement listes comme ouverts dans canon_initial.md -> jamais CANONICAL.
OPEN_IN_CANON = [
    "La nature exacte des formes terrifiantes.",
    "Le nombre exact des zones profondes.",
    "Les anomalies observables depuis la vitre.",
    "Les messages ou archives retrouves dans les ruines.",
    "Le vrai but de la plongee finale.",
]


_APOS = dict.fromkeys(map(ord, "\u2019\u2018\u02bc\u00b4"), "'")


def _norm(s: str) -> str:
    """Normalise espaces et apostrophes typographiques pour la recherche."""
    return re.sub(r"\s+", " ", ascii_fold(s.translate(_APOS))).strip().lower()


def _line_of(text: str, needle: str):
    """Numero de ligne 1-based du premier fragment correspondant, sinon None."""
    key = _norm(needle)[:28]
    for i, line in enumerate(text.splitlines(), 1):
        if key in _norm(line):
            return i
    return None


def build() -> dict:
    loaded = load_all()
    src = loaded[SRC]
    if not src["present"]:
        raise SystemExit(f"BLOCKED canon.source_missing: {SRC}")
    text = src["text"]
    entries = []

    def add(kind, display, role, extra=None):
        entries.append({
            "id": make_id(kind, display), "kind": kind, "display_name": display,
            "role": role, "status": "CANONICAL", "source": SRC,
            "source_line": _line_of(text, display), **(extra or {})})

    add("zone", "Abysse de Veyr", "monde")
    add("crew", "Pilote", "personnage joueur")
    for name, role in PLACES:
        add("zone", name, role)
    for name, role in CREW:
        add("crew", name, role)
    for (name,) in ARTIFACTS:
        add("artifact", name, "objet canonique")

    canon = {
        "canon_version": CANON_VERSION,
        "game": "Abyssal Glass",
        "locked": True,
        "source_files": {SRC: src["sha256"]},
        "world_name": WORLD_NAME,
        "player_name": PLAYER_NAME,
        "vessel_name": VESSEL_NAME,
        "entries": sorted(entries, key=lambda e: e["id"]),
        "immutable_rules": [
            {"text": r, "status": "CANONICAL", "source": SRC, "source_line": _line_of(text, r)}
            for r in IMMUTABLE_RULES],
        "naming_rule": {"text": NAMING_RULE, "status": "CANONICAL", "source": SRC},
        "declared_open": [
            {"text": t, "status": "TO_VALIDATE", "source": SRC, "source_line": _line_of(text, t)}
            for t in OPEN_IN_CANON],
        "forbidden": [
            "combat heroique comme boucle centrale",
            "lexique high fantasy / noms ornes",
            "surnaturel explicite sans mystere",
            "objet abyssal presente comme entierement rassurant",
        ],
    }
    return canon


def canonical_ids(canon) -> set:
    return {e["id"] for e in canon["entries"]}


def write(path=ROOT / "CANON" / "canon_central.json") -> tuple:
    canon = build()
    return canon, write_json(path, canon)
