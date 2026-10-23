---
name: ink-comment
description: Use to write comments on other people's LinkedIn posts — "comment on this post", the weekly engage-with list. Picks one of nine comment types based on the post; never "Great post!". Drafts only; the user posts.
version: 1.0.0
metadata: {inkedin: {agent: community}}
---

# ink-comment

Strong comments are the cheapest reach on LinkedIn, because they show up in the commenter's network too.

## Nine types (pick the one the post calls for)
| Type | When | Shape |
|---|---|---|
| Add a data point | post makes a claim | "On a mesuré la même chose : {chiffre, contexte}." |
| Counter-example | you've seen the opposite | "Chez nous ça a fait l'inverse, parce que {raison}." |
| Extend | post stops early | "Et l'étape d'après : {idée}." |
| Specific question | post is vague on how | "Comment vous avez géré {détail précis} ?" |
| Mini-story | you lived it | 2-3 sentences, one scene |
| Reframe | post misses the root cause | "Je crois que le vrai blocage est {X}." |
| Resource | you know a precise source | name it (no link unless asked) |
| Agree + nuance | 80 % right | "D'accord, sauf sur {point} : {pourquoi}." |
| Celebrate specifically | a peer's milestone | name the concrete thing, not "bravo" |

## Rules
- 1-4 sentences, 150-400 chars. First words must stand alone (comments truncate too).
- Must be impossible to paste under any other post.
- Never self-promote or pitch in a comment.
- Run `ink.py score` and fix SLOP/VOICE issues.
- Max 10 drafted comments/day. The user posts them by hand. Automating it breaks LinkedIn's ToS and their trust.
