THE RULE

A design names its failure modes, the recovery time and data-loss targets, the mechanism that meets each target, and how recovery is rehearsed. It also names the lock-in it creates and the effort to leave.

- A target with no mechanism is a gap, not a design.
- A backup counts only after a restore has been rehearsed.
- Blast-radius boundaries (accounts, projects, subscriptions, clusters, networks) are chosen so one failure or one compromised identity does not reach everything.
- Lock-in is weighed as a cost, not treated as a veto.

WHY

Availability claims fail at the unexamined single point, and migrations fail at the dependency nobody listed. Both are cheap to write down at design time and expensive to discover in an incident or a renewal.

HOW TO APPLY

For each component ask what happens when its zone, node, disk, network path or credentials are lost. Compare the answer with the stated targets. On self-hosted platforms (Proxmox, VMware) add hardware, power and the second site; on public clouds add the Region and the account boundary.

EXCEPTIONS

A short-lived prototype may accept a stated single point of failure, recorded as such with an end date.

JUDGED AGAINST

Each stated recovery target is followed by the mechanism and the rehearsal that backs it; the lock-in list is present.

RELATED

architect-decide-with-records; observability apply-signals
