---
name: ink-carousel
description: Use for LinkedIn document posts (carousels) — slide-by-slide copy, cover, and an accessible PDF. Best paired with direct-value, teardown, rewrite, list-promise and tier-list hooks.
version: 1.0.0
metadata: {inkedin: {agent: designer}}
---

# ink-carousel

## Structure (6-10 slides, 1080×1350)
1. **Cover**: the hook (≤ 8 words) + who it's for. This slide decides the swipe.
2. **Stakes**: why this matters, with one number or scene.
3-8. **One idea per slide**: title ≤ 6 words, body ≤ 25 words, one visual (diagram, before/after, real screenshot if publishable).
9. **Recap**: the whole thing on one slide (people screenshot this).
10. **Close**: one question or one action, plus name/handle.

## Rules
- Contrast AA minimum (4.5:1), body ≥ 28 px, no text in images without the same text in the post.
- Use the user's design tokens if `profile/brand.json` exists; otherwise neutral.
- Copy goes through `ink-human` like any post. The accompanying text post is 300-600 chars.
- Generate the PDF with the `pdf` or `claude-design` skill (HTML → PDF). Name it `YYYY-MM-DD_<slug>.pdf`.
- No employer-internal screens unless `guardrails.md` allows them.
