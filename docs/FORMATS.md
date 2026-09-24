# Documentation des formats, entrées et sorties

## Format d'échange entre étapes

Toutes les étapes échangent du **JSON UTF-8 déterministe** : clés triées,
indentation 2, saut de ligne final, `ensure_ascii=False`. Deux exécutions
produisent des octets identiques (`pipeline/util.py:jdump`).

## Entrées et sorties par étape

| Étape | Module | Entrée | Sortie |
|---|---|---|---|
| Lecture des entrées | `inputs.py` | `INPUT/*.md`, `CONTRACT/*.md` | état + SHA-256 par fichier |
| Canon verrouillé | `canon.py` | `canon_initial.md` | `CANON/canon_central.json` |
| Décisions | `decisions.py` | les 4 entrées | `REPORTS/decisions.json` |
| Contradictions | `contradictions.py` | toutes les entrées | `REPORTS/contradictions.json` |
| Ontologie | `ontology.py` | brief + canon | `ONTOLOGY/ontology.json` |
| Schémas | `schemas.py` | ontologie | `SCHEMAS/schemas.json` |
| Catalogues | `catalogs.py` | canon | `CATALOGS/catalogs.json` |
| Graphe | `graph.py` | catalogues | `GRAPH/world_graph.json`, `connectivity.json` |
| Manifests | `manifests.py` | canon + catalogues + graphe | `MANIFESTS/manifest_*.json` |
| Prompts | `prompts.py` | tout ce qui précède | `PROMPTS/**` |
| Adaptateur Blender | `blender_adapter.py` | manifest d'asset | job Blender / `BLOCKED` |
| Import | `importers.py` | réponse JSON + binaire | `ASSETS_BIN/**`, `REPORTS/import_report.json` |
| Validation | `validators.py` | tout | `REPORTS/validation_report.json` |
| Simulation | `simulate.py` | catalogues | `REPORTS/simulation_report.json` |
| Compilation | `compile_runtime.py` | tout | `RUNTIME/runtime_data.json` |
| Rapports | `reports.py` | tout | `REPORTS/*_report.json` |

## Format des binaires acceptés

- PNG indexé 8 bits, chunk `PLTE` présent, palette incluse dans `CANON/palette.json`.
- Dimensions multiples de 16 (tuile logique imposée par `constraints.md`).
- Taille ≤ 8 Mio.
- Stockés dans `ASSETS_BIN/<famille>/<asset_id>.<ext>`, **jamais modifiés**.
- Empreinte SHA-256 enregistrée dans `ASSETS_BIN/registry.json`.

## Codes d'erreur de vérification binaire

| Code | Signification |
|---|---|
| `asset.file_missing` | fichier absent, illisible, ou hors du dossier de livraison |
| `asset.file_format` | octets magiques non reconnus ou incohérents avec le manifest |
| `asset.file_corrupt` | CRC de chunk PNG invalide, segment JPEG invalide, troncature |
| `asset.file_hash` | SHA-256 réel ≠ SHA-256 déclaré |
| `asset.file_dimensions` | dimensions réelles ≠ dimensions du manifest |
| `asset.file_palette` | `PLTE` contient des couleurs hors palette imposée |
| `asset.file_too_large` | taille > 8 Mio |

Codes d'import : `import.unknown_asset`, `import.manifest_mismatch`,
`import.unknown_variant`, `import.unknown_direction`,
`import.partial_binary_declaration`, `import.generator_blocked`, `import.status`.

## Cycles de statut

```
asset   : PLANNED → GENERATED → IMPORTED → VALIDATED → RUNTIME_TESTED → ART_GREEN
entité  : SPECIFIED → SCHEMA_VALIDATED → IMPORTED → CATALOGED
          → GRAPH_CONNECTED → COMPILED → RUNTIME_TESTED → PRODUCTION_READY
info    : CANONICAL | DERIVED | PROPOSED | TO_VALIDATE
```

Aucun saut d'étape n'est possible : `pipeline/status.py` lève `ValueError`.
`BLOCKED` est un état terminal qui exige une levée explicite.
