#!/usr/bin/env python3
"""Import a plugin's .brain manifest into the brain as learned skills, processes and rules.

  import-brain.py <plugin>|--all [--only ID ...] [--apply] [--realm REALM]

Dry-run by default: prints what would enter the brain and writes nothing. --apply writes
the listed items (all, or only the --only ids). Already-imported ids are skipped.
The graph CLI is found through $BRAIN_GRAPH_PY, else $CLAUDE_PLUGIN_ROOT/scripts/graph.py,
else ~/Documents/memory-ledger/scripts/graph.py.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from processlib import load_process

ROOT = pathlib.Path(__file__).resolve().parent.parent
EDGE = re.compile(r"^- \*\*(Requires|Optional \(ordered\)|Optional \(enriching\)):\*\*\s*`([^`]+)`", re.M)


def graph_py():
    for c in (os.environ.get("BRAIN_GRAPH_PY"),
              os.environ.get("CLAUDE_PLUGIN_ROOT") and os.path.join(os.environ["CLAUDE_PLUGIN_ROOT"], "scripts", "graph.py"),
              str(pathlib.Path.home() / "Documents" / "memory-ledger" / "scripts" / "graph.py")):
        if c and pathlib.Path(c).is_file():
            return c
    sys.exit("graph.py not found; set BRAIN_GRAPH_PY")


def graph(*args):
    p = subprocess.run([sys.executable, GRAPH, *args], capture_output=True, text=True, encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


def exists(node_id):
    rc, out, _ = graph("get-node", "--id", node_id)
    return rc == 0 and '"ok": true' in out


def section(text, name):
    m = re.search(rf"^{name}\s*\n(.*?)(?=^[A-Z][A-Z ]+\s*$|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def items(plugin_dir):
    man = json.loads((plugin_dir / ".brain" / "manifest.json").read_text(encoding="utf-8"))
    plugin = man["plugin"]
    for s in man.get("skills", []):
        f = plugin_dir / s["file"]
        text = f.read_text(encoding="utf-8")
        desc = re.search(r"^description:\s*>-\s*\n((?:  .*\n)+)", text, re.M)
        when = " ".join(desc.group(1).split()) if desc else s["name"]
        body = text.split("---", 2)[2].strip()
        edges = {"Requires": [], "Optional (ordered)": [], "Optional (enriching)": []}
        for kind, target in EDGE.findall(text):
            edges[kind].append(target)
        yield {"kind": "skill", "id": f"skill_{s['name']}", "plugin": plugin, "name": s["name"],
               "title": s["name"], "when": when, "body": body, "edges": edges}
    for q in man.get("processes", []):
        pr = load_process(plugin_dir, plugin_dir / q["file"])
        yield {"kind": "process", "id": f"process_{plugin}_{q['id']}", "plugin": plugin, "title": pr["title"],
               "scenario": pr["scenario"], "body": pr["body"], "roles": pr["roles"]}
    for r in man.get("rules", []):
        text = (plugin_dir / ".brain" / r["file"]).read_text(encoding="utf-8")
        yield {"kind": "rule", "id": f"rule_learned_{plugin}_{r['id']}", "plugin": plugin, "title": r["title"],
               "scenario": r.get("scenario", r["title"]), "non_negotiable": r.get("non_negotiable", False),
               "text": text}


def apply(it, realm):
    if it["kind"] == "skill":
        e = it["edges"]
        cmd = ["add-skill", "--id", it["id"], "--name", it["name"], "--title", it["title"],
               "--when", it["when"], "--body", it["body"], "--no-file"]
        for flag, key in (("--requires", "Requires"), ("--waits-for", "Optional (ordered)"),
                          ("--enriched-by", "Optional (enriching)")):
            targets = [t for t in e[key] if t != "none"]
            if targets:
                cmd += [flag, ",".join(targets)]
        return graph(*cmd)
    if it["kind"] == "process":
        rc, out, err = graph("add-node", "--type", "process", "--id", it["id"], "--title", it["title"],
                             "--body", it["body"], "--props", json.dumps({"scenario": it["scenario"], "plugin": it["plugin"],
                                                                         "source": "learned"}), "--realm", realm)
        for role in it["roles"]:
            if exists(f"skill_{role}"):
                graph("add-edge", "--src", it["id"], "--dst", f"skill_{role}", "--rel", "performed-by")
        return rc, out, err
    t = it["text"]
    cmd = ["add-rule", "--id", it["id"], "--title", it["title"], "--source", "learned", "--section", it["plugin"],
           "--realm", realm, "--scenario", it["scenario"], "--the-rule", section(t, "THE RULE"),
           "--why", section(t, "WHY"), "--how-to-apply", section(t, "HOW TO APPLY")]
    for flag, name in (("--exceptions", "EXCEPTIONS"), ("--judged-against", "JUDGED AGAINST"), ("--related", "RELATED")):
        v = section(t, name)
        if v:
            cmd += [flag, v]
    if it["non_negotiable"]:
        cmd.append("--non-negotiable")
    return graph(*cmd)


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("plugin", nargs="?", help="plugin folder name, e.g. observability-in-a-box")
ap.add_argument("--all", action="store_true")
ap.add_argument("--only", nargs="*", default=[], help="import only these item ids")
ap.add_argument("--apply", action="store_true", help="write to the brain (default: dry-run)")
ap.add_argument("--realm", default="shared")
a = ap.parse_args()
if not a.plugin and not a.all:
    ap.error("name a plugin or pass --all")

GRAPH = graph_py()
dirs = sorted(p for p in (ROOT / "plugins").iterdir() if (p / ".brain" / "manifest.json").is_file()) if a.all \
    else [ROOT / "plugins" / a.plugin]
done = skipped = failed = 0
for d in dirs:
    for it in items(d):
        if a.only and it["id"] not in a.only:
            continue
        label = f"{it['kind']:5} {it['id']}"
        if exists(it["id"]):
            print(f"skip  {label} (already in the brain)")
            skipped += 1
        elif not a.apply:
            print(f"would {label}")
        else:
            rc, out, err = apply(it, a.realm)
            ok = '"ok": true' in out
            print(f"{'added' if ok else 'FAIL '} {label}" + ("" if ok else f"\n{out or err}"))
            done += ok
            failed += not ok
print(f"{'applied' if a.apply else 'dry-run'}: {done} added, {skipped} skipped, {failed} failed")
sys.exit(1 if failed else 0)
