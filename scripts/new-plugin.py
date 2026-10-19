#!/usr/bin/env python3
"""Scaffold a role plugin: new-plugin.py <role> <skill-id>   e.g. new-plugin.py data data-analyst"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

if len(sys.argv) != 3:
    sys.exit(__doc__)
role, skill = sys.argv[1], sys.argv[2]
plugin = f"{role}-in-a-box"
base = ROOT / "plugins" / plugin
if base.exists():
    sys.exit(f"{plugin} already exists")

(base / ".claude-plugin").mkdir(parents=True)
(base / "skills" / skill).mkdir(parents=True)
(base / ".claude-plugin" / "plugin.json").write_text(json.dumps({
    "name": plugin, "version": "0.1.0",
    "description": f"{role} role.", "author": {"name": "Gabriel Almilhatti"},
    "keywords": ["in-a-box", "role", role]}, indent=2) + "\n", encoding="utf-8")
tpl = (ROOT / "templates" / "skill-contract.md").read_text(encoding="utf-8")
(base / "skills" / skill / "SKILL.md").write_text(tpl.replace("<skill-id>", skill), encoding="utf-8")
(base / "README.md").write_text(f"# {plugin}\n\nSkill: [`{skill}`](skills/{skill}/SKILL.md).\n", encoding="utf-8")

(base / ".brain").mkdir()
(base / ".brain" / "manifest.json").write_text(json.dumps({
    "plugin": plugin, "skills": [{"name": skill, "file": f"skills/{skill}/SKILL.md"}], "rules": []}, indent=2) + "\n",
    encoding="utf-8")

mp = ROOT / ".claude-plugin" / "marketplace.json"
data = json.loads(mp.read_text(encoding="utf-8"))
data["plugins"].append({"name": plugin, "source": f"./plugins/{plugin}", "description": f"{role} role."})
mp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
print(f"created {plugin}; fill in the contract, add its edges to docs/skill-dependencies.md, run check-contracts.py")
