#!/usr/bin/env python3
"""Diff docs/research-sources.md against a baseline and name what cites each changed source.
Usage: sources-diff.py [--base <git-ref>] [--file <baseline.md>]   (default baseline: HEAD)
Baseline is the registry as it stood before the research; the working tree is the result."""
import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = "docs/research-sources.md"
COLS = ["source", "publisher", "kind", "read", "supports", "url"]
ROW = re.compile(r"^\| (S-\d{3}) \|(.*)\|\s*$")
RANK = {"search": 0, "partial": 1, "page": 2}


def parse(text):
    out = {}
    for line in text.splitlines():
        m = ROW.match(line)
        if m:
            cells = [c.strip() for c in m.group(2).split(" | ")]
            if len(cells) == len(COLS):
                out[m.group(1)] = dict(zip(COLS, cells))
    return out


ap = argparse.ArgumentParser()
ap.add_argument("--base", default="HEAD")
ap.add_argument("--file")
a = ap.parse_args()
if a.file:
    base_text = pathlib.Path(a.file).read_text(encoding="utf-8")
else:
    r = subprocess.run(["git", "show", f"{a.base}:{REG}"], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"cannot read {REG} at {a.base}: {r.stderr.strip()}")
    base_text = r.stdout
old, new = parse(base_text), parse((ROOT / REG).read_text(encoding="utf-8"))

added = sorted(set(new) - set(old))
removed = sorted(set(old) - set(new))
changed = {i: [c for c in COLS if old[i][c] != new[i][c]] for i in sorted(set(old) & set(new))}
changed = {i: c for i, c in changed.items() if c}

print(f"baseline: {len(old)} sources; now: {len(new)}")
print("\n## Added")
for i in added:
    print(f"- {i} {new[i]['source']} ({new[i]['kind']}, read: {new[i]['read']})")
print("\n## Removed")
for i in removed:
    print(f"- {i} {old[i]['source']}")
print("\n## Changed")
for i, cols in changed.items():
    for c in cols:
        flag = ""
        if c == "read" and RANK.get(new[i]["read"], 0) < RANK.get(old[i]["read"], 0):
            flag = "  [DOWNGRADE]"
        print(f"- {i} {c}: {old[i][c]!r} -> {new[i][c]!r}{flag}")

touched = set(added) | set(removed) | set(changed)
print("\n## Cited by (re-check these when their source changed)")
cite = re.compile(r"S-\d{3}")
for f in sorted((ROOT / "plugins").glob("*/.brain/rules/*.md")) + sorted((ROOT / "plugins").glob("*/processes/*.md")):
    hit = sorted(set(cite.findall(f.read_text(encoding="utf-8"))) & (set(changed) | set(removed)))
    if hit:
        print(f"- {f.relative_to(ROOT)}: {', '.join(hit)}")
