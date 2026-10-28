# Research sources

Every process under `plugins/*/processes/` and every rule that came from research cites sources by id from this table. `scripts/check-contracts.py` fails on a citation whose id is not here. Researched 2026-10-15.

## How to read the table

- **Kind:** `primary` is the standard, guide or official documentation itself. `secondary` is a summary, a vendor guide or a training page about the primary. Secondary sources carry less weight: a claim that rests only on one is marked in the process that uses it.
- **Read:** `page` means the page was fetched and read. `partial` means only part of the page came through (an index, an abstract). `search` means only a search-result summary was read; the page itself was not.
- A source's URL is where it was found, not a promise that the page still says the same thing.

## Registry

| ID | Source | Publisher | Kind | Read | Supports | URL |
|---|---|---|---|---|---|---|
| S-001 | The Scrum Guide (2020) | Schwaber and Sutherland, scrumguides.org | primary | page | agile roles, events, artifacts, commitments | https://scrumguides.org/scrum-guide.html |
| S-002 | The Kanban Guide | Scrum.org and Kanban University, kanbanguides.org | primary | page | Kanban practices, flow metrics | https://kanbanguides.org/english/ |
| S-003 | Hiring a Professional Product Owner (six stances) | Scrum.org | primary | search | Product Owner expectations | https://www.scrum.org/resources/blog/hiring-professional-product-owner |
| S-004 | The 6 Stances of a Scrum Master | Scrum.org | primary | search | Scrum Master expectations | https://www.scrum.org/resources/blog/6-stances-scrum-master |
| S-005 | Managing Incidents (Site Reliability Engineering, ch. 14) | Google | primary | page | incident roles, command, handoff, declaring early | https://sre.google/sre-book/managing-incidents/ |
| S-006 | Postmortem Culture (SRE, ch. 15) | Google | primary | page | blameless postmortems, triggers, review, follow-up | https://sre.google/sre-book/postmortem-culture/ |
| S-007 | Monitoring Distributed Systems (SRE, ch. 6) | Google | primary | page | golden signals, symptom-based paging | https://sre.google/sre-book/monitoring-distributed-systems/ |
| S-008 | Release Engineering (SRE, ch. 8) | Google | primary | page | release engineer role, hermetic builds, self-service releases | https://sre.google/sre-book/release-engineering/ |
| S-009 | Implementing SLOs (SRE Workbook) | Google | primary | page | SLIs, SLOs, error budgets, error budget policy | https://sre.google/workbook/implementing-slos/ |
| S-010 | SRE book table of contents | Google | primary | partial | what SREs are expected to cover | https://sre.google/sre-book/table-of-contents/ |
| S-011 | Code Review: the standard of code review | Google engineering practices | primary | page | reviewer duties, approval bar, conflict handling | https://google.github.io/eng-practices/review/reviewer/standard.html |
| S-012 | Code Review: the CL author's guide | Google engineering practices | primary | partial | author duties (index only) | https://google.github.io/eng-practices/review/developer/ |
| S-013 | Semantic Versioning 2.0.0 | semver.org | primary | page | version numbers, deprecation | https://semver.org/ |
| S-014 | Keep a Changelog 1.1.0 | keepachangelog.com | primary | page | changelog principles, change types | https://keepachangelog.com/en/1.1.0/ |
| S-015 | Diátaxis | Daniele Procida, diataxis.fr | primary | partial | four kinds of documentation (the per-kind detail did not come through) | https://diataxis.fr/ |
| S-016 | DORA capabilities | Google Cloud DORA | primary | page | delivery capabilities (the metric definitions did not come through) | https://dora.dev/capabilities/ |
| S-017 | AWS Well-Architected: the pillars | AWS | primary | partial | six pillars (list only) | https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html |
| S-018 | Azure Well-Architected Framework | Microsoft | primary | page | five pillars, review tools | https://learn.microsoft.com/en-us/azure/well-architected/ |
| S-019 | Google Cloud Well-Architected Framework | Google Cloud | primary | page | six pillars | https://docs.cloud.google.com/architecture/framework |
| S-020 | The C4 model | Simon Brown, c4model.com | primary | partial | diagram levels (usage guidance did not come through) | https://c4model.com/ |
| S-021 | Architectural Decision Records | adr.github.io | primary | page | what an ADR is | https://adr.github.io/ |
| S-022 | Disaster recovery options in the cloud (whitepaper) | AWS | primary | page | four DR strategies, testing, failover | https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html |
| S-023 | NIST SP 800-34 Rev. 1, Contingency Planning Guide | NIST | primary | partial | publication record only; the seven steps come from S-024 | https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final |
| S-024 | NIST 800-34: 7 steps to contingency planning | securityscientist.net | secondary | search | the seven-step contingency process, BIA outputs | https://securityscientist.net/blog/nist-contingency-planning-guide |
| S-025 | ISO 22301 exercising and testing programme | Glocert International | secondary | search | exercise requirements and types | https://www.glocertinternational.com/resources/guides/iso-22301-exercising-and-testing-program/ |
| S-026 | Secure Software Development Framework | NIST | primary | page | four practice groups | https://csrc.nist.gov/projects/ssdf |
| S-027 | OWASP Top Ten 2025 | OWASP | primary | page | ten risk categories | https://top10.owasp.org/2025 |
| S-028 | NIST Cybersecurity Framework 2.0 | NIST | primary | partial | hub page only; the six functions were not read | https://www.nist.gov/cyberframework |
| S-029 | FinOps Framework personas | FinOps Foundation | primary | search | personas and their goals | https://www.finops.org/framework/persona/finops-practitioner/ |
| S-030 | Observability primer | OpenTelemetry | primary | page | signals, instrumentation, SLI and SLO definitions | https://opentelemetry.io/docs/concepts/observability-primer/ |
| S-031 | Using EXPLAIN | PostgreSQL documentation | primary | page | reading plans, EXPLAIN ANALYZE runs the statement | https://www.postgresql.org/docs/current/using-explain.html |
| S-032 | CREATE INDEX | PostgreSQL documentation | primary | page | locks, CONCURRENTLY and its caveats | https://www.postgresql.org/docs/current/sql-createindex.html |
| S-033 | Use The Index, Luke | Markus Winand | primary | page | indexing for developers, across five engines | https://use-the-index-luke.com/ |
| S-034 | ISTQB-compliant testing process | infinity-group.pl | secondary | search | test process activities and work products | https://www.infinity-group.pl/blog/?p=3872 |
| S-035 | INVEST in good stories | innolution.com, after Bill Wake (2003) | secondary | search | story readiness criteria | https://innolution.com/resources/glossary/invest/ |
| S-036 | Requirement (ISO/IEC/IEEE 29148 characteristics) | Wikipedia | secondary | search | requirement quality characteristics; the standard itself was not read | https://en.wikipedia.org/wiki/Requirement |
| S-037 | BABOK Guide | IIBA | primary | search | six knowledge areas; the official page returned 404 to the fetcher | https://iiba.org/standards-and-resources/babok/ |
| S-038 | A guide to ITIL 4 incident and problem management | Virima | secondary | search | incident versus problem, service desk | https://www.virima.com/guide-to-itil-incident-and-problem-management/ |
| S-039 | Contract review checklist vs playbook | Bind | secondary | search | checklist and playbook split, escalation | https://bindlegal.com/resources/guides/contract-review-checklist/ |
| S-040 | Contract lifecycle management: playbooks | Association of Corporate Counsel | primary | search | playbook types and roles; the body is members-only | https://acc.com/resource-library/contract-lifecycle-management-clm-foundation-automation-contract-playbooks |
| S-041 | What does a product marketing manager do? | Pragmatic Institute | secondary | search | positioning and launch responsibilities | https://www.pragmaticinstitute.com/resources/articles/product/what-does-a-product-marketing-manager-do/ |
| S-042 | Employing COBIT 2019 for enterprise governance strategy | ISACA | primary | search | governance versus management, EDM, ISO/IEC 38500 principles | https://www.isaca.org/resources/news-and-trends/industry-news/2019/employing-cobit-2019-for-enterprise-governance-strategy |
| S-043 | Terraform recommended practices | HashiCorp | primary | partial | overview only | https://developer.hashicorp.com/terraform/cloud-docs/recommended-practices |
| S-044 | Threat Modeling Manifesto | threatmodelingmanifesto.org | primary | search | threat modeling as four questions; the site itself did not load (DNS), so wording comes through a search summary | https://threatmodelingmanifesto.org/ |
| S-045 | Threat Modeling Cheat Sheet | OWASP | primary | page | four questions, four steps (model, identify and rank, respond, review), when to model | https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html |
| S-046 | STRIDE threat model | Microsoft Learn (Threat Modeling Tool) | primary | page | the six STRIDE categories | https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats |
| S-047 | Guide to app architecture | Android Developers | primary | page | layers, single source of truth, unidirectional data flow, dependency injection | https://developer.android.com/topic/architecture |
| S-048 | Android Kotlin style guide | Android Open Source Project | primary | page | Android style rules for Kotlin | https://developer.android.com/kotlin/style-guide |
| S-049 | App security tips | Android Developers | primary | page | storage, permissions, networking, intents, input validation, credentials | https://developer.android.com/privacy-and-security/security-tips |
| S-050 | Thinking in React | react.dev | primary | page | component hierarchy, minimal state, one-way data flow | https://react.dev/learn/thinking-in-react |
| S-051 | Rules of Hooks | react.dev | primary | page | the two rules of Hooks; the purity rules on the page were not present and are not cited | https://react.dev/reference/rules/rules-of-hooks |
| S-052 | Google Java Style Guide | Google | primary | page | source layout, formatting, naming, practices, Javadoc | https://google.github.io/styleguide/javaguide.html |
| S-053 | Kotlin coding conventions | JetBrains, kotlinlang.org | primary | page | source organisation, naming, idiomatic use | https://kotlinlang.org/docs/coding-conventions.html |
| S-054 | PEP 8, style guide for Python code | Python Software Foundation | primary | page | layout, imports, naming, programming recommendations, when to deviate | https://peps.python.org/pep-0008/ |
| S-055 | Terraform style guide | HashiCorp | primary | page | naming, formatting, variables, outputs, file names, version pinning | https://developer.hashicorp.com/terraform/language/style |
| S-056 | CloudFormation best practices | AWS | primary | page | stack organisation, templates, change sets, drift, security | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html |
| S-057 | Organizing projects and stacks | Pulumi | primary | page | monolith, layered and micro-stacks; stack references | https://www.pulumi.com/docs/iac/using-pulumi/organizing-projects-stacks/ |
| S-058 | Secrets | Pulumi | primary | page | secrets in config and state | https://www.pulumi.com/docs/iac/concepts/secrets/ |
| S-059 | Projects | Pulumi | primary | page | project, stack settings, config files | https://www.pulumi.com/docs/iac/concepts/projects/ |
| S-060 | The Puppet language style guide (Puppet 7) | Puppet | primary | page | formatting, naming, resources, classes, parameters, modules | https://puppet.com/docs/puppet/7/style_guide |
| S-061 | Designing system configs: roles and profiles | Puppet | primary | search | the roles and profiles pattern; the page itself was not read | https://help.puppet.com/pe/2023.8/topics/designing_system_configs_roles_and_profiles.htm |
| S-062 | NIST SP 800-61 Rev. 3, Incident Response Recommendations | NIST | primary | partial | publication record only (April 2025, supersedes Rev. 2); the lessons-learned text was not read | https://csrc.nist.gov/pubs/sp/800/61/r3/final |
| S-063 | BPMN 2.0.2 | OMG | primary | partial | version and purpose only; the page does not describe gateways, events or flows, and the normative PDF was not read | https://www.omg.org/spec/BPMN/2.0.2/ |
| S-064 | Mermaid flowchart syntax | mermaid.js.org | primary | page | node shapes, edge labels, subgraphs, validity pitfalls | https://mermaid.js.org/syntax/flowchart.html |
| S-065 | Lei Geral de Proteção de Dados (Lei 13.709/2018) | Planalto | primary | partial | consent (arts. 5 XII, 8), legal bases (art. 7), legitimate interest (art. 10), data subject rights (art. 18); the last 25,000 characters were not read | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm |
| S-066 | The Business Model Canvas | Strategyzer | primary | page | one-page model of one business, a claim to test; the page does not list the nine blocks, which come from the skill's own text | https://www.strategyzer.com/library/the-business-model-canvas |
| S-067 | Plain language guide | digital.gov | primary | page | four groups: audience, writing, design, testing | https://digital.gov/guides/plain-language |
| S-068 | CAN-SPAM Act compliance guide for business | FTC | primary | page | eight requirements; no B2B exception | https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business |
| S-069 | SWOT analysis guides (bank and vendor pages) | various | secondary | search | internal versus external, 2x2, pairing factors, subjectivity, refresh; no single authoritative page | https://www.rbcroyalbank.com/business/pdf/Swot%20template.pdf |
| S-070 | 10/20/30 rule and the ten slides | Guy Kawasaki, through secondary pages | secondary | search | ten slides, twenty minutes, 30-point font; Kawasaki's own page returned 403 | https://astro.visible.vc/blog/guy-kawasaki-pitch-deck |

