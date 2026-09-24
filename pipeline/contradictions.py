"""Contradictions et ambiguites detectees entre les entrees officielles.

Aucune n'est resolue silencieusement: chacune porte une resolution proposee
et, quand elle touche la vision creative, reste TO_VALIDATE.
"""
from __future__ import annotations
from .util import ROOT, write_json
from .inputs import load_all, missing_optional

STATIC = [
    {
        "id": "contra_version_contrat",
        "severity": "BLOCKING_DOC",
        "kind": "incoherence_de_version",
        "sources": ["CONTRACT/architecture_contract.md", "commande utilisateur"],
        "detail": "Le contrat livre s'intitule 'Contrat d'architecture Graph-Driven V2' "
                  "alors que la commande exige la construction d'une 'Pipeline V5'.",
        "resolution": "La pipeline est nommee V5 (version du produit) et declare se "
                      "conformer au contrat V2 (version du contrat). Les deux numeros "
                      "sont distincts et traces separement dans pipeline/__init__.py. "
                      "Le contrat universel n'est PAS modifie.",
        "status": "RESOLVED_DOCUMENTED",
    },
    {
        "id": "contra_external_tools_absent",
        "severity": "BLOCKING",
        "kind": "entree_obligatoire_manquante",
        "sources": ["INPUT/external_tools.md", "commande utilisateur",
                    "CONTRACT/architecture_contract.md"],
        "detail": "La commande impose de lire INPUT/external_tools.md et en fait le "
                  "lieu de declaration des outils externes. Le bootstrapper ne le "
                  "contient pas, et le contrat V2 ne liste que 4 entrees officielles.",
        "resolution": "Fichier NON invente. Un gabarit vide et commente est fourni "
                      "dans docs/external_tools.template.md. Tant qu'il n'est pas "
                      "rempli, l'etape 'outils externes' reste BLOCKED.",
        "status": "BLOCKED",
    },
    {
        "id": "contra_chemin_blender",
        "severity": "BLOCKING",
        "kind": "outil_externe_absent",
        "sources": ["commande utilisateur"],
        "detail": "Le chemin 'C:\\CHEMIN\\A\\REMPLACER\\FRAMEWORK_BLENDER' est un "
                  "placeholder explicite; il n'existe pas, et aucun binaire 'blender' "
                  "n'est present dans l'environnement.",
        "resolution": "Aucun chemin invente, aucun outil de substitution. L'adaptateur "
                      "retourne BLOCKED avec le chemin manquant et la commande de "
                      "configuration a executer.",
        "status": "BLOCKED",
    },
    {
        "id": "contra_vocabulaire_agricole",
        "severity": "MAJOR",
        "kind": "livrables_sans_fondement_canonique",
        "sources": ["commande utilisateur", "CONTRACT/architecture_contract.md",
                    "INPUT/game_brief.md", "INPUT/canon_initial.md"],
        "detail": "La liste de livrables et le contrat exigent des catalogues de "
                  "cultures, machines, recettes, quetes, creatures et boss. Ce "
                  "vocabulaire est celui d'un jeu de ferme/artisanat. Abyssal Glass "
                  "est un survival horror sous-marin en vue unique: le canon et le "
                  "brief ne contiennent aucune culture, aucune machine de production, "
                  "aucune recette, aucun donneur de quete et aucun boss.",
        "resolution": "Ces catalogues sont declares NOT_APPLICABLE avec justification "
                      "ecrite, et non remplis de contenu invente. Les emplacements de "
                      "schema restent presents pour ne pas modifier le contrat. Les "
                      "analogues reels du jeu (systemes vitaux, anomalies, artefacts, "
                      "traces, evenements de tension) sont catalogues a leur place. "
                      "Promotion possible uniquement par decision du proprietaire.",
        "status": "TO_VALIDATE",
    },
    {
        "id": "contra_tir_vs_canon",
        "severity": "MAJOR",
        "kind": "contradiction_de_gameplay",
        "sources": ["INPUT/game_brief.md", "INPUT/canon_initial.md"],
        "detail": "game_brief.md liste 'tirer' parmi les decisions de survie, tandis "
                  "que canon_initial.md pose comme fait immuable que le jeu 'repose "
                  "sur la survie, l'observation et la peur, pas sur un combat de "
                  "style heroique', et que le brief lui-meme demande une 'tension "
                  "sans combat classique'.",
        "resolution": "Le canon prime sur le brief. 'tirer' n'est PAS catalogue comme "
                      "verbe de combat. Sa nature exacte (dispositif de dissuasion "
                      "non letal, tir de detresse, ou retrait pur) est une decision "
                      "creative du proprietaire.",
        "status": "TO_VALIDATE",
    },
    {
        "id": "contra_tuiles_vs_vue_unique",
        "severity": "MINOR",
        "kind": "ambiguite_technique",
        "sources": ["INPUT/constraints.md"],
        "detail": "constraints.md impose des 'tuiles logiques 16x16' tout en "
                  "specifiant que le joueur 'ne voit pas le monde entier: il voit "
                  "seulement une fenetre de profondeur'. Une grille de tuiles "
                  "parcourable est incompatible avec une vue unique fixe.",
        "resolution": "La tuile 16x16 est conservee comme unite de composition "
                      "graphique et de decoupe d'atlas (contrainte respectee), non "
                      "comme grille de deplacement. Le schema de map decrit une "
                      "'fenetre de profondeur' a couches, pas une tilemap.",
        "status": "RESOLVED_DOCUMENTED",
    },
    {
        "id": "ambig_vitrail_noire_genre",
        "severity": "INFO",
        "kind": "ambiguite_de_nommage",
        "sources": ["INPUT/canon_initial.md"],
        "detail": "'le Vitrail Noire' associe un nom masculin ('vitrail') a un "
                  "adjectif feminin ('noire'). Cela peut etre une intention "
                  "stylistique ou une coquille.",
        "resolution": "Le nom est repris VERBATIM comme canonique, sans correction. "
                      "Un validateur canonique interdit toute variante "
                      "('Vitrail Noir'). Confirmation du proprietaire souhaitee.",
        "status": "TO_VALIDATE",
    },
]


def build() -> dict:
    loaded = load_all()
    dynamic = []
    covered = {src for c in STATIC for src in c["sources"]}
    for path in missing_optional(loaded):
        if path in covered:
            continue  # deja couvert par une entree statique detaillee

        dynamic.append({"id": "contra_input_manquant_" + path.split("/")[-1].split(".")[0],
                        "severity": "BLOCKING", "kind": "entree_manquante",
                        "sources": [path], "detail": f"{path} absent du depot.",
                        "resolution": "Non invente. Voir docs/external_tools.template.md.",
                        "status": "BLOCKED"})
    for path, e in sorted(loaded.items()):
        if e["present"] and not e["utf8"]:
            dynamic.append({"id": "contra_encodage_" + path, "severity": "BLOCKING",
                            "kind": "encodage", "sources": [path],
                            "detail": "Fichier non decodable en UTF-8.",
                            "resolution": "Reencoder en UTF-8 sans BOM.",
                            "status": "BLOCKED"})
    items = STATIC + dynamic
    counts = {}
    for c in items:
        counts[c["severity"]] = counts.get(c["severity"], 0) + 1
    return {"total": len(items), "by_severity": dict(sorted(counts.items())),
            "blocking": sorted(c["id"] for c in items if c["status"] == "BLOCKED"),
            "items": sorted(items, key=lambda c: c["id"])}


def write(path=ROOT / "REPORTS" / "contradictions.json"):
    r = build()
    return r, write_json(path, r)
