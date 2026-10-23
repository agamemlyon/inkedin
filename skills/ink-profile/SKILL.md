---
name: ink-profile
description: Use to audit and rewrite a LinkedIn profile — "optimize my profile", "rewrite my headline/About", monthly cron. Scores 12 items out of 100 (rubric.json), checks topic consistency with content pillars, rewrites fix-first.
version: 1.0.0
metadata: {inkedin: {agent: strategist, reads: [content-dna.md, voice.md]}}
---

# ink-profile

0. Prefer `blitzapi.people.enrich` via Treg (about $0.0005/call): it returns the real headline, About, experience and skills, which `treg.linkedin.user.profile` often omits. Check: job title field duplicating the headline, emojis in titles, outdated skills.
1. Fetch the public profile via Treg (`treg.linkedin.user.profile`, ≈ $0.002). Public scrapes hide
   parts of experience/education. For a full audit, ask the user to paste headline, About, current role,
   Featured, and describe banner + photo.
2. Score every item in `rubric.json` honestly (first passes usually land 30-50). Show a table:
   item, points, score, the one thing that lost points.
3. **Consistency check**: headline + About must contain the vocabulary of the pillars in `content-dna.md`.
   LinkedIn's ranking matches post topics to declared expertise.
4. Rewrite in fix-first order (biggest gap × easiest fix). For each: current → proposed (FR and EN if
   the profile is bilingual) → why. Everything goes through `ink-human`.
5. Never invent achievements; numbers come from `proof.md` or get `{{ton chiffre}}`.
