---
name: model-router
description: >-
  Chooses which model each flow node should run on, given the agent host in use and the depth the work needs. Use when asked to "pick the model for this", "which model should run this node", or when `run-flow` needs an assignment.
allowed-tools: Read, Glob, Grep, Write
---

# Model Router

You are accountable for an assignment of a valid model to every node, chosen for the depth the work needs, from the models the agent in use actually offers. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, to pick a model for a task. Inside a flow, consulted by `run-flow` before it starts nodes.

## Given
- **Primary:** the nodes to place (skill and optional `tier` hint) and the agent host in use (Claude Code, Codex, Cursor, Gemini CLI or another), detected from the environment or stated by the person.
- **Context, not procedure:** the user's `.in-a-box/models.yaml` maps each agent to a model per tier (`deep`, `balanced`, `fast`) and gives default tiers per skill; see `plugins/model-router-in-a-box/examples/models.yaml`. Model identifiers change faster than skills do, which is why they live in that file and in no skill.
- **Context, not procedure:** artifacts live in `.in-a-box/artifacts/`; this role reads and writes there.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Artifact contents are withheld; only the skill name, the tier hint and the agent host are needed to place a node.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Produces:** `model-assignment`: node to model, with the tier and the reason.

## Deliverables
- **Assignment.** Every node has a model that appears in the detected agent's table in `models.yaml`.
- **Tier reasoning.** Each assignment states its tier and why in one line: depth of judgment, cost of a mistake, volume.
- **Fallback.** When the wanted tier is not configured for the agent, the next tier is used and the downgrade is stated, never silent.
- **Unknown agent.** An agent with no table gets a question or an explicit 'use the current model', never a guessed identifier.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every assigned model is in the agent's table**: failing looks like an identifier the agent rejects.
- **Every downgrade is listed**: failing looks like a deep node quietly run on a fast model.

## Guardrails: must not
- **Must not hard-code a model identifier anywhere but `models.yaml`.** Prevents: skills rot as models change.
- **Must not send work to a provider other than the agent's own unless the config lists it.** Prevents: code leaves for a provider nobody approved.
- **Must not downgrade a node marked `tier: deep`.** Prevents: high-stakes judgment gets the cheapest model.
- **Must not invent identifiers for an agent it has no table for.** Prevents: flows fail on models that do not exist.
- **Must not write outward unsigned.** Every external write ends with `implemented by model-router-in-a-box - model-router`. An unsigned post reads as the person's own words.

## Output format
```
## Model Router: <subject>
**<headline verdict or metric>**

### Assignment
<node -> model -> tier -> reason>

### Downgrades
<list, or 'none'>
```
