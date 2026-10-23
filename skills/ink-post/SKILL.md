---
name: ink-post
description: Use when the user wants a LinkedIn post, a hook, or "turn this into a post". Writes from real material in the user's voice, picks hooks from a 45-formula library, and ships nothing below the human-score gate.
version: 1.0.0
metadata:
  inkedin:
    agent: writer
    reads: [voice.md, content-dna.md, guardrails.md, proof.md, library/hooks/hooks.json, library/frameworks.md]
    writes: [data/queue/<date>_<slug>.md]
---

# ink-post

Turns one piece of **real material** into a LinkedIn post that sounds like its author.

Paths: `$INKEDIN_HOME` = framework repo, `$INKEDIN_PROFILE` = the user's private profile repo
(`profile/` + `data/`). If unset, look for `~/inkedin` and `~/inkedin-profile-*`.

## 0. Gate: no material, no post
A post needs **one specific true thing**: a scene, a number, a quote, a decision, a mistake.
If the input is thin ("post about AI"), do not pad. Run `ink-interview` or ask one batched
question: *what happened, to whom, when, and what did it cost or return?*
Material must come from the user (chat, voice memo, notes, `proof.md`). Never invent anecdotes.

## 1. Load context
1. `profile/voice.md` (mandatory; if missing, run `ink-voice` first)
2. `profile/content-dna.md` → which pillar does this serve? If none, say so.
3. `profile/guardrails.md` → confidentiality and truth rules
4. `profile/proof.md` → the only numbers you may use
5. `library/hooks/hooks.json` → formulas; filter by `needs` satisfied by the material

## 2. Three hooks, three families
Pick 3 eligible formulas from **different families**. Score each on 4U
(Urgent, Unique, Ultra-specific, Useful; 0-4). Show them numbered with the score and say
which you'd ship in one sentence. Skip families already used this week (`data/queue/`).

## 3. Draft
Shape (the structure from `library/frameworks.md` that fits: PAS, BAB, SCR, ABT, Story Spine):
```
Line 1   hook, alone, < 140 chars
Line 2   payoff of line 1, never setup
Body     1-3 line paragraphs, blank line between, concrete detail (who, when, number)
Turn     one line that reframes
Close    one specific question OR one instruction. Never both. Never "Thoughts?" / "Et vous ?"
```
900-1,300 characters. No outbound link in the body (first comment instead).
Hashtags: 0-3, at the end. Emoji: follow voice.md (default: none or one).
Write directly in the target language. For FR+EN, write FR then run `ink-localize`.

## 4. Human gate (mandatory)
```bash
python3 $INKEDIN_HOME/tools/ink.py clean draft.txt -o clean.txt --report --voice $INKEDIN_PROFILE/profile/voice.md
python3 $INKEDIN_HOME/tools/ink.py score clean.txt --voice $INKEDIN_PROFILE/profile/voice.md
```
Rewrite every structural tell by hand. Loop until PASS and score >= `quality_gate.min_human_score`.
After 3 failing rounds, start a new draft from a different hook; more passes won't fix a formula draft.
Then the self-check from the `humanizer` skill: *what makes this obviously AI?* Fix, re-score.

Compare against `voice.md` golden samples: sentence length, openers, tics. Closer to the samples wins.

## 5. Output
Fenced copy-ready block, then:
```
POST READY
pillar:    <pillar>          hook: #<id> <name> (4U <n>/4)
length:    <n> chars         lang: fr|en
human:     <score> PASS      proof: P00x, S00x
flags:     {{placeholders}} / CONFIDENTIALITY / none
slot:      <from plan>
```
Save to `data/queue/YYYY-MM-DD_<slug>.md` with frontmatter `status: review`.

## Visuals
- Optional `image:` + `image_alt:` in the draft frontmatter; `publish.py` uploads it (PNG/JPG/GIF ≤ 8 MB) and refuses to post if the upload fails.
- Original visuals only: no film or anime clips/stills (copyright). Render a homage instead (e.g. PIL-generated GIF), and always write alt text.

## Never
- Name or target a real person (influencer, colleague, client, competitor) unless guardrails.md allows it. Inspiration accounts never appear in posts.
- Exceed the DNA's cap on posts about the author's current job.
- Publish or schedule without an explicit "ok"/"yes" (status `approved`).
- Fabricate numbers, clients, quotes, or scenes. Unknown number → `{{ton chiffre}}` + flag.
- Two ideas in one post. Split them and say so.
