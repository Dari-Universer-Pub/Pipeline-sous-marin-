# Bootstrap Specification

Generated: 2026-09-24T18:46:38

## Input status

[
  {
    "file": "game_brief.md",
    "status": "LOADED",
    "characters": 2287
  },
  {
    "file": "canon_initial.md",
    "status": "LOADED",
    "characters": 1590
  },
  {
    "file": "constraints.md",
    "status": "LOADED",
    "characters": 1484
  },
  {
    "file": "open_decisions.md",
    "status": "LOADED",
    "characters": 792
  }
]

## Mandatory classification
Every fact must be classified as CANONICAL, DERIVED, PROPOSED or TO_VALIDATE. Creative unknowns must not be silently invented.

## Required integration proof
Every content type must pass import → schema → canon → graph → catalog → compiler → runtime fixture.

## Required binary asset verification
Delivered image files must be verified AS BINARIES at import time (stdlib only): real format via magic bytes, integrity (PNG chunk CRC), declared SHA-256 match, real dimensions equal to the manifest specification, real palette (PLTE) subset of the imposed palette, bounded file size. An image file that merely exists is NOT a conforming asset. Accepted binaries are stored under ASSETS_BIN/ and re-verified by a permanent validator family.

## Brief
# Brief — Abyssal Glass

## Identité

Nom provisoire : Abyssal Glass
Genre : survival horror / exploration sous-marine / tension psychologique
Perspective : jeu 2D pixel art, vue unique depuis l’intérieur d’un sous-marin
Plateforme : PC
Style général : sombre, oppressant, atmosphérique, ultra-immersif

## Prémisse

Le joueur pilote un petit sous-marin de recherche dans une zone abyssale où la lumière disparaît et où la mer semble observer en retour. À travers la vitre avant, il voit des formes mouvantes, des silhouettes impossibles, des yeux, des ombres massives, des structures anciennes et des corps qui n’auraient jamais dû être là.

Chaque plongée révèle une vérité plus terrifiante : la profondeur ne contient pas seulement des monstres, mais une conscience. Le sous-marin est un observatoire fragile dans une noirceur vivante.

## Rôle du joueur

Contrôler le sous-marin, gérer l’oxygène, la puissance, l’énergie et la stabilité du vaisseau, tout en observant ce qui se passe devant la vitre. Le joueur doit décider quand avancer, quand reculer, quand éteindre les lumières, quand fuir, et quoi faire avec les traces, enregistrements et éléments trouvés dans les profondeurs.

## Boucles principales

1. Plonger dans des zones abyssales inconnues.
2. Observer les anomalies à travers la vitre.
3. Gérer le système vital du sous-marin (oxygène, batterie, pression, carburant).
4. Découvrir des objets, traces, artefacts ou messages.
5. Prendre des décisions de survie : fuir, observer, réparer, tirer, ou s’éloigner.
6. Interpréter les signes pour comprendre ce qui habite les profondeurs.

## Systèmes souhaités

- navigation sous-marine ;
- gestion de la pression et de l’oxygène ;
- batterie / puissance / éclairage ;
- anomalies visuelles et phénomènes psychologiques ;
- exploration de zones profondes ;
- collecte de fragments / preuves / messages ;
- système de fuite et d’évasion ;
- événements de terreur contextuelle ;
- réparation de systèmes et improvisation ;
- détection de présences et d’ombres ;
- surcroît de tension sans combat classique.

## Contenu souhaité

Le nombre exact d’entrées, d’anomalies, de zones, d’artefacts et d’événements doit être dérivé par la pipeline à partir du système de tension et de survie, sans inventer de contenu arbitrairement.


## Canon
# Canon initial — Abyssal Glass

## Faits immuables

- Le monde s’appelle l’Abysse de Veyr.
- Le joueur est appelé le Pilote.
- Le sous-marin principal s’appelle le Vitrail Noire.
- La profondeur contient des traces d’une intelligence ancienne.
- Les objets trouvés dans les abysses ne sont jamais entièrement rassurants.
- Le jeu repose sur la survie, l’observation et la peur, pas sur un combat de style héroïque.

## Lieux connus

- Le Vitrail Noire : sous-marin de départ et point d’observation principal.
- La Faille des Échos : zone d’exploration sombre et instable.
- Le Corridor des Yeux : couloir profond où l’ombre paraît vivante.
- Les Ruines du Son : vestiges de structures anciennes et de matériel perdu.

## Personnages connus

- Mara : ingénieure de bord, responsable des systèmes du sous-marin.
- Ilyan : navigateur, qui refuse de regarder directement la vitre pendant les plongées.
- Sorel : chercheur de terrain, fasciné par les traces anciennes et jamais totalement serein.

## Objets canoniques

- Lampe de secours.
- Carte des profondeurs.
- Flasque d’oxygène.
- Fragment d’archive abyssale.
- Outil de réparation de coque.

## Règles de nommage

Les noms doivent être simples, claquants, sinistres, précis. Éviter toute surenchère fantasy, toute langue trop ornate, et toute référence trop explicite au surnaturel sans mystère.

## Éléments ouverts

- La nature exacte des formes terrifiantes.
- Le nombre exact des zones profondes.
- Les anomalies observables depuis la vitre.
- Les messages ou archives retrouvés dans les ruines.
- Le vrai but de la plongée finale.


