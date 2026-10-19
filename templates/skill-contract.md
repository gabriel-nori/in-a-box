---
name: <skill-id>
description: >-
  <What this role delivers, one sentence starting with a verb.> Use when asked to
  "<trigger>", "<trigger>", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep
---

<!--
  Copy to plugins/<role>-in-a-box/skills/<skill-id>/SKILL.md and fill in. See CONVENTIONS section 2.
  Declare WHAT must be true at the end and WHICH constraints may not be broken. Never the steps.
  Delete every comment before committing.
-->

# <Role Name>

<Two or three sentences: what this role is accountable for. The deliverable, not the activity.>

## When to use
<Standalone trigger, and the position in a flow.>

## Given
- **Primary:** <artifact or request> : <what this role takes from it>.
- **Context, not procedure:** <where things live, which command runs them>.

If a required input is missing, say so and work from what remains. Never invent it.

## Withheld
<What must never be passed in, and why. Or one line: nothing is withheld.>

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (ordered):** `<skill>` (`<artifact>`): <why starting early makes output wrong>.
- **Optional (enriching):** `<skill>` (`<artifact>`): <read if present, never wait>.
- **Produces:** `<artifact>`: <what it contains>.

## Deliverables
- **<Clause name>.** <What must be true or exist. No steps.>

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **<Checkable condition>**: failing looks like <...>.

## Guardrails: must not
- **Must not <action>.** Prevents: <failure>.
- **Must not write outward unsigned.** Every external write ends with `implemented by <plugin_name - skill_name>`.

## Output format
```
## <Role>: <subject>
**<headline>**

### <section>
<concrete content>
```
