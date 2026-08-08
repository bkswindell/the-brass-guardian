# AI Agent Memory

This directory is the durable collaboration layer for AI agents working on **The Brass Guardian / Aetherhaven** repository.

Its purpose is to let different agents share project context, decisions, handoffs, and agent-specific operating instructions without treating any model's private chat history as the source of truth.

## Mandatory Author-Control Policy

Before any creative or canonical work, every agent must read:

**[`shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md`](shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md)**

The human author retains final and exclusive artistic control over the project.

AI may provide ideas, critique, prose, images, plots, visual guidance, technical implementation, and other creative assistance, but **AI-generated material does not become canon merely because it was generated or written into a draft**.

No material canonical change may be adopted or committed as accepted project state without explicit author approval.

When approval is unclear, treat the material as a proposal.

## Directory Structure

```text
/agents/
  README.md
  /shared/
    PROJECT_CONTEXT.md
    AUTHORSHIP_AND_ARTISTIC_CONTROL.md
    HANDOFF_PROTOCOL.md
    DECISIONS.md
    CURRENT_WORK.md
  /proposals/
    README.md
    ACTIVE_CREATIVE_PROPOSALS.md
  /hermes/
    SOUL.md
  /gpt/
    SOUL.md
  /gemini/
    README.md
  /claude/
    README.md
```

Additional agent folders may be added later.

## Authority Order

AI agents must use the following precedence when information conflicts:

1. **Explicit current direction and approvals from the human author**
2. **Current creator-approved canonical Markdown files in the repository**
3. **Explicit creator decisions recorded in `/agents/shared/DECISIONS.md`**
4. **Repository standards such as `CANON_MARKDOWN_STANDARD.md` and `PROJECT_INDEX.md`**
5. **Shared agent context in `/agents/shared/`**
6. **Agent-specific instructions in `/agents/<agent>/`**
7. **Compiled manuscripts, PDFs, old drafts, and prior chat memory**

The Markdown canon is the primary development source for already-approved material. The compiled manuscript may lag behind current canon.

An agent's creative preference never outranks the author's decision.

Content under `/agents/proposals/` is **not part of the authority hierarchy as canon**. It is explicitly unapproved development material unless an entry records a later author approval and promotion.

## Shared vs. Agent-Specific Memory

### `/agents/shared/`

Information that another capable agent should know regardless of model belongs here:

- project purpose and creative principles
- authorship and approval rules
- cross-agent working conventions
- confirmed creator decisions
- current high-level priorities
- handoffs between agents
- unresolved questions worth preserving

### `/agents/proposals/`

Unapproved creative ideas worth preserving across sessions belong here.

Examples include proposed plots, characters, locations, organizations, artifacts, visual concepts, possible mystery explanations, terminology, or website narrative ideas.

**Proposal files are not canon.** Their purpose is to preserve useful possibilities without making them appear approved.

Read `/agents/proposals/README.md` before adding or promoting proposal material.

### `/agents/<agent>/`

Agent-specific material belongs in the corresponding folder:

- system/personality guidance
- model-specific workflows
- tool-use conventions
- implementation notes useful only to that agent

Do not duplicate large portions of canon into the agent folder. Link to the canonical source instead.

## Durable Memory Rule

If an agent learns something important in conversation that should affect future work, it should propose or make an appropriate update to this repository rather than relying on chat memory.

Durable project knowledge should become a file.

However, **proposal status must be preserved**. A speculative idea should never be written into durable memory in a way that makes it appear creator-approved.

If an unapproved creative idea is worth preserving, record it under `/agents/proposals/` rather than altering canon.

## Canon Discipline

Agents may propose new creative material, but proposals do not become canon merely because an AI wrote them.

When creating or modifying lore, distinguish between:

- **Established Canon** — supported by current creator-approved repository sources.
- **Supported Inference** — strongly implied but not confirmed.
- **Creative Proposal** — new material awaiting creator approval.

Never silently convert a proposal into canon.

Never alter an owning canon file to preserve an unapproved idea.

## Creative Commit Discipline

Material changes to story, characters, world-building, lore, visual canon, public narrative, or unresolved mysteries require author approval before being committed as accepted project state.

A direct author instruction to make a specific change is approval for that specific change.

It is not blanket authority to invent consequential surrounding details.

If a task requires additional material creative choices, surface those choices for review.

## Public-Site Discipline

Repository access does not imply publication approval. The repository contains story-sensitive and future material.

For public-facing work such as `thebrassguardian.com`, reveal atmosphere, characters, places, artifacts, side stories, rumors, and unresolved clues while protecting central plot answers and future-story revelations.

New public-facing narrative content is still creative material and requires author approval before it becomes accepted published project content.

**Tease the question, not the answer.**

## Updating Shared Memory

When adding a durable decision:

1. confirm that it was actually approved by the author;
2. record it in `shared/DECISIONS.md`;
3. update the canonical source file when appropriate and approved;
4. add cross-links rather than duplicating full lore;
5. note unresolved conflicts rather than inventing a resolution.

When preserving an unapproved creative idea, use `/agents/proposals/` instead of `shared/DECISIONS.md` or an owning canon file.

## Core Principle

**The author controls the story. Protect the wonder. Protect the canon. Leave doors unopened on purpose.**
