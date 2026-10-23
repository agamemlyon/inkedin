#!/usr/bin/env python3
"""InkedIn publish runner (no-agent cron). Publishes approved posts whose slot is due.
Prints nothing when there is nothing to do, so no Telegram message is sent."""
import datetime as dt
import glob
import os
import re
import subprocess

HOME = os.environ.get("INKEDIN_HOME", os.path.expanduser("~/inkedin"))
PROFILE = os.environ["INKEDIN_PROFILE"]
env = dict(os.environ, INKEDIN_HOME=HOME, INKEDIN_PROFILE=PROFILE)
now = dt.datetime.now()
out = []
for f in sorted(glob.glob(f"{PROFILE}/data/queue/*.md")):
    head = open(f, encoding="utf-8").read(800)
    if not re.search(r"^status:\s*approved\s*$", head, re.M):
        continue
    m = re.search(r"^slot:\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})", head, re.M)
    if not m or dt.datetime.fromisoformat(m.group(1)) > now:
        continue
    p = subprocess.run(["python3", f"{HOME}/tools/publish.py", "post", f], capture_output=True, text=True, env=env, timeout=180)
    status = "✅ Publié" if p.returncode == 0 else "⚠️ Échec publication"
    out.append(f"{status} : {os.path.basename(f)}\n{(p.stdout + p.stderr).strip()[-600:]}")
if out:
    print("InkedIn\n\n" + "\n\n".join(out))
