#!/usr/bin/env python3
"""Deterministic helpers for jobsearch-in-a-box. Standard library only, no network.

  jobkit.py guard  --draft FILE --source FILE [--source FILE ...]   facts in the draft that no source backs (exit 2 if any)
  jobkit.py years  ROLES.json [--today YYYY-MM]                     years of experience, overlapping roles counted once
  jobkit.py band   SCORE                                            the fit band for a 0-100 score
  jobkit.py dedupe POSTINGS.json [--seen SEEN.json]                 postings not seen before, same job twice counted once

Everything here follows a fixed model, so it is code and not a model's judgement.
"""
import argparse
import datetime
import json
import re
import sys

NUMBER_WORDS = {w: n for n, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
NUMBER_WORDS.update({"thirty": 30, "forty": 40, "fifty": 50, "hundred": 100})
CALENDAR = set("""january february march april may june july august september october november december
jan feb mar apr jun jul aug sep sept oct nov dec monday tuesday wednesday thursday friday saturday sunday""".split())
NOT_NAMES = {"i", "i'm", "i've", "i'd", "i'll", "ok"}
CREDENTIAL = re.compile(r"\b(certified|certification|certificate|licensed|license|accredited|chartered)\b", re.I)
NUMBER = re.compile(r"(?<![\w])(\d{1,3}(?:[,.  ]\d{3})+|\d+(?:[.,]\d+)?)\s*([km])?%?(?![\w])", re.I)
WORD = re.compile(r"[\w][\w&'+#.-]*", re.U)
CAPITAL = re.compile(r"[A-ZÀ-Ý][\w&'+#-]*", re.U)


def number_value(digits, suffix):
    grouped = re.fullmatch(r"\d{1,3}(?:[,.  ]\d{3})+", digits)
    value = float(re.sub(r"\D", "", digits)) if grouped else float(digits.replace(",", "."))
    return value * {"k": 1_000, "m": 1_000_000}.get((suffix or "").lower(), 1)


def numbers_in(text):
    found = [(m.group(0).strip(), number_value(m.group(1), m.group(2))) for m in NUMBER.finditer(text)]
    found += [(w, NUMBER_WORDS[w.lower()]) for w in re.findall(r"\b[a-z]+\b", text, re.I) if w.lower() in NUMBER_WORDS]
    return found


def sentence_starts(text):
    starts = {0}
    for m in re.finditer(r"(?:[.!?:;][\"')]?\s+|\n)\s*(?:[-*•]\s+)?(?=\S)", text.rstrip()):
        starts.add(m.end())
    return starts


def unverified(text, sources):
    """Names, acronyms, numbers and credentials in `text` that the sources do not contain, in order, once each."""
    haystack = "\n".join(sources).lower()
    words = {w.rstrip(".'").lower() for w in WORD.findall(haystack)}
    numbers = {v for _, v in numbers_in(haystack)}
    flags = []

    def flag(value):
        if value not in flags:
            flags.append(value)

    starts = sentence_starts(text)
    for m in CAPITAL.finditer(text):
        word = re.sub(r"['’]s$", "", m.group(0)).strip("-'")
        low = word.lower()
        acronym = sum(c.isupper() for c in word) >= 2
        if m.start() in starts and not acronym:
            continue
        if low in NOT_NAMES or low in CALENDAR or low in words or low in haystack:
            continue
        flag(word)
    for raw, value in numbers_in(text):
        if value in numbers or (raw.isalpha() and value <= 2):
            continue
        flag(raw)
    for m in CREDENTIAL.finditer(text):
        if m.group(1).lower()[:7] not in haystack:
            flag(m.group(1))
    return flags


def cmd_guard(args):
    draft = open(args.draft, encoding="utf-8").read()
    sources = [open(p, encoding="utf-8").read() for p in args.source]
    flags = unverified(draft, sources)
    print(json.dumps({"unverified": flags, "checked_against": args.source}, indent=2, ensure_ascii=False))
    return 2 if flags else 0


def month(value, today):
    if not value:
        return today
    year, mon = (int(x) for x in value.split("-")[:2])
    return year * 12 + mon - 1


def cmd_years(args):
    today_d = datetime.date.fromisoformat((args.today or datetime.date.today().isoformat()[:7]) + "-01")
    today = today_d.year * 12 + today_d.month - 1
    spans = sorted((month(r["start"], today), month(r.get("end"), today)) for r in json.load(open(args.roles)))
    merged = []
    for start, end in spans:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    months = sum(end - start for start, end in merged)
    print(json.dumps({"months": months, "years": months // 12}))
    return 0


def band(score):
    return "Excellent fit" if score >= 85 else "Good fit" if score >= 70 else "Possible fit" if score >= 50 else "Poor fit"


def cmd_band(args):
    print(band(max(0, min(100, args.score))))
    return 0


def key(posting):
    norm = lambda s: re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
    return f"{norm(posting.get('company'))}|{norm(posting.get('title'))}|{norm(posting.get('place'))}"


def cmd_dedupe(args):
    seen = set(json.load(open(args.seen))) if args.seen else set()
    fresh = []
    for posting in json.load(open(args.postings)):
        keys = {key(posting)} | ({posting["url"]} if posting.get("url") else set())
        if keys & seen:
            continue
        seen |= keys
        fresh.append(posting)
    print(json.dumps({"fresh": fresh, "seen": sorted(seen)}, indent=2, ensure_ascii=False))
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("guard"); p.add_argument("--draft", required=True); p.add_argument("--source", action="append", required=True); p.set_defaults(fn=cmd_guard)
    p = sub.add_parser("years"); p.add_argument("roles"); p.add_argument("--today"); p.set_defaults(fn=cmd_years)
    p = sub.add_parser("band"); p.add_argument("score", type=int); p.set_defaults(fn=cmd_band)
    p = sub.add_parser("dedupe"); p.add_argument("postings"); p.add_argument("--seen"); p.set_defaults(fn=cmd_dedupe)
    args = parser.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
