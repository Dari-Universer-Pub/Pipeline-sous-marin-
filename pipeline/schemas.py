"""Schemas de donnees + validateur structurel (stdlib seule, pas de jsonschema).

Mini-langage de schema:
  {"type": "str"|"int"|"bool"|"list"|"dict"|"id"|"enum"|"ref",
   "required": bool, "of": <schema>, "values": [...], "kind": "<type ontologie>",
   "min": n, "max": n, "multiple_of": n, "pattern": "regex"}
"""
from __future__ import annotations
import re
from . import SCHEMA_VERSION
from .ids import is_valid_id, PREFIXES
from .status import ASSET_LIFECYCLE, ENTITY_MATURITY, INFO_STATUS
from .util import ROOT, write_json

S = dict  # alias de lisibilite


def f(type, required=True, **kw):
    return dict(type=type, required=required, **kw)


TILE = 16

SCHEMAS = {
    "entity": {
        "id": f("id", kind=None), "kind": f("enum", values=sorted(PREFIXES)),
        "display_name": f("str", min=1, max=80),
        "status": f("enum", values=INFO_STATUS),
        "maturity": f("enum", values=ENTITY_MATURITY, required=False),
        "source": f("str"), "source_line": f("int", required=False),
    },
    "relation": {
        "from": f("id"), "type": f("str"), "to": f("id"),
        "status": f("enum", values=INFO_STATUS, required=False),
    },
    "world_state": {
        "id": f("id"), "depth_m": f("int", min=0, max=12000),
        "oxygen_pct": f("int", min=0, max=100),
        "battery_pct": f("int", min=0, max=100),
        "hull_integrity_pct": f("int", min=0, max=100),
        "lights_on": f("bool"), "current_zone": f("ref", kind="zone"),
        "elapsed_s": f("int", min=0),
    },
    "event": {
        "id": f("id"), "trigger": f("dict"), "preconditions": f("list", of=f("dict")),
        "participants": f("list", of=f("ref", kind=None)),
        "location": f("ref", kind="zone"), "temporality": f("dict"),
        "steps": f("list", of=f("dict"), min=1), "choices": f("list", of=f("dict")),
        "effects": f("list", of=f("dict"), min=1),
        "consequences": f("list", of=f("dict"), min=1),
        "fallback": f("dict"), "failure_conditions": f("list", of=f("dict")),
        "missable": f("bool"), "discovery_method": f("str"),
        "reachability_tests": f("list", of=f("str"), min=1),
    },
    "condition": {
        "subject": f("str"), "op": f("enum", values=["lt", "lte", "eq", "gte", "gt",
                                                     "has", "not_has", "in"]),
        "value": f("any"),
    },
    "effect": {
        "target": f("str"),
        "op": f("enum", values=["set", "add", "sub", "unlock", "reveal", "damage"]),
        "value": f("any"), "durable": f("bool", required=False),
    },
    "object": {   # artefact
        "id": f("id"), "display_name": f("str"), "category": f("str"),
        "function": f("str"), "gameplay_verb": f("id"),
        "obtained_by": f("list", of=f("str"), min=1),
        "loop_position": f("str"), "used_by": f("list", of=f("ref", kind=None)),
        "transformations": f("list", of=f("dict"), required=False),
        "progression": f("str"), "assets": f("list", of=f("ref", kind="asset")),
        "animations": f("list", of=f("ref", kind="animation")),
        "tests": f("list", of=f("str"), min=1),
        "status": f("enum", values=INFO_STATUS),
    },
    "dialogue": {
        "id": f("id"), "speaker": f("ref", kind="crew"),
        "requires_world_state": f("list", of=f("dict")),
        "requires_knowledge": f("list", of=f("ref", kind=None)),
        "forbidden_knowledge": f("list", of=f("ref", kind=None)),
        "relation_min": f("int", min=-100, max=100),
        "location": f("ref", kind="zone"), "time_band": f("str"),
        "lines": f("list", of=f("str"), min=1),
        "compiled": f("bool"),  # doit etre True: pas de LLM runtime
    },
    "asset": {
        "id": f("id"), "entity_id": f("id"), "family": f("id"),
        "asset_type": f("enum", values=["tile", "sprite", "silhouette", "readout",
                                        "panel", "overlay", "frame"]),
        "width": f("int", min=TILE, max=4096, multiple_of=TILE),
        "height": f("int", min=TILE, max=4096, multiple_of=TILE),
        "resolution": f("str"), "style": f("str"),
        "format": f("enum", values=["png", "jpeg"]),
        "palette": f("list", of=f("list"), min=1),
        "variants": f("list", of=f("id")),
        "directions": f("list", of=f("enum", values=["none", "front", "left", "right"])),
        "animations": f("list", of=f("ref", kind="animation")),
        "output_rules": f("dict"), "validations": f("list", of=f("str"), min=1),
        "status": f("enum", values=ASSET_LIFECYCLE + ["BLOCKED"]),
        "file": f("str", required=False),
        "file_sha256": f("str", required=False, pattern=r"^[0-9a-f]{64}$"),
        "produced_sha256": f("str", required=False, pattern=r"^[0-9a-f]{64}$"),
    },
    "animation": {
        "id": f("id"), "entity_id": f("id"),
        "state_or_action": f("id"),
        "direction": f("enum", values=["none", "front", "left", "right"]),
        "frames": f("int", min=1, max=64), "fps": f("int", min=1, max=60),
        "loop": f("bool"), "impact_frame": f("int", min=0, required=False),
        "logical_effect": f("dict"), "transitions": f("list", of=f("id")),
        "assets": f("list", of=f("ref", kind="asset"), min=1),
        "tests": f("list", of=f("str"), min=1),
        "status": f("enum", values=ASSET_LIFECYCLE + ["BLOCKED"]),
        "produced_sha256": f("str", required=False, pattern=r"^[0-9a-f]{64}$"),
    },
    "map": {   # "fenetre de profondeur", cf. contra_tuiles_vs_vue_unique
        "id": f("id"), "display_name": f("str"),
        "size": f("dict"), "depth_band": f("dict"),
        "regions": f("list", of=f("dict")), "layers": f("list", of=f("dict"), min=1),
        "entries": f("list", of=f("ref", kind="zone")),
        "exits": f("list", of=f("ref", kind="zone")),
        "collisions": f("list", of=f("dict")),
        "height_levels": f("list", of=f("int"), min=1),
        "terrains": f("list", of=f("id")), "transitions": f("list", of=f("dict")),
        "points_of_interest": f("list", of=f("dict")),
        "structures": f("list", of=f("dict")),
        "secret_zones": f("list", of=f("dict")),
        "resources": f("list", of=f("ref", kind="resource")),
        "placement_rules": f("list", of=f("id"), min=1),
        "navigation_rules": f("dict"), "spawn_rules": f("list", of=f("dict")),
        "seasonal_conditions": f("dict"),
        "relations": f("list", of=f("dict")),
        "seed": f("int", min=0),
    },
    "placement_rule": {
        "id": f("id"), "applies_to": f("id_glob"),
        "allowed_terrain": f("list", of=f("id"), min=1),
        "forbidden_terrain": f("list", of=f("id")),
        "density": f("dict"), "min_distance": f("int", min=0),
        "clustering": f("dict"), "season": f("str"), "weather": f("str"),
        "accessibility": f("str"), "discovery_conditions": f("list", of=f("dict")),
        "poi_relations": f("list", of=f("dict")),
    },
    "external_tool": {
        "id": f("id"), "name": f("str"), "role": f("str"),
        "path": f("str"), "path_exists": f("bool"),
        "entry_scripts": f("list", of=f("str")), "builders": f("list", of=f("str")),
        "input_formats": f("list", of=f("str")), "output_formats": f("list", of=f("str")),
        "output_paths": f("list", of=f("str")),
        "runtime_required": f("bool"),   # doit etre False
        "status": f("enum", values=["AVAILABLE", "BLOCKED", "UNDECLARED"]),
    },
}

