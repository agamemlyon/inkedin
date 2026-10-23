---
name: ink-interview
description: Use to harvest raw material for posts (PostCast / Meet Sona style) — "interview me", "I have an idea but no time to write", twice-weekly cron prompts. Asks 3-5 sharp questions, accepts text or voice replies, extracts facts into proof.md and ideas into data/ideas/.
version: 1.0.0
metadata:
  inkedin:
    agent: interviewer
    writes: [profile/proof.md, data/ideas/]
---

# ink-interview

Posts that don't read as AI start from what the author actually said, so this skill collects that.

## Run
1. Pick a topic: from the week plan, a scout idea, or the user's prompt.
2. Ask **3 questions max per batch**, built to extract *specifics*:
   - Scene: "C'était quand, où, avec qui ? Quelle phrase exacte a été dite ?"
   - Number: "Combien ? Avant/après ? En combien de temps ?"
   - Tension: "Qu'est-ce qui t'a surpris / énervé / fait changer d'avis ?"
   - Stake: "Si un pair faisait l'inverse, qu'est-ce qui lui arriverait ?"
   - Opinion: "Tu dirais quoi à quelqu'un qui pense le contraire ?"
3. Voice replies: transcribe (Hermes STT or `tools/transcribe` if configured). **Keep the transcript verbatim** in
   `data/ideas/<date>_<slug>.md` under `## Verbatim`. Its rhythm is the best voice sample you'll get.
4. Extract:
   - Facts/numbers/quotes → `profile/proof.md` with source `interview <date>` and publishability.
   - Idea card → `data/ideas/<date>_<slug>.md`: pillar, angle, candidate hooks (by `needs`), verbatim.
5. Follow-up only if a hook's `needs` is one detail away ("il me manque juste le chiffre avant").

## Rules
- Don't paraphrase the user into corporate language in the verbatim section.
- Flag confidential details (`guardrails.md`) right away and ask whether to anonymise them or drop them.
