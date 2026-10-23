# Agents

Sept rôles. Chacun est un prompt léger qui charge les skills listés dans sa ligne. Ils tournent dans
n'importe quel runtime qui sait lire des fichiers SKILL.md (Hermes, Claude Code, Codex…).

```
   scout ──┐                        ┌──> community (réponses / commentaires, brouillons seulement)
           ├──> strategist ──> writer ──> editor ──> [ OK HUMAIN ] ──> publish ──> analyst ──┐
interviewer┘        ^                                                                      │
                    └──────────────────── weights.json + calibrate <──────────────────────┘
```

| Agent | Skills | Déclencheur | Entrée → sortie | Peut publier ? |
|---|---|---|---|---|
| **scout** | ink-scout, ink-repurpose | cron quotidien, lien envoyé par l'utilisateur | flux, pairs → `data/ideas/` | non |
| **interviewer** | ink-interview, ink-voice | cron mardi/jeudi, « interviewe-moi » | questions → verbatim, `proof.md`, idées | non |
| **strategist** | ink-plan, ink-dna, ink-profile | cron du lundi | DNA + idées + poids → `data/queue/YYYY-WW.md` | non |
| **writer** | ink-post, ink-localize, ink-carousel | ligne du plan validée | idée + matière → draft (`status: review`) | non |
| **editor** | ink-human, ink-calibrate | chaque draft, calibrage mensuel | draft → score + réécriture ; modifs → règles de voix | non |
| **community** | ink-reply, ink-comment | cron quotidien du soir | commentaires → brouillons de réponses | **non, jamais** |
| **analyst** | ink-audit | cron du dimanche | posts publiés + stats → rapport + `weights.json` | non |

## La seule porte vers LinkedIn
Un post passe en `approved` uniquement quand l'utilisateur répond « ok ». Ensuite :
- `publishing.mode: copy` (par défaut) : le bloc final est envoyé, l'utilisateur colle et publie lui-même.
- `publishing.mode: api` : `tools/publish.py` publie via l'API officielle *Share on LinkedIn* (OAuth, scope
  `w_member_social`) au créneau prévu. Voir `docs/linkedin-api.md`.

Aucun agent ne like, ne commente, ne se connecte et n'envoie de DM sur LinkedIn.

## Statuts d'un post (frontmatter)
`idea → brief → draft → review → approved → scheduled → published → measured`