# Emplacements imposes par le contrat, sans fondement canonique (voir ontology).
SCHEMAS_NOT_APPLICABLE = ["crop", "machine", "recipe", "quest", "creature", "boss"]


# ------------------------------------------------------------ validateur

def _check(value, spec, path, known_ids, errors):
    t = spec["type"]
    if t == "any":
        return
    if t == "id_glob":
        base = value[:-1] if isinstance(value, str) and value.endswith("*") else value
        if not is_valid_id(base if base else "x"):
            errors.append({"code": "schema.id", "path": path,
                           "detail": f"motif d'identifiant invalide: {value!r}"})
        return
    if t == "id":
        if not is_valid_id(value):
            errors.append({"code": "schema.id", "path": path,
                           "detail": f"identifiant invalide: {value!r}"})
        return
    if t == "ref":
        if not is_valid_id(value):
            errors.append({"code": "schema.id", "path": path,
                           "detail": f"reference malformee: {value!r}"})
        elif known_ids is not None and value not in known_ids:
            errors.append({"code": "schema.ref_unknown", "path": path,
                           "detail": f"reference inconnue: {value!r}"})
        return
    if t == "enum":
        if value not in spec["values"]:
            errors.append({"code": "schema.enum", "path": path,
                           "detail": f"{value!r} hors de {spec['values']}"})
        return
    py = {"str": str, "int": int, "bool": bool, "list": list, "dict": dict}[t]
    if t == "int" and isinstance(value, bool):
        errors.append({"code": "schema.type", "path": path, "detail": "bool fourni pour int"})
        return
    if not isinstance(value, py):
        errors.append({"code": "schema.type", "path": path,
                       "detail": f"attendu {t}, recu {type(value).__name__}"})
        return
    if t == "int":
        if "min" in spec and value < spec["min"]:
            errors.append({"code": "schema.range", "path": path,
                           "detail": f"{value} < min {spec['min']}"})
        if "max" in spec and value > spec["max"]:
            errors.append({"code": "schema.range", "path": path,
                           "detail": f"{value} > max {spec['max']}"})
        if "multiple_of" in spec and value % spec["multiple_of"]:
            errors.append({"code": "schema.multiple", "path": path,
                           "detail": f"{value} n'est pas un multiple de {spec['multiple_of']}"})
    elif t == "str":
        if "min" in spec and len(value) < spec["min"]:
            errors.append({"code": "schema.length", "path": path, "detail": "chaine trop courte"})
        if "max" in spec and len(value) > spec["max"]:
            errors.append({"code": "schema.length", "path": path, "detail": "chaine trop longue"})
        if "pattern" in spec and not re.match(spec["pattern"], value):
            errors.append({"code": "schema.pattern", "path": path,
                           "detail": f"ne respecte pas {spec['pattern']}"})
    elif t == "list":
        if "min" in spec and len(value) < spec["min"]:
            errors.append({"code": "schema.length", "path": path,
                           "detail": f"{len(value)} element(s) < min {spec['min']}"})
        if "of" in spec:
            for i, item in enumerate(value):
                _check(item, spec["of"], f"{path}[{i}]", known_ids, errors)


