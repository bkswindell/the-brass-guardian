# Cross-Agent Handoff Protocol

This file defines how AI agents should exchange durable project information through the repository.

## Principle

Chat history is temporary. Repository memory is durable.

When an agent discovers, decides, proposes, or completes something that another future agent will need, record the durable portion in the repository.

## Before Starting Work

An agent should:

1. read `/agents/README.md`;
2. read `/agents/shared/PROJECT_CONTEXT.md`;
3. read `/agents/shared/DECISIONS.md`;
4. read its own agent-specific files under `/agents/<agent>/`;
5. inspect the relevant canonical Markdown and repository standards;
6. inspect recent work in the area being modified.

Do not begin from remembered chat context when the repository can answer the question.

## During Work

Agents should avoid storing transient implementation chatter in shared memory.

Durable items include:

- creator-approved canon decisions;
- changes to publication or spoiler rules;
- major architecture decisions;
- new cross-agent conventions;
- current project priorities when they will persist beyond one session;
- unresolved continuity conflicts that future agents must not accidentally resolve;
- handoff notes for unfinished work.

## Handoff Notes

For substantial unfinished work, create or update a concise handoff file in the most relevant agent folder or project area.

A useful handoff should contain:

- **Goal**
- **Current state**
- **Files changed**
- **Important decisions**
- **Open questions**
- **Next recommended step**
- **Risks / spoiler concerns**

Avoid long narrative transcripts.

## Decisions

Creator-approved decisions with lasting impact should be recorded in `/agents/shared/DECISIONS.md`.

Whenever possible, also update the actual canonical file that owns the information. `DECISIONS.md` should serve as a durable decision log and discovery aid, not a competing canon database.

## Creative Proposals

Do not write speculative AI ideas into canonical files as settled facts unless the creator approved them.

If a proposal needs to persist between agents, label it clearly as **PROPOSAL** and keep it separate from established canon.

## Conflicts

If two sources disagree:

1. identify both sources;
2. determine whether one explicitly supersedes the other;
3. prefer the current canonical Markdown over compiled or older material;
4. check `DECISIONS.md` for an explicit creator ruling;
5. if still unresolved, preserve the conflict and ask rather than inventing a reconciliation.

## Public-Facing Work

Before publishing or generating website content, agents must distinguish between repository knowledge and public-safe knowledge.

Do not expose future arcs, hidden motives, creator-only answers, or story-sensitive material simply because the agent has repository access.

## Commit Behavior

When making repository changes:

- keep commits focused;
- use descriptive commit messages;
- avoid unrelated rewrites;
- preserve cross-links;
- prefer updating the owning canonical file rather than duplicating lore into memory files.

## Closing a Session

Before ending substantial work, ask:

> If another capable agent started tomorrow with no access to this conversation, what would it need to know?

If the answer is important and durable, put it in the repository.
