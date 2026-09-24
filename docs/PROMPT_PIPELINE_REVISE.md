prompt pipeline :
Je démarre un nouveau projet de jeu.
Aucune ancienne pipeline de production n’est disponible. Tu ne dois donc pas supposer qu’une chaîne de prompts existante, un projet Godot existant ou une architecture précédente existe.
Un bootstrapper de pipeline est présent dans le dossier du projet.
Il contient les fichiers suivants :

* INPUT/game_brief.md
* INPUT/canon_initial.md
* INPUT/constraints.md
* INPUT/open_decisions.md
* INPUT/external_tools.md
* CONTRACT/architecture_contract.md

Cette liste est CE QUI EST ATTENDU, pas une garantie. Vérifie réellement la
présence de chaque fichier avant de commencer. Si l'un manque : ne l'invente
pas, ne le remplace pas par une supposition, BLOQUE l'étape qui en dépend,
signale-le explicitement dans le rapport de contradictions, et fournis un
gabarit vide commenté à remplir. Continue tout ce qui n'en dépend pas.

OUTIL EXTERNE : FRAMEWORK BLENDER
Un framework Blender existant sera utilisé pour produire les assets visuels, les sprites, les rendus, les modèles et éventuellement les animations.
Son chemin local actuel est :
C:\CHEMIN\A\REMPLACER\FRAMEWORK_BLENDER
Ce chemin est un emplacement temporaire propre à cette machine. Il devra être remplacé par le chemin réel du framework Blender avant l’exécution de la pipeline.
Le framework Blender doit être considéré comme un outil externe de production et non comme une modification du contrat architectural universel.
Tu dois :

* vérifier que ce chemin existe ;
* inspecter son arborescence ;
* identifier ses scripts d’entrée ;
* identifier ses builders disponibles ;
* identifier ses formats d’entrée ;
* identifier ses formats de sortie ;
* identifier ses chemins de sortie ;
* identifier les méthodes de génération d’assets ;
* identifier les méthodes de génération d’animations ;
* tester son fonctionnement avec un exemple minimal ;
* créer uniquement l’adaptateur nécessaire entre la Pipeline V5 et ce framework ;
* réutiliser ses builders existants autant que possible ;
* ne pas réécrire inutilement le framework ;
* ne pas remplacer ses systèmes fonctionnels ;
* ne pas modifier le contrat universel pour l’adapter à Blender.

L’adaptateur devra recevoir les manifests générés par la Pipeline V5 et transmettre au framework Blender :

* l’identifiant de l’entité ;
* l’identifiant de l’asset ;
* la famille visuelle ;
* le type d’asset ;
* les dimensions ;
* la résolution ;
* le style ;
* la palette ;
* les variantes ;
* les directions ;
* les animations attendues ;
* les règles de sortie ;
* les validations requises.

L’adaptateur devra retourner à la Pipeline V5 :

* les fichiers produits ;
* leur chemin de sortie ;
* leur identifiant ;
* leurs dimensions ;
* leurs formats ;
* leurs empreintes SHA-256 ;
* leur statut ;
* leurs warnings ;
* leurs erreurs ;
* les variantes réellement produites ;
* les directions réellement produites ;
* les animations réellement produites.

Les statuts minimums doivent être distingués :

* PLANNED ;
* GENERATED ;
* IMPORTED ;
* VALIDATED ;
* RUNTIME_TESTED ;
* ART_GREEN ;
* BLOCKED.

Un asset simplement généré par Blender ne doit jamais être considéré automatiquement comme terminé. Il doit être importé, validé, référencé par la pipeline et testé dans son contexte réel.
Si le chemin du framework Blender n’existe pas :

* ne l’invente pas ;
* ne remplace pas silencieusement le framework ;
* ne génère pas les assets avec une autre méthode ;
* retourne BLOCKED ;
* indique clairement le chemin manquant ;
* indique la commande ou la configuration à modifier.

Le jeu final ne doit pas dépendre de Blender ni d’un LLM pendant son exécution. Blender est uniquement utilisé hors ligne pendant la phase de production des assets et des animations.
Tu dois lire intégralement ces fichiers avant toute décision ou génération.
RÔLE DES FICHIERS D’ENTRÉE

* INPUT/game_brief.md décrit l’idée générale, le genre, la prémisse, le rôle du joueur, les boucles de gameplay et les systèmes souhaités.
* INPUT/canon_initial.md constitue la source de vérité narrative et contient les noms, lieux, personnages, objets et règles déjà décidés.
* INPUT/constraints.md contient les contraintes techniques, visuelles, de production, d’export et d’exécution.
* INPUT/open_decisions.md contient les choix encore indéterminés.
* INPUT/external_tools.md contient les outils externes, leurs chemins, leurs rôles et leurs règles d’intégration.
* CONTRACT/architecture_contract.md décrit les principes universels de la pipeline Graph-Driven.

Si le bootstrapper possède un script de génération, tu peux l’exécuter afin de produire sa spécification initiale, mais tu dois d’abord vérifier les fichiers générés et leur cohérence.
Tu dois distinguer les informations selon quatre statuts :

* CANONIQUE : information explicitement définie et non négociable.
* DÉDUITE : information dérivée logiquement du canon ou des systèmes.
* PROPOSÉE : recommandation technique ou créative proposée par toi.
* À_VALIDER : décision qui dépend encore du propriétaire du projet.

Tu ne dois jamais transformer silencieusement une décision créative ouverte en fait canonique.
OBJECTIF ACTUEL
Construire à partir du bootstrapper une Pipeline V5 Graph-Driven spécifique à ce nouveau jeu.
« V5 » désigne la version du PRODUIT que tu construis. Le contrat livré porte sa
propre version, qui peut différer. Ce n'est pas une contradiction : signale
simplement les deux numéros, et ne modifie jamais le contrat pour les aligner.
Tu ne dois pas développer directement le jeu final.
Tu dois construire la fabrique de production complète, autonome, documentée, testable et réutilisable qui permettra ensuite à une autre IA de générer le jeu.
Le bootstrapper n’est pas une ancienne pipeline à compléter. Il constitue le point de départ générique du projet.
Tu dois transformer :
Brief du jeu

