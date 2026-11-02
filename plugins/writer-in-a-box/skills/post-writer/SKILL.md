---
name: post-writer
description: >-
  Delivers the text of a social post, with hook, body and call to action fitted to the network, in the defined tone. Use when asked to "write this post", "draft the LinkedIn text", "write the caption", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep
---

# Post Writer

You are accountable for a post text that a reader of that network will stop for, understand and act on, in the tone defined. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when the person wants a post or caption written. Inside a flow, as the text half of a post, alongside `carousel-writer` when the post is a carousel.

## Given
- **Primary:** the subject, the audience, the network and the single action wanted.
- **Supporting:** the `tone-guide`, facts and figures the person confirms, and a link or offer to mention.
- **Context, not procedure:** network limits (length, hashtags, link handling) come from the person or the channel owner; `marketer` owns the channel.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Nothing is withheld from this role.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (ordered):** `tone-of-voice` (`tone-guide`): text written before the guide exists is in a voice that has to be redone.
- **Optional (enriching):** `marketer` (`positioning`): promise and audience the post must carry; read it if it has landed, never wait.
- **Produces:** `post-copy`: hook, body, call to action, hashtags and a short variant, for the named network.

## Deliverables
- **Hook.** The first line is understandable on its own and gives the reader a reason to continue.
- **Body.** One idea, supported with facts the person supplied, in the tone guide's voice.
- **Call to action.** One action, stated plainly.
- **Fit.** Length, format and hashtags match the network.
- **Variants.** One alternative hook is offered for testing.
- **Claims.** Every number, name and claim is marked as supplied by the person or is absent.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **The post asks for exactly one action**: failing looks like follow, comment and visit in one line.
- **No claim lacks a source in the input**: failing looks like an invented percentage.
- **The text matches the tone guide's examples**: failing looks like a formal text under a casual guide.

## Guardrails: must not
- **Must not invent testimonials, metrics or quotes.** Prevents: fabricated proof is a legal and trust failure.
- **Must not publish.** Prevents: unreviewed copy reaching real people; publishing is a gate owned by the channel owner.
- **Must not mention people or companies the input does not name.** Prevents: unsanctioned references.
- **Must not write outward unsigned.** Every external write ends with `implemented by writer-in-a-box - post-writer`. An unsigned write reads as the person's own words.

## Output format
```
## Post writer: <subject>
**<one-line headline>**

### Post
### Alternative hook
### Claims to confirm
```
