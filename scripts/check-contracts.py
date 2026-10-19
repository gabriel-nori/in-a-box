#!/usr/bin/env python3
"""Validate every SKILL.md against CONVENTIONS section 2 and 3."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SECTIONS = ["When to use", "Given", "Withheld", "Depends on", "Deliverables",
            "Judged against", "Guardrails: must not", "Output format"]
EDGE = re.compile(r"^- \*\*(Requires|Optional \(ordered\)|Optional \(enriching\)):\*\*\s*(.*)$")
NUMBERED = re.compile(r"^\s*\d+[.)]\s+\S")
FIRST_THEN = re.compile(r"\bfirst\b.*\bthen\b", re.I)

errors = []
skills = sorted((ROOT / "plugins").glob("*/skills/*/SKILL.md"))
declared = set()
specs = set()

for f in skills:
    rel = f.relative_to(ROOT).as_posix()
    text = f.read_text(encoding="utf-8")
    name = f.parent.name
    if not re.search(rf"^name:\s*{re.escape(name)}\s*$", text, re.M):
        errors.append(f"{rel}: frontmatter name must equal folder name '{name}'")
    heads = re.findall(r"^## (.+)$", text, re.M)
    present = [h for h in heads if h in SECTIONS]
    if present != SECTIONS:
        errors.append(f"{rel}: sections must be exactly {SECTIONS} in order, got {present}")
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue
        if NUMBERED.match(line):
            errors.append(f"{rel}:{i}: numbered step list is a defect")
        if FIRST_THEN.search(line):
            errors.append(f"{rel}:{i}: 'first... then...' is a defect")
    m = re.search(r"^## Depends on\n(.*?)(?=^## )", text, re.M | re.S)
    body = m.group(1) if m else ""
    for l in body.splitlines():
        s = re.match(r"^- \*\*Specializes:\*\*\s*`([^`]+)`", l)
        if s:
            specs.add((name, s.group(1)))
    edges = [EDGE.match(l) for l in body.splitlines()]
    edges = [e for e in edges if e]
    if not any(e.group(1) == "Requires" for e in edges):
        errors.append(f"{rel}: Depends on must declare Requires (write 'none' for a root)")
    if "**Produces:**" not in body:
        errors.append(f"{rel}: Depends on must declare Produces")
    for kind, rest in ((e.group(1), e.group(2)) for e in edges):
        key = {"Requires": "requires", "Optional (ordered)": "optional-ordered",
               "Optional (enriching)": "optional-enriching"}[kind]
        t = re.match(r"`([^`]+)`(?:\s*\(`([^`]+)`\))?", rest)
        if t:
            declared.add((name, key, t.group(1), t.group(2) or ""))
        elif rest.startswith("none"):
            declared.add((name, key, "none", ""))

table = (ROOT / "docs" / "skill-dependencies.md").read_text(encoding="utf-8")
mirrored = set()
for line in table.splitlines():
    cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
    if len(cells) == 4 and cells[1] in ("requires", "optional-ordered", "optional-enriching"):
        mirrored.add((cells[0], cells[1], cells[2], cells[3]))

# Orchestrator skills are covered by the table only when listed; compare role skills.
roles = {s.parent.name for s in skills if "orchestrator" not in s.as_posix()}
for e in sorted(x for x in declared if x[0] in roles and x not in mirrored):
    errors.append(f"docs/skill-dependencies.md missing edge {e}")
for e in sorted(x for x in mirrored if x not in declared):
    errors.append(f"docs/skill-dependencies.md has edge not in any skill: {e}")

spec_table = (ROOT / "docs" / "skill-specializations.md").read_text(encoding="utf-8")
spec_rows = set()
for line in spec_table.splitlines():
    cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
    if len(cells) == 2 and cells[0] not in ("Skill", "---"):
        spec_rows.add((cells[0], cells[1]))
names = {s.parent.name for s in skills}
for e in sorted(specs - spec_rows):
    errors.append(f"docs/skill-specializations.md missing {e}")
for e in sorted(spec_rows - specs):
    errors.append(f"docs/skill-specializations.md has {e} not declared by any skill")
for sk, base in sorted(specs):
    if base not in names:
        errors.append(f"{sk}: specializes unknown skill '{base}'")

import json

for plugin in sorted((ROOT / "plugins").glob("*/.claude-plugin/plugin.json")):
    pdir = plugin.parent.parent
    mf = pdir / ".brain" / "manifest.json"
    prel = pdir.relative_to(ROOT).as_posix()
    if not mf.is_file():
        errors.append(f"{prel}: missing .brain/manifest.json (CONVENTIONS section 8)")
        continue
    man = json.loads(mf.read_text(encoding="utf-8"))
    listed = {s["file"] for s in man.get("skills", [])}
    on_disk = {s.relative_to(pdir).as_posix() for s in pdir.glob("skills/*/SKILL.md")}
    for f in sorted(on_disk - listed):
        errors.append(f"{prel}/.brain/manifest.json: skill not listed: {f}")
    for entry in man.get("skills", []):
        if not (pdir / entry["file"]).is_file():
            errors.append(f"{prel}/.brain/manifest.json: missing file {entry['file']}")
    for r in man.get("rules", []):
        if not (pdir / ".brain" / r["file"]).is_file():
            errors.append(f"{prel}/.brain/manifest.json: missing rule file {r['file']}")
        else:
            rt = (pdir / ".brain" / r["file"]).read_text(encoding="utf-8")
            for sec in ("THE RULE", "WHY", "HOW TO APPLY"):
                if not re.search(rf"^{sec}\s*$", rt, re.M):
                    errors.append(f"{prel}/.brain/{r['file']}: missing section {sec}")

sys.path.insert(0, str(ROOT / "scripts"))
from processlib import SECTIONS as PROC_SECTIONS, load_process

registry = (ROOT / "docs" / "research-sources.md").read_text(encoding="utf-8")
source_ids = set(re.findall(r"^\| (S-\d{3}) \|", registry, re.M))
for plugin in sorted((ROOT / "plugins").glob("*/.claude-plugin/plugin.json")):
    pdir = plugin.parent.parent
    mf = pdir / ".brain" / "manifest.json"
    prel = pdir.relative_to(ROOT).as_posix()
    files = sorted(pdir.glob("processes/*.md"))
    listed = {x["file"] for x in json.loads(mf.read_text(encoding="utf-8")).get("processes", [])} if mf.is_file() else set()
    for f in files:
        q = load_process(pdir, f)
        rel = f.relative_to(ROOT).as_posix()
        if not q["has_meta"] or not (q["id"] and q["title"] and q["scenario"]):
            errors.append(f"{rel}: front matter needs id, title, scenario, roles, sources")
        if q["id"] != f.stem:
            errors.append(f"{rel}: id must equal the file name '{f.stem}'")
        if q["sections"] != PROC_SECTIONS:
            errors.append(f"{rel}: sections must be exactly {PROC_SECTIONS} in order, got {q['sections']}")
        for r in q["roles"]:
            if r not in {s.parent.name for s in skills}:
                errors.append(f"{rel}: role '{r}' is not a skill")
        if not q["sources"]:
            errors.append(f"{rel}: a process cites at least one source")
        for sid in q["sources"]:
            if sid not in source_ids:
                errors.append(f"{rel}: source {sid} is not in docs/research-sources.md")
        if q["file"] not in listed:
            errors.append(f"{prel}/.brain/manifest.json: process not listed: {q['file']} (run sync-manifest.py)")

import subprocess

stale = subprocess.run([sys.executable, str(ROOT / "scripts" / "gen-maps.py"), "--check"],
                       capture_output=True, text=True)
if stale.returncode:
    errors.extend(stale.stdout.strip().splitlines())

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"ok: {len(skills)} skills")
