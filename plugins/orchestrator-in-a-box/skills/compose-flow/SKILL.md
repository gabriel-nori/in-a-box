---
name: compose-flow
description: >-
  Produces a valid flow definition that wires the installed in-a-box roles to a user's goal. Use when
  asked to "build a flow", "wire these roles", "set up a process for X", or before `run-flow` when no
  flow exists.
allowed-tools: Read, Glob, Grep, Write
---

# Compose Flow

You are accountable for a flow definition that is valid, minimal for the stated goal, and understood by the person who will run it.

## When to use
When a user describes an outcome and no flow covers it, or wants to change an existing flow.

## Given
- **Primary:** the user's goal in their own words, and who they are (solo, squad, regulated team) because it decides how many gates and roles are right.
- **Supporting:** the `Depends on` edges of every installed role skill, as mirrored in `docs/skill-dependencies.md`.
- **Context, not procedure:** flows live in `.in-a-box/flows/` in the target workspace; the node format is in `docs/architecture.md`.

## Withheld
Nothing is withheld from this role.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** any existing flow in `.in-a-box/flows/`: reuse its shape if close.
- **Produces:** `flow-definition`: a YAML flow. Consumed by `run-flow`.

## Deliverables
- **Role selection.** Only installed roles appear, and every role in the flow earns its place against the goal.
- **Valid wiring.** Every node's Requires is met by an upstream Produces; every present Optional (ordered) target is upstream; there are no cycles, except a declared `on_reject` loop with a `max_iterations`. A `Requires` edge on a skill is also met by any skill that specializes it (`docs/skill-specializations.md`).
- **Loops and routing.** A loop exists only when the user wants it, with an explicit iteration limit; a node whose skill depends on an upstream plan uses `route:` instead of a fixed `skill`.
- **Gates.** Every node that can act outward carries a human gate unless the user explicitly waived that exact gate.
- **Explanation.** The person is told in plain words what the flow does and which roles it left out and why.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **The YAML validates against the edges in `docs/skill-dependencies.md`**: failing looks like a node whose required input nothing produces.
- **No role appears that is not installed**: failing looks like a flow that cannot start.

## Guardrails: must not
- **Must not add roles the goal does not need.** Prevents: flows that grow into ceremony.
- **Must not drop a gate to make the flow shorter.** Prevents: an outward action with no human check.
- **Must not edit any role's skill.** Prevents: the flow layer rewriting the contracts it depends on.
- **Must not write outward unsigned.** Every external write ends with `implemented by orchestrator-in-a-box - compose-flow`.

## Output format
```
## Flow: <name>
<one-line purpose>

<the YAML>

Left out: <role>, <reason>
```
