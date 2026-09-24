# PROMPT FAMILLE — {family}

Les elements de cette famille sont VISUELLEMENT INTERDEPENDANTS: ils doivent
etre produits ENSEMBLE et partager grammaire de forme, valeurs et palette.

## Contexte injecte
{context}

## Membres de la famille
{members}

## Regles
- Coherence inter-membres obligatoire (bords, valeurs, epaisseur de trait).
- Les transitions de terrain doivent raccorder sans couture sur 16 px.
- Meme palette imposee pour tous les membres.
- Un membre manquant => BLOCKED pour la famille entiere, pas de livraison partielle
  silencieuse.

## Reponse attendue
JSON strict: un objet racine avec `family` et `assets`: [ ... ] conforme au contrat.
