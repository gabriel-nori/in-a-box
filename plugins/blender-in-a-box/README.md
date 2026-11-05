# blender-in-a-box

Skill: [`blender-print-prep`](skills/blender-print-prep/SKILL.md). Delivers a mesh that is gated and exported for 3D printing (STL in mm).

Scripts run in headless Blender 5.x, no external service:

    blender -b --factory-startup --python-exit-code 1 --python scripts/bx_audit.py -- --import part.stl --deliverable --profile print --json out.json

Third-party code: see [THIRD_PARTY.md](THIRD_PARTY.md).