* Canon initial
* Contraintes
* Outils externes
* Décisions ouvertes
* Contrat architectural

en :
Pipeline de production spécifique au jeu.
La pipeline finale devra permettre à une autre IA de générer le jeu de manière cohérente, contrôlée, interconnectée et validée.
CAPACITÉS OBLIGATOIRES DE LA PIPELINE
La pipeline doit être capable de :

* lire le brief du jeu ;
* lire le canon initial ;
* lire les contraintes ;
* lire les outils externes ;
* lire les décisions ouvertes ;
* lire l’ontologie ;
* construire ou mettre à jour le graphe du monde ;
* préserver les informations canoniques ;
* détecter les contradictions ;
* distinguer le canon des propositions ;
* générer les catalogues fonctionnels ;
* déterminer le nombre d’objets nécessaires ;
* choisir leurs noms selon le canon ;
* déduire les systèmes nécessaires ;
* déduire les chaînes de production ;
* déduire les relations entre les entités ;
* générer les manifests d’objets ;
* générer les manifests d’assets ;
* générer les manifests d’animations ;
* générer les manifests de maps ;
* générer les règles de placement ;
* générer les règles d’adjacence des terrains ;
* générer les règles de navigation ;
* générer les prompts spécialisés ;
* injecter automatiquement le contexte dans chaque prompt ;
* générer les prompts par asset lorsque cela est nécessaire ;
* générer les prompts par famille lorsque les éléments sont interdépendants ;
* transmettre les manifests à l’adaptateur Blender ;
* récupérer les résultats du framework Blender ;
* vérifier les binaires des assets livrés (format réel par octets magiques, intégrité, empreinte SHA-256, dimensions réelles, palette réelle, taille bornée) ;
* stocker les binaires acceptés dans ASSETS_BIN sans jamais les modifier ;
* re-vérifier en permanence les binaires stockés et signaler toute altération ou suppression ;
* valider les assets et animations produits ;
* valider les données ;
* détecter les entités isolées ;
* détecter les objets sans utilité ;
* détecter les quêtes sans conséquence ;
* détecter les recettes incomplètes ;
* détecter les assets manquants ;
* détecter les animations manquantes ;
* détecter les directions manquantes ;
* détecter les variantes manquantes ;
* tester les chaînes de production ;
* tester les dépendances ;
* tester l’atteignabilité ;
* tester les règles de placement ;
* tester les conséquences ;
* simuler les comportements ;
* simuler les parties ;
* produire des rapports d’erreurs ;
* produire des rapports de maturité ;
* corriger ou régénérer les éléments invalides ;
* préparer les sorties pour un moteur de jeu ;
* versionner les données ;
* permettre la reproductibilité des générations procédurales ;
* gérer les sauvegardes et les migrations ;
* fonctionner sans LLM pendant l’exécution du jeu final.

LIVRABLES ATTENDUS
Tu dois livrer la pipeline et ses outils, pas le jeu final.

AVERTISSEMENT SUR CETTE LISTE : elle est générique et réutilisée d'un projet à
l'autre. Certains livrables nommés ci-dessous (cultures, machines, recettes,
quêtes, créatures, boss, saisons, économie monétaire…) peuvent n'avoir AUCUN
fondement dans le canon de CE jeu. Dans ce cas :
- ne les remplis pas de contenu inventé pour honorer la liste ;
- déclare-les NOT_APPLICABLE avec une justification écrite qui cite le canon ;
- identifie et catalogue à leur place les analogues RÉELS de ce jeu ;
- conserve l'emplacement de schéma pour ne pas modifier le contrat.
Remplir une case avec du vide déguisé est une faute plus grave que la laisser
déclarée non applicable.

Les livrables attendus sont :

1. Architecture complète de la pipeline.
2. Canon central verrouillé.
3. Rapport des informations canoniques, déduites, proposées et à valider.
4. Rapport des contradictions et ambiguïtés.
5. Ontologie complète.
6. Schémas JSON ou modèles de données.
7. Schéma des entités.
8. Schéma des relations.
9. Schéma des états du monde.
10. Schéma des événements.
11. Schéma des conditions.
12. Schéma des effets.
13. Schéma des objets.
14. Schéma des recettes.
15. Schéma des quêtes.
16. Schéma des dialogues contextuels.
17. Schéma des assets.
18. Schéma des animations.
19. Schéma des maps.
20. Schéma des outils externes.
21. Structure du graphe du monde.
22. Catalogue des systèmes de gameplay.
23. Catalogue fonctionnel des entités.
24. Catalogue des objets.
25. Catalogue des cultures.
26. Catalogue des ressources.
27. Catalogue des machines.
28. Catalogue des recettes.
29. Catalogue des PNJ.
30. Catalogue des créatures.
31. Catalogue des lieux.
32. Catalogue des quêtes.
33. Catalogue des événements.
34. Générateur de graphe.
35. Générateur de catalogues.
36. Générateur de manifests.
37. Adaptateur pour le framework Blender.
38. Manifest des objets.
39. Manifest des ressources.
40. Manifest des cultures.
41. Manifest des machines.
42. Manifest des recettes.
43. Manifest des quêtes.
44. Manifest des PNJ.
45. Manifest des créatures.
46. Manifest des maps.
47. Manifest du placement.
48. Manifest des assets.
49. Manifest des animations.
50. Manifest des transitions de terrains.
51. Manifest des effets et particules.
52. Générateur de prompts spécialisés.
53. Templates de prompts.
54. Injecteur automatique de contexte.
55. Système de génération par identifiant.
56. Système de génération par famille.
57. Système de génération par séquence animée.
58. Importateur des résultats produits par une autre IA.
59. Importateur des résultats du framework Blender.
60. Validateurs structurels.
61. Validateurs de schémas.
62. Validateurs de références.
63. Validateurs logiques.
64. Validateurs narratifs.
65. Validateurs canoniques.
66. Validateurs économiques.
67. Validateurs temporels.
68. Validateurs de progression.
69. Validateurs de maps.
70. Validateurs de navigation.
71. Validateurs de collisions.
72. Validateurs d’assets.
73. Validateurs d’animations.
74. Validateurs de placement.
75. Validateurs des sorties Blender.
76. Validateurs de connectivité du graphe.
77. Tests des chaînes de production.
78. Tests des dépendances.
79. Tests d’atteignabilité.
80. Tests de couverture.
81. Tests des entités orphelines.
82. Tests des assets inutilisés.
83. Tests des animations inutilisées.
84. Tests des événements impossibles.
85. Tests des quêtes bloquées.
86. Tests de cohérence des noms.
87. Tests de cohérence du canon.
88. Tests de sauvegarde.
89. Tests de migration.
90. Tests de reproductibilité.
91. Tests d’intégration Blender.
92. Tests d’intégration runtime.
93. Simulateur abstrait de parties.
94. Simulateur de routines.
95. Simulateur de chaînes de production.
96. Simulateur d’événements.
97. Rapport de maturité des éléments.
98. Rapport des éléments manquants.
99. Rapport des éléments isolés.
100. Rapport des contradictions.
101. Rapport des décisions encore ouvertes.
102. Rapport des erreurs de génération.
103. Rapport de compatibilité du framework Blender.
104. Matrice de traçabilité complète.
105. Documentation d’utilisation.
106. Documentation des formats.
107. Documentation des entrées et sorties.
108. Procédure complète d’exécution par une autre IA.
109. Vérificateur binaire des assets livrés (bibliothèque standard uniquement : octets magiques PNG/JPEG, CRC, SHA-256, dimensions réelles, palette réelle, taille bornée).
110. Stockage ASSETS_BIN des binaires acceptés, avec empreintes SHA-256 enregistrées.
111. Validateur permanent des binaires stockés (toute altération ou suppression détectée).

