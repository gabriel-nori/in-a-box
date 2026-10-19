#!/usr/bin/env python3
"""Create or refresh each plugin's .brain/manifest.json skill list from its skills/ folder.
Rules already listed are preserved; add new ones by hand (CONVENTIONS section 8)."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from processlib import load_process

ROOT = pathlib.Path(__file__).resolve().parent.parent

for plugin in sorted((ROOT / "plugins").iterdir()):
    if not (plugin / ".claude-plugin" / "plugin.json").is_file():
        continue
    mf = plugin / ".brain" / "manifest.json"
    old = json.loads(mf.read_text(encoding="utf-8")) if mf.is_file() else {}
    mf.parent.mkdir(exist_ok=True)
    data = {"plugin": plugin.name,
            "skills": [{"name": s.parent.name, "file": s.relative_to(plugin).as_posix()}
                       for s in sorted(plugin.glob("skills/*/SKILL.md"))],
            "processes": [{"id": q["id"], "title": q["title"], "file": q["file"], "scenario": q["scenario"],
                           "roles": q["roles"], "sources": q["sources"]}
                          for q in (load_process(plugin, f) for f in sorted(plugin.glob("processes/*.md")))],
            "rules": old.get("rules", [])}
    mf.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"{plugin.name}: {len(data['skills'])} skills, {len(data['processes'])} processes, {len(data['rules'])} rules")
