# Pipeline V5 Graph-Driven — *Abyssal Glass*

Fabrique de production autonome, documentée et testable, construite à partir du
bootstrapper et des entrées du projet.

> **Cette pipeline produit la fabrique, pas le jeu.** Aucun asset n'est généré en
> masse, aucune map finale n'est créée, aucune scène Godot n'est écrite.

Python 3.11+, **bibliothèque standard uniquement**, aucune dépendance externe.

```bash
python3 -m pipeline.cli all              # pipeline complète
python3 -m unittest discover -s tests    # 61 tests
```

## État actuel — 2 blocages réels

| # | Blocage | Effet | Levée |
|---|---|---|---|
| 1 | **Framework Blender introuvable.** Le chemin fourni (`C:\CHEMIN\A\REMPLACER\…`) est un placeholder explicite ; il n'existe pas. | Aucun asset produit. 23 assets/animations restent `PLANNED`. | `docs/external_tools.template.md` |
| 2 | **`INPUT/external_tools.md` absent** du bootstrapper (5 entrées livrées sur 6). | Les outils externes ne sont pas déclarés. | copier le gabarit dans `INPUT/` |

Aucun chemin n'a été inventé, aucun outil substitué, aucun placeholder dessiné.
Voir `REPORTS/BLOCKED.md`.

## Ce que disent les entrées

*Abyssal Glass* : survival horror sous-marin 2D pixel art, vue unique depuis la
vitre du **Vitrail Noire**, dans l'**Abysse de Veyr**. Godot 4, tuiles 16×16.
Survie, observation et peur — **pas** de combat héroïque (fait canonique).

## Arborescence

```
INPUT/            entrées officielles (inchangées)
CONTRACT/         contrat universel (NON modifié)
BOOTSTRAP/        bootstrapper d'origine, préservé
CANON/            canon verrouillé + palette
ONTOLOGY/         types d'entités et de relations
SCHEMAS/          schémas de données
CATALOGS/         catalogues fonctionnels
GRAPH/            graphe du monde + connectivité
MANIFESTS/        manifests de production
PROMPTS/          templates + prompts contextualisés d'exemple
ASSETS_IN/        dossier de livraison des binaires
ASSETS_BIN/       stockage de référence des binaires acceptés (jamais modifié)
RUNTIME/          sortie compilée pour le moteur
REPORTS/          tous les rapports
pipeline/         code de la pipeline (17 modules)
tests/            61 tests
tools/            générateur de fixtures PNG (tests uniquement)
docs/             RUN.md, FORMATS.md, gabarit outils externes
fixtures/         exemples de sortie valide et invalide
```

## Modules

| Module | Rôle |
|---|---|
| `util.py` | JSON déterministe, SHA-256, anti-traversée de chemin |
| `ids.py` | ID interne stable vs nom affiché, règles de nommage |
| `status.py` | cycles de vie, **aucun saut d'étape possible** |
| `inputs.py` | chargement + empreinte + contrôle UTF-8 des entrées |
| `canon.py` | canon verrouillé, chaque fait tracé à sa ligne source |
| `decisions.py` | 24 décisions : statut, source, justification, conséquences |
| `contradictions.py` | 7 contradictions détectées entre les entrées |
| `ontology.py` | 12 types d'entités, 17 relations, 6 types non applicables |
| `schemas.py` | 13 schémas + validateur structurel |
| `palette.py` | palette imposée (`PROPOSED`, modulaire) |
| `catalogs.py` | catalogues fonctionnels, quantités justifiées |
| `graph.py` | graphe + orphelins, puits, profondeur causale |
| `manifests.py` | manifests assets, animations, maps, placement, objets, PNJ |
| `prompts.py` | prompts par ID / par famille / par séquence + injecteur de contexte |
| `blender_adapter.py` | traduction V5 ↔ Blender, `BLOCKED` si absent |
| `binary_check.py` | **vérification binaire** PNG/JPEG (magie, CRC, SHA-256, dimensions, palette) |
| `assets_bin.py` | stockage intact + re-vérification permanente |
| `importers.py` | import, rejet, `IMPORTED` seulement si le binaire est conforme |
| `validators.py` | 19 familles de validateurs |
| `simulate.py` | 8 profils de joueur, état avant/après chaque action |
| `compile_runtime.py` | compilation Godot + preuve d'absence de LLM/Blender |
| `reports.py` | maturité, manquants, isolés, décisions, traçabilité |
| `cli.py` | orchestration |

## Garanties vérifiées par les tests

- Un fichier image **qui existe n'est pas un asset conforme** : un PNG renommé
  `.jpg`, tronqué, au CRC altéré, redimensionné, hors palette ou dont l'empreinte
  déclarée est fausse est **rejeté** avec un code d'erreur explicite.
- Un binaire accepté est copié **intact** et **jamais modifié** ; toute altération
  ou suppression ultérieure est détectée (`cli verify-bin`).
- Un asset `GENERATED` n'est **jamais** considéré comme terminé : seul `ART_GREEN`
  l'est, et les six étapes sont obligatoires.
- Le runtime compilé ne dépend **ni d'un LLM ni de Blender** (vérifié, et la
  détection est elle-même testée par injection d'une dépendance factice).
- Sorties JSON **déterministes octet par octet** ; même graine, même simulation.

## Honnêteté du contenu

Les catalogues dont le contenu est déclaré **ouvert** par le canon restent
**vides**, avec la décision qui les débloquera — plutôt que remplis d'inventions :
anomalies, traces, événements, ressources. De même, les catalogues réclamés par le
contrat mais sans fondement ici (cultures, machines, recettes, quêtes, créatures,
boss) sont déclarés `NOT_APPLICABLE` avec justification écrite.

Voir `REPORTS/open_decisions_report.json` et `REPORTS/contradictions.json`.

## Documentation

- `docs/RUN.md` — procédure complète d'exécution par une autre IA
- `docs/FORMATS.md` — formats, entrées/sorties de chaque étape, codes d'erreur
- `docs/external_tools.template.md` — gabarit de déclaration du framework Blender
