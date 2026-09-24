# PROMPT SEQUENCE ANIMEE — anim_systeme_batterie_etat_alerte

## Contexte injecte
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
    "filename": "asset_systeme_batterie_cadran.png",
    "format": "png",
    "output_dir": "ASSETS_IN/famille_cockpit",
    "tool": "framework_blender"
  },
  "functional_sheet": {
    "consequence": "noir total, perte de controle",
    "consumed_by": "projecteur, propulsion",
    "consumes": [
      "eclairage",
      "propulsion"
    ],
    "covering_tests": [
      "test_batterie_decroit",
      "test_extinction_reduit_conso"
    ],
    "decision": "dec_systemes_vitaux",
    "display_name": "Batterie",
    "failure_state": "etat_panne_seche",
    "id": "systeme_batterie",
    "obtained_by": "charge initiale",
    "required_animations": [
      "aiguille",
      "chute de tension"
    ],
    "required_assets": [
      "readout cadran 32x32"
    ],
    "status": "DERIVED",
    "used_by_system": "boucle 3 et boucle 5 (eteindre les lumieres)",
    "why_it_exists": "game_brief.md: 'batterie / puissance / eclairage'."
  },
  "graph_relations": {
    "degree": 3,
    "incoming": [
      {
        "from": "equipage_mara",
        "status": "CANONICAL",
        "to": "systeme_batterie",
        "type": "knows"
      },
      {
        "from": "systeme_projecteur",
        "status": "DERIVED",
        "to": "systeme_batterie",
        "type": "consumes"
      },
      {
        "from": "systeme_propulsion",
        "status": "DERIVED",
        "to": "systeme_batterie",
        "type": "consumes"
      }
    ],
    "outgoing": []
  },
  "manifest": {
    "animations": [],
    "asset_type": "readout",
    "blocked_by": null,
    "directions": [
      "none"
    ],
    "entity_id": "systeme_batterie",
    "family": "famille_cockpit",
    "format": "png",
    "height": 32,
    "id": "asset_systeme_batterie_cadran",
    "output_rules": {
      "dir": "ASSETS_IN/famille_cockpit",
      "filename": "asset_systeme_batterie_cadran.png",
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
    "status": "IMPORTED",
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
    "variants": [
      "nominal",
      "alerte",
      "critique"
    ],
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
  "production_status": "IMPORTED",
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


## Sequence
entite: systeme_batterie
etat/action: etat_alerte
direction: none
frames: 4   fps: 6   boucle: True
frame d'impact: 0
effet logique declenche: {'target': 'systeme_batterie.alarm', 'op': 'set', 'value': True}
transitions possibles: ['etat_nominal', 'etat_critique']

## Regles
- L'animation n'est PAS seulement visuelle: la frame d'impact doit coincider
  avec l'instant ou l'effet logique s'applique dans le moteur.
- Le nombre de frames livre doit etre EXACTEMENT 4.
- Chaque frame respecte la palette imposee et les dimensions de l'asset source.

## Reponse attendue
JSON strict conforme au contrat, avec `produced_animations` renseigne.
