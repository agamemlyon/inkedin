# Méthodologies de référence

Ce fichier sert de base aux agents `strategist`, `writer` et `editor`. Chaque méthode est réduite à ce qu'un agent peut appliquer : la règle, quand l'utiliser et le piège à éviter. Les sources sont citées pour qu'on puisse aller les lire.

---

## 1. Stratégie de contenu

### Content DNA (adapté de Supergrow et Scripe)
Le positionnement se dit en une phrase, sous la forme *« J'aide {audience} à {résultat} grâce à {angle unique} »*. Il se décline en 3 à 5 piliers, chacun avec ses angles et ses formats. Chaque post répond à une seule question : *quel pilier fait-il avancer ?*

### Matrice de contenu (Justin Welsh)
Les piliers sont croisés avec des types de post. Une semaine variée pioche dans plusieurs types.

| Type | Rôle | Hooks associés |
|---|---|---|
| Actionnable | Comment faire X | direct-value, list-promise, zero-click-value |
| Motivant | Ce qui est possible | before-after, milestone-reflection |
| Analytique | Pourquoi X marche ou rate | myth-bust, counterintuitive-data, teardown |
| Contrarian | Ce que tout le monde rate | contrarian-take, unpopular-rule, name-the-enemy |
| Observation | Ce que je vois | prediction, overheard, behind-the-scenes |
| Récit | Ce qui m'est arrivé | mistake-confession, i-was-wrong, story-cold-open |

### Hero / Hub / Hygiene (Google)
- **Hygiene** (60 %) : réponses aux questions que l'audience se pose déjà. Valeur directe, *zero-click*.
- **Hub** (30 %) : séries récurrentes, comme un teardown mensuel ou une « question du jeudi ».
- **Hero** (10 %) : 1 post par mois plus ambitieux, avec carrousel, données propres ou prise de position forte.

### Cohérence thématique (algorithme LinkedIn 2025-2026)
Le ranking de LinkedIn, basé sur un modèle de langage (*360Brew*), compare le sujet d'un post à l'expertise que déclare ton profil. Concrètement, un post hors piliers est moins distribué. La règle : au moins 80 % des posts dans les piliers, et un profil (headline, À propos) qui reprend les mêmes mots.

### Signaux de distribution
- Ce qui compte, dans l'ordre : temps de lecture (*dwell time*), commentaires longs, enregistrements, partages avec texte. Un like pèse peu.
- Les 60 à 90 premières minutes comptent : il faut être disponible pour répondre.
- Pas de lien externe dans le corps du post. Le lien va en premier commentaire.
- 3 hashtags maximum, voire aucun.
- La sanction pour engagement bait (« Commente OUI si… ») est documentée.

---

## 2. Copywriting (structure du corps)

| Méthode | Squelette | Quand l'utiliser |
|---|---|---|
| **PAS** (Problem, Agitate, Solve) | problème → pourquoi c'est pire qu'on croit → solution | posts warning ou myth-bust |
| **BAB** (Before, After, Bridge) | avant → après → le pont | before-after, time-anchor |
| **AIDA** | attention → intérêt → désir → action | rarement, ça sonne pub |
| **SCR / Minto** (Situation, Complication, Résolution) | contexte → tension → réponse | posts analytiques, audience direction |
| **ABT** (And, But, Therefore, Randy Olson) | « X et Y, mais Z, donc W » | récit court, pitch en 3 phrases |
| **4U** (Urgent, Unique, Ultra-spécifique, Utile) | grille pour noter le hook | `editor` : hook noté sur 4, au moins 3 exigé |
| **Rule of One** (Masterson) | une idée, une émotion, une promesse, une action | contrôle final : un post = une idée |
| **Niveaux de conscience** (Eugene Schwartz) | inconscient → conscient du problème → de la solution → du produit → très conscient | le `strategist` choisit le hook selon le niveau de l'audience visée |

## 3. Viralité et mémorisation

