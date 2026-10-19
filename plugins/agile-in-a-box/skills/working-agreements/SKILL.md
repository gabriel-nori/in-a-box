---
name: working-agreements
description: >-
  Delivers the team's Definition of Done, Definition of Ready and working agreements as short, checkable lists the team actually holds. Use when asked to "write our Definition of Done", "Definition of Ready", "DoD", "DoR", "team working agreements", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Write
---

# Working Agreements

You are accountable for agreements the team can check an item against in under a minute. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when a team has none, has stale ones, or keeps disagreeing on what 'done' means. Feeds `issue-writer` and the facilitators.

## Given
- **Primary:** the request text from the user or the orchestrator.
- **Supporting:** any artifact listed under Optional in Depends on, when present.
- **Context, not procedure:** artifacts live in `.in-a-box/artifacts/`; this role reads and writes there.
- **Context, not procedure:** Definition of Done is the shared quality bar every increment must meet (code reviewed, tests passing, docs updated, deployed to a stated environment, acceptance criteria verified); it can exist at story, sprint and release level. Definition of Ready is the entry bar for a story to be pulled into a sprint (understood, small, estimated, acceptance criteria, dependencies cleared).
- **Context, not procedure:** agreements are few (about 5 to 10 items each), written as checkable statements, and owned by the team; the facilitator proposes, the team decides.
- **Context, not procedure:** a Definition of Done only ratchets up through a retro decision; lowering it to hit a date is a recorded exception, not a silent change.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Individual performance data about team members is withheld; the role reports on the system and the work, not on the person.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `developer` (`implementation-summary`): what the team already does in practice, to match the written bar to reality; read it if it has landed, never wait.
- **Optional (enriching):** `qa-tester` (`qa-report`): the quality gates the team already runs; read it if it has landed, never wait.
- **Produces:** `working-agreements`: Definition of Done, Definition of Ready and working agreements, each item checkable, with the date and owner of the last review.

## Deliverables
- **Definition of Done.** A list of checkable statements per level, each answerable yes or no.
- **Definition of Ready.** A list of checkable entry conditions for a story.
- **Working agreements.** Core hours, ceremony etiquette, WIP limits and how disagreement is handled, each stated as a behaviour.
- **Review cadence.** The date the agreements were set and when they are next reviewed.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every item is checkable yes or no**: failing looks like 'high quality code'.
- **The lists are short enough to hold in the head**: failing looks like a 30-line checklist nobody reads.

## Guardrails: must not
- **Must not impose the agreements from outside the team.** Prevents: they are ignored.
- **Must not lower the Definition of Done silently to meet a date.** Prevents: debt is hidden instead of chosen.
- **Must not write outward unsigned.** Every external write ends with `implemented by agile-in-a-box - working-agreements`. An unsigned post reads as the person's own words.

## Output format
```
## Working Agreements: <subject>
**<headline verdict or metric>**

### Definition of Done
<checkable items>

### Definition of Ready
<checkable items>

### Working agreements
<behaviours>

### Review cadence
<set on, next review>
```
