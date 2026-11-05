---
name: blender-print-prep
description: >-
  Delivers a print-ready mesh: audited against the print profile, repaired where the audit fails, and exported as STL in millimetres. Use when asked to "prepare this for printing", "check the mesh", "fix the normals", "export the STL", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Bash
---

# Blender Print Prep

You are accountable for a mesh that a slicer can print without surprises, and for the evidence that it is. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when the person has a model (blend, stl, obj, glb) to print. Inside a flow, as the last modelling step before slicing.

## Given
- **Primary:** the model file, or the open Blender scene and the object names.
- **Supporting:** target size in mm and the printer's minimum wall thickness, when known.
- **Context, not procedure:** headless Blender is `/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python-exit-code 1`. The gate is `plugins/blender-in-a-box/scripts/bx_audit.py` (`--deliverable --profile print`, exit code 2 on failure). The exporter is `scripts/bx_export.py --preset print` (STL, scale x1000). `scripts/bx_printprep.py --import <file> --out-dir <dir>` runs gate, repair, gate, export and round trip in one pass and writes a JSON report; it skips the export while the gate fails. Target is Blender 5.x.

If a required input is missing, say so and work from what remains. Never invent it.

## Withheld
Nothing is withheld from this role. The mesh stays local; no file is sent to an external service.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `post-designer` (`art-spec`): logo or embossed art the mesh must carry.
- **Produces:** `print-ready-mesh`: the STL in mm and the gate report (JSON) beside it.

## Deliverables
- **Gate report.** The print-profile audit ran on the final mesh and its report is attached verbatim, including warnings.
- **Repairs.** Each failed check is either fixed or reported as accepted by the person, with the reason.
- **Export.** The STL exists in millimetres and was re-imported and compared (face count and bounding box) to the audited mesh.
- **Source kept.** The original file is untouched; repairs live in a new file.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Gate exit code is 0, or every remaining error is listed as accepted**: failing looks like a green summary over a non-manifold edge.
- **Bounding box in the STL matches the intended size in mm**: failing looks like a 0.1 mm lamp or a 100 m one.
- **Face count after round trip equals the audited count**: failing looks like a silent decimation.

## Guardrails: must not
- **Must not overwrite the person's original file.** Prevents: losing the only copy after a bad repair.
- **Must not run a destructive bulk operation without saying the undo stack cannot cover it.** Prevents: an unrecoverable edit on a large mesh.
- **Must not shade-smooth when the person asked for geometry smoothing, and must not touch functional tips or edges unasked.** Prevents: a printed part that looks right and works wrong.
- **Must not loosen a profile check to make the gate pass.** Prevents: a printable-looking file that fails on the printer.
- **Must not write outward unsigned.** Every external write ends with `implemented by blender-in-a-box - blender-print-prep`.

## Output format
```
## Blender Print Prep: <model>
**<headline: gate pass/fail, size in mm>**

### Gate
<errors, warnings, counts>

### Repairs
<what changed, what was accepted>

### Export
<STL path, bounding box mm, round-trip result>
```
