---
name: ink-dna
description: Use to define or revise LinkedIn positioning — "what should I be known for", pillars, audience, series. Produces content-dna.md from the profile, past posts and a short interview.
version: 1.0.0
metadata: {inkedin: {agent: strategist, writes: [profile/content-dna.md]}}
---

# ink-dna

1. Read the current profile (Treg `treg.linkedin.user.profile`), `voice.md` positions, the last 20 posts and their engagement.
2. Ask in one batch: who do you want reading you in 12 months (job titles)? What do you want them to
   ask you for? What topic could you talk about for 2 hours without slides?
3. Draft:
   - Positioning sentence: *J'aide {audience} à {résultat} grâce à {angle}.*
   - 3-5 pillars. Each needs **proof the author has** (lived, not read). Reject pillars without it.
   - Audience table with Schwartz awareness levels.
   - 1-2 Hub series, 1 common enemy (category design), 1 candidate coined term.
   - Cadence + FR/EN mix.
4. Check consistency with the profile headline/About (360Brew topic matching). If they diverge, queue `ink-profile`.
5. Show the user and iterate. Save `profile/content-dna.md` (template in `profile.example/`).
