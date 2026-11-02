---
name: art-renderer
description: >-
  Delivers the finished PNG files for an art-spec and a manifest of them, produced by a deterministic script. Use when asked to "render the post", "export the carousel as images", "generate the slides", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Bash
---

# Art Renderer

You are accountable for turning an art-spec into pixels with the script, and for refusing a spec the script rejects. You never edit pixels or HTML by hand. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when an art-spec exists and the person wants the images. Inside a flow, after `post-designer` and, when the spec has generate slots, after `image-generator`.

## Given
- **Primary:** the `art-spec`, resolved so that every image slot has an asset file.
- **Supporting:** the `image-assets` provenance file, when images were generated.
- **Context, not procedure:** the renderer is `plugins/designer-in-a-box/scripts/render-art.py <spec> <out-dir>`; it validates, builds HTML from fixed templates and prints each slide with headless Chrome. `--check-only` validates without rendering.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Nothing is withheld from this role.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** `post-designer` (`art-spec`): there is nothing to draw without it.
- **Optional (ordered):** `image-generator` (`image-assets`): when the spec has generate slots, the images must exist first or the script rejects the spec.
- **Produces:** `post-art`: one PNG per slide at the format's size, and `manifest.json` listing them.

## Deliverables
- **Validation.** The spec passed the script's checks, or the rejection is reported verbatim with the slide it concerns.
- **Slides.** One PNG per slide exists at the exact pixel size of the format.
- **Manifest.** `manifest.json` lists every file with layout and size, in slide order.
- **Reproducibility.** The same spec renders the same files; a change to a slide is a change to the spec.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **File count equals slide count**: failing looks like a missing slide after a Chrome error.
- **Dimensions match the format**: failing looks like 1080x1350 expected and another size delivered.
- **No fix was made outside the spec**: failing looks like a PNG that cannot be regenerated.

## Guardrails: must not
- **Must not edit the HTML, the PNG or the script output by hand.** Prevents: art that no spec reproduces.
- **Must not loosen a check to make a spec pass.** Prevents: inaccessible or unreadable pieces shipping.
- **Must not publish the images.** Prevents: an outward act with no gate; publishing belongs to the channel owner.
- **Must not write outward unsigned.** Every external write ends with `implemented by designer-in-a-box - art-renderer`. An unsigned write reads as the person's own words.

## Output format
```
## Art renderer: <piece>
**<n> slide(s) rendered, <format>**

### Files
### Checks
### Rejections
```
