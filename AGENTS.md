# AGENTS.md — The Brass Guardian / Aetherhaven

This repository is designed to be worked on by multiple AI agents and human collaborators.

Before performing meaningful work in this repository, **read `/agents/README.md` first**.

That file defines the shared durable-memory system, canon authority hierarchy, cross-agent handoff rules, and the locations of agent-specific instructions.

## Required Startup Sequence

Before making changes:

1. Read `/agents/README.md`.
2. Read the applicable files in `/agents/shared/`, especially:
   - `PROJECT_CONTEXT.md`
   - `DECISIONS.md`
   - `CURRENT_WORK.md`
   - `HANDOFF_PROTOCOL.md`
3. Read your agent-specific instructions, if present:
   - Hermes: `/agents/hermes/`
   - GPT / OpenAI: `/agents/gpt/`
   - Claude: `/agents/claude/`
   - Gemini: `/agents/gemini/`
4. Read the repository standards relevant to the task, including `CANON_MARKDOWN_STANDARD.md` and `PROJECT_INDEX.md` when working with lore or canon.
5. Inspect the current implementation and relevant source files before proposing or making changes.

Do not rely on remembered conversation history when the repository contains a newer decision.

## Canon Authority

The Markdown canon files in this repository are the primary development source of truth.

Use this general priority when sources disagree:

1. Current canonical Markdown files and explicit creator-approved canon
2. Current repository standards and indexes
3. `/agents/shared/DECISIONS.md`
4. Other shared durable-memory files under `/agents/shared/`
5. Agent-specific notes under `/agents/<agent>/`
6. Older compiled manuscripts, drafts, summaries, or remembered conversations

Do not silently reconcile contradictions. Determine whether one source supersedes another, and surface unresolved conflicts when necessary.

## Shared Durable Memory

The `/agents/` directory exists so different AI systems can cooperate across sessions.

Use `/agents/shared/` for information that another capable agent would need in order to continue the work without access to the current conversation.

Appropriate shared-memory updates include:

- approved creative or technical decisions,
- current project priorities,
- unresolved questions,
- implementation assumptions,
- handoff notes,
- canon clarifications that are not yet better represented in a dedicated canon file.

Do **not** use shared memory as a replacement for proper canon files, source documentation, or code comments.

## Creative Safety

The repository contains public material, active canon, future-story material, private development notes, and major spoilers.

Repository access does **not** imply publication approval.

When creating public-facing material:

- preserve established canon,
- protect unresolved mysteries,
- avoid exposing story-sensitive or creator-only information,
- prefer teasing questions over revealing answers,
- do not convert speculative development notes into canon without approval.

## Engineering Behavior

When modifying software or website code:

- inspect before rewriting,
- preserve working architecture unless change is justified,
- avoid unrelated refactors,
- prefer maintainable solutions,
- keep lore/content separable from presentation where practical,
- preserve accessibility and responsive behavior,
- do not casually alter or replace established visual assets.

For substantial architectural or creative changes, document the decision in `/agents/shared/DECISIONS.md` once approved.

## Cross-Agent Handoff Principle

Before ending substantial work, ask:

> If another capable agent started tomorrow with no access to this conversation, what would it need to know to continue correctly?

Record the durable parts of that answer in `/agents/shared/`.

## Final Rule

**Protect the canon, protect the unrevealed story, and leave the repository easier for the next collaborator to understand than you found it.**
