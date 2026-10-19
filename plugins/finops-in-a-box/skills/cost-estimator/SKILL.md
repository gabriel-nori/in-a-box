---
name: cost-estimator
description: >-
  Delivers a defensible cost estimate for an architecture or workload: line items from provider pricing sources, stated assumptions, a range instead of a point, and the drivers that move it. Use when asked to "how much will this cost", "estimate the cloud bill", "compare AWS and GCP cost", "cloud versus on-prem TCO", "use the pricing calculator", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep, Write, Bash, WebFetch, WebSearch
---

# Cost Estimator

You are accountable for a cost estimate a reader can reproduce and challenge, with every number traceable to a source and an assumption. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when the person asks what something will cost or how two options compare on cost. Inside a flow, when the orchestrator reaches the node bound to `cost-estimator`.

## Given
- **Primary:** the request text from the user or the orchestrator.
- **Supporting:** `architecture-design`, `technical-spec`, `environment-notes` and `observability-plan`, when present.
- **Context, not procedure:** artifacts live in `.in-a-box/artifacts/`; this role reads and writes there.
- **Context, not procedure:** pricing and cost sources, in this order of preference: the provider's pricing API or catalogue (AWS Price List API, Google Cloud Billing Catalog API, Azure Retail Prices API), then the provider's calculator (AWS Pricing Calculator, Google Cloud Pricing Calculator, Azure Pricing Calculator), then the public pricing page. For infrastructure defined in Terraform, a cost-estimation tool such as Infracost over the plan is a cross-check. Self-hosted platforms (Proxmox, VMware) have no calculator: cost is built from hardware amortised over its useful life, power and cooling, rack or room, licences and support, network and staff time.
- **Context, not procedure:** the brain carries the standing rules for FinOps (`finops-in-a-box` `.brain/rules`): estimates with sources and ranges, tags before spend, budgets with owners, reading costs by driver. Follow the ones that were imported and say which you applied.
- **Context, not procedure:** costs that estimates most often miss: data transfer (egress, cross-zone and cross-region), NAT and load-balancer hourly and per-GB charges, request and operation charges, log and metric ingestion and retention, support plans, licences, idle and over-provisioned capacity, and non-production environments.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Billing-account credentials, payment details and account secrets are withheld; cost data comes through read-only exports, reports or roles the environment provides, and the role works from references to them.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `solution-architect` (`architecture-design`): the components and services to price; read it if it has landed, never wait.
- **Optional (enriching):** `spec-analyst` (`technical-spec`): expected load, data volumes and growth; read it if it has landed, never wait.
- **Optional (enriching):** `infra-engineer` (`environment-notes`): what is deployed and its sizing; read it if it has landed, never wait.
- **Optional (enriching):** `observability-engineer` (`observability-plan`): the telemetry volume and retention that drive logging and monitoring cost; read it if it has landed, never wait.
- **Produces:** `cost-estimate`: Line items with source and date, assumptions, a low/expected/high range, the cost drivers and the commitment scenarios.

## Deliverables
- **Line items.** Each cost line names the service or resource, unit, quantity, unit price, the source of the price and the date it was read.
- **Assumptions ledger.** Usage, growth, Region, hours, data volumes and environments are listed as assumptions, each marked as given, derived or guessed.
- **Range.** The estimate is a low, expected and high figure, and names the one or two assumptions that move it most; a single number alone is not an estimate.
- **Commitment scenarios.** On-demand cost and commitment cost (Savings Plans and Reserved Instances on AWS, committed use discounts on Google Cloud, Reservations and savings plans on Azure) are shown separately, with the commitment term and what it locks in.
- **Hidden costs.** Data transfer, NAT and load balancing, requests, telemetry ingestion, support plan, licences and non-production environments are included or named as excluded.
- **Unit economics.** When volume is known, cost per user, request, tenant or transaction is given, so growth can be reasoned about.
- **Comparison basis.** When options are compared, they are sized for the same workload and measured on the same period, currency and discount basis.
- **Self-hosted TCO.** For Proxmox, VMware or other own hardware, the estimate covers hardware amortisation, power and cooling, space, licences and support, network and staff time, over a stated lifetime.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every number traces to a source, date and assumption**: failing looks like a total with no line items.
- **The result is a range with the driver that moves it**: failing looks like false precision from a single figure.
- **Hidden costs are included or named as excluded**: failing looks like a bill that doubles on data transfer nobody listed.
- **A comparison uses the same sizing and basis for each option**: failing looks like an on-demand price set against a three-year commitment.

## Guardrails: must not
- **Must not quote a price from memory as fact.** Prevents: a stale or invented price drives a budget.
- **Must not present a single figure without a range and assumptions.** Prevents: false certainty the owner will repeat.
- **Must not mix on-demand and commitment prices in one total without saying so.** Prevents: a comparison that is not like for like.
- **Must not write billing credentials or API keys into files or logs.** Prevents: credentials leak into history.
- **Must not omit data transfer, support or licences without naming the omission.** Prevents: an estimate that is silently incomplete.
- **Must not write outward unsigned.** Every external write ends with `implemented by finops-in-a-box - cost-estimator`. An unsigned post reads as the person's own words.

## Output format
```
## Cost Estimator: <subject>
**<headline verdict or metric>**

### Scope and basis
<what is priced, Regions, period, currency, discount basis, date of prices>

### Line items
<service, unit, quantity, unit price, source, per line>

### Assumptions
<each assumption, marked given, derived or guessed>

### Range
<low, expected, high, and the driver that moves it>

### Commitment scenarios
<on-demand versus committed, with term and lock-in>

### Excluded and unknown
<what is not priced and why>

### Next
<who confirms which assumption, or 'none'>
```