CE QUE TU NE DOIS PAS FAIRE MAINTENANT
Ne fais pas les actions suivantes :

* ne suppose pas qu’une ancienne pipeline existe ;
* ne cherche pas à compléter une chaîne de prompts absente ;
* ne commence pas le développement complet dans Godot ;
* ne construis pas la Vertical Slice comme produit final ;
* ne génère pas massivement les assets ;
* ne crée pas toutes les maps finales ;
* ne produis pas tous les sprites ;
* ne produis pas toutes les animations ;
* ne crée pas toutes les scènes du jeu ;
* ne lance pas une campagne massive de génération de contenu ;
* ne remplace pas la pipeline par une simple suite de prompts ;
* ne considère pas le bootstrapper comme le jeu final ;
* ne remplace pas les fichiers d’entrée par des inventions ;
* ne transforme pas une décision ouverte en fait canonique sans la documenter ;
* ne modifie pas le contrat architectural universel sans signaler précisément la modification ;
* ne suppose pas que le jeu doit être exécuté dans cette session ;
* ne génère pas d’objets sans utilité ;
* ne génère pas d’assets sans entité correspondante ;
* ne génère pas d’animations sans action ou état correspondant ;
* ne génère pas de quêtes sans déclencheur et conséquence ;
* ne génère pas de recettes sans ingrédients et résultat ;
* ne génère pas de maps sans règles de placement et de navigation ;
* ne crée pas de placeholders présentés comme du contenu final ;
* ne remplis pas artificiellement les quantités demandées ;
* ne crées pas de noms numérotés ou génériques pour atteindre une cible ;
* ne fais pas passer un schéma vide pour un livrable complet ;
* ne réécris pas inutilement le framework Blender ;
* ne remplace pas Blender silencieusement par un autre outil ;
* ne considère pas un asset Blender simplement rendu comme validé ;
* ne considère jamais un fichier image comme conforme sans vérification binaire réelle : l’existence du fichier, son nom ou son extension ne suffisent pas ;
* ne recrée, ne redessine, ne retouche et ne remplace jamais un binaire livré et accepté ;
* ne corrige jamais silencieusement un binaire manquant, corrompu ou altéré : le signaler comme erreur bloquante ;
* ne code pas en dur le chemin local du framework Blender dans le contrat universel ;
* ne place JAMAIS une fixture de test dans ASSETS_BIN : ce dossier est le
  stockage de référence du contenu validé, pas un bac à sable ;
* ne présente jamais une fixture générée par un script de test comme une
  « preuve de fonctionnement » livrable sous forme d'asset ;
* ne laisse jamais deux assets distincts partager le même binaire : deux
  asset_id différents ne peuvent pas avoir la même empreinte SHA-256 ;
* ne déclare jamais avoir exécuté une commande ou une vérification que tu n'as
  pas réellement lancée.

Les assets, animations, maps et contenus doivent uniquement être décrits dans des manifests et des spécifications de production, sauf quelques exemples minimaux destinés à tester la pipeline.
GESTION DES DÉCISIONS
Pour toute information manquante :

1. Vérifie si elle existe dans canon_initial.md.
2. Vérifie si elle peut être déduite du brief.
3. Vérifie si elle peut être déduite des systèmes de gameplay.
4. Vérifie si elle est purement technique.
5. Si elle est technique, propose une valeur par défaut modulaire et documente-la.
6. Si elle concerne la vision créative, inscris-la dans DECISION_PROPRIETAIRE.
7. Vérifie si elle concerne le framework Blender ou un autre outil externe.
8. Si elle concerne un outil externe, lis external_tools.md.
9. Si elle est nécessaire pour continuer, bloque uniquement l’étape concernée.
10. N’invente jamais silencieusement un fait narratif ou une règle du monde.
11. N’invente jamais un chemin local ou un outil externe absent.

Chaque décision produite doit être accompagnée de :

* son statut ;
* sa source ;
* sa justification ;
* ses dépendances ;
* ses conséquences ;
* les éléments qu’elle affecte.

GÉNÉRATION DES QUANTITÉS
Le nombre d’objets, de cultures, de ressources, de machines, de recettes, de quêtes, de PNJ, de créatures, de maps, d’assets et d’animations ne doit pas être choisi arbitrairement.
Il doit être calculé à partir de :

* la boucle principale ;
* les systèmes de gameplay ;
* les chaînes de production ;
* la progression ;
* le canon ;
* les relations ;
* les lieux ;
* les saisons ;
* les actions disponibles ;
* les besoins de navigation ;
* les états ;
* les directions ;
* les variantes ;
* les contextes ;
* les contraintes visuelles.

Avant de valider une quantité, la pipeline doit expliquer :

