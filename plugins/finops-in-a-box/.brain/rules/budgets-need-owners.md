THE RULE

A budget is defined with scope, amount, period, an actual and a forecast threshold, recipients, and the response expected at each threshold. Every budget and every alert has a named owner who has a first action.

- Alert on forecast as well as actual, so there is time to act.
- Notify a person or a monitored channel, not an unwatched list.
- Automated actions that stop or delete resources are a decision with a gate, never a default, and are kept to non-production scope unless a human approved otherwise.
- Budgets are defined as code so they are reviewed and reproducible.

WHY

A budget that alerts nobody, or alerts too late, only records the overspend. A budget that silently kills production trades a bill for an outage.

HOW TO APPLY

Write the budget as a definition `infra-engineer` can apply. For each threshold write who is told and what they do. Review the thresholds when scope, traffic or commitments change.

EXCEPTIONS

Sandbox and training accounts may use a hard automated stop, recorded as such.

JUDGED AGAINST

Every budget control names an owner, a forecast threshold and a response.

RELATED

finops tag-before-you-spend; observability alerting-and-slos
