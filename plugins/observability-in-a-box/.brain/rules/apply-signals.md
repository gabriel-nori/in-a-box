THE RULE

Every tool, service and job built or deployed gets the three signals and a way to follow one request across them.

- Logs: structured (JSON), levelled, one event per line, each carrying the correlation id, the service name and the version.
- Metrics: rate, errors and duration for anything a user or caller waits on (RED); utilisation, saturation and errors for resources (USE). Names are stable and units are in the name.
- Traces: instrument through OpenTelemetry where the stack allows; propagate the trace context across every process, queue and HTTP hop; the trace id is the correlation id in logs.
- Deployment: every deploy, rollback and config change is emitted as an event or marker on the same timeline.
- The application starts and works with the telemetry backend absent; the backend is configured by environment and secret references only.

WHY

An incident is solved by following one request through the system. Signals that cannot be joined by an id, or that die when the vendor key is missing, are evidence you cannot use when you need it. Vendor-neutral instrumentation keeps the choice of APM reversible.

HOW TO APPLY

When writing or reviewing a service, check the five points above before calling it done. Prefer the repo's existing stack; otherwise OpenTelemetry SDK plus a collector. Metrics labels come from a small closed set (route template, status class, method), never user ids, request ids or raw URLs. Record which of these points a deliverable met in its observability plan.

EXCEPTIONS

A short-lived script with no callers needs only structured logs with its job id. A component that cannot be instrumented (third-party SaaS) is observed from its edge: the calls you make to it.

JUDGED AGAINST

Each component in the plan has logs, metrics and traces (or a stated exception), shares one correlation id, and starts with the backend disabled.

RELATED

observability-alerting-and-slos; observability-log-hygiene; observability-read-signals
