---
name: ink-reply
description: Use to handle comments under the user's own LinkedIn posts — "reply to my comments", daily-comments cron. Fetches comments via Treg, triages them, drafts replies in voice. The user posts them; nothing is sent automatically.
version: 1.0.0
metadata: {inkedin: {agent: community, reads: [data/published/]}}
---

# ink-reply

1. For each post published in the last 72 h (`data/published/`), fetch comments via Treg
   `treg.linkedin.post.comments` (≈ $0.002). Skip comments already in `data/feedback/replied.jsonl`.
2. Triage, in this order:
   - **lead**: a potential client, recruiter, speaking invite or collaborator → reply first, suggest a DM
   - **substance**: adds an argument or a counter-example → reply with a real point, ask a follow-up
   - **peer**: someone from the target audience → reply by name with something specific
   - **support**: "great post" type → short thanks + one detail; or a reaction only
   - **noise / bot / pod**: ignore
3. Reply rules: 1-3 sentences, reference *their* words, end with a question only if you want the thread
   to continue. No "Merci pour ton commentaire !" boilerplate. Run each through `ink.py score`; replies
   are short, so look at SLOP and VOICE and ignore BURSTINESS.
4. Output a digest grouped by post: comment excerpt → draft reply → [copy]. Log to `data/feedback/replied.jsonl`
   once the user confirms they posted it.
