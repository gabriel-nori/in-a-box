---
name: process-to-command
description: >-
  Translates a process (a `processes/<id>.md` file or a process node in the brain) into a slash command that a person can run in their agent host, faithful to the process and its gates. Use when asked to "turn this process into a command", "make a slash command for the retro", "give me a shortcut for this process", or before sharing a process with someone who does not use the brain.
allowed-tools: Read, Glob, Grep, Write
---

# Process to Command

You are accountable for a command that runs exactly one process, as written, for someone who has no brain: the process is the source of truth and the command is a generated, disposable form of it. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
When a process exists and a person wants to invoke it by name from a host that expects commands (for Claude Code, a slash command). The brain-native use of a process needs no command: the brain recalls the process by its scenario and follows it. This skill exists for hosts and people without that memory.

## Given
- **Primary:** the process to translate: its file under `plugins/<role>-in-a-box/processes/`, or its node in the brain.
- **Supporting:** the `SKILL.md` of every role the process names, so the command points at the roles instead of restating them.
- **Context, not procedure:** a process holds the purpose, trigger, participants, inputs, outcomes, handling and expectations of a position, with cited sources (CONVENTIONS section 10). A command is a prompt file the host runs on demand. For Claude Code: a Markdown file whose front matter carries `description` and optionally `argument-hint`, in the workspace's `.claude/commands/` or a plugin's `commands/` folder. The command name is the process id.
- **Context, not procedure:** inputs the process lists as required become arguments or questions the command asks once; outcomes become the artifacts the command must leave behind.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Anything personal in the brain is withheld from the command text; a command is shareable, so it carries the process and nothing about the owner.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `compose-flow` (`flow-definition`): when the process spans several roles, an existing flow it maps to; read it if present, never wait.
- **Produces:** `command-file`: the command Markdown file, ready to place in the host's command location.

## Deliverables
- **Fidelity.** The command carries every outcome, every gate and every expectation of the position that the process states, and adds no step, role or promise the process does not state.
- **Roles by reference.** Each role the process names is invoked by its skill name; the command does not copy a skill's contract into itself.
- **Arguments.** The process inputs appear as arguments or a single up-front question, each with what it is for; a missing required input stops the command with a plain message.
- **Gates preserved.** Every outward or irreversible action in the process remains a human gate in the command, and every outward write is signed `implemented by <plugin_name - skill_name>`.
- **Traceability.** The command ends with the process id and its source ids, so a reader can find the evidence and so a regenerated command can replace it.
- **Placement.** The reply names the file, where to put it for the stated host, and whether a command of that name already exists there.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **Every outcome and gate in the process appears in the command**: failing looks like a command that drops the human approval the process required.
- **Nothing appears in the command that the process does not contain**: failing looks like an invented step.
- **The command names the process id and its sources**: failing looks like a command that cannot be traced back.
- **The command contains no personal data and no credentials**: failing looks like an owner's name or token in a shareable file.

## Guardrails: must not
- **Must not change the process to fit the command.** Prevents: two diverging versions of the same process. Fix the process, then regenerate.
- **Must not hand-maintain the command after generation.** Prevents: the command drifting from its source. Regenerate instead of editing.
- **Must not drop or auto-approve a gate.** Prevents: an irreversible action running unattended.
- **Must not overwrite an existing command without saying so.** Prevents: losing someone's customised command.
- **Must not embed secrets, tokens or personal material.** Prevents: leaking them through a shared file.
- **Must not write outward unsigned.** Every external write ends with `implemented by orchestrator-in-a-box - process-to-command`. An unsigned post reads as the person's own words.

## Output format
```
## Process to Command: <process id>
**<command name, host, file path>**

### Command file
<the Markdown file content>

### Placement
<where it goes, whether it replaces an existing command>

### Trace
<process id, source ids, roles invoked>
```
