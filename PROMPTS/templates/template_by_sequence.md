# PROMPT SEQUENCE ANIMEE — {animation_id}

## Contexte injecte
{context}

## Sequence
entite: {entity_id}
etat/action: {state_or_action}
direction: {direction}
frames: {frames}   fps: {fps}   boucle: {loop}
frame d'impact: {impact_frame}
effet logique declenche: {effect}
transitions possibles: {transitions}

## Regles
- L'animation n'est PAS seulement visuelle: la frame d'impact doit coincider
  avec l'instant ou l'effet logique s'applique dans le moteur.
- Le nombre de frames livre doit etre EXACTEMENT {frames}.
- Chaque frame respecte la palette imposee et les dimensions de l'asset source.

## Reponse attendue
JSON strict conforme au contrat, avec `produced_animations` renseigne.
