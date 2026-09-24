"""Cycles de vie. Aucune etape ne peut etre sautee."""
from __future__ import annotations

# Cycle de vie d'un asset (prompt utilisateur, section REGLES D'INTEGRATION BLENDER)
ASSET_LIFECYCLE = ["PLANNED", "GENERATED", "IMPORTED", "VALIDATED",
                   "RUNTIME_TESTED", "ART_GREEN"]
BLOCKED = "BLOCKED"

# Maturite d'une entite (CONTRACT/architecture_contract.md, "Statuts de maturite")
ENTITY_MATURITY = ["SPECIFIED", "SCHEMA_VALIDATED", "IMPORTED", "CATALOGED",
                   "GRAPH_CONNECTED", "COMPILED", "RUNTIME_TESTED",
                   "PRODUCTION_READY"]

# Statuts d'information (CONTRACT: CANONICAL/DERIVED/PROPOSED/TO_VALIDATE)
INFO_STATUS = ["CANONICAL", "DERIVED", "PROPOSED", "TO_VALIDATE"]


def _advance(cycle, current, target):
    if current == BLOCKED:
        raise ValueError("status.blocked: une entite BLOCKED doit etre debloquee explicitement")
    if current not in cycle or target not in cycle:
        raise ValueError(f"status.unknown: {current!r} -> {target!r}")
    ci, ti = cycle.index(current), cycle.index(target)
    if ti != ci + 1:
        raise ValueError(
            f"status.skip: {current} -> {target} interdit; "
            f"prochaine etape obligatoire = {cycle[ci + 1]}")
    return target


def advance_asset(current: str, target: str) -> str:
    """Avance d'exactement un cran. Un asset GENERATED n'est jamais ART_GREEN."""
    return _advance(ASSET_LIFECYCLE, current, target)


def advance_entity(current: str, target: str) -> str:
    return _advance(ENTITY_MATURITY, current, target)


def is_complete_asset(status: str) -> bool:
    """Seul ART_GREEN est termine. GENERATED/IMPORTED/VALIDATED = incomplet."""
    return status == "ART_GREEN"


def reached(cycle, status, milestone) -> bool:
    if status == BLOCKED or status not in cycle:
        return False
    return cycle.index(status) >= cycle.index(milestone)
