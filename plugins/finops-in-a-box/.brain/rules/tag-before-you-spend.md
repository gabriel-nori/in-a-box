THE RULE

The allocation scheme is defined before resources are created: the required tags or labels, the account, project or subscription boundaries, and the owner each maps to. Resources are created with them, enforced by policy where the platform allows. Spend that cannot be attributed is reported as a finding.

- A small, mandatory set (owner, environment, workload or cost centre) beats a long optional one.
- Allocation keys are part of the infrastructure code, not applied afterwards by hand.
- Some costs cannot be tagged (support, some data transfer); they are allocated by a stated rule.

WHY

Costs that cannot be attributed cannot be owned, and tagging after the fact is partial, manual and never finished.

HOW TO APPLY

Add the mandatory keys to modules and templates, enforce them with the platform's policy mechanism, and have `cost-monitor` report the untagged share each period.

EXCEPTIONS

Shared platform resources may carry a platform owner instead of a workload owner.

JUDGED AGAINST

A reader can split the bill by owner and environment, and the unattributed share is stated.

RELATED

finops budgets-need-owners; finops read-costs-by-driver
