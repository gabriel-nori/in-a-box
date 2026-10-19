THE RULE

Logs and traces never carry secrets or personal data, and redaction happens at the source.

- Never log tokens, passwords, API keys, authorization headers, cookies, full request or response bodies, or personal identifiers (email, document numbers, addresses).
- Log identifiers that are safe to join on (internal ids, hashed ids) and the shape of a failure, not its payload.
- Redaction is implemented in the logging layer or the collector pipeline, not left to each call site, and it is tested with a known fake secret.
- Retention is stated per log class: debug short, audit and security long, and access to them is restricted.

WHY

A telemetry backend is a second database with weaker access control and long retention. One logged token or address becomes a leak that is copied into backups, dashboards and screenshots.

HOW TO APPLY

When reviewing a logger configuration or a trace attribute list, search for the fields above and for whole-object logging (`log(request)`, `log(user)`). Add a test that writes a fake secret through the pipeline and asserts it never reaches the output. When findings must quote telemetry, quote patterns and ids of the incident, not the data.

EXCEPTIONS

Audit logs that must record who did what keep the actor id, never the credential. Debug logging of payloads may be enabled temporarily in a non-production environment with synthetic data.

JUDGED AGAINST

Redaction exists in one central place, a test proves it, and no log format or span attribute names a secret or personal-data field.

RELATED

observability-apply-signals; rule on personal material staying in the brain
