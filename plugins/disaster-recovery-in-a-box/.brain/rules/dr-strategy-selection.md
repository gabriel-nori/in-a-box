THE RULE

Choose the cheapest recovery strategy that still meets the recovery time and recovery point targets.

What must be true at the end:
- A chosen strategy per workload with its cost, failover mechanism, and test plan.

How it is handled:
- Four strategies, from low cost and complexity to high: backup and restore, pilot light, warm standby, multi-site active/active.
- Backup and restore suits data loss and corruption, and a data-centre loss for a highly available workload; regional disasters or regulation push toward the other three.
- Pilot light has data replicated and core infrastructure provisioned with servers switched off; warm standby runs a scaled-down fully functional copy that can take traffic at once; active/active serves from all Regions.
- Use infrastructure as code so the recovery site can be redeployed without error.
- For failover prefer data-plane operations over control-plane ones. Automatic failover on health checks can trigger a needless failover on a false alarm; manual initiation of automated steps is common.
- Replication does not protect against corruption or malicious deletion: keep versioned or point-in-time backups too.
- Test regularly.

WHY

Trigger: A workload is designed or its recovery targets change.

Inputs:
- RTO and RPO per workload, the definition of disaster (a data centre, a Region, an attack or data corruption), regulatory requirements.

HOW TO APPLY

Participants: DR planner, architect, workload owner, and the person who owns the budget.

Expectations of the position:
- **DR planner:** ties each choice to RTO and RPO and states the cost of the choice.

RELATED

Sources (S-022): S-022 (AWS whitepaper, primary, read in full). It is AWS-specific; the principles carry over, service names do not.

Roles: dr-planner, solution-architect. Outcomes, not an order: the dependency edges between the roles' skills decide what runs first.
