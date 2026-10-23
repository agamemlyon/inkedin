#!/usr/bin/env python3
"""
ink - the InkedIn anti-slop toolkit (FR + EN). Standard library only.

    ink score draft.txt                 six-check panel, human score 0-100
    ink score before.txt after.txt      show the delta
    ink clean draft.txt -o clean.txt    strip invisibles, typography, unicode bold, safe lexicon swaps
    ink score draft.txt --json          machine-readable (used by agents and crons)
    --lang fr|en|auto                   default auto
    --voice path/to/voice.md            honours the `allow:` list in your voice profile

Checks (higher = more human):
    BURSTINESS   sentence-length variation          models write even
    SPECIFICITY  numbers, names, dates per 100 words  models write abstract
    SLOP         lexicon hits per 100 words          stock vocabulary
    FINGERPRINT  invisibles, em dashes, curly quotes, unicode bold
    VOICE        first person, spoken markers, structural tells
    FORMAT       emoji bullets, emoji density, hashtag walls, broetry, CTA bait

Verdict = 0.6 * mean + 0.4 * weakest check. PASS >= 70 with no check < 55.

These are local heuristics modelled on the signals public detectors use.
They are not GPTZero / Originality and cannot promise those verdicts.
Inspired by Jake Schincariol's li-human (MIT), rewritten for bilingual use.
"""
import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, "..", "library", "slop"))

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿœŒ'’-]+")
NUM_RE = re.compile(r"\b\d[\d  ,.]*\s?(?:%|€|\$|k€|M€|k|M|h|min|ms|px|x)?(?=\W|$)|[€$]\s?\d")
DATE_RE = re.compile(r"(?i)\b(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre|monday|tuesday|wednesday|thursday|friday|saturday|sunday|january|february|march|april|june|july|august|september|october|november|december|hier|yesterday|ce matin|this morning)\b")
PROPER_RE = re.compile(r"(?<![.!?]\s)(?<!^)(?<!\n)\b[A-ZÀ-Ö][a-zà-öø-ÿ]{2,}\b")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B55\u231A-\u23FF]|[0-9]\ufe0f?\u20e3")
HASHTAG_RE = re.compile(r"(?<!\w)#\w+")
# Unicode "bold/italic" letters people paste from LinkedIn text generators
MATH_ALNUM = (0x1D400, 0x1D7FF)

FR_HINTS = re.compile(r"(?i)\b(?:le|la|les|des|une|est|et|que|qui|pour|dans|pas|avec|sur|c'est|j'ai|nous|vous)\b")
EN_HINTS = re.compile(r"(?i)\b(?:the|and|is|are|that|with|for|you|this|it's|i'm|was|have)\b")

