THE RULE

Quotas, limits, region and zone availability, feature support, prices, support and end-of-life dates, and licence terms are verified against the provider's current documentation or pricing source, and the answer carries the source and the date checked.

- When a fact cannot be checked in the session, mark it as unverified and name where to confirm it.
- A fact that decides the design (a quota, a feature, a licence term) is an open decision until verified.
- Licence and support terms for self-hosted platforms are treated the same way and are the most likely to have changed.

WHY

Providers change features, quotas, prices and terms constantly, and model memory lags. A stale fact that becomes a design constraint is expensive and hard to see afterwards.

HOW TO APPLY

Use the provider's own documentation, pricing pages or API. Record the source and date beside the fact in the artifact. Re-check anything older than the decision it supports.

EXCEPTIONS

Stable, structural facts (what an availability zone is) need no citation.

JUDGED AGAINST

Every provider-specific number or capability in the artifact has a source and a date, or is marked unverified.

RELATED

finops estimate-with-sources; architect-decide-with-records
