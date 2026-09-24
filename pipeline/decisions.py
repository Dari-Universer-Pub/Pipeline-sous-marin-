"""Registre des decisions. Chaque decision porte statut, source, justification,
dependances, consequences et elements affectes.

Regle absolue: une decision creative ouverte n'est JAMAIS promue en fait canonique.
"""
from __future__ import annotations
from .util import ROOT, write_json

BRIEF, CANON, CONSTR, OPEN = ("INPUT/game_brief.md", "INPUT/canon_initial.md",
                              "INPUT/constraints.md", "INPUT/open_decisions.md")


def D(id, statement, status, source, justification, depends_on, consequences, affects,
      value=None, owner=None):
    return {"id": id, "statement": statement, "status": status, "source": source,
            "justification": justification, "depends_on": depends_on,
            "consequences": consequences, "affects": affects,
            "value": value, "owner": owner or ("PROPRIETAIRE"
                                               if status == "TO_VALIDATE" else "PIPELINE")}


DECISIONS = [
    # ---------------------------------------------------- CANONIQUE (contraintes)
    D("dec_moteur_cible", "Le moteur cible est Godot 4.", "CANONICAL", CONSTR,
      "Enonce explicitement dans constraints.md, section Technique.",
      [], ["Le compilateur runtime emet du JSON chargeable par Godot 4."],
      ["compile_runtime", "schema_asset", "RUNTIME/"], value="godot4"),
    D("dec_tuile_logique", "La tuile logique mesure 16x16 pixels.", "CANONICAL", CONSTR,
      "Enonce explicitement dans constraints.md ('Tuiles logiques : 16 x 16 pixels').",
      [], ["Toute dimension d'asset doit etre un multiple de 16."],
      ["manifest_assets", "validators.assets", "blender_adapter"], value=16),
    D("dec_echelle_entiere", "Rendu pixel art a mise a l'echelle entiere.", "CANONICAL",
      CONSTR, "Enonce explicitement dans constraints.md.",
      ["dec_tuile_logique"], ["Aucun asset ne doit etre redimensionne apres livraison."],
      ["validators.assets", "assets_bin"], value=True),
    D("dec_vue_unique", "L'ecran montre seulement la vitre, le cockpit et l'abysse devant.",
      "CANONICAL", CONSTR,
      "Enonce dans constraints.md et confirme par game_brief.md (perspective).",
      [], ["Les 'maps' ne sont pas des tilemaps parcourables mais des fenetres de "
           "profondeur; le schema de map est adapte en consequence."],
      ["schema_map", "manifest_maps", "placement"], value="fenetre_de_profondeur"),
    D("dec_sans_llm_runtime", "Le jeu final ne depend pas d'un LLM a l'execution.",
      "CANONICAL", CONSTR, "Enonce dans constraints.md section IA et dans le contrat.",
      [], ["Les dialogues essentiels sont compiles en donnees conditionnelles."],
      ["compile_runtime", "validators.runtime"], value=True),

    # ---------------------------------------------------- DEDUIT
    D("dec_systemes_vitaux",
      "Le sous-marin expose 5 systemes vitaux: oxygene, batterie, coque/pression, "
      "propulsion/carburant, projecteur/eclairage.", "DERIVED", BRIEF,
      "game_brief.md enumere explicitement 'oxygene, puissance, energie et stabilite' "
      "puis 'oxygene, batterie, pression, carburant' et 'batterie / puissance / "
      "eclairage'. Les 5 systemes sont l'union de ces enumerations, sans ajout.",
      ["dec_vue_unique"],
      ["Chaque systeme genere des etats, donc des animations de cadran et d'alarme.",
       "Chaque systeme definit une condition d'echec de plongee."],
      ["catalogue_systemes", "manifest_animations", "graphe"],
      value=["systeme_oxygene", "systeme_batterie", "systeme_coque",
             "systeme_propulsion", "systeme_projecteur"]),
    D("dec_equipage_trois", "L'equipage non-joueur compte exactement 3 membres.",
      "DERIVED", CANON,
      "canon_initial.md nomme Mara, Ilyan et Sorel et personne d'autre. "
      "Aucun quatrieme membre ne peut etre ajoute sans decision du proprietaire.",
      [], ["Le catalogue PNJ est ferme a 3 entrees + le Pilote."],
      ["catalogue_equipage", "schema_dialogue"], value=3),
    D("dec_zones_canoniques",
      "3 zones d'exploration canoniques + 1 zone de base (le Vitrail Noire).",
      "DERIVED", CANON,
      "canon_initial.md liste 4 lieux connus. Le Vitrail Noire est decrit comme "
      "'sous-marin de depart', donc base et non zone d'exploration.",
      [], ["Le catalogue de zones est initialise a ces 4 entrees uniquement."],
      ["catalogue_zones", "manifest_maps"], value=4),
    D("dec_artefacts_canoniques", "5 objets canoniques, aucun autre.", "DERIVED", CANON,
      "canon_initial.md enumere 5 objets sous 'Objets canoniques'.",
      [], ["Tout objet supplementaire est une proposition a valider."],
      ["catalogue_artefacts", "manifest_objets"], value=5),

    # ---------------------------------------------------- PROPOSE (technique, modulaire)
    D("dec_palette", "Palette de production imposee: 16 teintes abyssales.", "PROPOSED",
      "pipeline",
      "Aucune palette n'est specifiee dans les entrees. constraints.md impose "
      "'sombre, oppressant'. Valeur technique par defaut, modulaire: modifiable dans "
      "CANON/palette.json sans toucher au canon narratif.",
      ["dec_echelle_entiere"],
      ["Les PNG indexes livres sont rejetes si leur PLTE sort de cette palette."],
      ["binary_check", "manifest_assets", "prompts"], value="CANON/palette.json"),
    D("dec_dimensions_asset",
      "Dimensions par defaut: cadran 32x32, silhouette d'anomalie 96x96, "
      "plaque de cockpit 160x64, tuile de fond 16x16.", "PROPOSED", "pipeline",
      "Derive de la tuile 16x16 (tous multiples de 16) et de la vue unique. "
      "Valeurs techniques par defaut, surchargeables par manifest.",
      ["dec_tuile_logique", "dec_vue_unique"],
      ["Le validateur d'asset compare les dimensions reelles a ces valeurs."],
      ["manifest_assets", "blender_adapter"], value=None),
    D("dec_graine_procedurale", "Graine procedurale par defaut = 20260924.", "PROPOSED",
      "pipeline", "Necessaire a la reproductibilite exigee par le contrat. "
      "Valeur arbitraire mais fixee et versionnee.",
      [], ["Deux executions a graine identique produisent des sorties identiques."],
      ["reproducibility", "manifest_maps"], value=20260924),

    # ---------------------------------------------------- A VALIDER (proprietaire)
    D("dec_nb_zones_profondes", "Nombre exact de zones abyssales.", "TO_VALIDATE", OPEN,
      "Liste explicitement comme ouverte dans open_decisions.md ET canon_initial.md. "
      "La pipeline propose 3 (les zones canoniques) comme plancher, sans le figer.",
      ["dec_zones_canoniques"],
      ["Bloque le dimensionnement du manifest de maps au-dela des 4 zones canoniques."],
      ["catalogue_zones", "manifest_maps"], value={"plancher_canonique": 4, "retenu": None}),
    D("dec_nb_anomalies", "Nombre exact d'anomalies visibles depuis la vitre.",
      "TO_VALIDATE", OPEN,
      "Ouvert dans open_decisions.md et canon_initial.md. La nature meme des formes "
      "est declaree ouverte: en deduire un nombre reviendrait a inventer du canon.",
      ["dec_nature_formes"],
      ["Le catalogue d'anomalies reste vide; seule une fixture de test existe."],
      ["catalogue_anomalies", "manifest_assets", "manifest_animations"], value=None),
    D("dec_nature_formes", "Nature exacte des formes terrifiantes.", "TO_VALIDATE", CANON,
      "Declare ouvert sous 'Elements ouverts' dans canon_initial.md. "
      "C'est le coeur creatif du jeu: la pipeline ne le tranche pas.",
      [], ["Bloque anomalies, animations de presence, et la plongee finale."],
      ["catalogue_anomalies", "prompts.famille_anomalie"], value=None),
    D("dec_nb_artefacts", "Nombre exact d'artefacts recuperables au-dela des 5 canoniques.",
      "TO_VALIDATE", OPEN, "Ouvert dans open_decisions.md.",
      ["dec_artefacts_canoniques"], ["Le manifest d'objets s'arrete aux 5 canoniques."],
      ["catalogue_artefacts"], value={"plancher_canonique": 5, "retenu": None}),
    D("dec_duree_plongee", "Duree d'une plongee.", "TO_VALIDATE", OPEN,
      "Ouvert dans open_decisions.md. Impacte directement l'equilibrage oxygene/batterie.",
      ["dec_systemes_vitaux"], ["Bloque le validateur economique et temporel."],
      ["validators.temporel", "simulate"], value=None),
    D("dec_frequence_degats", "Frequence des degats de coque et de perte d'oxygene.",
      "TO_VALIDATE", OPEN, "Ouvert dans open_decisions.md.",
      ["dec_duree_plongee"], ["Bloque l'equilibrage de la tension."],
      ["validators.economique", "simulate"], value=None),
    D("dec_procedural_fond", "Niveau de generation procedurale du fond marin.",
      "TO_VALIDATE", OPEN, "Ouvert dans open_decisions.md.",
      ["dec_graine_procedurale"], ["Determine si les maps sont fixes ou generees."],
      ["manifest_maps", "reproducibility"], value=None),
    D("dec_fin_de_boucle", "Presence ou non d'elements narratifs de fin de boucle.",
      "TO_VALIDATE", OPEN, "Ouvert dans open_decisions.md; lie au 'vrai but de la "
      "plongee finale' declare ouvert dans le canon.",
      [], ["Bloque le catalogue d'evenements terminaux."], ["catalogue_evenements"],
      value=None),
    D("dec_coherence_psy", "Degre de coherence psychologique entre apparitions et indices.",
      "TO_VALIDATE", OPEN, "Ouvert dans open_decisions.md.",
      ["dec_nature_formes"], ["Bloque le validateur narratif sur les anomalies."],
      ["validators.narratif"], value=None),
    D("dec_importance_maintenance", "Importance des ressources de maintenance.",
      "TO_VALIDATE", OPEN, "Ouvert dans open_decisions.md.",
      ["dec_systemes_vitaux"], ["Bloque le dimensionnement des ressources."],
      ["catalogue_ressources"], value=None),
    D("dec_nb_evenements", "Nombre exact d'evenements de tension ou de fuite.",
      "TO_VALIDATE", OPEN, "Ouvert dans open_decisions.md.",
      ["dec_nb_anomalies"], ["Le catalogue d'evenements reste vide hors fixture."],
      ["catalogue_evenements"], value=None),

    # ---------------------------------------------------- BLOQUE (outil externe)
    D("dec_chemin_blender",
      "Chemin local du framework Blender: 'C:\\\\CHEMIN\\\\A\\\\REMPLACER\\\\FRAMEWORK_BLENDER'.",
      "BLOCKED", "prompt utilisateur",
      "Le chemin fourni est un emplacement temporaire explicitement marque "
      "'A REMPLACER'. Il n'existe pas. INPUT/external_tools.md, qui devrait le "
      "declarer, est absent du bootstrapper. Aucun chemin n'est invente.",
      [], ["Toute generation d'asset reelle est BLOCKED.",
           "L'adaptateur est livre, teste a vide, mais ne produit aucun binaire."],
      ["blender_adapter", "manifest_assets", "ASSETS_BIN"], value=None),
]


def by_status() -> dict:
    out = {}
    for d in DECISIONS:
        out.setdefault(d["status"], []).append(d["id"])
    return {k: sorted(v) for k, v in sorted(out.items())}


def build() -> dict:
    return {"decision_count": len(DECISIONS), "by_status": by_status(),
            "decisions": sorted(DECISIONS, key=lambda d: d["id"])}


def write(path=ROOT / "REPORTS" / "decisions.json"):
    r = build()
    return r, write_json(path, r)