### STEPPS (Jonah Berger, *Contagious*)
On partage un post parce qu'il apporte au moins un de ces six leviers :
- **S**ocial currency : partager te fait paraître malin ;
- **T**riggers : le sujet revient souvent dans le quotidien du lecteur ;
- **E**motion : le post déclenche une émotion forte (colère, admiration, amusement) ;
- **P**ublic : le comportement est visible ;
- **P**ractical value : c'est utile ;
- **S**tories : l'idée tient dans une histoire.

Le `strategist` coche au moins 2 leviers par post.

### SUCCESs (Chip et Dan Heath, *Made to Stick*)
Une idée qui reste est **S**imple, **U**nexpected, **C**oncrete, **C**redible, **E**motional, et racontée en **S**tory. L'`editor` s'en sert comme grille de relecture.

### Hook Point (Brendan Kane)
Tu as 3 secondes. Le hook doit créer une *rupture de schéma* par rapport à ce que le lecteur a vu dans les 10 posts précédents. Test : si ton hook ressemble aux 3 derniers posts de ton feed, il faut le réécrire.

### Category design (*Play Bigger*)
Nommer un problème (name-the-enemy) et forger un terme (coined-term) qu'on réutilise post après post. À long terme, c'est ce qui fait qu'on t'associe à une idée.

---

## 4. Storytelling

- **Story Spine** (Kenn Adams) : *Il était une fois… Chaque jour… Jusqu'au jour où… À cause de ça… À cause de ça… Jusqu'à ce que… Depuis…*
- **Story Circle** (Dan Harmon), version courte : confort → besoin → départ → recherche → trouvaille → prix payé → retour → changement.
- **In medias res** : on ouvre au milieu de la scène (« Mardi, 17h40. »). C'est le marqueur le plus fort d'un texte écrit par un humain.
- **Show, don't tell** : la réplique exacte, le chiffre, le lieu, l'heure. Jamais « c'était un moment fort ».

## 5. UX writing (appliqué aux posts)

- **Voice chart** (Torrey Podmajersky, *Strategic Writing for UX*) : pour chaque principe de voix, on définit vocabulaire, concision, ton et ponctuation, avec des exemples « on dit / on ne dit pas ». C'est la structure de `voice.md`.
- **4 dimensions du ton** (Nielsen Norman Group) : drôle ↔ sérieux, formel ↔ décontracté, respectueux ↔ irrévérencieux, enthousiaste ↔ factuel. La voix fixe une position par dimension, et le ton varie selon le contexte (post, réponse, DM).
- **Voix ≠ ton** (guide Mailchimp) : la voix ne change pas, le ton s'adapte au moment.
- **Front-loading et F-pattern** (NN/g) : le mot porteur de sens en début de ligne. Sur mobile, on lit les 2 à 3 premiers mots de chaque paragraphe.
- **Plain language** : phrases de 8 à 20 mots en moyenne, un mot courant plutôt qu'un mot savant, voix active. Indicateurs : Flesch pour l'anglais, Kandel-Moles pour le français, viser 60 et plus.
- **Écriture inclusive et accessible** : pas de texte en gras Unicode (𝗯𝗼𝗹𝗱), illisible pour les lecteurs d'écran. Emoji en fin de phrase et jamais à la place d'un mot, pour la même raison.

## 6. Animation de communauté

- **Échelle d'engagement** : lecteur → réacteur → commentateur → contributeur → ambassadeur. Chaque réponse aide quelqu'un à monter d'un cran.
- **Règle des 15 minutes avant et après** (pratique répandue) : commenter 3 à 5 posts de pairs avant de publier, et répondre à chaque commentaire dans l'heure qui suit.
- **Commentaires à valeur**, jamais « Super post ! ». Neuf types sont décrits dans `skills/ink-comment`.
- **Tri des réponses** (inspiré de li-reply) : lead → fond → pair → soutien → bruit.

## 7. Mesure (côté produit)

- Taux d'engagement = (réactions + commentaires × 3 + partages × 5) / impressions.
- Multiple de portée = impressions du post / médiane des 10 derniers posts.
- Score de conversation = commentaires de plus de 15 mots / commentaires totaux.
- Conversion vers le profil = visites du profil et nouveaux abonnés sur 48 h.
- **Tests A/B** : on ne teste qu'une variable à la fois (famille de hook, format ou créneau), sur au moins 4 posts par bras avant de conclure.