* pourquoi l’élément existe ;
* quel système l’utilise ;
* comment il est obtenu ;
* quelles entités le consomment ;
* quelles conséquences il produit ;
* quels assets sont nécessaires ;
* quelles animations sont nécessaires ;
* quels tests le couvrent.

RÈGLES DE NOMMAGE
Les noms doivent être cohérents avec :

* le canon ;
* la culture du monde ;
* l’époque ;
* le niveau technologique ;
* le ton ;
* les régions ;
* les factions ;
* les matériaux ;
* la fonction de l’élément.

Sépare toujours :
ID interne stable :
objet_pioche_cuivre
Nom affiché :
Pioche en cuivre
Les identifiants internes doivent être :

* stables ;
* uniques ;
* en minuscules ;
* sans espaces ;
* sans accents ;
* composés uniquement de caractères sûrs et d’underscores.

Les noms affichés peuvent conserver les accents et la langue du jeu.
Aucun nom ne doit être inventé s’il entre en contradiction avec le canon.
RÈGLES DES OBJETS
Chaque objet doit avoir :

* un identifiant ;
* un nom ;
* une catégorie ;
* une fonction ;
* un verbe de gameplay ;
* un moyen d’obtention ;
* une place dans une boucle ;
* des utilisateurs ;
* des transformations éventuelles ;
* des relations ;
* une place dans la progression ;
* des assets nécessaires ;
* des animations nécessaires si l’objet est utilisé ;
* des tests.

Un objet sans utilité réelle doit être rejeté, déclaré décoratif ou marqué comme décision à valider.
Il ne doit jamais être ajouté uniquement pour atteindre un nombre.
RÈGLES DES MAPS
Une map ne doit pas être une simple collection d’images.
Chaque map doit définir :

* sa taille ;
* ses régions ;
* ses zones ;
* ses chemins ;
* ses entrées ;
* ses sorties ;
* ses collisions ;
* ses niveaux de hauteur ;
* ses terrains ;
* ses transitions ;
* ses points d’intérêt ;
* ses bâtiments ;
* ses zones secrètes ;
* ses ressources ;
* ses règles de placement ;
* ses règles de navigation ;
* ses règles de spawn ;
* ses conditions saisonnières ;
* ses relations avec les autres maps.

Les règles de placement doivent préciser :

* terrain autorisé ;
* terrain interdit ;
* densité ;
* distance minimale ;
* regroupement ;
* saison ;
* météo ;
* accessibilité ;
* conditions de découverte ;
* relations avec les points d’intérêt.

RÈGLES DES ASSETS
COUVERTURE VISUELLE DES ENTITÉS (règle universelle, valable pour tout type)
La règle « un asset doit avoir une entité » a une réciproque, tout aussi
obligatoire : toute entité CANONIQUE doit avoir soit des assets planifiés, soit
une décision écrite qu'elle n'est jamais montrée à l'écran.

Une entité canonique sans aucun asset planifié est une DÉCISION, jamais un
oubli. Les deux seules issues acceptables sont :
- elle est visible, et ses assets et animations figurent aux manifests ;
- elle est délibérément hors champ, et cela est inscrit comme décision du
  propriétaire, avec sa justification.

L'entre-deux silencieux est interdit. Si tu ne sais pas laquelle des deux
s'applique, POSE LA QUESTION au lieu de trancher.

Cette règle ne dépend d'aucun type d'entité : elle s'applique aux objets, lieux,
personnages, créatures, machines, ressources, phénomènes, et à tout ce que le
canon de CE jeu nomme. Un jeu sans personnages y est soumis exactement autant
qu'un jeu qui en a.

Un asset ne doit jamais être généré isolément sans contexte.
Chaque asset doit être rattaché à :

* une entité ;
* une famille ;
* une fonction ;
* une map ou un inventaire ;
* des dimensions ;
* une résolution ;
* un style ;
* une palette ;
* des variantes ;
* des règles d’utilisation ;
* une validation ;
* son fichier binaire et son empreinte SHA-256, vérifiés dès qu’il est livré.

La pipeline doit produire les assets par familles cohérentes lorsqu’ils sont interdépendants :

* familles de terrains ;
* tilesets ;
* transitions ;
* familles d’outils ;
* familles de machines ;
* familles de cultures ;
* familles de personnages ;
* familles de créatures ;
* familles d’objets.

Un prompt individuel peut être utilisé pour un asset indépendant, mais les éléments dépendants visuellement doivent être produits par famille.
RÈGLES D’INTÉGRATION BLENDER
Le framework Blender est un outil de production hors ligne.
La pipeline doit rester responsable de :

* l’identité de l’entité ;
* la fonction gameplay ;
* le canon ;
* les relations ;
* les dimensions attendues ;
* les variantes ;
* les directions ;
* les animations attendues ;
* les règles de placement ;
* la validation ;
* l’intégration runtime.

Le framework Blender est responsable de :

* la production visuelle ;
* les modèles ;
* les matériaux ;
* les rendus ;
* les sprites ;
* les animations produites par Blender ;
* les exports demandés.

L’adaptateur Blender doit :

* lire le manifest ;
* sélectionner le builder approprié ;
* transmettre les paramètres ;
* respecter l’asset_id ;
* respecter l’entity_id ;
* respecter les chemins de sortie ;
* produire les variantes demandées ;
* produire les directions demandées ;
* générer un rapport ;
* retourner les empreintes SHA-256 des fichiers produits ;
* retourner les dimensions ;
* signaler les erreurs ;
* transmettre les sorties aux validateurs.

Un asset suit obligatoirement ce cycle :
PLANNED
→ GENERATED
→ IMPORTED
→ VALIDATED
→ RUNTIME_TESTED
→ ART_GREEN
Un asset généré mais non importé est incomplet.
Un asset importé mais non validé est incomplet.
Un asset validé mais jamais utilisé dans son contexte réel est incomplet.
VÉRIFICATION BINAIRE DES ASSETS LIVRÉS (OBLIGATOIRE)
Un fichier image qui existe n’est pas automatiquement un asset conforme. Tout binaire livré (par le framework Blender ou par une autre IA) doit être vérifié EN BINAIRE à l’importation, avec la bibliothèque standard uniquement (aucune dépendance externe) :

