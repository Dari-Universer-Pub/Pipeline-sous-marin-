# Procédure d'exécution par une autre IA

Cette pipeline est autonome. Elle ne nécessite ni cette session, ni réseau, ni
dépendance externe. **Python 3.11+, bibliothèque standard uniquement.**

## 0. Pré-requis

```bash
cd <racine du dépôt>
python3 --version          # >= 3.11
python3 -m unittest discover -s tests   # doit afficher OK
```

## 1. Lire, dans l'ordre

| Ordre | Fichier | Rôle |
|---|---|---|
| 1 | `INPUT/game_brief.md` | idée, genre, boucles, systèmes |
| 2 | `INPUT/canon_initial.md` | **source de vérité narrative** |
| 3 | `INPUT/constraints.md` | contraintes techniques et runtime |
| 4 | `INPUT/open_decisions.md` | décisions non tranchées |
| 5 | `INPUT/external_tools.md` | **ABSENT** — voir `docs/external_tools.template.md` |
| 6 | `CONTRACT/architecture_contract.md` | principes universels (non modifié) |

## 2. Charger l'état de la pipeline

| Fichier | Contenu |
|---|---|
| `CANON/canon_central.json` | canon verrouillé, chaque fait tracé à sa ligne source |
| `CANON/palette.json` | palette imposée (statut `PROPOSED`) |
| `ONTOLOGY/ontology.json` | types d'entités et de relations |
| `SCHEMAS/schemas.json` | schémas de données |
| `CATALOGS/catalogs.json` | catalogues fonctionnels |
| `GRAPH/world_graph.json` | graphe du monde |
| `MANIFESTS/manifest_*.json` | manifests de production |

## 3. Exécuter

```bash
python3 -m pipeline.cli all            # pipeline complète
python3 -m pipeline.cli canon          # canon + décisions + contradictions
python3 -m pipeline.cli manifests      # ontologie + graphe + manifests
python3 -m pipeline.cli prompts        # prompts contextualisés d'exemple
python3 -m pipeline.cli blender [path] # inspection du framework Blender
python3 -m pipeline.cli validate       # 19 familles de validateurs
python3 -m pipeline.cli verify-bin     # re-vérification des binaires stockés
python3 -m pipeline.cli simulate       # 8 profils de joueur
python3 -m pipeline.cli compile        # compilation runtime
python3 -m pipeline.cli report         # maturité, manquants, traçabilité
```

**Codes de sortie :** `0` succès · `1` échec de validation · `2` étape bloquée.

## 4. Déclarer le framework Blender

Tant qu'il n'est pas déclaré, l'étape Blender retourne `BLOCKED` et **aucun asset
n'est produit**. Voir `docs/external_tools.template.md` pour les trois voies de
déclaration. N'inventez jamais un chemin.

## 5. Boucle de production d'un asset

```
manifest (PLANNED)
  └─> prompt contextualisé        PROMPTS/examples/*.md
       └─> adaptateur Blender      pipeline/blender_adapter.py
            └─> binaire livré dans ASSETS_IN/<famille>/
                 └─> import + VÉRIFICATION BINAIRE   pipeline/importers.py
                      ├─ échec -> BLOCKED + code d'erreur, RIEN n'est réparé
                      └─ succès -> copie INTACTE dans ASSETS_BIN + empreinte
                           └─> validateurs -> VALIDATED
                                └─> test en contexte réel -> RUNTIME_TESTED
                                     └─> ART_GREEN
```

Un asset simplement rendu par Blender **n'est pas terminé**. Les six étapes sont
obligatoires et aucune ne peut être sautée (`pipeline/status.py` lève une erreur).

## 6. Réinjecter un résultat

```python
from pipeline.importers import import_result
from pipeline.manifests import build as manifests_build
# ... construire canon/catalogs/graph, puis:
r = import_result(reponse_json, manifests["assets"]["entries"])
print(r["status"], r["errors"])
```

Format de la réponse : `fixtures/examples/reponse_valide.json`.
Exemple rejeté et ses codes : `fixtures/examples/reponse_invalide.json`.

## 7. Procédure de correction

1. Lire le code d'erreur dans `REPORTS/import_report.json`.
2. Corriger **uniquement** le champ signalé, puis relivrer.
3. Ne jamais redessiner un binaire **déjà accepté** : `store()` refuse un
   remplacement par un binaire d'empreinte différente.
4. Un binaire manquant ou corrompu est une **erreur bloquante**, jamais comblée
   par un placeholder.

## 8. Procédure de reprise

La pipeline est **idempotente et déterministe** : relancer `cli all` reconstruit
tous les artefacts à l'identique, octet par octet. `ASSETS_BIN/registry.json`
porte l'état durable des binaires acceptés ; `cli verify-bin` en contrôle
l'intégrité à tout moment.

## 9. Ce qui reste à trancher

Voir `REPORTS/open_decisions_report.json` (12 entrées). Les décisions
`TO_VALIDATE` appartiennent au **propriétaire du projet**, pas à l'IA. En
particulier `dec_nature_formes` bloque les anomalies, leurs assets et leurs
animations : c'est le cœur créatif du jeu, et il n'est pas inventé ici.
