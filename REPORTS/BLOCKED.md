# Rapport de blocage

Deux étapes sont bloquées. Aucune n'a été contournée par une invention.

---

## 1. Framework Blender introuvable

**Statut :** `BLOCKED` · décision `dec_chemin_blender` · contradiction `contra_chemin_blender`

**Chemin manquant :**

```
C:\CHEMIN\A\REMPLACER\FRAMEWORK_BLENDER
```

Ce chemin est explicitement marqué « À REMPLACER » dans la commande. Il n'existe
pas. Aucun binaire `blender` n'est présent dans l'environnement.

**Ce qui n'a pas été fait, délibérément :**

- aucun chemin inventé ;
- aucun outil de substitution ;
- aucun asset généré par un autre moyen ;
- aucun placeholder dessiné à la place d'un binaire attendu.

**Conséquence :** 13 assets et 10 animations restent au statut `PLANNED`.
`ASSETS_BIN` ne contient que les fixtures du test de bout en bout.

**Levée — trois voies équivalentes :**

```bash
# 1. argument du CLI
python3 -m pipeline.cli blender /chemin/reel/FRAMEWORK_BLENDER

# 2. variable d'environnement
export ABYSSAL_BLENDER_FRAMEWORK="/chemin/reel/FRAMEWORK_BLENDER"   # POSIX
setx ABYSSAL_BLENDER_FRAMEWORK "D:\chemin\reel\FRAMEWORK_BLENDER"   # Windows

# 3. fichier de configuration
cat > config/external_tools.json <<'JSON'
{ "blender_framework": { "path": "/chemin/reel/FRAMEWORK_BLENDER" } }
JSON
```

Une fois déclaré, `python3 -m pipeline.cli blender` inspecte l'arborescence
réelle et remplit le rapport de compatibilité : scripts d'entrée, builders,
formats d'entrée et de sortie, chemins de sortie. **Rien n'est présumé de son
contenu avant inspection.**

---

## 2. `INPUT/external_tools.md` absent

**Statut :** `BLOCKED` · contradiction `contra_external_tools_absent`

La commande impose de lire `INPUT/external_tools.md` et en fait la source de
vérité des outils externes. Le bootstrapper livré ne le contient pas : il fournit
5 fichiers d'entrée sur les 6 attendus. Le contrat V2, lui, n'en liste que 4.

**Ce qui n'a pas été fait :** le fichier n'a pas été inventé.

**Levée :**

```bash
cp docs/external_tools.template.md INPUT/external_tools.md
# puis remplir avec les valeurs réelles
python3 -m pipeline.cli all
```

---

## Décisions ouvertes bloquant du contenu

Ces décisions appartiennent au **propriétaire du projet**. La pipeline ne les
tranche pas et ne promeut aucune d'elles en fait canonique.

| Décision | Ce qu'elle bloque |
|---|---|
| `dec_nature_formes` | catalogue d'anomalies, `famille_anomalies`, effets de présence |
| `dec_nb_anomalies` | dimensionnement des assets et animations d'anomalie |
| `dec_nb_artefacts` | `famille_traces`, contenu des archives des Ruines du Son |
| `dec_nb_evenements` | catalogue d'événements de tension |
| `dec_duree_plongee` | validateurs économique et temporel |
| `dec_frequence_degats` | équilibrage de la tension |
| `dec_importance_maintenance` | catalogue de ressources |
| `dec_procedural_fond` | maps fixes ou générées |
| `dec_fin_de_boucle` | événements terminaux |
| `dec_coherence_psy` | validateur narratif sur les anomalies |
| `dec_nb_zones_profondes` | maps au-delà des 4 zones canoniques |
| `ambig_vitrail_noire_genre` | confirmation du nom canonique (repris verbatim) |

Détail complet et conséquences : `REPORTS/open_decisions_report.json`.
