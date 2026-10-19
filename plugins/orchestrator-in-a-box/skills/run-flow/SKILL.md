---
name: run-flow
description: >-
  Executes a flow definition across role skills, handing artifacts between them and stopping at gates.
  Use when asked to "run the flow", "start this process", or "continue the paused run".
allowed-tools: Read, Glob, Grep, Write, Task
---

# Run Flow

You are accountable for every node of the flow reaching a recorded outcome, with artifacts handed over intact and no gate crossed without a human.

## When to use
When a flow definition exists and the person wants it executed or resumed.

## Given
- **Primary:** a flow definition, and the initial input the first node needs.
- **Context, not procedure:** artifacts go in `.in-a-box/artifacts/`, run records in `.in-a-box/runs/<run-id>.md`.

If the flow is invalid, say so and stop. Never repair it silently.

## Withheld
Each role receives only the artifacts its `Depends on` names. The roles' own reasoning is not forwarded, so each role's judgment stays independent.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** `compose-flow` (`flow-definition`): the flow to run, or one the person supplies.
- **Optional (enriching):** a previous run record: resume from it.
- **Optional (enriching):** `model-router` (`model-assignment`): the model each node should run on; use it when present, otherwise run nodes on the current model.
- **Produces:** `run-record`: node outcomes, artifacts produced, gates passed.

## Deliverables
- **Complete or paused run.** Every node is `done`, `skipped with reason`, or `waiting at a gate`; none is silently missing.
- **Intact handoffs.** Each node received exactly the artifacts it requires, unmodified.
- **Routed nodes.** A node with `route: <artifact>` runs once per assignment in that artifact, each with the skill the artifact names; a skill that is not installed fails the node.
- **Applied models.** When a `model-assignment` exists, each node is started as its own subagent (`Task`) on the model assigned to it. The record shows the model each node ran on. Where the host cannot start a node on a chosen model, the node runs on the current model and the record says so, never a silent substitution.
- **Bounded loops.** A node with `on_reject` sends a rejection back to the declared node and re-runs from there, at most `max_iterations` times; each pass is recorded, and the run pauses for a human when the limit is hit.
- **Run record.** The record lists each node, its outcome, its iteration, its model and its artifact path.

## Judged against
The output is correct when a reader who never saw the run can confirm, from the record alone:

- **Every node has an outcome**: failing looks like a node with no entry.
- **Every node shows the model it ran on**: failing looks like an assignment that was computed but is not in the record.
- **Every gated node shows a human decision before its outward effect**: failing looks like a deploy with no recorded approval.

## Guardrails: must not
- **Must not cross a gate without a recorded human decision.** Prevents: irreversible outward actions with no check.
- **Must not continue past a failed required node.** Prevents: downstream roles working from missing input.
- **Must not loop past `max_iterations` or loop on a flow that does not declare `on_reject`.** Prevents: an endless reject-and-rework cycle that burns budget.
- **Must not alter an artifact between roles.** Prevents: a role judged on something it did not produce.
- **Must not write outward unsigned.** Every external write ends with `implemented by orchestrator-in-a-box - run-flow`.

## Output format
```
## Run <run-id>: <flow name>
**<done | paused at <node> | failed at <node>>**

| Node | Skill | Model | Outcome | Artifact |
|---|---|---|---|---|
```
