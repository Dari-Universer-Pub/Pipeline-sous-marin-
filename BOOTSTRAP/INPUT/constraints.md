# Contraintes de production

## Technique

- Moteur cible : Godot 4.
- Jeu 2D pixel art à la première personne / vue unique depuis la vitre du sous-marin.
- Perspective : l’écran montre seulement la vitre, le cockpit, et l’abyssal devant.
- Tuiles logiques : 16 × 16 pixels.
- Rendu pixel art avec mise à l’échelle entière.
- Données exportables en JSON ou ressources Godot.
- Le joueur ne voit pas le monde entier : il voit seulement une fenêtre de profondeur et ce qu’elle laisse passer.

## Architecture

- Le canon est une source de vérité.
- Les entités sont reliées dans un graphe.
- Les objets, anomalies, traces et structures sont générés depuis les systèmes de survie et d’exploration.
- Les assets sont dérivés des entités, des anomalies et des conditions de la plongée.
- Les animations sont dérivées des états du sous-marin, des alarmes, des frissons visuels et des présences.
- Les zones doivent inclure pression, obscurité, mouvements, phénomènes, dangers et indices narratifs.

## IA

- Le LLM est utilisé hors ligne pour concevoir, générer, vérifier et corriger.
- Le jeu final ne doit pas dépendre d’un LLM en permanence.
- Aucun prompt ne doit fonctionner sans contexte canonique.

## Qualité

- Aucun objet orphelin.
- Aucun asset non référencé.
- Aucune anomalie sans trace dans le monde.
- Aucune zone de plongée sans tension ou menace claire.
- Toute sortie doit être validée avant import.
- L’atmosphère doit rester oppressante sans jamais devenir incohérente.
