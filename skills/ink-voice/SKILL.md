---
name: ink-voice
description: Use when building or refreshing a voice.md — "learn my writing style", "create my voice profile", onboarding a new InkedIn user. Combines corpus analysis (LinkedIn posts via Treg, messages, notes) with a 15-minute interview, because published posts are often already polluted by AI.
version: 1.0.0
metadata:
  inkedin:
    agent: interviewer
    writes: [profile/voice.md, profile/corpus/golden/]
---

# ink-voice

A voice profile built only from past LinkedIn posts copies whatever AI tics those posts already had.
So this skill triangulates from three sources and trusts the **most spontaneous** one most.

## Sources, by trust level
1. **Spoken / spontaneous** (highest): voice memos, Telegram/Slack messages, talk transcripts, a 15-min interview.
2. **Written for peers**: internal docs, emails, comments they wrote under other people's posts.
3. **Published posts** (lowest): fetch via Treg `treg.linkedin.user.posts` (≈ $0.002/call), then
   **score each with `ink.py`**. Posts scoring < 50 are not voice samples; they show which tics to remove.

## Steps
1. Collect. Save raw text to `profile/corpus/` (posts as `posts/YYYY-MM-DD_<id>.txt`).
2. Measure. For each human-sourced sample: mean sentence length, std dev, openers, closers,
   first-person rate, anglicisms, emoji, punctuation habits, recurring words (top 30 non-stopwords).
3. Interview (if spoken samples are thin). Ask, one batch at a time, ask for voice replies if possible:
   - "Raconte-moi la dernière fois que tu as été vraiment énervé au boulot." (rhythm, emotion)
   - "Explique ton job à quelqu'un qui n'y connaît rien." (vocabulary level)
   - "Un truc que tout ton secteur croit et que tu trouves faux ?" (positions)
   - "Un post LinkedIn que tu as détesté, et pourquoi ?" (anti-voice)
   - "Trois mots que tu dis tout le temps ?" (tics)
4. Fill `profile/voice.md` (template: `profile.example/voice.md`): 4 NN/g dials, voice chart,
   mechanics, lexicon (`allow:` list), positions.
5. Pick 3-5 golden samples (spontaneous text, ≥ 150 words, human score ≥ 80) → `profile/corpus/golden/`.
6. Show the user a summary and **3 sample sentences written in their voice**. Ask "is that you?" and iterate.

## Output rule
Every claim in voice.md cites what it was measured on ("mean 11.2 words, measured on 6 voice memos").
