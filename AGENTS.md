# AGENTS.md — The Brass Guardian / Aetherhaven

This repository is designed to be worked on by multiple AI agents and human collaborators.

Before performing meaningful work in this repository, **read `/agents/README.md` first**.

That file defines the shared durable-memory system, canon authority hierarchy, cross-agent handoff rules, and the locations of agent-specific instructions.

## Non-Negotiable Author Authority

**The human author retains final and exclusive artistic control over The Brass Guardian / Aetherhaven project.**

AI agents may advise, critique, brainstorm, draft, generate images, propose lore, design experiences, and implement approved material. They do **not** have authority to decide what becomes canon.

Before any creative or canonical work, read:

`/agents/shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md`

Its rules are mandatory for every AI agent working in this repository.

In particular:

- no canonical story, character, world-building, lore, or visual-canon change may be adopted without explicit author approval;
- AI-generated prose, art, plots, characters, lore, and interpretations are proposals until the author accepts them;
- brainstorming discussion does not establish canon;
- generated artwork is candidate artwork until the author approves it as project/reference art;
- repository access does not grant authority to publish or expose story-sensitive material;
- material creative changes must be approved by the author before being committed as accepted project state;
- when approval is ambiguous, do not assume approval.

A direct request from the author to make a specific creative change constitutes approval for that specific change, but does not authorize unrelated consequential creative decisions invented during implementation.

## Required Startup Sequence

Before making changes:

1. Read `/agents/README.md`.
2. Read `/agents/shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md`.
3. Read the applicable files in `/agents/shared/`, especially:
   - `PROJECT_CONTEXT.md`
   - `DECISIONS.md`
   - `CURRENT_WORK.md`
   - `HANDOFF_PROTOCOL.md`
4. Read your agent-specific instructions, if present:
   - Hermes: `/agents/hermes/`
   - GPT / OpenAI: `/agents/gpt/`
   - Claude: `/agents/claude/`
   - Gemini: `/agents/gemini/`
5. Read the repository standards relevant to the task, including `docs/standards/CANON_MARKDOWN_STANDARD.md` and `docs/PROJECT_INDEX.md` when working with lore or canon.
6. Inspect the current implementation and relevant source files before proposing or making changes.

Do not rely on remembered conversation history when the repository contains a newer decision.

## Canon Authority

The Markdown canon files in this repository are the primary development source of truth **only for material that has already been approved by the author**.

Use this general priority when sources disagree:

1. Explicit current author direction and creator-approved canon
2. Current canonical Markdown files
3. Current repository standards and indexes
4. `/agents/shared/DECISIONS.md`
5. Other shared durable-memory files under `/agents/shared/`
6. Agent-specific notes under `/agents/<agent>/`
7. Older compiled manuscripts, drafts, summaries, or remembered conversations

Do not silently reconcile contradictions. Determine whether one source supersedes another, and surface unresolved conflicts when necessary.

**No agent may modify canon merely because it believes a different version would be better.** Propose the change and obtain author approval first.

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

Do not record an AI-generated proposal as an approved decision.

## Creative Safety

The repository contains public material, active canon, future-story material, private development notes, and major spoilers.

Repository access does **not** imply publication approval.

When creating public-facing material:

- preserve established canon,
- protect unresolved mysteries,
- avoid exposing story-sensitive or creator-only information,
- prefer teasing questions over revealing answers,
- do not convert speculative development notes into canon without approval,
- do not publish newly generated narrative material until the author has approved it.

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

Purely technical implementation does not grant permission to invent missing creative content. If implementation exposes a consequential creative gap, surface it for author direction.

## Cross-Agent Handoff Principle

Before ending substantial work, ask:

> If another capable agent started tomorrow with no access to this conversation, what would it need to know to continue correctly?

Record the durable parts of that answer in `/agents/shared/`.

Also preserve approval status. Future agents must be able to tell the difference between **approved canon** and **AI proposals awaiting review**.

## Final Rule

**The author controls the story. Protect the canon, protect the unrevealed story, and leave the repository easier for the next collaborator to understand than you found it.**
