"""Catalogues fonctionnels. Chaque entree justifie son existence.

Regle: aucune entree n'est ajoutee pour atteindre un nombre. Les catalogues
dont le contenu est declare OUVERT dans le canon restent VIDES, avec la
raison du vide et la decision qui les debloquera.
"""
from __future__ import annotations
from .ids import make_id
from .ontology import NOT_APPLICABLE
from .util import ROOT, write_json

# ------------------------------------------------ systemes vitaux (DERIVED)
SYSTEMS = [
    dict(display="Oxygène", failure="etat_asphyxie", consumes=["temps", "effort"],
         why="game_brief.md: 'gerer l'oxygene'. Condition de survie primaire.",
         used_by="boucle 3 (gestion du systeme vital)",
         obtained="reserve initiale + Flasque d'oxygène (artefact canonique)",
         consumed_by="duree de plongee, avaries de coque",
         consequence="asphyxie = fin de plongee",
         assets=["readout cadran 32x32", "overlay d'alarme"],
         anims=["aiguille", "clignotement d'alerte"],
         tests=["test_oxygene_decroit", "test_asphyxie_termine_plongee"]),
    dict(display="Batterie", failure="etat_panne_seche", consumes=["eclairage", "propulsion"],
         why="game_brief.md: 'batterie / puissance / eclairage'.",
         used_by="boucle 3 et boucle 5 (eteindre les lumieres)",
         obtained="charge initiale", consumed_by="projecteur, propulsion",
         consequence="noir total, perte de controle",
         assets=["readout cadran 32x32"], anims=["aiguille", "chute de tension"],
         tests=["test_batterie_decroit", "test_extinction_reduit_conso"]),
    dict(display="Coque", failure="etat_breche", consumes=[],
         why="game_brief.md: 'gerer la pression'; constraints.md: zones sous pression.",
         used_by="boucle 1 et boucle 5", obtained="integrite initiale",
         consumed_by="pression de profondeur, impacts",
         consequence="breche = perte d'oxygene acceleree",
         assets=["readout cadran 32x32", "overlay de fissure"],
         anims=["fissure progressive", "alarme de breche"],
         tests=["test_pression_endommage_coque", "test_breche_accelere_perte_oxygene"]),
    dict(display="Propulsion", failure="etat_derive", consumes=["batterie"],
         why="game_brief.md: 'piloter le sous-marin', 'quand avancer, quand reculer'.",
         used_by="boucle 1 et boucle 5 (fuir)", obtained="carburant initial",
         consumed_by="deplacement, fuite",
         consequence="derive: le Pilote ne peut plus fuir",
         assets=["readout cadran 32x32"], anims=["poussee", "cale"],
         tests=["test_fuite_requiert_propulsion"]),
    dict(display="Projecteur", failure="etat_obscurite", consumes=["batterie"],
         why="game_brief.md: 'quand eteindre les lumieres' — verbe de gameplay central.",
         used_by="boucle 2 (observer) et boucle 5",
         obtained="equipement de bord + Lampe de secours (artefact canonique)",
         consumed_by="batterie",
         consequence="obscurite: les anomalies changent de comportement",
         assets=["overlay de faisceau", "readout 32x32"],
         anims=["allumage", "extinction", "vacillement"],
         tests=["test_extinction_modifie_visibilite"]),
]

# ------------------------------------------------ actions (DERIVED du brief)
ACTIONS = [
    ("Avancer", "systeme_propulsion", "boucle 1"),
    ("Reculer", "systeme_propulsion", "boucle 5"),
    ("Observer", None, "boucle 2"),
    ("Eteindre les lumières", "systeme_projecteur", "boucle 5"),
    ("Fuir", "systeme_propulsion", "boucle 5"),
    ("Réparer", "systeme_coque", "boucle 5"),
    ("Récupérer", None, "boucle 4"),
    ("Interpréter", None, "boucle 6"),
]

ZONE_ROLES = {
    "zone_le_vitrail_noire": ("base", "Point d'observation et de depart. N'est pas une "
                                      "zone d'exploration (canon: 'sous-marin de depart')."),
    "zone_la_faille_des_echos": ("exploration", "Canon: 'sombre et instable'."),
    "zone_le_corridor_des_yeux": ("exploration", "Canon: 'l'ombre parait vivante'."),
    "zone_les_ruines_du_son": ("exploration", "Canon: 'vestiges de structures anciennes "
                                              "et de materiel perdu'."),
}

