"""Ontologie d'Abyssal Glass: types d'entites et types de relations.

Les types sont deduits du brief et du canon. Les types issus du vocabulaire
agricole du contrat (culture, machine, recette) sont declares NOT_APPLICABLE
avec justification, jamais remplis d'inventions (cf. contra_vocabulaire_agricole).
"""
from __future__ import annotations
from .util import ROOT, write_json

ENTITY_TYPES = {
    "vessel_system": dict(status="DERIVED", id_prefix="systeme",
        description="Systeme vital du Vitrail Noire (oxygene, batterie, coque, "
                    "propulsion, projecteur).",
        required=["id", "display_name", "failure_state", "consumes", "readout_asset"],
        source="INPUT/game_brief.md"),
    "zone": dict(status="CANONICAL", id_prefix="zone",
        description="Fenetre de profondeur explorable. N'est pas une tilemap.",
        required=["id", "display_name", "depth_band", "pressure", "darkness",
                  "threats", "narrative_clues", "connects_to"],
        source="INPUT/canon_initial.md"),
    "anomaly": dict(status="TO_VALIDATE", id_prefix="anomalie",
        description="Phenomene observable depuis la vitre. Nature declaree OUVERTE "
                    "dans le canon: aucune entree canonique n'existe.",
        required=["id", "display_name", "visible_in", "tension_curve", "reveals",
                  "player_responses", "assets", "animations"],
        source="INPUT/open_decisions.md"),
    "artifact": dict(status="CANONICAL", id_prefix="artefact",
        description="Objet recuperable. Canon: jamais entierement rassurant.",
        required=["id", "display_name", "category", "function", "gameplay_verb",
                  "obtained_by", "used_by", "loop_position", "assets", "tests"],
        source="INPUT/canon_initial.md"),
    "trace": dict(status="TO_VALIDATE", id_prefix="trace",
        description="Indice, enregistrement ou message trouve. Contenu OUVERT.",
        required=["id", "display_name", "found_in", "evidence_of", "known_by"],
        source="INPUT/open_decisions.md"),
    "crew": dict(status="CANONICAL", id_prefix="equipage",
        description="Membre d'equipage ou Pilote.",
        required=["id", "display_name", "function", "goals", "knows", "forbidden_knowledge",
                  "relations", "routines"],
        source="INPUT/canon_initial.md"),
    "event": dict(status="TO_VALIDATE", id_prefix="evenement",
        description="Evenement de tension, de fuite ou de consequence.",
        required=["id", "trigger", "preconditions", "participants", "location",
                  "steps", "effects", "consequences", "fallback", "failure_conditions",
                  "missable", "discovery_method"],
        source="INPUT/open_decisions.md"),
    "action": dict(status="DERIVED", id_prefix="action",
        description="Verbe de gameplay disponible au Pilote.",
        required=["id", "display_name", "affects", "animation", "preconditions"],
        source="INPUT/game_brief.md"),
    "state": dict(status="DERIVED", id_prefix="etat",
        description="Etat discret d'un systeme ou du vaisseau.",
        required=["id", "owner", "severity", "transitions", "animation"],
        source="INPUT/constraints.md"),
    "asset": dict(status="DERIVED", id_prefix="asset",
        description="Fichier visuel rattache a une entite et a une famille.",
        required=["id", "entity_id", "family", "asset_type", "width", "height",
                  "format", "palette", "variants", "directions", "status"],
        source="INPUT/constraints.md"),
    "animation": dict(status="DERIVED", id_prefix="anim",
        description="Sequence synchronisee avec un etat ou une action.",
        required=["id", "entity_id", "state_or_action", "direction", "frames", "fps",
                  "loop", "impact_frame", "logical_effect", "transitions", "assets"],
        source="INPUT/constraints.md"),
    "resource": dict(status="TO_VALIDATE", id_prefix="ressource",
        description="Consommable de maintenance. Importance declaree OUVERTE.",
        required=["id", "display_name", "produced_by", "consumed_by"],
        source="INPUT/open_decisions.md"),
}

# Types imposes par le contrat mais sans fondement dans ce canon.
NOT_APPLICABLE = {
    "crop": "Abyssal Glass n'a ni agriculture ni saison de culture. Aucune mention "
            "dans le brief ni le canon.",
    "machine": "Aucune machine de production/transformation dans le canon. Les "
               "systemes du sous-marin sont modelises par 'vessel_system'.",
    "recipe": "Aucun artisanat ni transformation d'ingredients dans le brief. La "
              "'reparation' est modelisee comme action sur un vessel_system.",
    "quest": "Aucun donneur de quete dans le canon. Les objectifs emergent des "
             "evenements et des traces; modelises par 'event' et 'trace'.",
    "creature": "La nature des formes est declaree OUVERTE dans le canon. Les "
                "modeliser serait inventer le coeur creatif du jeu.",
    "boss": "Le canon exclut explicitement le combat de style heroique.",
}

RELATION_TYPES = {
    "consumes":     dict(domain=["vessel_system", "action"], range=["resource", "vessel_system"]),
    "produces":     dict(domain=["vessel_system"], range=["resource", "state"]),
    "repairs":      dict(domain=["artifact", "action"], range=["vessel_system"]),
    "threatens":    dict(domain=["anomaly", "zone", "event"], range=["vessel_system", "crew"]),
    "observed_in":  dict(domain=["anomaly", "trace"], range=["zone"]),
    "located_in":   dict(domain=["artifact", "trace", "crew"], range=["zone"]),
    "connects_to":  dict(domain=["zone"], range=["zone"]),
    "reveals":      dict(domain=["trace", "anomaly", "event"], range=["trace", "event"]),
    "evidence_of":  dict(domain=["trace"], range=["anomaly", "event"]),
    "triggered_by": dict(domain=["event"], range=["action", "state", "anomaly", "zone"]),
    "requires":     dict(domain=["action", "event"], range=["artifact", "vessel_system", "state"]),
    "damages":      dict(domain=["anomaly", "event", "zone"], range=["vessel_system"]),
    "knows":        dict(domain=["crew"], range=["trace", "event", "anomaly"]),
    "depicts":      dict(domain=["asset"], range=["*"]),
    "animates":     dict(domain=["animation"], range=["state", "action"]),
    "uses_asset":   dict(domain=["animation"], range=["asset"]),
    "has_state":    dict(domain=["vessel_system", "crew"], range=["state"]),
}


def build() -> dict:
    return {
        "ontology_version": "1.0.0", "game": "Abyssal Glass",
        "entity_types": dict(sorted(ENTITY_TYPES.items())),
        "relation_types": dict(sorted(RELATION_TYPES.items())),
        "not_applicable": dict(sorted(
            {k: {"reason": v, "status": "NOT_APPLICABLE",
                 "contradiction": "contra_vocabulaire_agricole"}
             for k, v in NOT_APPLICABLE.items()}.items())),
    }


def write(path=ROOT / "ONTOLOGY" / "ontology.json"):
    o = build()
    return o, write_json(path, o)
