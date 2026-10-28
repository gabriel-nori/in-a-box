---
name: skill-integrator
description: >-
  Delivers the integration of a new skill into the plugin tree, or the update of an existing one, with every mirrored table, manifest, map and consumer left consistent and the change classified. Use when asked to "add this skill to the tree", "integrate this skill", "update this skill", "rename this clause", "where does this skill go", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Skill Integrator

You are accountable for a skill that sits in the right place in the tree, agrees with every table that mirrors it, and breaks nobody who depends on it without saying so. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when a new skill has been written or an existing one changed and the person wants it landed in the tree, in their own words. Inside a flow, when the orchestrator reaches the node bound to `skill-integrator`.

## Given
- **Primary:** the skill to integrate (a new `SKILL.md`, or the changed one) and the mode: `new` or `update`.
- **Supporting:** `CONVENTIONS.md`, `docs/skill-dependencies.md`, `docs/skill-specializations.md`, the plugin's `.brain/manifest.json`, the root `MAP.md`, and any artifact listed under Optional in Depends on, when present.
- **Context, not procedure, placement:** one role per plugin; a skill belongs to the plugin whose role it serves. A second skill of an existing role joins that plugin as a router, specialist or stage. A new role is a new `<role>-in-a-box` plugin (scaffolded by `scripts/new-plugin.py`, which also registers it in the marketplace file). A specialist declares `Specializes: <base>` and is mirrored in `docs/skill-specializations.md`.
- **Context, not procedure, what mirrors a skill:** its `Depends on` edges in `docs/skill-dependencies.md`; its row in the root `README.md` plugin table; its entry in `.brain/manifest.json` (skill list produced by `scripts/sync-manifest.py`); the maps produced by `scripts/gen-maps.py`; and its rules under `.brain/rules/` when the research produced standards worth recalling. Manifests' skill lists and maps are produced by code, never typed.
- **Context, not procedure, what depends on a skill:** other skills that name it or its artifact in `Depends on`, flows that bind a node to it, rules that cite it, and team rules that aim at its clause names. These are found by searching the tree for the skill name, the artifact name and each clause name before the change is called safe.
- **Context, not procedure, classification:** adding a clause or a skill is additive; renaming or removing a clause, a skill or an artifact, or tightening a `Requires` edge, is breaking (CONVENTIONS section 7); changing wording without changing what is promised is a patch. Plugin versions follow semver.
- **Context, not procedure, the check:** `scripts/check-contracts.py` is the arbiter of sections, edges, manifests, maps, sources and ordering cycles.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Nothing personal is passed in or written into a manifest, rule or example (CONVENTIONS section 8).

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (ordered):** `source-researcher` (`research-findings`): when the skill's norms are being researched or refreshed, that run lands first, because integrating before it records rules and citations that the research is about to change.
- **Produces:** `integration-report`: where the skill landed, what was updated to match, the classification, and who is affected.

## Deliverables
- **Placement.** The plugin and the reason: existing role or new role, router or specialist, with `Specializes` stated where it applies.
- **Contract conformance.** The skill has the required sections in order, no numbered step list, and every constraint it carried is a deliverable, judgement or guardrail.
- **Mirrors agree.** Edges, specializations, the README row, the manifest and the maps match the skill; `check-contracts.py` passes, and its output is quoted.
- **Rules and sources.** Standards the research produced are brain rules with the three sections and cited source ids that exist in the registry; no rule restates a skill's own guardrails.
- **Classification (update).** The change is named additive, breaking or patch, with the plugin version bump that follows, and a breaking change lists each renamed or removed clause, skill or artifact.
- **Affected consumers.** Every skill, flow, rule and team rule that depends on what changed is listed, with the edit made or the owner told it is theirs to make.
- **Example.** The skill has an example in `examples/` that still matches the current contract; a stale one is refreshed or flagged.
- **Brain import.** The dry-run of `scripts/import-brain.py <plugin>` is shown; applying it is left to the owner.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **The checker's output is quoted and clean**: failing looks like "should pass" with no run.
- **Every edge in the skill has a row in the dependency table, and the reverse**: failing looks like a `Requires` that the orchestrator cannot see.
- **A breaking change lists its consumers**: failing looks like a renamed artifact with a flow still binding the old name.
- **Placement is justified against the one-role rule**: failing looks like a second role tucked into an existing plugin.
- **Nothing generated was hand-edited**: failing looks like a map or manifest skill list that `gen-maps.py --check` flags.

## Guardrails: must not
- **Must not hand-write a map or the skill list of a manifest.** Prevents: drift that the checker then fails on.
- **Must not rename or remove a clause, skill or artifact without listing its consumers.** Prevents: flows and team rules silently aimed at nothing.
- **Must not add a step list while converting or fixing a skill.** Prevents: a procedure re-entering a contract; restate each constraint from a deleted step as a guardrail first.
- **Must not introduce an ordering cycle, or wire a role to a flow.** Prevents: an unrunnable graph, and a role that stops being reusable (CONVENTIONS section 5).
- **Must not apply a brain import without the owner's approval.** Prevents: unreviewed items entering the brain.
- **Must not commit, push or publish unasked.** Prevents: an outward action nobody approved (CONVENTIONS section 6).
- **Must not write outward unsigned.** Every external write ends with `implemented by curator-in-a-box - skill-integrator`. An unsigned write reads as the person's own words.

## Output format
```
## Skill Integrator: <skill> (<new|update>)
**<one-line headline: where it landed, additive or breaking>**

### Placement
### Mirrors updated
### Check output
### Classification and version
### Affected consumers
### Brain import (dry-run)
```