* format réel vérifié par les octets magiques (PNG : signature + IHDR ; JPEG : SOI + SOFn) — le nom du fichier et son extension ne font jamais foi ;
* intégrité structurelle (CRC de chaque chunk PNG ; segments JPEG valides) ;
* empreinte SHA-256 réelle du fichier == empreinte déclarée à la livraison ;
* dimensions réelles lues dans le binaire == dimensions spécifiées par le manifest ;
* palette réelle (PLTE pour un PNG indexé) incluse dans la palette imposée par la spécification ;
* taille du fichier bornée (par défaut ≤ 8 Mo) ;
* fichier déclaré présent dans le dossier de livraison attendu, sans traversée de chemins hors de ce dossier.

La réponse JSON d’un asset livré avec son image porte deux champs supplémentaires :

* file : chemin du binaire livré ;
* file_sha256 : empreinte SHA-256 déclarée.

Sans ces champs, la réponse reste une spécification valide (asset décrit, binaire attendu plus tard). Avec ces champs, toute non-conformité binaire entraîne le REJET avec un code d’erreur explicite : asset.file_missing, asset.file_corrupt, asset.file_hash, asset.file_dimensions, asset.file_palette, asset.file_too_large, asset.file_format.
Le statut IMPORTED n’est accordé à un asset avec binaire que si la vérification binaire a réussi. Un asset GENERATED mais non vérifié en binaire est incomplet.
UNICITÉ DES EMPREINTES (règle bloquante) : deux asset_id distincts ne peuvent
jamais partager la même empreinte SHA-256. Un doublon signifie qu'un mauvais
fichier a été livré, copié ou importé. C'est une ERREUR BLOQUANTE, détectée
automatiquement à chaque import ET à chaque exécution des validateurs, jamais
laissée à une inspection manuelle.

VÉRIFICATION APRÈS COPIE (règle bloquante) : toute copie ou déplacement d'un
binaire doit être suivi d'un recalcul de son empreinte SHA-256 AVANT tout
import. Une copie n'est jamais présumée fidèle.

Chaque binaire accepté est copié INTACT dans ASSETS_BIN/<famille>/<asset_id>.<ext> et son empreinte SHA-256 est enregistrée. ASSETS_BIN est le stockage de référence des binaires validés ; la pipeline ne le modifie jamais.
Une famille de validation permanente re-vérifie les binaires stockés à chaque exécution (présence, empreinte, intégrité) : toute altération ou suppression d’un binaire accepté est une ERREUR bloquante, jamais corrigée silencieusement.
La pipeline ne recrée, ne redessine, ne retouche et ne régénère jamais un binaire livré et accepté. Si un binaire est manquant ou corrompu : BLOCKED avec rapport précis (fichier, champ, problème), jamais de placeholder dessiné à la place.
RÈGLES DES ANIMATIONS
Les animations doivent être déduites des :

* états ;
* actions ;
* outils ;
* directions ;
* terrains ;
* contextes ;
* interactions ;
* machines ;
* PNJ ;
* animaux ;
* créatures ;
* boss ;
* événements.

Chaque animation doit préciser :

* entité ;
* état ou action ;
* direction ;
* nombre de frames ;
* fréquence ;
* boucle ou non ;
* événement d’impact ;
* effet logique déclenché ;
* transitions possibles ;
* assets requis ;
* tests associés.

Une animation ne doit pas seulement être visuelle. Elle doit être synchronisée avec le système de gameplay.
RÈGLES DES PNJ ET AGENTS
Chaque PNJ ou agent important doit pouvoir avoir :

* une identité ;
* une fonction ;
* des objectifs ;
* des besoins ;
* des croyances ;
* des connaissances limitées ;
* des relations ;
* des émotions ;
* des routines ;
* des lieux fréquentés ;
* des horaires ;
* des souvenirs ;
* des réactions conditionnelles ;
* des conséquences ;
* des assets nécessaires, ou la décision explicite qu'il n'est jamais montré ;
* des animations nécessaires si le PNJ est visible.

Les PNJ sont soumis à la COUVERTURE VISUELLE DES ENTITÉS énoncée dans les
règles des assets, comme toute autre entité canonique.

Les dialogues doivent être générés à partir de :

* l’état du monde ;
* la mémoire du PNJ ;
* les informations connues ;
* les informations interdites ;
* la relation avec le joueur ;
* le lieu ;
* l’heure ;
* la météo ;
* l’événement récent ;
* les objectifs du PNJ.

Un dialogue ne doit jamais révéler un fait que le PNJ ne connaît pas.
RÈGLES DES QUÊTES ET ÉVÉNEMENTS
Chaque quête ou événement doit définir :

* un identifiant ;
* un déclencheur ;
* des préconditions ;
* des participants ;
* un lieu ;
* une temporalité ;
* des étapes ;
* des choix ;
* des effets ;
* des conséquences ;
* une solution de repli ;
* des conditions d’échec ;
* une possibilité d’être manqué ;
* une méthode de découverte ;
* des tests d’atteignabilité.

Respecte le principe :
Simulation avant narration.
Une narration ne doit jamais produire une conséquence que le moteur ne sait pas simuler.
RÈGLES DE CONNECTIVITÉ
Le graphe doit détecter :

* entités orphelines ;
* objets sans usage ;
* objets à usage unique inutile ;
* recettes sans ingrédients ;
* recettes sans sortie ;
* quêtes sans donneur ;
* quêtes sans conséquence ;
* PNJ sans routine ;
* PNJ sans interaction ;
* lieux sans fonction ;
* ressources sans producteur ;
* ressources sans consommateur ;
* assets sans entité ;
* animations sans action ;
* actions sans animation ;
* systèmes qui ne communiquent avec aucun autre ;
* secrets sans chemin de découverte ;
* événements jamais atteignables.

Une simple relation technique ne suffit pas à considérer une entité comme utile.
La pipeline doit aussi mesurer :

* nombre de relations ;
* profondeur causale ;
* nombre de systèmes affectés ;
* nombre de chemins de progression ;
* utilisation pendant les simulations ;
* conséquences durables ;
* résilience si le joueur ignore l’élément.

VALIDATION
La pipeline doit fournir au minimum :
Validation structurelle :

