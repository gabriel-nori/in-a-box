THE RULE

Read telemetry from the symptom to the cause, on one timeline, and say how sure you are.

- Start with what users or callers experience and size it: error rate, latency percentile, affected scope, start time. Use p95/p99 and rates, not averages.
- Put deploys, config changes and alerts on the same timeline as the signals before arguing a cause.
- Follow one failing request by its correlation id from the edge to the first component that misbehaves; compare it with a healthy one.
- Separate symptom, cause and trigger. A deploy that precedes an error is a candidate, not a verdict; rule out the leading alternative with a signal.
- Label every finding confirmed, likely or hypothesis, cite the source and time, and name the single next check that would settle it.
- Missing data is a finding. Say which source could not be read; never fill a gap by assumption.

WHY

Telemetry invites pattern-matching: the first spike gets blamed. Sizing the symptom, ordering events and stating confidence keeps the diagnosis honest and tells the next person where to look.

HOW TO APPLY

Use the reading guide in the observability plan when it exists: it says which query answers which question and what bad looks like. Without a plan, derive the question first, then pick the signal. Read-only: do not silence alerts, edit dashboards or change retention while investigating.

EXCEPTIONS

During an active outage, mitigation (rollback, scale-out, feature flag off) may come before the full reading, as long as the pre-mitigation state is captured first.

JUDGED AGAINST

The findings state window and sources, open with a sized symptom, carry a timeline, cite evidence per claim, and give a confidence and a next check per open finding.

RELATED

observability-apply-signals; observability-alerting-and-slos; observability-log-hygiene
