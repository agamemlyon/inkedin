---
name: ink-localize
description: Use to adapt a post between French and English (MagicPost-style multi-language). Rewrites for the target culture and audience instead of translating, then re-runs the human gate in the target language.
version: 1.0.0
metadata: {inkedin: {agent: writer}}
---

# ink-localize

Translations sound translated, so this skill adapts the post for the other language.

1. Keep: the material (scene, numbers, quotes), the hook *family*, the position.
2. Rewrite the hook natively; a different formula is fine if it works better in the target language.
3. FR → EN: shorter sentences, contractions (I'm, didn't), fewer abstractions, US/UK date format per audience,
   drop French-only references or explain them in 3 words.
   EN → FR: no franglais beyond what `voice.md` allows, tutoiement/vouvoiement per voice.md, French
   typography optional (LinkedIn readers type plain spaces).
4. Numbers: 1 400 → 1,400 ; 12 % → 12% ; 40 k€ → €40k.
5. Run `ink.py score --lang <target>` and fix it until it passes.
6. Same-day double posting in two languages hurts reach. Space them ≥ 48 h or pick one per audience.