* champs obligatoires ;
* types ;
* identifiants ;
* références ;
* formats ;
* encodage UTF-8.

Validation canonique :

* noms respectés ;
* éléments interdits absents ;
* faits non contradictoires ;
* distinction entre canon et proposition.

Validation logique :

* conditions atteignables ;
* effets valides ;
* dépendances complètes ;
* absence de boucles impossibles.

Validation narrative :

* motivations cohérentes ;
* voix distinctes ;
* mémoire respectée ;
* secrets progressifs ;
* continuité des relations.

Validation économique :

* prix ;
* récompenses ;
* ressources ;
* boucles d’argent ;
* transformations ;
* équilibre.

Validation temporelle :

* saisons ;
* horaires ;
* durée ;
* événements ;
* disponibilité des ressources.

Validation des maps :

* accessibilité ;
* collisions ;
* chemins ;
* entrées ;
* sorties ;
* navigation ;
* placements valides ;
* zones secrètes découvrables.

Validation des assets et animations :

* fichiers présents et lisibles en binaire (octets magiques, intégrité CRC/segments) ;
* empreinte SHA-256 réelle du fichier == empreinte déclarée ;
* dimensions réelles lues dans le binaire == dimensions spécifiées ;
* palette réelle incluse dans la palette imposée ;
* taille de fichier bornée ;
* binaires acceptés présents dans ASSETS_BIN et non altérés (re-vérification permanente) ;
* dimensions ;
* transparence ;
* directions ;
* variantes ;
* états ;
* empreintes uniques ;
* références ;
* absence d’assets inutilisés ;
* compatibilité avec le manifest ;
* compatibilité avec le framework Blender.

SIMULATION ET TESTS
Les profils ci-dessous sont GÉNÉRIQUES : remplace ceux qui n'ont aucun sens
pour ce jeu par leurs équivalents réels, déduits de ses boucles de gameplay,
et dis lesquels tu as remplacés et pourquoi.
La pipeline doit simuler plusieurs profils :

* joueur agriculteur ;
* joueur explorateur ;
* joueur social ;
* joueur qui ignore les quêtes ;
* joueur qui optimise l’économie ;
* joueur qui rate des événements ;
* joueur qui se spécialise dans une activité ;
* joueur qui prend des décisions opposées au parcours prévu.

Les tests doivent vérifier :

* progression ;
* accessibilité ;
* économie ;
* chaînes de production ;
* routines ;
* relations ;
* événements ;
* conséquences ;
* secrets ;
* sauvegardes ;
* migrations ;
* reproductibilité ;
* résilience ;
* importation ;
* compilation ;
* runtime ;
* assets produits par Blender ;
* animations produites par Blender.

Un test doit vérifier un état avant et après une action. Un simple test d’existence de fichier ne suffit pas.
FONCTIONNEMENT SANS LLM À L’EXÉCUTION
Le LLM doit être utilisé hors ligne pour :

* concevoir ;
* générer ;
* proposer ;
* corriger ;
* analyser ;
* documenter ;
* valider.

Le framework Blender doit être utilisé hors ligne pour :

* produire les assets ;
* produire les sprites ;
* produire les modèles ;
* produire les rendus ;
* produire les animations prévues.

Le jeu final doit fonctionner sans LLM ni Blender obligatoire pour :

* déplacement ;
* collisions ;
* navigation ;
* routines ;
* croissance ;
* récoltes ;
* machines ;
* économie ;
* dialogues essentiels ;
* quêtes ;
* événements ;
* animations compilées ;
* sauvegardes ;
* progression ;
* conséquences.

Les dialogues essentiels doivent être compilés dans des données conditionnelles.
Les règles et effets doivent être exécutés par un moteur déterministe.
Un éventuel LLM présent en runtime ne doit jamais pouvoir modifier librement :

* le canon ;
* la progression ;
* les règles ;
* les statistiques ;
* les sauvegardes ;
* les objets ;
* les quêtes majeures ;
* les secrets non débloqués.

HONNÊTETÉ DES RAPPORTS
Ton rapport final est un document technique, pas une vitrine.

* n'affirme jamais avoir lancé une commande que tu n'as pas lancée ;
* colle la sortie BRUTE des commandes de vérification, pas ton résumé ;
* si un test échoue, dis-le avec sa sortie ; ne le contourne pas ;
* si tu n'as pas implémenté un item demandé, dis-le explicitement plutôt que
  de le passer sous silence : une omission déclarée est un choix, une omission
  silencieuse est une faute ;
* distingue toujours « conforme » (passe les contrôles automatiques) de
  « réussi » (répond réellement au besoin) ;
* si tu as pris une décision discutable, signale-la au lieu de l'enterrer.

VERSIONNEMENT, SAUVEGARDES ET REPRODUCTIBILITÉ
La pipeline doit prévoir :

* versionnement des schémas ;
* versionnement du canon ;
* historique des modifications ;
* dépendances ;
* migrations ;
* compatibilité des sauvegardes ;
* graines procédurales ;
* reproductibilité des maps ;
* rapports par version ;
* possibilité de revenir à une version antérieure ;
* sorties JSON déterministes ;
* empreintes SHA-256 des assets, enregistrées à l’acceptation et re-vérifiées à chaque exécution ;
* traçabilité des versions Blender utilisées.

PROMPTS SPÉCIALISÉS
La pipeline peut générer un prompt individuel pour chaque :

* objet ;
* ressource ;
* culture ;
* machine ;
* recette ;
* asset ;
* animation ;
* PNJ ;
* dialogue ;
* quête ;
* événement ;
* tuile ;
* transition ;
* élément de map.

Cependant, les prompts ne doivent jamais être indépendants.
Chaque prompt doit être automatiquement construit à partir de :

* canon central ;
* ontologie ;
* graphe ;
* manifest ;
* fiche fonctionnelle ;
* relations entrantes ;
* relations sortantes ;
* contraintes visuelles ;
* dimensions ;
* variantes ;
* animations ;
* règles de placement ;
* critères de validation ;
* dépendances ;
* sortie attendue ;
* outil externe à utiliser si nécessaire.

Pour les éléments visuellement interdépendants, utilise un prompt par famille.
Pour une séquence animée, utilise un prompt par séquence.
Pour un tileset, utilise un prompt par famille de terrain.
Chaque prompt doit documenter :