## Constraints
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


## Open decisions
# Décisions encore ouvertes

Ces points peuvent être proposés par l’IA sous forme de recommandations, mais ils doivent être signalés comme décisions ouvertes :

- nombre exact de zones abyssales ;
- nombre exact d’anomalies visibles depuis la vitre ;
- nombre exact d’artefacts récupérables ;
- nombre exact d’événements de tension ou de fuite ;
- niveau de génération procédurale du fond marin ;
- durée d’une plongée ;
- fréquence des dégâts de coque et d’oxygène ;
- importance des ressources de maintenance ;
- présence ou non d’éléments narratifs de fin de boucle ;
- degré de cohérence psychologique entre les apparitions et les indices trouvés.

L’IA peut choisir des valeurs techniques par défaut, mais ne doit pas transformer silencieusement une décision créative en fait canonique.


## Architecture contract
# Contrat d’architecture Graph-Driven V2

## Mission

Construire une pipeline de production autonome, documentée, testable et réutilisable pour un nouveau jeu. La pipeline produit les données, manifests, prompts, validateurs et compilateurs nécessaires. Elle ne produit pas le jeu final pendant cette phase.

## Entrées officielles

- `INPUT/game_brief.md` : direction, genre, prémisse et boucles.
- `INPUT/canon_initial.md` : source de vérité narrative et noms non négociables.
- `INPUT/constraints.md` : contraintes techniques, visuelles et runtime.
- `INPUT/open_decisions.md` : décisions créatives encore ouvertes.

Chaque information reçoit un statut : `CANONICAL`, `DERIVED`, `PROPOSED` ou `TO_VALIDATE`.

## Flux obligatoire

```text
Brief + Canon + Contraintes + Décisions ouvertes
    ↓
Analyse et rapport de contradictions
    ↓
Canon central verrouillé
    ↓
Ontologie et schémas
    ↓
Systèmes de gameplay
    ↓
Catalogue fonctionnel
    ↓
Graphe du monde
    ↓
Manifestes objets, maps, placement, assets, animations
    ↓
Prompts spécialisés contextualisés
    ↓
Génération externe par une autre IA
    ↓
Importation
    ↓
Validation
    ↓
Correction ou régénération ciblée
    ↓
Compilation runtime
```

## Obligations de contenu

Les quantités doivent être déduites des systèmes, chaînes de production, progression, canon, états, directions, variantes et contextes. Aucun objet, asset, animation, quête ou dialogue ne doit être créé sans fonction, relation et test.

Les maps doivent inclure structure, terrain, transitions, relief, collisions, navigation, placement, POI et secrets. Les assets doivent être générés par familles quand ils sont interdépendants. Les animations doivent être liées aux états, actions, directions et effets logiques.

## Intégration de bout en bout obligatoire

Un schéma, un validateur ou un fichier de catalogue ne prouve pas qu’une fonctionnalité est intégrée.

Pour chaque type de contenu, fournir une fixture réaliste traversant :

```text
entrée
→ importation
→ validation du schéma
→ validation du canon
→ validation du graphe
→ catalogue
→ état de pipeline
→ compilation
→ sortie runtime
→ vérification finale
```

Une fonctionnalité est incomplète si elle possède un schéma mais aucun import réel, un validateur mais aucun test d’intégration, un catalogue mais aucun chargement par le compilateur, ou un compilateur sans sortie runtime vérifiée.

## Statuts de maturité

Chaque entité doit pouvoir être suivie par :

`SPECIFIED → SCHEMA_VALIDATED → IMPORTED → CATALOGED → GRAPH_CONNECTED → COMPILED → RUNTIME_TESTED → PRODUCTION_READY`

Aucune entité ne peut être déclarée `PRODUCTION_READY` sans `RUNTIME_TESTED`.

## Tests obligatoires

Chaque domaine doit avoir :

- un test nominal ;
- un test de rejet ;
- un test de volume ;
- un test de donnée orpheline ;
- un test de reproductibilité ;
- un test d’intégration runtime.

Tester au minimum : objets, ressources, cultures, recettes, machines, PNJ, dialogues, quêtes, événements, créatures, boss, maps, placement, assets, animations et sauvegardes.

## Prompts spécialisés

Les prompts peuvent être individuels pour des éléments indépendants, par famille pour les éléments visuellement interdépendants et par séquence pour les animations. Aucun prompt ne doit être isolé : il reçoit le canon, l’ontologie, le graphe, le manifest, la fonction, les relations, dimensions, variantes, animations, placement, sortie attendue et validations.

Une information manquante provoque `BLOCKED`, jamais une invention silencieuse.

## Runtime

Le LLM intervient hors ligne pour concevoir, générer, corriger et valider. Le jeu final doit fonctionner sans LLM pour règles, déplacement, navigation, routines, dialogues compilés, quêtes, événements, animations, sauvegardes et progression.

## Reproductibilité et maintenance

Prévoir versionnement, migrations, graines procédurales, sorties déterministes, rapports, sauvegardes, reprise et matrice de traçabilité. Les sorties JSON doivent être stables octet par octet lorsque cela est possible.


## First deliverables
Produce the architecture, ontology, schemas, canon registry, decision report, graph, catalogs, manifests, prompt templates, importers, validators, traceability matrix and end-to-end fixtures before mass content generation.
