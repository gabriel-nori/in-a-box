# orchestrator-in-a-box

Connects the `<role>-in-a-box` plugins into flows the user defines.

Skills:

- [`compose-flow`](skills/compose-flow/SKILL.md): turns a user's goal into a valid flow definition from the installed roles.
- [`run-flow`](skills/run-flow/SKILL.md): executes a flow, passing artifacts between roles and pausing at gates.
- [`process-to-command`](skills/process-to-command/SKILL.md): turns a process (`plugins/*/processes/*.md`) into a slash command for hosts and people without the brain.

Example flows: [`examples/idea-to-release.yaml`](examples/idea-to-release.yaml), and [`examples/spec-to-ship.yaml`](examples/spec-to-ship.yaml) (spec, tech lead routing, parallel developers, QA, acceptance loop, docs, changelog, ship).