ARTIFACT_FUNCTION = {
    "artefact_lampe_de_secours": ("outil", "action_observer", "systeme_projecteur",
        "Eclairer sans consommer la batterie principale.", "boucle 2"),
    "artefact_carte_des_profondeurs": ("information", "action_interpreter", None,
        "Situer les zones et leurs liaisons.", "boucle 1"),
    "artefact_flasque_d_oxygene": ("consommable", "action_recuperer", "systeme_oxygene",
        "Prolonger la plongee.", "boucle 3"),
    "artefact_fragment_d_archive_abyssale": ("preuve", "action_interpreter", None,
        "Porter une trace de l'intelligence ancienne (canon).", "boucle 6"),
    "artefact_outil_de_reparation_de_coque": ("outil", "action_reparer", "systeme_coque",
        "Restaurer l'integrite de la coque.", "boucle 5"),
}

EMPTY_REASON = {
    "anomalies": ("dec_nature_formes", "La nature exacte des formes terrifiantes et les "
                  "anomalies observables sont declarees OUVERTES dans canon_initial.md "
                  "et open_decisions.md. Les remplir serait inventer le coeur creatif."),
    "traces": ("dec_nb_artefacts", "Les messages et archives retrouves dans les ruines "
               "sont declares OUVERTS dans canon_initial.md."),
    "evenements": ("dec_nb_evenements", "Le nombre d'evenements de tension et la "
                   "presence d'elements de fin de boucle sont declares OUVERTS."),
    "ressources": ("dec_importance_maintenance", "L'importance des ressources de "
                   "maintenance est declaree OUVERTE dans open_decisions.md."),
}


def build(canon) -> dict:
    zones = []
    for e in canon["entries"]:
        if e["kind"] != "zone" or e["id"] == "zone_abysse_de_veyr":
            continue
        role, why = ZONE_ROLES[e["id"]]
        zones.append({"id": e["id"], "display_name": e["display_name"], "role": role,
                      "status": "CANONICAL", "justification": why,
                      "source": e["source"], "source_line": e["source_line"]})

    systems = []
    for s in SYSTEMS:
        sid = make_id("system", s["display"])
        systems.append({
            "id": sid, "display_name": s["display"], "status": "DERIVED",
            "decision": "dec_systemes_vitaux", "failure_state": s["failure"],
            "consumes": s["consumes"], "why_it_exists": s["why"],
            "used_by_system": s["used_by"], "obtained_by": s["obtained"],
            "consumed_by": s["consumed_by"], "consequence": s["consequence"],
            "required_assets": s["assets"], "required_animations": s["anims"],
            "covering_tests": s["tests"]})

    actions = [{"id": make_id("action", d), "display_name": d, "status": "DERIVED",
                "affects": aff, "loop": loop, "source": "INPUT/game_brief.md"}
               for d, aff, loop in ACTIONS]

    artifacts = []
    for e in canon["entries"]:
        if e["kind"] != "artifact":
            continue
        cat, verb, target, fn, loop = ARTIFACT_FUNCTION[e["id"]]
        artifacts.append({
            "id": e["id"], "display_name": e["display_name"], "status": "CANONICAL",
            "category": cat, "function": fn, "gameplay_verb": verb,
            "acts_on": target, "loop_position": loop,
            "source": e["source"], "source_line": e["source_line"],
            "justification": "Objet canonique enumere dans canon_initial.md."})

    crew = [{"id": e["id"], "display_name": e["display_name"], "status": "CANONICAL",
             "function": e["role"], "source": e["source"], "source_line": e["source_line"]}
            for e in canon["entries"] if e["kind"] == "crew"]

    empty = {name: {"entries": [], "count": 0, "status": "BLOCKED_OPEN_DECISION",
                    "blocking_decision": dec, "reason": why}
             for name, (dec, why) in sorted(EMPTY_REASON.items())}

    return {
        "catalog_version": "1.0.0",
        "systemes_vitaux": {"entries": systems, "count": len(systems), "status": "DERIVED"},
        "zones": {"entries": zones, "count": len(zones), "status": "CANONICAL"},
        "artefacts": {"entries": artifacts, "count": len(artifacts), "status": "CANONICAL"},
        "equipage": {"entries": crew, "count": len(crew), "status": "CANONICAL"},
        "actions": {"entries": actions, "count": len(actions), "status": "DERIVED"},
        **empty,
        "non_applicables": {k: {"status": "NOT_APPLICABLE", "reason": v,
                                "contradiction": "contra_vocabulaire_agricole"}
                            for k, v in sorted(NOT_APPLICABLE.items())},
    }


def all_ids(cat) -> set:
    out = set()
    for key, block in cat.items():
        if isinstance(block, dict) and "entries" in block:
            out |= {e["id"] for e in block["entries"]}
    return out


def write(canon, path=ROOT / "CATALOGS" / "catalogs.json"):
    c = build(canon)
    return c, write_json(path, c)
