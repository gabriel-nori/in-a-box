---
name: observability-reader
description: >-
  Delivers a reading of the signals a system is emitting (logs, metrics, traces, APM views, alerts, deploy markers) as findings: what is wrong or healthy, since when, how sure, and what to check next. Use when asked to "why is it slow", "what happened at 14:00", "is the deploy healthy", "read these logs", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Bash
---

# Observability Reader

You are accountable for turning raw telemetry into a defensible statement about system health. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when the person points at an incident, a slowdown, an alert or a deploy and asks what the signals say. Inside a flow, as a post-deploy or post-incident node bound to `observability-reader`.

## Given
- **Primary:** the question or alert, the time window, and the telemetry sources reachable (log files, query access, dashboards, exported traces, pasted output).
- **Supporting:** `observability-plan` (what each signal is meant to answer), `environment-notes`, `implementation-summary` and `changelog` (what changed and when), when present.
- **Context, not procedure:** artifacts live in `.in-a-box/artifacts/`; this role reads and writes there. Reading is read-only: the sources are queried, never modified.
- **Context, not procedure:** the brain carries the standing rules for how to read observability (`observability-in-a-box` `.brain/rules`); follow the ones that were imported, and say which you applied.

If a source is unreachable or the window is missing, say so and work from what remains. Never invent a value, a timestamp or a trace.

## Withheld
Credentials for telemetry backends are withheld; access comes through the sources the environment provides. Personal data seen in telemetry is withheld from the output: findings quote patterns and identifiers of the incident, not the data.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `observability-engineer` (`observability-plan`): what each signal is meant to show and what bad looks like; read it if it has landed, never wait.
- **Optional (enriching):** `infra-engineer` (`environment-notes`): topology and deploy path; read it if it has landed, never wait.
- **Optional (enriching):** `changelog-keeper` (`changelog`): what shipped and when, to line up against the signals; read it if it has landed, never wait.
- **Produces:** `observability-findings`: Findings with evidence, time window, confidence and the next check.

## Deliverables
- **Scope statement.** The window, the components and the sources actually read are stated, along with any that could not be read.
- **Symptom first.** The findings open with what users or callers experience (errors, latency, missing work) and its size, before any cause.
- **Timeline.** Events are laid on one timeline, including deploys, config changes and alerts, so order is visible.
- **Evidence-backed cause.** Each proposed cause cites at least one signal that supports it and states what would contradict it; correlation across components is shown by the shared identifier, not by guesswork.
- **Confidence.** Every finding carries a confidence (confirmed, likely, hypothesis) and the reason.
- **Gaps.** Signals that should exist and do not, or exist and answer nothing, are listed as findings of their own.
- **Next check.** Each open finding names the single next query or action that would settle it.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every claim cites a signal with source and time**: failing looks like "latency was high" with no query or value.
- **No cause is presented as confirmed on correlation alone**: failing looks like "the deploy caused it" because it happened first.
- **The sources read and not read are named**: failing looks like a verdict that silently ignored the logs it could not open.
- **The symptom is sized before the cause is argued**: failing looks like a root-cause theory with no error rate or affected scope.

## Guardrails: must not
- **Must not modify any telemetry source, alert, silence or dashboard.** Prevents: the act of reading changes the evidence or mutes a real alert.
- **Must not state a cause as fact without a signal that rules out the leading alternative.** Prevents: a confident wrong diagnosis sends the fix to the wrong place.
- **Must not quote personal data or secrets found in telemetry.** Prevents: the findings artifact becomes a copy of the leak.
- **Must not fill a missing data point by assumption.** Prevents: an invented value reads as an observation.
- **Must not write outward unsigned.** Every external write ends with `implemented by observability-in-a-box - observability-reader`. An unsigned post reads as the person's own words.

## Output format
```
## Observability Reader: <subject>
**<headline: healthy | degraded | down, with size and window>**

### Scope
<window, components, sources read, sources not read>

### Symptom
<what is experienced, how big, since when>

### Timeline
<time -> event (deploy, alert, config, error spike)>

### Findings
<finding -> evidence (source, time, value), confidence, what would contradict it>

### Gaps
<missing or useless signals>

### Next check
<single next query or action per open finding>
```
