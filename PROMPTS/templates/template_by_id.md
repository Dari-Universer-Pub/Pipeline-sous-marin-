# PROMPT ASSET — {asset_id}

Tu produis UN asset pour le jeu Abyssal Glass via le framework Blender declare.

## Contexte injecte (ne rien deviner, tout est fourni)
{context}

## Tache
Produire l'asset `{asset_id}` de l'entite `{entity_id}`, famille `{family}`,
en {width}x{height} px, format {fmt}, palette imposee ({palette_size} teintes),
variantes: {variants}, directions: {directions}.

## Regles
- Respecter EXACTEMENT asset_id, entity_id et le chemin de sortie.
- Ne jamais inventer un fait narratif ni un nom hors canon.
- Si une information manque: repondre BLOCKED avec la liste `missing`.
- Un asset rendu n'est PAS termine: il sera importe, verifie en binaire, valide,
  puis teste en contexte runtime.

## Reponse attendue
JSON strict conforme a `response_contract` ci-dessus.