* ses entrées ;
* ses sorties ;
* son contexte ;
* ses contraintes ;
* son format de réponse ;
* ses validations ;
* sa stratégie de correction ;
* son comportement en cas d’information manquante ;
* son outil de production ;
* son chemin de sortie ;
* son statut de production.

Si une information nécessaire manque, le prompt doit retourner BLOCKED au lieu d’inventer.
FONCTIONNEMENT DE LA PIPELINE
La pipeline doit fonctionner ainsi :
INPUT/game_brief.md
INPUT/canon_initial.md
INPUT/constraints.md
INPUT/open_decisions.md
INPUT/external_tools.md
CONTRACT/architecture_contract.md
↓
Analyse des entrées
↓
Canon central verrouillé
↓
Rapport des décisions
↓
Rapport de compatibilité des outils externes
↓
Ontologie
↓
Schémas
↓
Systèmes de gameplay
↓
Catalogue fonctionnel
↓
Graphe du monde
↓
Règles
↓
Manifestes
↓
Prompts spécialisés contextualisés
↓
Adaptateur Blender si asset visuel requis
↓
Génération externe par une autre IA
↓
Importation des résultats
↓
Validation
↓
Régénération ciblée si nécessaire
↓
Compilation pour le moteur de jeu
L’autre IA exécutera les prompts générés par la pipeline.
Elle ne devra jamais devoir deviner :

* le canon ;
* le contexte ;
* la fonction de l’élément ;
* les relations ;
* le style ;
* les dimensions ;
* les variantes ;
* les animations ;
* les règles de placement ;
* les validations nécessaires ;
* les effets attendus ;
* les contraintes de nommage ;
* l’outil externe à utiliser ;
* le chemin de sortie ;
* le format attendu.

ORDRE DE TRAVAIL OBLIGATOIRE
Ne génère pas le jeu final au début.
Suis précisément cet ordre :

0. Produire l’AUDIT DE COUVERTURE — PASSE 1 (plan). Avant d’écrire la moindre
   ligne de code, recense chaque item exigé par ce prompt et déclare, pour
   chacun, comment tu comptes l’implémenter et comment tu le prouveras. Les
   manques doivent apparaître comme des cases vides dans un PLAN, pas comme
   des défauts découverts dans un livrable. Soumets ce tableau avant de
   construire. Toute case sans implémentation prévue est une question à me
   poser, pas une chose à laisser de côté.
1. Vérifier la présence des fichiers du bootstrapper.
2. Lire intégralement INPUT/game_brief.md.
3. Lire intégralement INPUT/canon_initial.md.
4. Lire intégralement INPUT/constraints.md.
5. Lire intégralement INPUT/open_decisions.md.
6. Lire intégralement INPUT/external_tools.md.
7. Lire intégralement CONTRACT/architecture_contract.md.
8. Vérifier l’encodage et la lisibilité des fichiers.
9. Vérifier que le chemin du framework Blender existe.
10. Inspecter l’arborescence du framework Blender.
11. Identifier ses scripts d’entrée et builders.
12. Tester le framework Blender avec un exemple minimal.
13. Extraire le canon initial.
14. Identifier les noms, lieux, personnages, règles et éléments non négociables.
15. Identifier les éléments déductibles.
16. Identifier les éléments proposés.
17. Identifier les décisions appartenant au propriétaire.
18. Produire un rapport des contradictions et ambiguïtés.
19. Produire un rapport de compatibilité du framework Blender.
20. Construire le canon central verrouillé.
21. Construire l’ontologie.
22. Construire les schémas.
23. Construire les systèmes de gameplay.
24. Construire le catalogue fonctionnel.
25. Construire le graphe du monde initial.
26. Définir les types de relations.
27. Générer les manifests.
28. Générer les règles de placement.
29. Générer les règles de navigation.
30. Générer les manifests d’assets.
31. Générer les manifests d’animations.
32. Construire l’adaptateur Blender.
33. Générer les templates de prompts.
34. Générer quelques prompts contextualisés d’exemple.
35. Construire les importateurs.
36. Construire les validateurs.
37. Construire le vérificateur binaire des assets livrés (octets magiques, intégrité, empreinte SHA-256, dimensions réelles, palette réelle, taille bornée) et le stockage ASSETS_BIN.
38. Construire les tests de connectivité.
39. Construire les tests de chaînes de production.
40. Construire les tests d’atteignabilité.
41. Construire les tests de couverture.
42. Construire le simulateur abstrait.
43. Tester la pipeline avec un petit jeu de données.
44. Tester la génération d’un manifeste.
45. Tester la génération de prompts.
46. Tester l’adaptateur Blender.
47. Tester l’import d’un résultat fictif.
48. Tester le rejet d’un résultat invalide.
49. Tester la détection d’une entité orpheline.
50. Tester la détection d’un asset non référencé.
51. Tester la détection d’une animation sans action.
52. Tester la validation d’un asset Blender.
53. Tester la vérification binaire d’un asset livré : fichier conforme accepté, copié intact dans ASSETS_BIN, empreinte enregistrée.
54. Tester le rejet d’un binaire corrompu, tronqué, redimensionné, hors palette ou dont l’empreinte déclarée est fausse.
55. Tester la reproductibilité de deux générations.
56. Tester la documentation.
57. Produire le rapport de maturité.
58. Produire le rapport des éléments manquants.
59. Produire le rapport des décisions ouvertes.
60. Produire la matrice de traçabilité.
61. Produire l’arborescence finale.
62. Produire la liste des scripts.
63. Produire le rôle de chaque script.
64. Produire les entrées et sorties de chaque étape.
65. Produire le format d’échange entre les étapes.
66. Produire la procédure d’exécution par une autre IA.
67. Produire un test minimal de bout en bout.
68. Vérifier que la pipeline ne dépend pas d’un LLM runtime.
69. Vérifier que le jeu final ne dépend pas de Blender runtime.
70. Produire l’AUDIT DE COUVERTURE décrit ci-dessous.
71. Vérifier qu’aucun doublon d’empreinte SHA-256 n’existe entre deux asset_id.
71b. Vérifier la COUVERTURE VISUELLE DES ENTITÉS : lister chaque entité
   canonique et, en face, ses assets planifiés ou la décision écrite qu’elle
   n’est jamais montrée. Aucune ligne ne peut rester vide des deux côtés.
