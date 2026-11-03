# designer-in-a-box

Role: **Designer**. Accountable for pieces whose composition, balance and accessibility can be checked, delivered as a specification and rendered by code.

Skills: [`design-foundations`](skills/design-foundations/SKILL.md) produces `design-rules`; [`post-designer`](skills/post-designer/SKILL.md) produces `art-spec`; [`art-renderer`](skills/art-renderer/SKILL.md) produces `post-art`; [`image-generator`](skills/image-generator/SKILL.md) produces `image-assets` through a diffusion model, behind a gate; [`design-reviewer`](skills/design-reviewer/SKILL.md) produces `design-review`.

Scripts (need Python 3 and Chrome):

- `scripts/render-art.py <art-spec.json> <out-dir>`: validates the spec, renders one PNG per slide and writes `manifest.json`. `--check-only` validates only. Example spec: `examples/art-spec.json`.
- `scripts/generate-image.py <art-spec.json> <out-dir>`: knows no image service. Writes `image-requests.json`, `image-brief.md` (plain text for any LLM or image model) and a hash. After the images exist as `<slot>.png`, `--attach <folder> --by <maker>` fills the art-spec and records provenance. Reaching a model (and the approval for that step) belongs to the process that runs the plugin, not to this plugin.

Planned: `ux-designer`, `ui-designer`, `brand-designer`, `web-designer`, `app-designer`.
