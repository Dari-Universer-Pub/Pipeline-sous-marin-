# PROMPT FAMILLE — famille_fond_abyssal

Les elements de cette famille sont VISUELLEMENT INTERDEPENDANTS: ils doivent
etre produits ENSEMBLE et partager grammaire de forme, valeurs et palette.

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
    "filename": "asset_zone_la_faille_des_echos_fond.png",
    "format": "png",
    "output_dir": "ASSETS_IN/famille_fond_abyssal",
    "tool": "framework_blender"
  },
  "functional_sheet": {
    "display_name": "La Faille des Échos",
    "id": "zone_la_faille_des_echos",
    "justification": "Canon: 'sombre et instable'.",
    "role": "exploration",
    "source": "INPUT/canon_initial.md",
    "source_line": 15,
    "status": "CANONICAL"
  },
  "graph_relations": {
    "degree": 3,
    "incoming": [
      {
        "from": "zone_le_vitrail_noire",
        "status": "DERIVED",
        "to": "zone_la_faille_des_echos",
        "type": "connects_to"
      }
    ],
    "outgoing": [
      {
        "from": "zone_la_faille_des_echos",
        "status": "DERIVED",
        "to": "zone_le_vitrail_noire",
        "type": "connects_to"
      },
      {
        "from": "zone_la_faille_des_echos",
        "status": "DERIVED",
        "to": "systeme_coque",
        "type": "damages"
      }
    ]
  },
  "manifest": {
    "animations": [],
    "asset_type": "tile",
    "blocked_by": null,
    "directions": [
      "none"
    ],
    "entity_id": "zone_la_faille_des_echos",
    "family": "famille_fond_abyssal",
    "format": "png",
    "height": 16,
    "id": "asset_zone_la_faille_des_echos_fond",
    "output_rules": {
      "dir": "ASSETS_IN/famille_fond_abyssal",
      "filename": "asset_zone_la_faille_des_echos_fond.png",
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
    "producer": "framework_blender",
    "resolution": "16x16@1x",
    "status": "PLANNED",
    "style": "pixel art 2D, mise a l'echelle entiere, sombre / oppressant / atmospherique, vue unique depuis l'interieur du sous-marin",
    "validations": [
      "binaire: octets magiques PNG + IHDR",
      "binaire: CRC valide sur chaque chunk",
      "binaire: SHA-256 reel == SHA-256 declare",
      "binaire: dimensions reelles == 16x16",
      "binaire: PLTE inclus dans palette_abysse_16",
      "binaire: taille <= 8 Mio",
      "reference: entity_id present dans le graphe"
    ],
    "variants": [
      "proche",
      "moyen",
      "lointain"
    ],
    "width": 16
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
  "production_status": "PLANNED",
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
    "binaire: dimensions reelles == 16x16",
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


## Membres de la famille
- asset_zone_la_faille_des_echos_fond (16x16, variantes: ['proche', 'moyen', 'lointain'])
- asset_zone_le_corridor_des_yeux_fond (16x16, variantes: ['proche', 'moyen', 'lointain'])
- asset_zone_les_ruines_du_son_fond (16x16, variantes: ['proche', 'moyen', 'lointain'])

## Regles
- Coherence inter-membres obligatoire (bords, valeurs, epaisseur de trait).
- Les transitions de terrain doivent raccorder sans couture sur 16 px.
- Meme palette imposee pour tous les membres.
- Un membre manquant => BLOCKED pour la famille entiere, pas de livraison partielle
  silencieuse.

## Reponse attendue
JSON strict: un objet racine avec `family` et `assets`: [ ... ] conforme au contrat.