def validate(name: str, doc: dict, known_ids=None) -> list[dict]:
    """Valide un document contre un schema. Retourne la liste des erreurs."""
    if name not in SCHEMAS:
        return [{"code": "schema.unknown", "path": name,
                 "detail": f"schema inconnu: {name}"}]
    spec, errors = SCHEMAS[name], []
    if not isinstance(doc, dict):
        return [{"code": "schema.type", "path": name, "detail": "document non-objet"}]
    for key, fspec in sorted(spec.items()):
        if key not in doc:
            if fspec.get("required", True):
                errors.append({"code": "schema.missing_field", "path": f"{name}.{key}",
                               "detail": "champ obligatoire absent"})
            continue
        _check(doc[key], fspec, f"{name}.{key}", known_ids, errors)
    for key in sorted(doc):
        if key not in spec:
            errors.append({"code": "schema.unknown_field", "path": f"{name}.{key}",
                           "detail": "champ non declare au schema"})
    return errors


def build() -> dict:
    return {"schema_version": SCHEMA_VERSION, "tile_size": TILE,
            "schemas": {k: SCHEMAS[k] for k in sorted(SCHEMAS)},
            "not_applicable": SCHEMAS_NOT_APPLICABLE}


def write(path=ROOT / "SCHEMAS" / "schemas.json"):
    s = build()
    return s, write_json(path, s)
