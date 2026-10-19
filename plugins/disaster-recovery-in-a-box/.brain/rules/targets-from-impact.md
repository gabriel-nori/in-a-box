THE RULE

RPO and RTO are derived from the business impact of losing a service, not picked from a tier template. Each service gets a maximum tolerable downtime, a maximum tolerable data loss, the impact curve behind them, and an owner who accepted the numbers.

- Start from the business process, then the services and data it depends on.
- A service inherits the strictest target of any process that depends on it, and so do its dependencies.
- RTO covers detection, decision, recovery and verification, not only the restore.
- Tiers are a summary of the analysis, not a substitute for it.

WHY

Targets copied from a template are either too loose, and the business finds out during the outage, or too tight, and the money goes to resilience nobody needed.

HOW TO APPLY

For every service write: process served, impact per hour of downtime, data loss tolerance, resulting RTO and RPO, dependencies that cap them, and who signed off.

EXCEPTIONS

A first-pass plan may use provisional tiers if it says so and schedules the analysis.

JUDGED AGAINST

Every RPO and RTO traces to an impact statement and a named owner.

RELATED

disaster-recovery measured-recovery-beats-claimed; finops estimate-with-sources
