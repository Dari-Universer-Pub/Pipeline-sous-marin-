# Message à donner à l'autre IA

Copiez-collez le bloc ci-dessous. Deux variantes selon que le framework Blender
est disponible ou non.

---

## Variante A — vous AVEZ le framework Blender

> Tu reprends une pipeline de production déjà construite, dans ce dépôt.
> Tu ne conçois rien : tu l'exécutes et tu produis le contenu qu'elle demande.
>
> **1. Lis d'abord, intégralement :**
> `README.md`, puis `docs/RUN.md`, puis `docs/FORMATS.md`.
>
> **2. Déclare le framework Blender** (remplace par le chemin réel) :
> ```bash
> export ABYSSAL_BLENDER_FRAMEWORK="/chemin/reel/FRAMEWORK_BLENDER"
> ```
>
> **3. Vérifie que tout part d'un état sain :**
> ```bash
> python3 -m unittest discover -s tests     # doit afficher OK (61 tests)
> python3 -m pipeline.cli all               # doit sortir en code 0
> ```
> Si le code de sortie est 2, l'étape Blender est encore bloquée : lis
> `REPORTS/BLOCKED.md` et corrige la déclaration du chemin. N'invente jamais
> un chemin et ne substitue jamais un autre outil.
>
> **4. Inspecte le framework et rends-moi son rapport :**
> ```bash
> python3 -m pipeline.cli blender
> cat REPORTS/blender_compatibility.json
> ```
> Dis-moi ses scripts d'entrée, ses builders, ses formats d'entrée et de
> sortie réels. Ne présume rien de son contenu avant de l'avoir inspecté.
>
> **5. Produis les assets, un par un, en suivant les manifests.**
> Les prompts sont déjà contextualisés : `PROMPTS/examples/` pour les
> exemples, `PROMPTS/templates/` pour les gabarits. Tout le contexte
> (canon, graphe, dimensions, palette, validations) est injecté
> automatiquement — tu n'as rien à deviner et rien à inventer.
>
> **6. Réinjecte chaque résultat dans la pipeline :**
> livre le binaire dans `ASSETS_IN/<famille>/`, puis importe-le avec
> `pipeline.importers.import_result` en fournissant `file` et `file_sha256`.
> Format exact : `fixtures/examples/reponse_valide.json`.
>
> **7. Règles non négociables :**
> - un asset seulement rendu par Blender n'est PAS terminé ; il doit passer
>   `IMPORTED → VALIDATED → RUNTIME_TESTED → ART_GREEN` ;
> - si un binaire est rejeté, lis le code d'erreur, corrige UNIQUEMENT le
>   champ signalé, relivre. Ne redessine jamais un binaire déjà accepté ;
> - un binaire manquant ou corrompu est une erreur bloquante : signale-la,
>   ne la comble jamais par un placeholder ;
> - s'il te manque une information, réponds `BLOCKED` avec la liste de ce qui
>   manque. N'invente jamais un fait narratif, un nom ou une règle du monde.
>
> **8. Ne touche pas aux décisions ouvertes.** Les 12 entrées de
> `REPORTS/open_decisions_report.json` m'appartiennent. En particulier
> `dec_nature_formes` (la nature des formes terrifiantes) : ne la tranche pas,
> et ne remplis pas les catalogues qui en dépendent.
>
> **9. À la fin, rends-moi :** `python3 -m pipeline.cli report` et dis-moi
> combien d'assets sont réellement `ART_GREEN`, lesquels sont bloqués et
> pourquoi.

---

## Variante B — vous N'AVEZ PAS encore le framework Blender

Dans ce cas l'autre IA ne peut produire aucun asset. Faites-lui faire le travail
qui ne dépend pas de Blender :

> Tu reprends une pipeline de production déjà construite, dans ce dépôt.
> Lis `README.md`, `docs/RUN.md`, puis `REPORTS/BLOCKED.md`.
>
> Le framework Blender n'est pas disponible : **ne produis aucun asset** et
> n'essaie aucun outil de substitution. C'est normal que
> `python3 -m pipeline.cli all` sorte en code 2.
>
> Fais uniquement ceci :
> 1. `python3 -m unittest discover -s tests` — confirme que les 61 tests passent.
> 2. `python3 -m pipeline.cli all` — rends-moi la sortie complète.
> 3. Lis `REPORTS/open_decisions_report.json` et
>    `REPORTS/contradictions.json`, puis propose-moi, pour chaque décision
>    ouverte, **deux ou trois options** avec leurs conséquences sur le reste
>    du jeu. Ne tranche aucune d'elles toi-même, ne les écris nulle part
>    comme des faits.
> 4. Dis-moi ce qui se débloquerait en cascade si je tranchais
>    `dec_nature_formes` en premier.

---

## Ce qu'il ne faut PAS lui dire

- « génère tous les assets » → la pipeline produit par familles cohérentes,
  pas en campagne massive ;
- « invente les anomalies » → c'est la seule décision qui bloque le plus de
  contenu, et elle vous appartient ;
- « corrige le binaire manquant » → un binaire manquant est une erreur
  bloquante, jamais comblée.
