# Outils externes — GABARIT À REMPLIR

> **Ce fichier est un gabarit, pas une déclaration.**
> `INPUT/external_tools.md` est **absent** du bootstrapper livré. Son contenu n'a
> **pas** été inventé. Copiez ce gabarit vers `INPUT/external_tools.md`,
> remplissez-le avec les valeurs **réelles** de votre machine, puis relancez
> `python3 -m pipeline.cli all`.

## Framework Blender

```yaml
id: framework_blender
name: "<nom réel du framework>"
role: "production visuelle hors ligne: modèles, matériaux, rendus, sprites, animations"
path: "<CHEMIN RÉEL — remplace C:\CHEMIN\A\REMPLACER\FRAMEWORK_BLENDER>"
entry_script: "<script d'entrée réel, ex: main.py>"
builders: []            # laissé vide: rempli par l'inspection réelle
input_formats: ["json"]
output_formats: ["png"]
output_paths: ["ASSETS_IN/<famille>"]
blender_version: "<version réelle>"
runtime_required: false  # DOIT rester false: le jeu final ne dépend pas de Blender
```

## Déclaration du chemin — trois voies équivalentes

La pipeline résout le chemin dans cet ordre, et **n'invente jamais** :

1. argument explicite passé au CLI
   ```bash
   python3 -m pipeline.cli blender /chemin/reel/FRAMEWORK_BLENDER
   ```
2. variable d'environnement
   ```bash
   export ABYSSAL_BLENDER_FRAMEWORK="/chemin/reel/FRAMEWORK_BLENDER"   # POSIX
   setx ABYSSAL_BLENDER_FRAMEWORK "D:\chemin\reel\FRAMEWORK_BLENDER"   # Windows
   ```
3. fichier `config/external_tools.json`
   ```json
   { "blender_framework": { "path": "/chemin/reel/FRAMEWORK_BLENDER" } }
   ```

Si aucune voie ne donne un dossier existant, l'étape Blender retourne `BLOCKED`.
Aucun asset n'est produit par un autre moyen, aucun placeholder n'est dessiné.
