# model-router-in-a-box

Role: **Model router**. Skill: [`model-router`](skills/model-router/SKILL.md). Picks a model per flow node from the agent in use. Produces `model-assignment`.

Model identifiers live only in the user's `.in-a-box/models.yaml` (see [`examples/models.yaml`](examples/models.yaml)), never in a skill.

Limit: the router decides, the host applies. In Claude Code a skill cannot switch the running session's model, but `run-flow` can start each node as a subagent with the assigned model.
