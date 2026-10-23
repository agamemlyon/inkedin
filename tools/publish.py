#!/usr/bin/env python3
"""
publish.py - post an APPROVED InkedIn draft to your own LinkedIn profile via the official API.

    publish.py post data/queue/2026-10-28_slug.md            # publish (refuses anything not `status: approved`)
    publish.py post data/queue/2026-10-28_slug.md --dry-run  # show exactly what would be sent
    publish.py whoami                                         # check the LinkedIn connection

Transport: Treg (`treg call linkedin rest/posts`). The OAuth token (scope w_member_social) lives in the
Treg vault and is never read by this script or by the agent. Without Treg, set LINKEDIN_TOKEN and it calls
api.linkedin.com directly.

Draft file format (markdown + frontmatter):
    ---
    status: approved
    lang: fr
    hook: 17
    ---
    ## Final
    <the exact text to post>

Hard rules enforced here, not just in prompts:
  - status must be `approved`
  - text must pass `ink score` at the configured threshold
  - no {{placeholders}} left
  - max 3,000 characters
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ink  # noqa: E402

RESERVED = set("\\|{}@[]()<>*_~")


def linkedin_version():
    """LinkedIn versions are YYYYMM and retire after ~12 months; target two months back."""
    override = os.environ.get("LINKEDIN_VERSION")
    if override:
        return override
    d = dt.date.today().replace(day=1) - dt.timedelta(days=45)
    return d.strftime("%Y%m")


def parse(path):
    raw = open(path, encoding="utf-8").read()
    fm, body = {}, raw
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
        body = m.group(2)
    sec = re.search(r"^## Final\s*\n(.*?)(?=^## |\Z)", body, re.S | re.M)
    text = (sec.group(1) if sec else body).strip()
    fence = re.match(r"^```[a-z]*\n(.*?)\n```$", text, re.S)
    if fence:
        text = fence.group(1).strip()
    return raw, fm, text


def escape_little_text(text):
    """LinkedIn 'little text format': reserved characters must be backslash-escaped. Hashtags stay as-is."""
    return "".join("\\" + c if c in RESERVED else c for c in text)


def call(path, method="GET", body=None, extra_headers=()):
    token = os.environ.get("LINKEDIN_TOKEN")
    if token:  # direct mode
        req = urllib.request.Request("https://api.linkedin.com/" + path, method=method,
                                     data=json.dumps(body).encode() if body else None)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")
        for h in extra_headers:
            k, v = h.split(":", 1)
            req.add_header(k.strip(), v.strip())
        with urllib.request.urlopen(req) as r:
            return r.status, dict(r.headers), r.read().decode() or "{}"
    cmd = ["treg", "call", "linkedin", path, "--method", method]
    for h in extra_headers:
        cmd += ["--header", h]
    tmp = None
    if body is not None:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(body, tmp, ensure_ascii=False)
        tmp.close()
        cmd += ["--file", tmp.name, "--content-type", "application/json"]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    finally:
        if tmp:
            os.unlink(tmp.name)
    return (0 if p.returncode == 0 else p.returncode), {}, (p.stdout + p.stderr).strip()


def whoami():
    code, _, out = call("v2/userinfo")
    data = json.loads(out[out.find("{"):]) if "{" in out else {}
    if "sub" not in data:
        sys.exit(f"LinkedIn connection not available: {out[:300]}")
    return data


def load_gate():
    prof = os.environ.get("INKEDIN_PROFILE", "")
    cfg = os.path.join(prof, "inkedin.yaml")
    gate = {"min_human_score": 70, "min_check": 55}
    if os.path.exists(cfg):
        for line in open(cfg, encoding="utf-8"):
            m = re.match(r"\s*(min_human_score|min_check)\s*:\s*(\d+)", line)
            if m:
                gate[m.group(1)] = int(m.group(2))
    return gate


def cmd_post(a):
    raw, fm, text = parse(a.file)
    problems = []
    if fm.get("status") != "approved":
        problems.append(f"status is '{fm.get('status')}', not 'approved'. Reply OK on the draft first.")
    if re.search(r"\{\{.*?\}\}", text):
        problems.append("placeholders {{...}} still in the text")
    if len(text) > 3000:
        problems.append(f"{len(text)} chars > 3000")
    voice = os.path.join(os.environ.get("INKEDIN_PROFILE", ""), "profile", "voice.md")
    r = ink.run(text, fm.get("lang", "auto"), ink.load_allow(voice))
    gate = load_gate()
    worst = min(c["score"] for c in r["checks"].values())
    if r["overall"] < gate["min_human_score"] or worst < gate["min_check"]:
        problems.append(f"ink score {r['overall']} (weakest {r['weakest']} {worst}) below gate "
                        f"{gate['min_human_score']}/{gate['min_check']}")
    if problems and not a.force_dry:
        print("REFUSED:\n - " + "\n - ".join(problems))
        sys.exit(2)

    me = whoami()
    body = {
        "author": f"urn:li:person:{me['sub']}",
        "commentary": escape_little_text(text),
        "visibility": a.visibility,
        "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    headers = [f"LinkedIn-Version: {linkedin_version()}", "X-Restli-Protocol-Version: 2.0.0"]
    print(f"author:  {me.get('name')} ({body['author']})")
    print(f"version: {linkedin_version()}   ink: {r['overall']} {r['verdict']}   chars: {len(text)}")
    if a.dry_run or a.force_dry:
        print("\nDRY RUN, nothing sent. Body:\n" + json.dumps(body, ensure_ascii=False, indent=1))
        if problems:
            print("\nWould be REFUSED:\n - " + "\n - ".join(problems))
        return
    code, hdrs, out = call("rest/posts", "POST", body, headers)
    if code not in (0, 201):
        sys.exit(f"LinkedIn error {code}: {out[:500]}")
    urn = hdrs.get("x-restli-id") or (re.search(r"urn:li:(?:share|ugcPost):\d+", out) or [None])[0]
    print(f"PUBLISHED {urn or '(URN not returned, check your profile)'}")
    now = dt.datetime.now().isoformat(timespec="minutes")
    updated = raw.replace("status: approved", f"status: published\npublished_at: {now}\npost_urn: {urn or ''}", 1)
    dest_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(a.file))), "published")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, os.path.basename(a.file))
    open(dest, "w", encoding="utf-8").write(updated)
    if os.path.abspath(dest) != os.path.abspath(a.file):
        os.remove(a.file)
    print(f"moved to {dest}")


def main():
    p = argparse.ArgumentParser(prog="publish")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("post")
    s.add_argument("file")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--force-dry", action="store_true", help="dry-run even if the gate fails (debug)")
    s.add_argument("--visibility", default="PUBLIC", choices=["PUBLIC", "CONNECTIONS"])
    sub.add_parser("whoami")
    a = p.parse_args()
    if a.cmd == "whoami":
        me = whoami()
        print(f"{me.get('name')}  urn:li:person:{me['sub']}  LinkedIn-Version {linkedin_version()}")
    else:
        cmd_post(a)


if __name__ == "__main__":
    main()
