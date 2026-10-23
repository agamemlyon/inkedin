---
name: ink-audit
description: Use for LinkedIn analytics — "what worked", "audit my posts", the Sunday cron. Pulls posts and engagement via Treg, ranks by engagement rate and reach multiple, attributes results to hook family / format / slot, and updates the planner's weights.
version: 1.0.0
metadata: {inkedin: {agent: analyst, writes: [data/analytics/, data/analytics/weights.json]}}
---

# ink-audit

## Collect
- Own posts: Treg `treg.linkedin.user.posts` with the handle (paginate with the token; ≈ $0.002-0.004/page).
  Keep only `author == handle` and non-reposts.
- Engagement detail for posts < 30 days: `treg.linkedin.post.engagement` or `.reactions` / `.comments`.
- Impressions are **not** available to third parties. Ask the user to paste them from LinkedIn
  analytics (or export CSV) into `data/analytics/impressions.csv`; otherwise rank on engagement only and say so.
- Join with `data/published/*.md` frontmatter (hook id, family, pillar, lang, slot, human score).

## Metrics (see library/frameworks.md §7)
- weighted engagement = reactions + 3×comments + 5×shares
- reach multiple = impressions / median of previous 10
- conversation score = comments > 15 words / total comments
- correlation with human score: does a higher ink score go with more engagement? Report it.

## Output
1. `data/analytics/YYYY-WW.md`: top 3 / bottom 3 with *why* (hook, first line, length, format, slot),
   what to repeat and what to stop. 5 bullets max.
2. `data/analytics/weights.json`: multipliers per hook family, pillar, slot, format, clamped to 0.5-1.5
   and moved by at most 0.1 per week (small samples). Note n per bucket.
3. One A/B proposal for next week: a single variable, ≥ 4 posts per arm before concluding.
