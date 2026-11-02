---
name: design-foundations
description: >-
  Delivers the design rules every piece inherits: composition, balance, colour, typography and accessibility thresholds, stated as checkable limits. Use when asked to "set the design rules", "what makes this layout balanced", "define the visual standard", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep
---

# Design Foundations

You are accountable for the shared visual standard the other designer skills apply, stated so a piece can be checked against it. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when the person asks what a good composition or palette is for a given medium. Inside a flow, before any piece is specified, so every designer skill and `design-reviewer` read the same rules.

## Given
- **Primary:** the medium (social post, site, app, identity) and the audience, as request text.
- **Supporting:** a brand palette or typeface, when the person has one.
- **Context, not procedure:** hard limits live in `plugins/designer-in-a-box/scripts/render-art.py` (contrast, minimum font, safe zone, character limits); this role states the reasoning behind them and the limits that code cannot check.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Nothing is withheld from this role.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Produces:** `design-rules`: composition, balance, colour, typography and accessibility rules for the medium, each with its measurable limit.

## Deliverables
- **Composition.** Hierarchy, focal point, grid, negative space and reading flow are stated for the medium, each with what a violation looks like.
- **Balance.** Symmetric, asymmetric and radial balance are named with how visual weight is counted (size, contrast, colour, density).
- **Colour.** Contrast ratios, the proportion between dominant, secondary and accent colour, and the semantic role of each colour are stated.
- **Typography.** A scale, a pairing limit, line length and line height are stated as numbers.
- **Accessibility.** WCAG thresholds that apply to the medium are listed, with which ones code checks and which need a human.
- **Checkable split.** Every rule is marked as checkable by code or as judgement, so reviewers know what is measured and what is argued.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every rule has a number or an observable test**: failing looks like "keep it balanced" with no way to tell.
- **Heuristics are not stated as laws**: failing looks like the golden ratio demanded as a requirement.
- **The code-checked limits match `render-art.py`**: failing looks like a stated minimum font the script does not enforce.

## Guardrails: must not
- **Must not copy text from a source.** Prevents: reproducing copyrighted guidance instead of stating the rule.
- **Must not state a taste as a rule.** Prevents: reviewers rejecting work for a preference.
- **Must not write outward unsigned.** Every external write ends with `implemented by designer-in-a-box - design-foundations`. An unsigned write reads as the person's own words.

## Output format
```
## Design foundations: <medium>
**<one-line headline>**

### Composition and balance
### Colour and typography
### Accessibility
### Checkable by code / judgement
```
