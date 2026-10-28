# in-a-box

A set of role plugins for Claude Code, plus an orchestrator that connects them on demand.

Status: private, skeleton (v0.1.0). Not yet published.

## Idea

Instead of defining one fixed flow, `in-a-box` defines **roles**. Each role is a plugin named `<role>-in-a-box`, specialised in one job (developer, product owner, security, and so on). On top of them, `orchestrator-in-a-box` lets a user wire roles together into their own flows, so the same building blocks serve very different users: a solo founder, a startup squad, a regulated enterprise.

Roles ship as parts, and the orchestrator assembles them into flows.

## Plugins

| Plugin | Role | Skill | Produces |
|---|---|---|---|
| `dev-in-a-box` | Developer | `spec-analyst`, `tech-lead`, `developer`, `developer-python`, `developer-java`, `developer-android`, `developer-react`, `developer-sql`, `code-reviewer`, `code-reviewer-python`, `code-reviewer-java`, `code-reviewer-android`, `code-reviewer-react`, `code-reviewer-sql`, `code-reviewer-iac` | `technical-spec`, `test-plan`, `interface-contracts`, `work-plan`, `implementation-summary`, `review-report` |
| `po-in-a-box` | Product Owner | `product-owner`, `acceptance-reviewer` | `refined-requirement`, `acceptance-decision` |
| `qa-in-a-box` | QA | `qa-tester` | `qa-report` |
| `docs-in-a-box` | Documentation | `documenter`, `changelog-keeper` | `documentation`, `changelog` |
| `model-router-in-a-box` | Model router | `model-router` | `model-assignment` |
| `business-in-a-box` | Business Analyst | `business-analyst` | `business-case` |
| `security-in-a-box` | Security Reviewer, Threat Modeler | `security-reviewer`, `threat-modeler` | `threat-notes`, `threat-model` |
| `marketing-in-a-box` | Marketer | `marketer` | `positioning` |
| `lawyer-in-a-box` | Legal Counsel | `legal-counsel` | `legal-notes` |
| `support-in-a-box` | Support Agent | `support-agent` | `support-resolution` |
| `infra-in-a-box` | Infra Engineer | `infra-engineer`, `infra-terraform`, `infra-pulumi`, `infra-cloudformation`, `infra-puppet`, `infra-ansible` | `environment-notes` |
| `observability-in-a-box` | Observability Engineer, Reader | `observability-engineer`, `observability-reader`, `incident-commander` | `observability-plan`, `observability-findings`, `incident-record` |
| `postmortem-in-a-box` | Postmortem Author (outage, defect, vulnerability, attack) | `postmortem-author`, `postmortem-defect`, `postmortem-security` | `postmortem` |
| `architect-in-a-box` | Solution Architect | `solution-architect`, `architect-aws`, `architect-gcp`, `architect-azure`, `architect-proxmox`, `architect-vmware` | `architecture-design` |
| `finops-in-a-box` | FinOps | `cost-estimator`, `budget-planner`, `cost-monitor` | `cost-estimate`, `budget-plan`, `cost-findings` |
| `disaster-recovery-in-a-box` | Disaster Recovery | `dr-planner`, `continuity-standards`, `dr-tester` | `dr-plan`, `continuity-compliance`, `dr-test-report` |
| `governance-in-a-box` | Governance | `policy-author`, `risk-register`, `controls-auditor`, `decision-steward` | `policy-set`, `risk-register`, `control-findings`, `decision-log` |
| `release-in-a-box` | Release Manager | `release-manager` | `release-plan` |
| `dba-in-a-box` | Database Administrator | `dba`, `dba-postgres`, `dba-mysql`, `dba-sqlserver` | `query-review` |
| `research-in-a-box` | Source Researcher | `source-researcher` | `research-findings` |
| `curator-in-a-box` | Skill Integrator | `skill-integrator` | `integration-report` |
| `orchestrator-in-a-box` | Flow composer and runner | `compose-flow`, `run-flow`, `process-to-command` | flows, run records |

## Processes, not commands

The plugins are designed to be used with the brain. A process exists only where the source fixes an order of steps (`plugins/<plugin>/processes/`); everywhere else a skill states the result it owes and its dependency edges decide what runs first, and standards worth recalling live as brain rules (`.brain/rules/`). Both cite the sources in [docs/research-sources.md](docs/research-sources.md), and the brain recalls them by situation. `process-to-command` turns a process into a slash command for anyone who works without the brain. See CONVENTIONS section 10.

## Layout

```
.claude-plugin/marketplace.json   marketplace listing every plugin
plugins/<role>-in-a-box/          one plugin per role
plugins/orchestrator-in-a-box/    flow composition and execution
docs/                             architecture, dependency graph
templates/                        skill contract and plugin templates
scripts/                          new-plugin.py, check-contracts.py
CONVENTIONS.md                    the rules every skill follows
```

## Core principle: skills are contracts

Every skill declares what must be true when it finishes and which constraints it may not break. It never lists the steps. See [CONVENTIONS.md](CONVENTIONS.md) and [templates/skill-contract.md](templates/skill-contract.md).

## Working on it

```
python3 scripts/check-contracts.py            # validate every skill against the contract shape
python3 scripts/new-plugin.py <role> <skill>  # scaffold a new role plugin
```

Try it locally:

```
claude plugin marketplace add ./
claude plugin install dev-in-a-box@in-a-box
```

See [docs/architecture.md](docs/architecture.md) for how roles, artifacts and flows fit together.
