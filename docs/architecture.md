# Architecture

## Processes

Beside the contract skills, each plugin carries processes: what a position does in a situation, sourced from the field's own standards (CONVENTIONS section 10). The brain recalls them; `process-to-command` produces a command from one when a host needs it.

## Three layers

1. **Roles** (`<role>-in-a-box`): each plugin owns one job, expressed as a contract skill. A role consumes named artifacts and produces one.
2. **Artifacts**: the only coupling between roles. Plain files in `.in-a-box/artifacts/`. A role does not know who produced its input or who reads its output.
3. **Orchestrator** (`orchestrator-in-a-box`): composes roles into flows and runs them.

```
 user intent
     |
     v
 orchestrator ---- reads ----> skill Depends on edges (docs/skill-dependencies.md)
     |
     |  flow = nodes (role bound to a skill) + edges (artifact handoffs) + gates
     v
 role skill --reads--> artifacts --writes--> artifact --> next role
```

## Why contracts make this work

The orchestrator can wire any role to any other only if each role states, machine-readably, what it needs and what it produces. The `Depends on` section is that statement. Because skills declare outcomes and not steps, a role keeps working when the flow around it changes.

## Flow definition

A flow is a YAML file, kept per user or team in `.in-a-box/flows/`. Example: [`plugins/orchestrator-in-a-box/examples/idea-to-release.yaml`](../plugins/orchestrator-in-a-box/examples/idea-to-release.yaml).

```yaml
name: idea-to-release
nodes:
  - id: refine
    skill: product-owner
  - id: build
    skill: developer
    after: [refine]
  - id: review
    skill: security-reviewer
    after: [build]
    gate: human        # pause before outward effects
```

Validity, checked before running: every node's `Requires` is satisfied by an upstream node's `Produces` (a specialist satisfies an edge on its base skill); every `Optional (ordered)` target that is present in the flow is upstream of the node; no cycles, except a declared loop.

Two node features beyond `skill` and `after`:

- `route: <artifact>`: the node fans out, one run per assignment in the artifact, each with the skill the artifact names. This is how `tech-lead` hands units to `developer-python`, `developer-react` and so on.
- `on_reject: {to: <node>, max_iterations: N}`: a bounded loop. A rejection from this node re-runs the flow from `to`, at most N times, then pauses for a human. The back edge is the `Optional (enriching)` edge from the target to this node's artifact (for example `tech-lead` reading `acceptance-decision`), so it never counts as a cycle.

The dev flow ([`spec-to-ship.yaml`](../plugins/orchestrator-in-a-box/examples/spec-to-ship.yaml)): `product-owner` -> `spec-analyst` -> `tech-lead` -> developers (routed) -> `qa-tester` -> `acceptance-reviewer` -> `documenter` -> `changelog-keeper` -> ship.

## Model routing

`model-router-in-a-box` assigns a model per node from the agent host in use, using the user's `.in-a-box/models.yaml`. It decides; the host applies (for example by starting each node as a subagent on the assigned model).

## Customization levels

- Pick roles: install only the plugins you need.
- Pick the flow: compose your own, or start from an example.
- Pick the rules: per-team rules attach to deliverable clause names in each skill.

## Open questions

- Flow format: YAML now, with `route` and a bounded `on_reject` loop; revisit if conditional branching is needed.
- `release-in-a-box` now exists as its own role; the example flows still end in `infra-engineer`'s ship node and are not yet rewired to it.
- QA scope declaration: free text in the node today; may need a schema.
- Where run state lives (`.in-a-box/runs/`) and how a paused gate resumes.
- Artifact schema: free Markdown now, front-matter for machine-readable fields later.
- Commercial and licensing model, once the repo opens up.
