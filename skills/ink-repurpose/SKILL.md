---
name: ink-repurpose
description: Use to turn a source (article, video, podcast, talk, newsletter, internal doc) into LinkedIn posts — "make a post from this link", Tugan.ai-style. Extracts the real ideas, adds the author's own take, never summarises someone else's work as if it were theirs.
version: 1.0.0
metadata: {inkedin: {agent: writer, writes: [data/ideas/]}}
---

# ink-repurpose

1. Fetch the source (`web_extract`, `youtube-content` skill for videos, `read_file` for docs). Read it in full;
   a snippet isn't enough.
2. Extract 3-7 **atomic claims** with their evidence and a quote/timestamp. Note the author and URL.
3. For each claim ask the user (batched): *agree / disagree / have you seen this yourself?* The post is built
   on the **reaction**, not the summary. A post without the author's own position is just a link-share.
4. Map each reacted claim to an idea card (`data/ideas/`) with candidate hooks: myth-bust, contrarian-take,
   teardown, counterintuitive-data, prediction.
5. Hand over to `ink-post`. Credit the source in the first comment (no link in the body).

Never present a third party's numbers as the author's own. Write "selon {source}".
