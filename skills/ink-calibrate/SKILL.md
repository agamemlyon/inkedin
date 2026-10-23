---
name: ink-calibrate
description: Use monthly or after 5+ approved posts — "learn from my edits", ContentIn/Oiti-style memory of corrections. Diffs AI drafts against what the user actually published and turns repeated edits into voice.md rules and lexicon entries.
version: 1.0.0
metadata: {inkedin: {agent: editor, reads: [data/queue/, data/published/], writes: [profile/voice.md, data/feedback/edits.jsonl]}}
---

# ink-calibrate

1. For each post with both a draft (`data/queue/…` `## Draft` section) and the published text
   (`data/published/…` or fetched via Treg), compute a word-level diff (`difflib`).
2. Log every substitution, deletion and insertion to `data/feedback/edits.jsonl`.
3. Find patterns (≥ 2 occurrences): words always replaced, sentence types always cut,
   openers/closers rewritten, length always trimmed, emoji removed or added.
4. Propose rules to the user, each with its evidence:
   - "Tu remplaces toujours « optimiser » par « gagner du temps » (3×)" → lexicon `ban` + preferred word
   - "Tu coupes systématiquement la dernière phrase" → voice rule "end on the turn, no moral"
5. On approval: append to voice.md §8 *Journal des corrections* and, for words, to `allow:` or to a
   personal ban list. Re-run `ink.py score` on the golden samples to make sure nothing regressed.