## Tried and not read

| URL | What happened | Effect |
|---|---|---|
| https://www.scrum.org/resources/what-is-a-product-owner | empty page for the fetcher | Product Owner stances rest on S-001 and the search summary S-003 |
| https://www.scrum.org/resources/what-is-a-scrum-master | empty page | Scrum Master stances rest on S-001 and S-004 |
| https://www.finops.org/framework/ | HTTP 403 | FinOps rests on persona pages seen through search (S-029) |
| https://www.iiba.org/business-analysis-body-of-knowledge/ | HTTP 404 | BABOK rests on S-037 and search summaries |
| https://owasp.org/www-project-threat-modeling/ | HTTP 404 | threat modeling rests on S-044 to S-046 instead |
| https://www.atlassian.com/incident-management/handbook | body not returned | incident process rests on S-005 only |
| https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html | HTTP 429 | Ansible norms stay as already written in `infra-ansible` |
| https://threatmodelingmanifesto.org/ | DNS failure on two tries | S-044 rests on a search summary |
| https://www.pulumi.com/docs/iac/concepts/best-practices/ | HTTP 404 | Pulumi norms rest on S-057 to S-059; community best-practice pages were seen only through search and are not cited |
| https://guykawasaki.com/the_only_10_slides_you_need_in_your_pitch/ | HTTP 403 | pitch norms rest on the secondary S-070 |
| https://www.gov.br/anpd/.../guia-orientativo-hipoteses-legais-...-legitimo-interesse.pdf | HTTP 404 | legitimate interest rests on LGPD art. 10 (S-065); ANPD guidance not read |
| Sequoia Capital's own pitch template | only SEO mirrors found, none citing Sequoia | not cited |
| https://www.puppet.com/docs/puppet/latest/style_guide.html | 301 to a landing page | the style guide was read at the Puppet 7 URL (S-060) |
| https://docs.ansible.com/ansible/latest/tips_tricks/sample_setup.html | HTTP 429 | Ansible norms stay as already written in `infra-ansible` |
| https://doi.org/10.6028/NIST.SP.800-61r3 | not fetched | the lessons-learned guidance of S-062 is not cited |

## Gaps to close

- **No primary text for:** ISTQB (S-034), ISO/IEC/IEEE 29148 (S-036), ITIL 4 (S-038), ISO 22301 (S-025) and ISO/IEC 38500 (S-042). These standards are paid or members-only. Processes built on them say so and stay conservative.
- **Roles with thin evidence:** `marketing-in-a-box` (S-041, an article), `lawyer-in-a-box` (S-039, S-040, a checklist guide and a members-only library), `support-in-a-box` (S-038).
- **Researched on 2026-10-16:** threat modeling (S-044 to S-046), Android, Java, Kotlin, React and Python style and structure (S-047 to S-054), Terraform, CloudFormation, Pulumi and Puppet (S-055 to S-061).\n- **Still not researched:** FinOps capabilities and lifecycle, cloud-provider service maps (the `architect-*` specialists keep their current text), Ansible (the page was rate-limited), TypeScript beyond React, SQL dialect style guides, and NIST SP 800-61 lessons-learned text (S-062 is metadata only).
