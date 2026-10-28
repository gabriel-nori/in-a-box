# Skill dependencies

Mirror of every `Depends on` section (CONVENTIONS section 3). `scripts/check-contracts.py` fails when a skill and this table disagree. The orchestrator reads these edges to validate and order flows.

| Skill | Edge | Target | Artifact |
|---|---|---|---|
| `product-owner` | optional-enriching | `business-analyst` | `business-case` |
| `product-owner` | requires | `none` |  |
| `business-analyst` | optional-enriching | `marketer` | `positioning` |
| `business-analyst` | requires | `none` |  |
| `business-analyst` | optional-enriching | `estimator` | `estimate` |
| `security-reviewer` | optional-ordered | `developer` | `implementation-summary` |
| `security-reviewer` | optional-enriching | `infra-engineer` | `environment-notes` |
| `security-reviewer` | requires | `none` |  |
| `marketer` | optional-enriching | `business-analyst` | `business-case` |
| `marketer` | optional-enriching | `product-owner` | `refined-requirement` |
| `marketer` | requires | `none` |  |
| `legal-counsel` | optional-enriching | `security-reviewer` | `threat-notes` |
| `legal-counsel` | requires | `none` |  |
| `support-agent` | optional-enriching | `developer` | `implementation-summary` |
| `support-agent` | optional-enriching | `infra-engineer` | `environment-notes` |
| `support-agent` | requires | `none` |  |
| `developer` | requires | `tech-lead` | `interface-contracts` |
| `developer` | optional-enriching | `spec-analyst` | `technical-spec` |
| `developer` | optional-enriching | `security-reviewer` | `threat-notes` |
| `developer` | optional-enriching | `infra-engineer` | `environment-notes` |
| `developer-python` | requires | `tech-lead` | `interface-contracts` |
| `developer-python` | optional-enriching | `spec-analyst` | `technical-spec` |
| `developer-python` | optional-enriching | `security-reviewer` | `threat-notes` |
| `developer-python` | optional-enriching | `infra-engineer` | `environment-notes` |
| `developer-java` | requires | `tech-lead` | `interface-contracts` |
| `developer-java` | optional-enriching | `spec-analyst` | `technical-spec` |
| `developer-java` | optional-enriching | `security-reviewer` | `threat-notes` |
| `developer-java` | optional-enriching | `infra-engineer` | `environment-notes` |
| `developer-android` | requires | `tech-lead` | `interface-contracts` |
| `developer-android` | optional-enriching | `spec-analyst` | `technical-spec` |
| `developer-android` | optional-enriching | `security-reviewer` | `threat-notes` |
| `developer-android` | optional-enriching | `infra-engineer` | `environment-notes` |
| `developer-react` | requires | `tech-lead` | `interface-contracts` |
| `developer-react` | optional-enriching | `spec-analyst` | `technical-spec` |
| `developer-react` | optional-enriching | `security-reviewer` | `threat-notes` |
| `developer-react` | optional-enriching | `infra-engineer` | `environment-notes` |
| `spec-analyst` | requires | `product-owner` | `refined-requirement` |
| `spec-analyst` | optional-enriching | `security-reviewer` | `threat-notes` |
| `spec-analyst` | optional-enriching | `infra-engineer` | `environment-notes` |
| `tech-lead` | requires | `spec-analyst` | `technical-spec` |
| `tech-lead` | optional-enriching | `acceptance-reviewer` | `acceptance-decision` |
| `acceptance-reviewer` | requires | `product-owner` | `refined-requirement` |
| `acceptance-reviewer` | requires | `qa-tester` | `qa-report` |
| `qa-tester` | requires | `developer` | `implementation-summary` |
| `qa-tester` | requires | `spec-analyst` | `test-plan` |
| `documenter` | requires | `acceptance-reviewer` | `acceptance-decision` |
| `documenter` | optional-enriching | `product-owner` | `refined-requirement` |
| `documenter` | optional-enriching | `spec-analyst` | `technical-spec` |
| `documenter` | optional-enriching | `tech-lead` | `interface-contracts` |
| `documenter` | optional-enriching | `developer` | `implementation-summary` |
| `documenter` | optional-enriching | `qa-tester` | `qa-report` |
| `changelog-keeper` | requires | `acceptance-reviewer` | `acceptance-decision` |
| `changelog-keeper` | optional-enriching | `documenter` | `documentation` |
| `changelog-keeper` | optional-enriching | `developer` | `implementation-summary` |
| `model-router` | requires | `none` |  |
| `infra-engineer` | requires | `none` |  |
| `infra-engineer` | optional-enriching | `developer` | `implementation-summary` |
| `infra-engineer` | optional-enriching | `security-reviewer` | `threat-notes` |
| `infra-engineer` | optional-enriching | `changelog-keeper` | `changelog` |
| `infra-terraform` | requires | `none` |  |
| `infra-terraform` | optional-enriching | `developer` | `implementation-summary` |
| `infra-terraform` | optional-enriching | `security-reviewer` | `threat-notes` |
| `infra-terraform` | optional-enriching | `changelog-keeper` | `changelog` |
| `infra-terraform` | optional-enriching | `observability-engineer` | `observability-plan` |
| `infra-pulumi` | requires | `none` |  |
| `infra-pulumi` | optional-enriching | `developer` | `implementation-summary` |
| `infra-pulumi` | optional-enriching | `security-reviewer` | `threat-notes` |
| `infra-pulumi` | optional-enriching | `changelog-keeper` | `changelog` |
| `infra-pulumi` | optional-enriching | `observability-engineer` | `observability-plan` |
| `infra-cloudformation` | requires | `none` |  |
| `infra-cloudformation` | optional-enriching | `developer` | `implementation-summary` |
| `infra-cloudformation` | optional-enriching | `security-reviewer` | `threat-notes` |
| `infra-cloudformation` | optional-enriching | `changelog-keeper` | `changelog` |
| `infra-cloudformation` | optional-enriching | `observability-engineer` | `observability-plan` |
| `infra-puppet` | requires | `none` |  |
| `infra-puppet` | optional-enriching | `developer` | `implementation-summary` |
| `infra-puppet` | optional-enriching | `security-reviewer` | `threat-notes` |
| `infra-puppet` | optional-enriching | `changelog-keeper` | `changelog` |
| `infra-puppet` | optional-enriching | `observability-engineer` | `observability-plan` |
| `observability-engineer` | requires | `none` |  |
| `observability-engineer` | optional-enriching | `developer` | `implementation-summary` |
| `observability-engineer` | optional-enriching | `infra-engineer` | `environment-notes` |
| `observability-engineer` | optional-enriching | `security-reviewer` | `threat-notes` |
| `observability-reader` | requires | `none` |  |
| `observability-reader` | optional-enriching | `observability-engineer` | `observability-plan` |
| `observability-reader` | optional-enriching | `infra-engineer` | `environment-notes` |
| `observability-reader` | optional-enriching | `changelog-keeper` | `changelog` |
| `infra-ansible` | requires | `none` |  |
| `infra-ansible` | optional-enriching | `developer` | `implementation-summary` |
| `infra-ansible` | optional-enriching | `security-reviewer` | `threat-notes` |
| `infra-ansible` | optional-enriching | `changelog-keeper` | `changelog` |
| `infra-ansible` | optional-enriching | `observability-engineer` | `observability-plan` |
| `infra-ansible` | optional-enriching | `solution-architect` | `architecture-design` |
| `infra-ansible` | optional-enriching | `budget-planner` | `budget-plan` |
| `infra-cloudformation` | optional-enriching | `solution-architect` | `architecture-design` |
| `infra-cloudformation` | optional-enriching | `budget-planner` | `budget-plan` |
| `infra-engineer` | optional-enriching | `solution-architect` | `architecture-design` |
| `infra-engineer` | optional-enriching | `budget-planner` | `budget-plan` |
| `infra-pulumi` | optional-enriching | `solution-architect` | `architecture-design` |
| `infra-pulumi` | optional-enriching | `budget-planner` | `budget-plan` |
| `infra-puppet` | optional-enriching | `solution-architect` | `architecture-design` |
| `infra-puppet` | optional-enriching | `budget-planner` | `budget-plan` |
| `infra-terraform` | optional-enriching | `solution-architect` | `architecture-design` |
| `infra-terraform` | optional-enriching | `budget-planner` | `budget-plan` |
| `business-analyst` | optional-enriching | `cost-estimator` | `cost-estimate` |
| `solution-architect` | requires | `none` |  |
| `solution-architect` | optional-enriching | `product-owner` | `refined-requirement` |
| `solution-architect` | optional-enriching | `spec-analyst` | `technical-spec` |
| `solution-architect` | optional-enriching | `security-reviewer` | `threat-notes` |
| `solution-architect` | optional-enriching | `business-analyst` | `business-case` |
| `solution-architect` | optional-enriching | `infra-engineer` | `environment-notes` |
| `architect-aws` | requires | `none` |  |
| `architect-aws` | optional-enriching | `product-owner` | `refined-requirement` |
| `architect-aws` | optional-enriching | `spec-analyst` | `technical-spec` |
| `architect-aws` | optional-enriching | `security-reviewer` | `threat-notes` |
| `architect-aws` | optional-enriching | `business-analyst` | `business-case` |
| `architect-aws` | optional-enriching | `infra-engineer` | `environment-notes` |
| `architect-gcp` | requires | `none` |  |
| `architect-gcp` | optional-enriching | `product-owner` | `refined-requirement` |
| `architect-gcp` | optional-enriching | `spec-analyst` | `technical-spec` |
| `architect-gcp` | optional-enriching | `security-reviewer` | `threat-notes` |
| `architect-gcp` | optional-enriching | `business-analyst` | `business-case` |
| `architect-gcp` | optional-enriching | `infra-engineer` | `environment-notes` |
| `architect-azure` | requires | `none` |  |
| `architect-azure` | optional-enriching | `product-owner` | `refined-requirement` |
| `architect-azure` | optional-enriching | `spec-analyst` | `technical-spec` |
| `architect-azure` | optional-enriching | `security-reviewer` | `threat-notes` |
| `architect-azure` | optional-enriching | `business-analyst` | `business-case` |
| `architect-azure` | optional-enriching | `infra-engineer` | `environment-notes` |
| `architect-proxmox` | requires | `none` |  |
| `architect-proxmox` | optional-enriching | `product-owner` | `refined-requirement` |
| `architect-proxmox` | optional-enriching | `spec-analyst` | `technical-spec` |
| `architect-proxmox` | optional-enriching | `security-reviewer` | `threat-notes` |
| `architect-proxmox` | optional-enriching | `business-analyst` | `business-case` |
| `architect-proxmox` | optional-enriching | `infra-engineer` | `environment-notes` |
| `architect-vmware` | requires | `none` |  |
| `architect-vmware` | optional-enriching | `product-owner` | `refined-requirement` |
| `architect-vmware` | optional-enriching | `spec-analyst` | `technical-spec` |
| `architect-vmware` | optional-enriching | `security-reviewer` | `threat-notes` |
| `architect-vmware` | optional-enriching | `business-analyst` | `business-case` |
| `architect-vmware` | optional-enriching | `infra-engineer` | `environment-notes` |
| `cost-estimator` | requires | `none` |  |
| `cost-estimator` | optional-enriching | `solution-architect` | `architecture-design` |
| `cost-estimator` | optional-enriching | `spec-analyst` | `technical-spec` |
| `cost-estimator` | optional-enriching | `infra-engineer` | `environment-notes` |
| `cost-estimator` | optional-enriching | `observability-engineer` | `observability-plan` |
| `budget-planner` | requires | `none` |  |
| `budget-planner` | optional-enriching | `cost-estimator` | `cost-estimate` |
| `budget-planner` | optional-enriching | `business-analyst` | `business-case` |
| `budget-planner` | optional-enriching | `solution-architect` | `architecture-design` |
| `budget-planner` | optional-enriching | `tech-lead` | `work-plan` |
| `cost-monitor` | requires | `none` |  |
| `cost-monitor` | optional-enriching | `cost-estimator` | `cost-estimate` |
| `cost-monitor` | optional-enriching | `budget-planner` | `budget-plan` |
| `cost-monitor` | optional-enriching | `infra-engineer` | `environment-notes` |
| `cost-monitor` | optional-enriching | `changelog-keeper` | `changelog` |
| `infra-ansible` | optional-enriching | `dr-planner` | `dr-plan` |
| `infra-cloudformation` | optional-enriching | `dr-planner` | `dr-plan` |
| `infra-engineer` | optional-enriching | `dr-planner` | `dr-plan` |
| `infra-pulumi` | optional-enriching | `dr-planner` | `dr-plan` |
| `infra-puppet` | optional-enriching | `dr-planner` | `dr-plan` |
| `infra-terraform` | optional-enriching | `dr-planner` | `dr-plan` |
| `dr-planner` | requires | `none` |  |
| `dr-planner` | optional-enriching | `solution-architect` | `architecture-design` |
| `dr-planner` | optional-enriching | `infra-engineer` | `environment-notes` |
| `dr-planner` | optional-enriching | `security-reviewer` | `threat-notes` |
| `dr-planner` | optional-enriching | `observability-engineer` | `observability-plan` |
| `dr-planner` | optional-enriching | `business-analyst` | `business-case` |
| `dr-planner` | optional-enriching | `cost-estimator` | `cost-estimate` |
| `continuity-standards` | requires | `none` |  |
| `continuity-standards` | optional-enriching | `dr-planner` | `dr-plan` |
| `continuity-standards` | optional-enriching | `dr-tester` | `dr-test-report` |
| `continuity-standards` | optional-enriching | `legal-counsel` | `legal-notes` |
| `continuity-standards` | optional-enriching | `security-reviewer` | `threat-notes` |
| `dr-tester` | requires | `none` |  |
| `dr-tester` | optional-enriching | `dr-planner` | `dr-plan` |
| `dr-tester` | optional-enriching | `infra-engineer` | `environment-notes` |
| `dr-tester` | optional-enriching | `observability-reader` | `observability-findings` |
| `policy-author` | requires | `none` |  |
| `policy-author` | optional-enriching | `legal-counsel` | `legal-notes` |
| `policy-author` | optional-enriching | `security-reviewer` | `threat-notes` |
| `policy-author` | optional-enriching | `risk-register` | `risk-register` |
| `policy-author` | optional-enriching | `controls-auditor` | `control-findings` |
| `policy-author` | optional-enriching | `decision-steward` | `decision-log` |
| `risk-register` | requires | `none` |  |
| `risk-register` | optional-enriching | `security-reviewer` | `threat-notes` |
| `risk-register` | optional-enriching | `business-analyst` | `business-case` |
| `risk-register` | optional-enriching | `dr-planner` | `dr-plan` |
| `risk-register` | optional-enriching | `legal-counsel` | `legal-notes` |
| `risk-register` | optional-enriching | `policy-author` | `policy-set` |
| `risk-register` | optional-enriching | `controls-auditor` | `control-findings` |
| `controls-auditor` | requires | `none` |  |
| `controls-auditor` | optional-enriching | `policy-author` | `policy-set` |
| `controls-auditor` | optional-enriching | `risk-register` | `risk-register` |
| `controls-auditor` | optional-enriching | `continuity-standards` | `continuity-compliance` |
| `controls-auditor` | optional-enriching | `legal-counsel` | `legal-notes` |
| `controls-auditor` | optional-enriching | `security-reviewer` | `threat-notes` |
| `controls-auditor` | optional-enriching | `infra-engineer` | `environment-notes` |
| `controls-auditor` | optional-enriching | `decision-steward` | `decision-log` |
| `decision-steward` | requires | `none` |  |
| `decision-steward` | optional-enriching | `policy-author` | `policy-set` |
| `decision-steward` | optional-enriching | `risk-register` | `risk-register` |
| `decision-steward` | optional-enriching | `solution-architect` | `architecture-design` |
| `decision-steward` | optional-enriching | `controls-auditor` | `control-findings` |
| `agile-facilitator` | requires | `none` |  |
| `agile-facilitator` | optional-enriching | `backlog-prioritizer` | `prioritized-backlog` |
| `agile-facilitator` | optional-enriching | `agile-metrics` | `agile-charts` |
| `agile-facilitator` | optional-enriching | `working-agreements` | `working-agreements` |
| `agile-metrics` | requires | `none` |  |
| `agile-metrics` | optional-enriching | `estimator` | `estimate` |
| `backlog-prioritizer` | requires | `none` |  |
| `backlog-prioritizer` | optional-enriching | `product-owner` | `refined-requirement` |
| `backlog-prioritizer` | optional-enriching | `business-analyst` | `business-case` |
| `backlog-prioritizer` | optional-enriching | `estimator` | `estimate` |
| `backlog-prioritizer` | optional-enriching | `issue-writer` | `ready-issue` |
| `estimator` | requires | `none` |  |
| `estimator` | optional-enriching | `issue-writer` | `ready-issue` |
| `estimator` | optional-enriching | `agile-metrics` | `agile-charts` |
| `estimator` | optional-enriching | `working-agreements` | `working-agreements` |
| `facilitate-daily` | requires | `none` |  |
| `facilitate-daily` | optional-enriching | `backlog-prioritizer` | `prioritized-backlog` |
| `facilitate-daily` | optional-enriching | `agile-metrics` | `agile-charts` |
| `facilitate-daily` | optional-enriching | `working-agreements` | `working-agreements` |
| `facilitate-planning` | requires | `none` |  |
| `facilitate-planning` | optional-enriching | `backlog-prioritizer` | `prioritized-backlog` |
| `facilitate-planning` | optional-enriching | `agile-metrics` | `agile-charts` |
| `facilitate-planning` | optional-enriching | `working-agreements` | `working-agreements` |
| `facilitate-refinement` | requires | `none` |  |
| `facilitate-refinement` | optional-enriching | `backlog-prioritizer` | `prioritized-backlog` |
| `facilitate-refinement` | optional-enriching | `agile-metrics` | `agile-charts` |
| `facilitate-refinement` | optional-enriching | `working-agreements` | `working-agreements` |
| `facilitate-retro` | requires | `none` |  |
| `facilitate-retro` | optional-enriching | `backlog-prioritizer` | `prioritized-backlog` |
| `facilitate-retro` | optional-enriching | `agile-metrics` | `agile-charts` |
| `facilitate-retro` | optional-enriching | `working-agreements` | `working-agreements` |
| `issue-writer` | requires | `none` |  |
| `issue-writer` | optional-enriching | `product-owner` | `refined-requirement` |
| `issue-writer` | optional-enriching | `working-agreements` | `working-agreements` |
| `issue-writer` | optional-enriching | `estimator` | `estimate` |
| `working-agreements` | requires | `none` |  |
| `working-agreements` | optional-enriching | `developer` | `implementation-summary` |
| `working-agreements` | optional-enriching | `qa-tester` | `qa-report` |
| `developer-sql` | requires | `tech-lead` | `interface-contracts` |
| `developer-sql` | optional-enriching | `spec-analyst` | `technical-spec` |
| `developer-sql` | optional-enriching | `security-reviewer` | `threat-notes` |
| `developer-sql` | optional-enriching | `infra-engineer` | `environment-notes` |
| `developer` | optional-enriching | `dba` | `query-review` |
| `developer-python` | optional-enriching | `dba` | `query-review` |
| `developer-java` | optional-enriching | `dba` | `query-review` |
| `developer-android` | optional-enriching | `dba` | `query-review` |
| `developer-react` | optional-enriching | `dba` | `query-review` |
| `developer-sql` | optional-enriching | `dba` | `query-review` |
| `dba` | requires | `none` |  |
| `dba` | optional-enriching | `developer` | `implementation-summary` |
| `dba` | optional-enriching | `observability-reader` | `observability-findings` |
| `dba` | optional-enriching | `infra-engineer` | `environment-notes` |
| `dba-postgres` | requires | `none` |  |
| `dba-postgres` | optional-enriching | `developer` | `implementation-summary` |
| `dba-postgres` | optional-enriching | `observability-reader` | `observability-findings` |
| `dba-postgres` | optional-enriching | `infra-engineer` | `environment-notes` |
| `dba-mysql` | requires | `none` |  |
| `dba-mysql` | optional-enriching | `developer` | `implementation-summary` |
| `dba-mysql` | optional-enriching | `observability-reader` | `observability-findings` |
| `dba-mysql` | optional-enriching | `infra-engineer` | `environment-notes` |
| `dba-sqlserver` | requires | `none` |  |
| `dba-sqlserver` | optional-enriching | `developer` | `implementation-summary` |
| `dba-sqlserver` | optional-enriching | `observability-reader` | `observability-findings` |
| `dba-sqlserver` | optional-enriching | `infra-engineer` | `environment-notes` |
| `code-reviewer` | requires | `none` |  |
| `code-reviewer` | optional-ordered | `developer` | `implementation-summary` |
| `code-reviewer` | optional-enriching | `tech-lead` | `interface-contracts` |
| `code-reviewer` | optional-enriching | `security-reviewer` | `threat-notes` |
| `code-reviewer` | optional-enriching | `dba` | `query-review` |
| `incident-commander` | requires | `none` |  |
| `incident-commander` | optional-enriching | `observability-reader` | `observability-findings` |
| `incident-commander` | optional-enriching | `observability-engineer` | `observability-plan` |
| `incident-commander` | optional-enriching | `infra-engineer` | `environment-notes` |
| `incident-commander` | optional-enriching | `dr-planner` | `dr-plan` |
| `postmortem-author` | requires | `none` |  |
| `postmortem-author` | optional-ordered | `incident-commander` | `incident-record` |
| `postmortem-author` | optional-enriching | `observability-reader` | `observability-findings` |
| `postmortem-author` | optional-enriching | `observability-engineer` | `observability-plan` |
| `release-manager` | requires | `none` |  |
| `release-manager` | optional-ordered | `qa-tester` | `qa-report` |
| `release-manager` | optional-ordered | `acceptance-reviewer` | `acceptance-decision` |
| `release-manager` | optional-enriching | `changelog-keeper` | `changelog` |
| `release-manager` | optional-enriching | `infra-engineer` | `environment-notes` |
| `release-manager` | optional-enriching | `observability-engineer` | `observability-plan` |
| `code-reviewer-python` | requires | `none` |  |
| `code-reviewer-python` | optional-ordered | `code-reviewer-sql` | `review-report` |
| `code-reviewer-python` | optional-enriching | `security-reviewer` | `threat-notes` |
| `code-reviewer-java` | requires | `none` |  |
| `code-reviewer-java` | optional-ordered | `code-reviewer-sql` | `review-report` |
| `code-reviewer-java` | optional-enriching | `security-reviewer` | `threat-notes` |
| `code-reviewer-android` | requires | `none` |  |
| `code-reviewer-android` | optional-ordered | `code-reviewer-sql` | `review-report` |
| `code-reviewer-android` | optional-enriching | `security-reviewer` | `threat-notes` |
| `code-reviewer-android` | optional-enriching | `threat-modeler` | `threat-model` |
| `code-reviewer-react` | requires | `none` |  |
| `code-reviewer-react` | optional-ordered | `code-reviewer-sql` | `review-report` |
| `code-reviewer-react` | optional-enriching | `security-reviewer` | `threat-notes` |
| `code-reviewer-sql` | requires | `none` |  |
| `code-reviewer-sql` | optional-ordered | `dba` | `query-review` |
| `code-reviewer-sql` | optional-enriching | `security-reviewer` | `threat-notes` |
| `code-reviewer-iac` | requires | `none` |  |
| `code-reviewer-iac` | optional-enriching | `security-reviewer` | `threat-notes` |
| `code-reviewer-iac` | optional-enriching | `threat-modeler` | `threat-model` |
| `postmortem-defect` | requires | `none` |  |
| `postmortem-defect` | optional-enriching | `code-reviewer` | `review-report` |
| `postmortem-defect` | optional-enriching | `qa-tester` | `qa-report` |
| `postmortem-security` | requires | `none` |  |
| `postmortem-security` | optional-enriching | `security-reviewer` | `threat-notes` |
| `postmortem-security` | optional-enriching | `threat-modeler` | `threat-model` |
| `postmortem-security` | optional-enriching | `legal-counsel` | `legal-notes` |
| `threat-modeler` | requires | `none` |  |
| `threat-modeler` | optional-enriching | `solution-architect` | `architecture-design` |
| `threat-modeler` | optional-enriching | `infra-engineer` | `environment-notes` |
| `threat-modeler` | optional-enriching | `legal-counsel` | `legal-notes` |
| `security-reviewer` | optional-enriching | `threat-modeler` | `threat-model` |
| `spec-analyst` | optional-enriching | `process-modeler` | `process-model` |
| `marketer` | optional-enriching | `swot-analyst` | `swot` |
| `marketer` | optional-enriching | `canvas-designer` | `business-model-canvas` |
| `marketer` | optional-enriching | `communicator` | `communication-guide` |
| `communicator` | requires | `none` |  |
| `communicator` | optional-enriching | `marketer` | `positioning` |
| `communicator` | optional-enriching | `support-agent` | `support-resolution` |
| `relationship-designer` | requires | `none` |  |
| `relationship-designer` | optional-enriching | `communicator` | `communication-guide` |
| `relationship-designer` | optional-enriching | `support-agent` | `support-resolution` |
| `pitcher` | requires | `none` |  |
| `pitcher` | optional-enriching | `swot-analyst` | `swot` |
| `pitcher` | optional-enriching | `canvas-designer` | `business-model-canvas` |
| `pitcher` | optional-enriching | `business-analyst` | `business-case` |
| `pitcher` | optional-enriching | `communicator` | `communication-guide` |
| `product-owner` | optional-enriching | `canvas-designer` | `business-model-canvas` |
| `product-owner` | optional-enriching | `process-modeler` | `process-model` |
| `process-modeler` | requires | `none` |  |
| `process-modeler` | optional-enriching | `business-analyst` | `business-case` |
| `process-modeler` | optional-enriching | `canvas-designer` | `business-model-canvas` |
| `business-analyst` | optional-enriching | `swot-analyst` | `swot` |
| `business-analyst` | optional-enriching | `canvas-designer` | `business-model-canvas` |
| `canvas-designer` | requires | `none` |  |
| `canvas-designer` | optional-enriching | `swot-analyst` | `swot` |
| `canvas-designer` | optional-enriching | `business-analyst` | `business-case` |
| `swot-analyst` | requires | `none` |  |
| `swot-analyst` | optional-enriching | `business-analyst` | `business-case` |
