---
name: ink-scout
description: Use for LinkedIn content watch (veille) — daily cron, "find me post ideas", "what are peers posting". Reads RSS/newsletters and peers' posts via Treg, keeps a swipe file of high-performing structures, outputs idea cards tied to pillars.
version: 1.0.0
metadata: {inkedin: {agent: scout, writes: [data/ideas/, data/swipe/]}}
---

# ink-scout

1. Sources from `inkedin.yaml`: `data_sources.feeds` (RSS, newsletters), `data_sources.peers` (LinkedIn handles).
2. Peers: Treg `treg.linkedin.user.posts` (limit 10) per handle, at most once a week per peer. For posts whose
   engagement is ≥ 2× that peer's median, store in `data/swipe/` **the structure only**: hook family,
   first line, length, format, close type. Never copy wording.
3. Feeds: keep items matching a pillar (keyword + judgement); max 5 per day.
4. For each kept item, write an idea card in `data/ideas/<date>_<slug>.md`: source, the claim, pillar,
   **the question to ask the author** (their reaction is the post), candidate hooks.
5. Daily digest of 3 ideas max to the approval channel. Keep it short.

Budget: about 10 peers × 1 call/week ≈ $0.10/month.
