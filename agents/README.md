# AI Agent Memory

This directory is the durable collaboration layer for AI agents working on **The Brass Guardian / Aetherhaven** repository.

Its purpose is to let different agents share project context, decisions, handoffs, and agent-specific operating instructions without treating any model's private chat history as the source of truth.

## Directory Structure

```text
/agents/
  README.md
  /shared/
    PROJECT_CONTEXT.md
    HANDOFF_PROTOCOL.md
    DECISIONS.md
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

1. **Current canonical Markdown files in the repository**
2. **Explicit creator decisions recorded in `/agents/shared/DECISIONS.md`**
3. **Repository standards such as `CANON_MARKDOWN_STANDARD.md` and `PROJECT_INDEX.md`**
4. **Shared agent context in `/agents/shared/`**
5. **Agent-specific instructions in `/agents/<agent>/`**
6. **Compiled manuscripts, PDFs, old drafts, and prior chat memory**

The Markdown canon is the primary development source. The compiled manuscript may lag behind current canon.

## Shared vs. Agent-Specific Memory

### `/agents/shared/`

Information that another capable agent should know regardless of model belongs here:

- project purpose and creative principles
- cross-agent working conventions
- confirmed creator decisions
- current high-level priorities
- handoffs between agents
- unresolved questions worth preserving

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

## Canon Discipline

Agents may propose new creative material, but proposals do not become canon merely because an AI wrote them.

When creating or modifying lore, distinguish between:

- **Established Canon** — supported by current repository sources.
- **Supported Inference** — strongly implied but not confirmed.
- **Creative Proposal** — new material awaiting creator approval.

Never silently convert a proposal into canon.

## Public-Site Discipline

Repository access does not imply publication approval. The repository contains story-sensitive and future material.

For public-facing work such as `thebrassguardian.com`, reveal atmosphere, characters, places, artifacts, side stories, rumors, and unresolved clues while protecting central plot answers and future-story revelations.

**Tease the question, not the answer.**

## Updating Shared Memory

When adding a durable decision:

1. record it in `shared/DECISIONS.md`;
2. update the canonical source file when appropriate;
3. add cross-links rather than duplicating full lore;
4. note unresolved conflicts rather than inventing a resolution.

## Core Principle

**Protect the wonder. Protect the canon. Leave doors unopened on purpose.**
