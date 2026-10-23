---
name: ink-plan
description: Use for "plan my LinkedIn week", "what should I post", or the Monday cron. Builds a weekly plan of 3-5 posts balancing pillars, hook families, content-matrix types, STEPPS levers, FR/EN mix and slots, weighted by past performance.
version: 1.0.0
metadata:
  inkedin:
    agent: strategist
    reads: [content-dna.md, data/ideas/, data/analytics/weights.json, library/hooks/hooks.json]
    writes: [data/queue/YYYY-WW.md]
---

# ink-plan

## Inputs
- `profile/content-dna.md`: pillars + shares, series, cadence, slots, FR/EN mix
- `data/ideas/`: idea cards with material (only ideas with material are eligible)
- `data/analytics/weights.json` (from `ink-audit`): per-family and per-slot multipliers; default 1.0
- Last 2 weeks of `data/queue/` → avoid repeats

## Algorithm
1. Slots = `cadence.posts_per_week` from `inkedin.yaml`.
2. Allocate slots to pillars by target share, correcting for last 4 weeks' drift.
3. For each slot choose an idea card whose material satisfies at least one hook's `needs`.
   If none exists for a pillar, schedule an `ink-interview` prompt instead of a weak post.
4. Choose the hook family: no repeat in the week, weighted by `weights.json`, and
   mix matrix types (at least 1 actionable/value, 1 tension or story).
5. Check STEPPS: each post ticks at least 2 levers; note which.
6. Language per slot following the FR/EN mix. EN posts are adaptations aimed at an international audience.
7. Hero/Hub/Hygiene: at most 1 Hero per month; series (Hub) on their fixed day.
8. Engagement block: 5-10 people to engage with this week (peers from `data_sources.peers`
   + recent commenters). Suggest them only. The user does the commenting.

## Output `data/queue/YYYY-WW.md`
```
| Slot | Pillar | Idea | Hook (family) | Type | STEPPS | Lang | Material | Status |
```
Plus "Missing material" (questions for `ink-interview`) and "Engage with" list.
Send the summary to the approval channel; the user can swap, drop or approve each line.
