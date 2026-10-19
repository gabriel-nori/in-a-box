THE RULE

A significant architecture choice is recorded with the options considered (at least two real ones), the criteria, the choice, the reason, and what it would cost to reverse.

- Choices the design cannot easily undo (platform, data store, network and account layout, identity model) are always recorded.
- A choice made for a requirement names the requirement; a choice made for preference says so.
- A decision that depends on an unverified fact is marked open, with the check that would close it.

WHY

Architecture is mostly decisions that outlive the people who made them. Without the options and the reason, the next team either repeats the debate or keeps a choice nobody can defend.

HOW TO APPLY

Write the record next to the design (the `architecture-design` artifact or an ADR file the repo already uses). Keep it short: context, options, decision, consequences. Link it from the hand-off to `infra-engineer`.

EXCEPTIONS

Trivial and easily reversed choices (a naming scheme, a library version) need no record.

JUDGED AGAINST

Every irreversible choice in the design has a record that lists a rejected option and the reversal cost.

RELATED

architect-verify-provider-facts; architect-design-for-failure-and-exit