72. Vérifier qu’ASSETS_BIN ne contient aucune fixture de test.
73. Relire ce prompt en entier et corriger tout item omis, ou le déclarer.

AUDIT DE COUVERTURE (OBLIGATOIRE, EN DEUX PASSES)
Ce prompt contient de longues listes. Une omission y est facile et invisible.

PASSE 1 — LE PLAN, AVANT DE CONSTRUIRE (étape 0)
Recense chaque item exigé et produis un tableau à trois colonnes :

  item exigé | comment je vais l'implémenter | comment je le prouverai

Une case vide en colonne 2 est un manque VISIBLE avant qu'il ne devienne un
défaut. Ne la comble pas en inventant : pose-moi la question. Cette passe
coûte quelques minutes et évite de colmater après coup.

PASSE 2 — LA VÉRIFICATION, APRÈS AVOIR CONSTRUIT (étape 70)
Avant de déclarer quoi que ce soit terminé, reprends CHAQUE item de CHAQUE
liste de ce prompt — capacités obligatoires, livrables numérotés, familles de
validation, tests exigés, règles des objets / maps / assets / animations / PNJ
/ quêtes, connectivité, versionnement — et produis un tableau à quatre
colonnes :

  item exigé | état | où c'est implémenté (fichier:fonction) | preuve

L'état vaut IMPLÉMENTÉ, PARTIEL, NON IMPLÉMENTÉ ou NON APPLICABLE.
Règles de cet audit :

* la preuve est un test qui passe, une sortie de commande ou un chemin de
  fichier précis — jamais une affirmation ;
* PARTIEL et NON IMPLÉMENTÉ exigent une raison écrite en une phrase ;
* NON APPLICABLE exige une citation du canon qui le justifie ;
* ne vérifie pas la présence d'une chaîne de caractères dans le code :
  vérifie le COMPORTEMENT, en l'exécutant sur un cas qui doit échouer ;
* compte les items et donne le total : exigés, implémentés, partiels, omis ;
* compare la PASSE 2 à la PASSE 1 : tout écart entre ce que tu avais prévu
  et ce que tu as réellement livré doit être expliqué, ligne par ligne.

Cet audit est un livrable. Une pipeline sans son audit de couverture est
incomplète, même si tout le reste fonctionne.

RÉSULTAT FINAL ATTENDU
À la fin de cette étape, je veux obtenir un dossier de pipeline complet construit à partir du bootstrapper et des fichiers d’entrée du projet.
Ce dossier doit être autonome, documenté, testable et transmissible à une autre IA sans nécessiter la présence de cette session.
L’autre IA devra pouvoir :

1. lire la documentation ;
2. charger le canon ;
3. charger l’ontologie ;
4. charger les contraintes ;
5. charger les outils externes ;
6. exécuter les scripts de pipeline ;
7. obtenir les manifests ;
8. recevoir les prompts contextualisés ;
9. utiliser l’adaptateur Blender ;
10. générer les éléments du jeu ;
11. réinjecter les résultats dans la pipeline ;
12. lancer les validateurs ;
13. corriger ou régénérer les éléments invalides ;
14. compiler les données ;
15. produire les fichiers finaux pour le moteur du jeu.

LIVRABLES À VÉRIFIER AVANT DE DÉCLARER LA PIPELINE TERMINÉE
Vérifie que le dossier contient réellement :

* une documentation principale ;
* une arborescence claire ;
* un canon central ;
* une ontologie ;
* des schémas ;
* un graphe ;
* un catalogue fonctionnel ;
* des manifests ;
* des règles de placement ;
* des templates de prompts ;
* un injecteur de contexte ;
* un adaptateur Blender ;
* un importateur ;
* des validateurs ;
* des tests ;
* un simulateur ;
* des rapports ;
* une matrice de traçabilité ;
* une documentation d’exécution ;
* un exemple de sortie valide ;
* un exemple de sortie invalide ;
* une procédure de correction ;
* une procédure de reprise ;
* une preuve de fonctionnement de la pipeline ;
* une preuve de compatibilité avec le framework Blender ;
* une preuve d’intégration de bout en bout.

CONDITIONS DE FIN
La pipeline ne peut être déclarée terminée que si :

* les fichiers d’entrée ont été lus ;
* le canon central a été produit ;
* les décisions ouvertes sont listées ;
* les contradictions sont signalées ;
* l’ontologie est cohérente ;
* les schémas passent leurs tests ;
* le graphe est construit ;
* les relations sont validées ;
* les manifests sont générés ;
* les prompts contextualisés sont générés ;
* l’adaptateur Blender est documenté et testé ;
* l’importation fonctionne ;
* les validateurs fonctionnent ;
* les entités orphelines sont détectées ;
* les assets manquants sont détectés ;
* les animations manquantes sont détectées ;
* les résultats invalides sont rejetés ;
* les binaires livrés sont vérifiés en binaire (format réel, intégrité, empreinte SHA-256, dimensions, palette, taille) ;
* les binaires acceptés sont stockés intacts dans ASSETS_BIN et la re-vérification permanente ne remonte aucune altération ;
* les corrections ciblées sont documentées ;
* le test minimal de bout en bout réussit ;
* la reproductibilité est vérifiée ;
* le jeu final n’a pas besoin d’un LLM pendant son exécution ;
* le jeu final n’a pas besoin de Blender pendant son exécution ;
* l’audit de couverture est produit dans ses DEUX passes (plan puis
  vérification), chiffré, et chaque item PARTIEL ou NON IMPLÉMENTÉ y porte sa
  raison ;
* tout écart entre le plan annoncé en passe 1 et le livrable réel est expliqué ;
* aucun doublon d’empreinte SHA-256 n’existe entre deux asset_id ;
* chaque entité canonique a soit des assets planifiés, soit une décision écrite
  qu’elle n’est jamais montrée ;
* ASSETS_BIN ne contient aucune fixture de test.

Tu dois donc terminer la fabrique qui produira le jeu, et non produire le jeu lui-même.
Ne génère pas massivement le jeu final pendant cette phase.
