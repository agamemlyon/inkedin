# InkedIn

**LinkedIn, écrit à l'encre.** Un système open source de skills, d'agents et de crons pour faire
vivre un compte LinkedIn sans que ça sonne IA.

*Written in ink.* Open-source skills, agents and crons that run a LinkedIn presence in your own voice,
in French and English, with a human approval gate on every word.

```
idée / mémo vocal ──> interview ──> plan hebdo ──> draft ──> détecteur anti-slop ──> TON OK ──> publication ──> stats ──> on recommence
```

## Ce qu'il y a dedans
| | |
|---|---|
| **15 skills** `ink-*` | post, plan, interview, voice, dna, human, repurpose, carousel, localize, reply, comment, profile, audit, scout, calibrate |
| **7 agents** | scout, interviewer, strategist, writer, editor, community, analyst ([agents/](agents/README.md)) |
| **9 crons** | veille quotidienne, plan du lundi, interviews, drafts J-1, publication, digest des commentaires, analytics, recalibrage de la voix, audit du profil ([crons/](crons/crons.yaml)) |
| **45 hooks** FR/EN | les 21 de *linkedin-agent-skill* + 24 nouveaux (teardown, coined term, name the enemy, cross-domain analogy, iceberg, rewrite…) ([library/hooks](library/hooks/hooks.json)) |
| **Méthodes** | Content DNA, matrice Welsh, Hero/Hub/Hygiene, PAS/BAB/SCR/ABT, 4U, Schwartz, STEPPS, SUCCESs, Hook Point, category design, Story Spine, voice chart Podmajersky, 4 dimensions de ton NN/g ([library/frameworks.md](library/frameworks.md)) |
| **Détecteur `ink`** | 6 checks, bilingue FR/EN, stdlib seule, tout tourne en local ([tools/ink.py](tools/ink.py)) |

## Démarrage
```bash
git clone https://github.com/<you>/inkedin ~/inkedin
mkdir ~/inkedin-profile-moi && cp -r ~/inkedin/profile.example ~/inkedin-profile-moi/profile
cp ~/inkedin/inkedin.example.yaml ~/inkedin-profile-moi/inkedin.yaml
export INKEDIN_HOME=~/inkedin INKEDIN_PROFILE=~/inkedin-profile-moi

# installer les skills (Hermes / Claude Code)
ln -s ~/inkedin/skills ~/.hermes/skills/inkedin        # Hermes
cp -r ~/inkedin/skills/ink-* ~/.claude/skills/          # Claude Code

# essayer le détecteur
python3 tools/ink.py score tests/fixtures/slop_fr.txt
```
Commence ensuite par **`ink-voice`** puis **`ink-dna`**. Tous les autres skills lisent ces deux fichiers.

**Ton profil reste privé.** Le framework (ce repo) est public, et `profile/` + `data/` vivent dans
un repo à part que tu gardes privé. Le `.gitignore` empêche de les committer ici par erreur.

## Le détecteur
```
$ python3 tools/ink.py score tests/fixtures/slop_fr.txt
  BURSTINESS   #############...........  55.4
  SPECIFICITY  ######################## 100.0
  SLOP         ........................   0.0   (véritable, levier, dans un monde où, en constante évolution)
  FINGERPRINT  ######################## 100.0
  VOICE        ........................   0.0   5 structural tells
  FORMAT       ........................   0.0   6 emoji, 4 lines start with an emoji, 5 hashtags
  HUMAN SCORE  ######..................  25.5   FLAGGED
```
Ce que l'outil ne promet **pas** : battre GPTZero ou rendre un texte « indétectable ». Ce sont des heuristiques
locales calquées sur les signaux que regardent les détecteurs. La vraie protection, c'est la matière :
une scène, un chiffre, une opinion qui viennent de toi. D'où `ink-interview`.

## Les règles du système
1. **Rien n'est publié sans ton OK explicite.**
2. **Aucune interaction automatisée** sur LinkedIn (likes, commentaires, DM, invitations). Les agents rédigent, tu envoies.
3. **Rien n'est inventé.** Un chiffre inconnu devient `{{ton chiffre}}`, une anecdote vient d'une interview ou d'une note.
4. **Les données LinkedIn sont lues sans toucher à ton compte** : Treg (lecture seule, ~0,002 $/appel), sans cookies.

Voir [docs/linkedin-api.md](docs/linkedin-api.md) et [docs/ROADMAP.md](docs/ROADMAP.md).

## Crédits
- Hooks n°1 à 21, structure de la rubrique profil et idée d'un panel de détection : Jake Schincariol,
  [linkedin-agent-skill](https://github.com/Jakeschincariol/linkedin-agent-skill) (MIT).
- Patterns d'écriture IA : [blader/humanizer](https://github.com/blader/humanizer) (MIT), d'après *Wikipedia: Signs of AI writing*.
- Le code de `tools/ink.py` est réécrit pour le bilingue. Voir [NOTICE](NOTICE).

MIT. Prends-le, adapte-le, partage-le.