FIRST_PERSON = {
    "fr": re.compile(r"(?i)\b(?:je|j'|j’|moi|mon|ma|mes|me|m'|on|nous|notre|nos)\b|\bj['’]"),
    "en": re.compile(r"(?i)\b(?:i|i'm|i've|i'd|me|my|mine|we|us|our)\b"),
}
SPOKEN = {
    # oral markers: dropped "ne", "y a", "ça", short interjections
    "fr": re.compile(r"(?i)\b(?:c'est pas|c’est pas|j'sais|y a|y'a|ça|bref|du coup|genre|franchement|perso|bon,|ouais|en vrai)\b"),
    "en": re.compile(r"(?i)\b\w+'(?:s|t|re|ve|ll|d|m)\b"),
}


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Linear map: value at `human` -> 100, at `machine` -> 0."""
    if human == machine:
        return 100.0
    return clamp((value - machine) / (human - machine) * 100)


def load_lex(lang):
    shared = json.load(open(os.path.join(LIB, "shared.json"), encoding="utf-8"))
    lex = json.load(open(os.path.join(LIB, f"{lang}.json"), encoding="utf-8"))
    return shared, lex


def load_allow(voice_path):
    if not voice_path or not os.path.exists(voice_path):
        return set()
    allow = set()
    for line in open(voice_path, encoding="utf-8"):
        m = re.match(r"\s*[-*]?\s*allow\s*:\s*(.+)", line, re.I)
        if m:
            allow |= {w.strip().lower() for w in m.group(1).split(",") if w.strip()}
    return allow


def detect_lang(text):
    fr, en = len(FR_HINTS.findall(text)), len(EN_HINTS.findall(text))
    return "fr" if fr >= en else "en"


def strip_hashtags_urls(text):
    return re.sub(r"https?://\S+", " ", HASHTAG_RE.sub(" ", text))


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(strip_hashtags_urls(text)) if len(s.split()) >= 2]


def words(text):
    return WORD_RE.findall(strip_hashtags_urls(text))


def phrase_regex(term):
    esc = re.escape(term).replace(r"\ ", r"\s+")
    esc = re.sub(r"['’]", "['’]", esc)
    left = r"(?<![\wÀ-ÿ])"
    # single words also match their plural / simple inflections (robust -> robustes, foster -> fosters)
    suffix = r"(?:s|es|e|ed|d|x)?" if re.fullmatch(r"[\wÀ-ÿ-]+", term) else ""
    right = suffix + (r"(?![\wÀ-ÿ])" if term[-1].isalnum() else "")
    return re.compile(left + esc + right, re.IGNORECASE)


# ---------------------------------------------------------------- checks

def check_burstiness(text):
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 70.0, f"only {len(lens)} sentences, not enough to judge"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    return scale(cv, human=0.70, machine=0.22), f"variation {cv:.2f} across {len(lens)} sentences (want 0.55+)"


def check_specificity(text):
    w = words(text)
    if not w:
        return 0.0, "empty"
    hits = len(NUM_RE.findall(text)) + len(DATE_RE.findall(text)) + len(set(PROPER_RE.findall(text)))
    density = hits * 100 / len(w)
    return scale(density, human=5.0, machine=0.5), f"{hits} concrete markers, {density:.1f}/100 words (want 4+)"


def check_slop(text, lex, allow):
    w = words(text)
    if not w:
        return 0.0, "empty", []
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        if entry["find"].lower() in allow:
            continue
        n = len(phrase_regex(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    detail = f"{hits} stock terms, {density:.1f}/100 words"
    if found:
        detail += " (" + ", ".join(found[:6]) + (", ..." if len(found) > 6 else "") + ")"
    return scale(density, human=0.0, machine=3.0), detail, found


def check_fingerprint(text, lang):
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf" and c not in "\u200d\ufe0f")
    em = text.count("—")
    # ’ is what iOS/Android keyboards type natively, so the apostrophe is not a tell.
    curly = sum(text.count(c) for c in "‘“”")
    ellip = text.count("…")
    bold = sum(1 for c in text if MATH_ALNUM[0] <= ord(c) <= MATH_ALNUM[1])
    # French typography legitimately uses narrow NBSP before ; : ! ? so we only count it in EN
    nbsp = sum(text.count(c) for c in "\u00a0\u202f\u2009") if lang == "en" else 0
    total = invisible * 4 + em * 2 + curly * 0.5 + ellip + nbsp + (bold / 4)
    per1k = total * 1000 / max(len(text), 1)
    detail = f"{invisible} invisible, {em} em dash, {curly} curly double/open quote, {ellip} ellipsis char, {bold} unicode-bold chars"
    return scale(per1k, human=0.0, machine=10.0), detail


def check_voice(text, lex, lang):
    w = words(text)
    if not w:
        return 0.0, "empty", []
    per100 = 100 / len(w)
    person = len(FIRST_PERSON[lang].findall(text)) * per100
    spoken = len(SPOKEN[lang].findall(text)) * per100
    tells = []
    for s in lex["structures"]:
        n = len(re.compile(s["regex"]).findall(text))
        if n:
            tells.append((s["name"], n, s["fix"]))
    n_tells = sum(t[1] for t in tells)
    spoken_target = 2.0 if lang == "en" else 0.8
    # Analytical third-person writing is still human: markers lift the score, absence doesn't sink it.
    base = scale(person, human=4.0, machine=0.3) * 0.55 + scale(spoken, human=spoken_target, machine=0.0) * 0.45
    score = 45 + base * 0.55 - n_tells * 15
    detail = f"{person:.1f} first-person/100w, {spoken:.1f} spoken markers/100w, {n_tells} structural tells"
    return clamp(score), detail, tells


def check_format(text, shared):
    fmt = shared["format"]
    w = words(text)
    issues, penalty = [], 0
    emoji = len(EMOJI_RE.findall(text))
    emoji_density = emoji * 100 / max(len(w), 1)
    if emoji_density > fmt["max_emoji_per_100_words"]:
        penalty += min(40, (emoji_density - fmt["max_emoji_per_100_words"]) * 12)
        issues.append(f"{emoji} emoji ({emoji_density:.1f}/100w)")
    bullets = len(re.findall(fmt["emoji_bullet_regex"], text))
    if bullets >= 2:
        penalty += 8 * bullets
        issues.append(f"{bullets} lines start with an emoji")
    tags = len(HASHTAG_RE.findall(text))
    if tags > fmt["max_hashtags"]:
        penalty += 8 * (tags - fmt["max_hashtags"])
        issues.append(f"{tags} hashtags")
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) >= fmt["broetry_min_lines"]:
        one_liners = sum(1 for l in lines if len(l.split()) <= 14 and len(SENT_RE.findall(l)) <= 1)
        if one_liners / len(lines) >= fmt["broetry_ratio"]:
            penalty += 25
            issues.append(f"broetry ({one_liners}/{len(lines)} one-liners)")
    blist = [len(b.split()) for b in re.findall(r"(?m)^\s*(?:[-*•]|\d+[.)]|[0-9]\ufe0f?\u20e3)\s*(.+)$", text)]
    if len(blist) >= 3 and statistics.pstdev(blist) < 1.6:
        penalty += 12
        issues.append("uniform bullet lengths")
    return clamp(100 - penalty), (", ".join(issues) or "clean")


CHECKS = ["BURSTINESS", "SPECIFICITY", "SLOP", "FINGERPRINT", "VOICE", "FORMAT"]


def run(text, lang="auto", allow=None):
    allow = allow or set()
    if lang == "auto":
        lang = detect_lang(text)
    shared, lex = load_lex(lang)
    b = check_burstiness(text)
    sp = check_specificity(text)
    sl = check_slop(text, lex, allow)
    fp = check_fingerprint(text, lang)
    vo = check_voice(text, lex, lang)
    fo = check_format(text, shared)
    scores = [b[0], sp[0], sl[0], fp[0], vo[0], fo[0]]
    details = [b[1], sp[1], sl[1], fp[1], vo[1], fo[1]]
    overall = 0.6 * statistics.mean(scores) + 0.4 * min(scores)
    verdict = "PASS" if overall >= 70 and min(scores) >= 55 else ("REVIEW" if overall >= 50 else "FLAGGED")
    return {
        "lang": lang,
        "chars": len(text),
        "checks": {k: {"score": round(s, 1), "detail": d} for k, s, d in zip(CHECKS, scores, details)},
        "slop_terms": sl[2],
        "structural_tells": [{"name": n, "count": c, "fix": f} for n, c, f in vo[2]],
        "overall": round(overall, 1),
        "weakest": CHECKS[scores.index(min(scores))],
        "verdict": verdict,
    }


def bar(score, width=24):
    filled = int(round(score / 100 * width))
    return "#" * filled + "." * (width - filled)


def print_report(r, label=None, delta=None):
    if label:
        print(f"\n  {label}  [{r['lang']}, {r['chars']} chars]")
    for k in CHECKS:
        c = r["checks"][k]
        print(f"  {k:<12} {bar(c['score'])} {c['score']:5.1f}   {c['detail']}")
    print("  " + "-" * 60)
    d = f"   ({delta:+.1f})" if delta is not None else ""
    print(f"  HUMAN SCORE  {bar(r['overall'])} {r['overall']:5.1f}   {r['verdict']}{d}")
    if r["structural_tells"]:
        print("\n  Rewrite by hand:")
        for t in r["structural_tells"]:
            print(f"   - {t['name']} x{t['count']}: {t['fix']}")


# ---------------------------------------------------------------- clean

def unbold(ch):
    """Map unicode mathematical alphanumerics back to ASCII via NFKC."""
    return unicodedata.normalize("NFKC", ch)


def clean(text, lang="auto", allow=None):
    allow = allow or set()
    if lang == "auto":
        lang = detect_lang(text)
    shared, lex = load_lex(lang)
    report = []
    inv = {e["char"] for e in shared["invisible"]}
    out_chars, removed = [], 0
    for i, ch in enumerate(text):
        is_zwj_in_emoji = ch == "\u200d" and i > 0 and EMOJI_RE.match(text[i - 1] if i else "")
        if (ch in inv or (unicodedata.category(ch) == "Cf" and ch not in "\ufe0f")) and not is_zwj_in_emoji:
            removed += 1
            continue
        if MATH_ALNUM[0] <= ord(ch) <= MATH_ALNUM[1]:
            ch = unbold(ch)
        out_chars.append(ch)
    text = "".join(out_chars)
    if removed:
        report.append(f"removed {removed} invisible characters")
    for t in shared["typographic"]:
        n = text.count(t["find"])
        if n:
            text = text.replace(t["find"], t["replace"])
            report.append(f"{t['name']} x{n}")
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r",\s*([.!?])", r"\1", text)
    for e in lex["words"] + lex["phrases"]:
        if e["replace"] is None or e["find"].lower() in allow:
            continue
        rx = phrase_regex(e["find"])

        def rep(m, r=e["replace"]):
            s = m.group(0)
            return r[:1].upper() + r[1:] if s[:1].isupper() else r

        text, n = rx.subn(rep, text)
        if n:
            report.append(f"'{e['find']}' -> '{e['replace']}' x{n}")
    return text, report


# ---------------------------------------------------------------- cli

def read(path):
    if path == "-":
        return sys.stdin.read()
    return open(path, encoding="utf-8").read()


def main():
    p = argparse.ArgumentParser(prog="ink", description="InkedIn anti-slop toolkit")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("score")
    s.add_argument("files", nargs="+")
    c = sub.add_parser("clean")
    c.add_argument("file")
    c.add_argument("-o", "--out")
    c.add_argument("--report", action="store_true")
    for sp in (s, c):
        sp.add_argument("--lang", default="auto", choices=["auto", "fr", "en"])
        sp.add_argument("--voice", default=os.environ.get("INKEDIN_VOICE"))
        sp.add_argument("--json", action="store_true")
    a = p.parse_args()
    allow = load_allow(a.voice)

    if a.cmd == "score":
        results = [run(read(f), a.lang, allow) for f in a.files]
        if a.json:
            print(json.dumps(results if len(results) > 1 else results[0], ensure_ascii=False, indent=1))
        else:
            prev = None
            for f, r in zip(a.files, results):
                print_report(r, f, None if prev is None else r["overall"] - prev)
                prev = r["overall"]
        sys.exit(0 if results[-1]["verdict"] == "PASS" else 1)

    text = read(a.file)
    cleaned, report = clean(text, a.lang, allow)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(cleaned)
    else:
        sys.stdout.write(cleaned)
    if a.report or a.json:
        before, after = run(text, a.lang, allow), run(cleaned, a.lang, allow)
        if a.json:
            print(json.dumps({"changes": report, "before": before, "after": after}, ensure_ascii=False, indent=1), file=sys.stderr)
        else:
            print("\n\n  CHANGES", file=sys.stderr)
            for line in report or ["nothing to clean"]:
                print("   - " + line, file=sys.stderr)
            print(f"\n  score {before['overall']} -> {after['overall']} ({after['verdict']})", file=sys.stderr)


if __name__ == "__main__":
    main()
