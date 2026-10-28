# Example: skill-integrator

Input: "Rename the `swot` artifact to `swot-analysis`." Mode: update.

## Skill Integrator: swot-analyst (update)
**Breaking: an artifact rename; two consumers need the new name.**

### Placement
Stays in `business-in-a-box` (role unchanged, no new plugin).

### Mirrors updated
- `docs/skill-dependencies.md`: `canvas-designer` optional-enriching edge now targets `swot-analysis`.
- README row, manifest skill list and maps regenerated with `sync-manifest.py` and `gen-maps.py`.

### Check output
`check-contracts.py`: OK (quoted in full in the real report).

### Classification and version
Breaking (artifact renamed). `business-in-a-box` 0.1.0 -> 0.2.0.

### Affected consumers
- `canvas-designer` SKILL.md and its dependency row: edited.
- A flow in `.in-a-box/flows/` binding the old name: owner's to edit; listed here.

### Brain import (dry-run)
Lists the changed skill and nothing else; not applied, waiting on the owner.
