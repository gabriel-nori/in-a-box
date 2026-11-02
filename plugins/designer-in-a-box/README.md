# designer-in-a-box

Role: **Designer**. Accountable for pieces whose composition, balance and accessibility can be checked, delivered as a specification and rendered by code.

Skills: [`design-foundations`](skills/design-foundations/SKILL.md) produces `design-rules`; [`post-designer`](skills/post-designer/SKILL.md) produces `art-spec`; [`art-renderer`](skills/art-renderer/SKILL.md) produces `post-art`; [`image-generator`](skills/image-generator/SKILL.md) produces `image-assets` through a diffusion model, behind a gate; [`design-reviewer`](skills/design-reviewer/SKILL.md) produces `design-review`.

Scripts (need Python 3 and Chrome):

- `scripts/render-art.py <art-spec.json> <out-dir>`: validates the spec, renders one PNG per slide and writes `manifest.json`. `--check-only` validates only. Example spec: `examples/art-spec.json`.
- `scripts/generate-image.py <art-spec.json> <out-dir>`: dry run writes `image-requests.json` and a hash. Sending needs `--send --provider <name> --authorize <hash>`. A provider is a JSON adapter `{"command": [...]}` in `~/.in-a-box/image-providers/`; none is built in. `providers/gemini.py` is a Gemini adapter: copy `providers/gemini.json` to `~/.in-a-box/image-providers/`, replace `<path-to>`, and set `GEMINI_API_KEY` (or `~/.in-a-box/secrets/gemini.key`). Not yet run against the live API.

Planned: `ux-designer`, `ui-designer`, `brand-designer`, `web-designer`, `app-designer`.
