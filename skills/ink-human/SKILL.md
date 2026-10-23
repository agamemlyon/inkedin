---
name: ink-human
description: Use when text must not read as AI — "humanize", "de-slop", "does this sound like ChatGPT", or before any post, comment, reply or DM is shown. Runs the bilingual FR/EN six-check detector, auto-cleans fingerprints, and hands back structural tells to rewrite.
version: 1.0.0
metadata:
  inkedin:
    agent: editor
    tools: [tools/ink.py]
---

# ink-human

Two layers. Run both and score with the tool instead of judging by eye.

## Layer A: deterministic (`tools/ink.py`, stdlib only, runs locally)
```bash
python3 $INKEDIN_HOME/tools/ink.py clean draft.txt -o clean.txt --report   # invisibles, em dashes, curly quotes, 𝗯𝗼𝗹𝗱, safe swaps
python3 $INKEDIN_HOME/tools/ink.py score clean.txt                          # six checks, verdict
python3 $INKEDIN_HOME/tools/ink.py score draft.txt clean.txt                # delta
python3 $INKEDIN_HOME/tools/ink.py score clean.txt --json                   # for agents / crons
```
Language is auto-detected (`--lang fr|en` to force). `--voice voice.md` honours the user's `allow:` list.

| Check | Measures | Machine-looking |
|---|---|---|
| BURSTINESS | sentence length variation | even rhythm |
| SPECIFICITY | numbers, names, dates /100 words | abstract nouns |
| SLOP | FR/EN lexicon hits /100 words | stock vocabulary |
| FINGERPRINT | invisibles, em dash, curly double quotes, unicode bold | typographically perfect |
| VOICE | first person, spoken markers, structural tells | "Ce n'est pas X, c'est Y" |
| FORMAT | emoji bullets, emoji density, hashtag walls, broetry, uniform bullets | LinkedIn template look |

Verdict = 0.6 × mean + 0.4 × weakest. PASS ≥ 70 with no check < 55.

## Layer B: judgement (you)
1. Rewrite every line listed under "Rewrite by hand". Keep the meaning and change the shape.
2. Apply the `humanizer` skill's 34 patterns. The ones that matter most at post length: AI vocabulary,
   negative parallelism, rule of three, staged reveals, signposting, reassurance kickers, punchy kickers.
3. Ask *"what makes this obviously AI?"* and answer in 2-3 bullets. Fix, re-score.
4. Read it aloud in the author's voice (`voice.md`). If they wouldn't say a sentence at a coffee machine, rewrite it.

## Honesty
These are local heuristics, not GPTZero, Originality or Copyleaks. Never tell the user a text is
"undetectable". What actually protects them is **real material**: a scene, a number, an opinion they hold.

## Maintaining the lexicon
`library/slop/{fr,en,shared}.json` are meant to be edited. New tic spotted in the wild → add it.
Word genuinely the user's → `allow:` in their voice.md, not deleted globally.
Run `python3 -m unittest discover $INKEDIN_HOME/tests` after any edit.
