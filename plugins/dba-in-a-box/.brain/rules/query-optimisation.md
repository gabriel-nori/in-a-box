THE RULE

Make a query fast enough on the data it will meet, without changing what it returns.

What must be true at the end:
- A `query-review` with evidence, the smallest change that fixes the problem, its cost, and how equivalence of results was confirmed.

How it is handled:
- Read the plan: compare estimated and actual rows; a large gap points to stale statistics and a poor plan. For repeated nodes, multiply per-loop figures by the loop count.
- `EXPLAIN ANALYZE` executes the statement, so a write is wrapped in a transaction and rolled back.
- Check indexing basics: column order against the predicates, functions or type mismatches on indexed columns, bind variables, indexes for joins, sorting and grouping.
- Every index adds write and storage cost; name it. Redundant indexes waste resources.
- A plan from a database with different volume or statistics than production is a hypothesis.

WHY

Trigger: A query is slow, is about to ship against a large table, or a developer consults the DBA.

Inputs:
- The query, the engine and version, the schema and indexes, table sizes.
- The execution plan with real row counts.

HOW TO APPLY

Participants: The developer who owns the query, the DBA, and whoever runs the database.

Expectations of the position:
- **DBA:** evidence before opinion; the smallest safe change; states the trade-off.
- **Developer:** brings the real query and data volumes, and owns the application side of the fix.

RELATED

Sources (S-031, S-033): S-031 (PostgreSQL docs, primary, read). S-033 (Use The Index, Luke, primary, read; engine-neutral). Other engines' plan tools are named in the specialist skills, not sourced here.

Roles: dba, dba-postgres, developer-sql. Outcomes, not an order: the dependency edges between the roles' skills decide what runs first.
