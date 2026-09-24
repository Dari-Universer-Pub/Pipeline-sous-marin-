# PROMPT ASSET — asset_artefact_carte_des_profondeurs_icone

Tu produis UN asset pour le jeu Abyssal Glass via le framework Blender declare.

## Contexte injecte (ne rien deviner, tout est fourni)
{
  "canon": {
    "declared_open": [
      "La nature exacte des formes terrifiantes.",
      "Le nombre exact des zones profondes.",
      "Les anomalies observables depuis la vitre.",
      "Les messages ou archives retrouves dans les ruines.",
      "Le vrai but de la plongee finale."
    ],
    "forbidden": [
      "combat heroique comme boucle centrale",
      "lexique high fantasy / noms ornes",
      "surnaturel explicite sans mystere",
      "objet abyssal presente comme entierement rassurant"
    ],
    "immutable_rules": [
      "La profondeur contient des traces d'une intelligence ancienne.",
      "Les objets trouves dans les abysses ne sont jamais entierement rassurants.",
      "Le jeu repose sur la survie, l'observation et la peur, pas sur un combat de style heroique."
    ],
    "naming_rule": "Les noms doivent etre simples, claquants, sinistres, precis. Eviter toute surenchere fantasy, toute langue trop ornate, et toute reference trop explicite au surnaturel sans mystere.",
    "player_name": "le Pilote",
    "vessel_name": "le Vitrail Noire",
    "world_name": "l'Abysse de Veyr"
  },
  "correction_strategy": "En cas de rejet, corriger UNIQUEMENT le champ signale par le code d'erreur et relivrer. Ne jamais redessiner un binaire deja accepte.",
  "expected_output": {
    "filename": "asset_artefact_carte_des_profondeurs_icone.png",
    "format": "png",
    "output_dir": "ASSETS_IN/famille_artefacts",
    "tool": "framework_blender"
  },
  "functional_sheet": {
    "acts_on": null,
    "category": "information",
    "display_name": "Carte des profondeurs",
    "function": "Situer les zones et leurs liaisons.",
    "gameplay_verb": "action_interpreter",
    "id": "artefact_carte_des_profondeurs",
    "justification": "Objet canonique enumere dans canon_initial.md.",
    "loop_position": "boucle 1",
    "source": "INPUT/canon_initial.md",
    "source_line": 28,
    "status": "CANONICAL"
  },
  "graph_relations": {
    "degree": 2,
    "incoming": [],
    "outgoing": [
      {
        "from": "artefact_carte_des_profondeurs",
        "status": "DERIVED",
        "to": "zone_le_vitrail_noire",
        "type": "located_in"
      },
      {
        "from": "artefact_carte_des_profondeurs",
        "status": "DERIVED",
        "to": "action_interpreter",
        "type": "requires"
      }
    ]
  },
  "manifest": {
    "animations": [],
    "asset_type": "sprite",
    "blocked_by": null,
    "directions": [
      "none"
    ],
    "entity_id": "artefact_carte_des_profondeurs",
    "family": "famille_artefacts",
    "format": "png",
    "height": 32,
    "id": "asset_artefact_carte_des_profondeurs_icone",
    "output_rules": {
      "dir": "ASSETS_IN/famille_artefacts",
      "filename": "asset_artefact_carte_des_profondeurs_icone.png",
      "indexed": true,
      "max_bytes": 8388608,
      "must_declare": [
        "file",
        "file_sha256"
      ],
      "no_resize_after_delivery": true
    },
    "palette": [
      [
        3,
        5,
        8
      ],
      [
        8,
        12,
        18
      ],
      [
        14,
        22,
        30
      ],
      [
        20,
        34,
        44
      ],
      [
        28,
        50,
        60
      ],
      [
        38,
        70,
        78
      ],
      [
        52,
        94,
        98
      ],
      [
        72,
        120,
        118
      ],
      [
        98,
        148,
        140
      ],
      [
        140,
        180,
        172
      ],
      [
        186,
        210,
        200
      ],
      [
        232,
        238,
        230
      ],
      [
        86,
        28,
        32
      ],
      [
        140,
        52,
        44
      ],
      [
        196,
        126,
        58
      ],
      [
        58,
        24,
        66
      ]
    ],
    "produced_sha256": "27d517f629b8952b14d2dcee5223b5c85f76d9f3c5ecbee05c086a2d3a1df9cf",
    "producer": "framework_blender",
    "resolution": "32x32@1x",
    "status": "ART_GREEN",
    "style": "pixel art 2D, mise a l'echelle entiere, sombre / oppressant / atmospherique, vue unique depuis l'interieur du sous-marin",
    "validations": [
      "binaire: octets magiques PNG + IHDR",
      "binaire: CRC valide sur chaque chunk",
      "binaire: SHA-256 reel == SHA-256 declare",
      "binaire: dimensions reelles == 32x32",
      "binaire: PLTE inclus dans palette_abysse_16",
      "binaire: taille <= 8 Mio",
      "reference: entity_id present dans le graphe"
    ],
    "variants": [],
    "width": 32
  },
  "ontology": {
    "entity_types": [
      "action",
      "animation",
      "anomaly",
      "artifact",
      "asset",
      "crew",
      "event",
      "resource",
      "state",
      "trace",
      "vessel_system",
      "zone"
    ],
    "not_applicable": [
      "boss",
      "creature",
      "crop",
      "machine",
      "quest",
      "recipe"
    ],
    "relation_types": [
      "animates",
      "connects_to",
      "consumes",
      "damages",
      "depicts",
      "evidence_of",
      "has_state",
      "knows",
      "located_in",
      "observed_in",
      "produces",
      "repairs",
      "requires",
      "reveals",
      "threatens",
      "triggered_by",
      "uses_asset"
    ]
  },
  "production_status": "ART_GREEN",
  "response_contract": {
    "binary_fields": {
      "file": "chemin du binaire livre, OBLIGATOIREMENT sous ASSETS_IN/<famille>/",
      "file_sha256": "empreinte SHA-256 reelle du binaire livre (64 hex minuscules)"
    },
    "binary_rule": "Sans 'file' et 'file_sha256', la reponse reste une SPECIFICATION valide (binaire attendu plus tard). Avec ces champs, toute non-conformite binaire entraine le REJET.",
    "error_codes": [
      "asset.file_missing",
      "asset.file_corrupt",
      "asset.file_hash",
      "asset.file_dimensions",
      "asset.file_palette",
      "asset.file_too_large",
      "asset.file_format"
    ],
    "forbidden": [
      "inventer un fait narratif",
      "inventer un nom hors canon",
      "redimensionner apres rendu",
      "livrer hors palette imposee",
      "presenter un placeholder comme contenu final"
    ],
    "format": "JSON strict, UTF-8, une seule racine objet",
    "on_missing_information": "Retourner {\"status\": \"BLOCKED\", \"missing\": [...]} et NE RIEN INVENTER.",
    "required_fields": [
      "asset_id",
      "entity_id",
      "status",
      "width",
      "height",
      "format",
      "variants",
      "directions"
    ]
  },
  "validations": [
    "binaire: octets magiques PNG + IHDR",
    "binaire: CRC valide sur chaque chunk",
    "binaire: SHA-256 reel == SHA-256 declare",
    "binaire: dimensions reelles == 32x32",
    "binaire: PLTE inclus dans palette_abysse_16",
    "binaire: taille <= 8 Mio",
    "reference: entity_id present dans le graphe"
  ],
  "visual_constraints": {
    "engine": "Godot 4",
    "palette_size": 16,
    "scaling": "entiere",
    "style": "pixel art 2D, mise a l'echelle entiere, sombre / oppressant / atmospherique, vue unique depuis l'interieur du sous-marin",
    "tile": 16,
    "view": "vue unique depuis l'interieur du sous-marin"
  }
}


## Tache
Produire l'asset `asset_artefact_carte_des_profondeurs_icone` de l'entite `artefact_carte_des_profondeurs`, famille `famille_artefacts`,
en 32x32 px, format png, palette imposee (16 teintes),
variantes: aucune, directions: ['none'].

## Regles
- Respecter EXACTEMENT asset_id, entity_id et le chemin de sortie.
- Ne jamais inventer un fait narratif ni un nom hors canon.
- Si une information manque: repondre BLOCKED avec la liste `missing`.
- Un asset rendu n'est PAS termine: il sera importe, verifie en binaire, valide,
  puis teste en contexte runtime.

## Reponse attendue
JSON strict conforme a `response_contract` ci-dessus.
