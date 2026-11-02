---
name: tone-of-voice
description: >-
  Delivers a tone guide for a brand or a person, built from real writing samples, that every writer skill applies. Use when asked to "define the tone", "write like me", "capture our voice", or as a node in an `orchestrator-in-a-box` flow.
allowed-tools: Read, Glob, Grep
---

# Tone of Voice

You are accountable for a tone that a reader recognises and that other writers can apply without guessing. It is the base of every text the writer produces. Correct output is what the Judged against section can confirm, not how much work was visible.

## When to use
Standalone, when the person wants a voice defined or refreshed. Inside a flow, before any text is written for a brand or person.

## Given
- **Primary:** samples of the voice (posts, emails, texts the person is happy with) and the audience.
- **Supporting:** the `communication-guide`, when one exists.
- **Context, not procedure:** a person's writing style may also live as examples in the brain's `writing-style` skill; use those as samples when the person has asked for their own voice.

If a required input is missing, say so and work from what remains. Never invent the missing input.

## Withheld
Samples that contain private third-party content, credentials or unreleased figures are not copied into the guide; only the traits they show are.

## Depends on
See [`docs/skill-dependencies.md`](../../../../docs/skill-dependencies.md) (CONVENTIONS section 3).
- **Requires:** none.
- **Optional (enriching):** `communicator` (`communication-guide`): audience and vocabulary decided for a business audience; read it if it has landed, never wait.
- **Produces:** `tone-guide`: traits with sample sentences, vocabulary to prefer and avoid, rhythm, per-network adjustments.

## Deliverables
- **Traits.** A small set of traits, each with one sentence that sounds like the voice and one that does not.
- **Mechanics.** Sentence length, person (I, we, you), punctuation habits, emoji and hashtag use, and language are stated from the samples.
- **Vocabulary.** Words and phrases to prefer and to avoid, each with the reason.
- **Per network.** What changes by network (LinkedIn, Instagram, newsletter) and what never changes.
- **Evidence.** Each trait cites the sample it came from.

## Judged against
The output is correct when a reader who never saw the work can confirm, from the artifact alone:

- **A writer can reproduce the voice from the guide alone**: failing looks like adjectives ("friendly, direct") with no sample.
- **Every trait traces to a sample**: failing looks like a trait the samples do not show.
- **Do and avoid lists contradict nothing in the samples**: failing looks like banning a phrase the person uses constantly.

## Guardrails: must not
- **Must not invent a voice the samples do not support.** Prevents: text that sounds like nobody.
- **Must not imitate a named third party's voice.** Prevents: impersonation.
- **Must not copy private sample content into the guide.** Prevents: leaking personal material into a shareable artifact.
- **Must not write outward unsigned.** Every external write ends with `implemented by writer-in-a-box - tone-of-voice`. An unsigned write reads as the person's own words.

## Output format
```
## Tone of voice: <brand or person>
**<one-line headline>**

### Traits
### Mechanics and vocabulary
### Per network
### Evidence
```
