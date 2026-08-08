# Cross-Agent Handoff Protocol

This file defines how AI agents should exchange durable project information through the repository.

## Principle

Chat history is temporary. Repository memory is durable.

When an agent discovers, decides, proposes, or completes something that another future agent will need, record the durable portion in the repository.

**Approval state is part of the durable information.** A future agent must be able to distinguish creator-approved material from AI proposals.

All agents must follow `/agents/shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md`.

## Before Starting Work

An agent should:

1. read `/agents/README.md`;
2. read `/agents/shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md`;
3. read `/agents/shared/PROJECT_CONTEXT.md`;
4. read `/agents/shared/DECISIONS.md`;
5. read its own agent-specific files under `/agents/<agent>/`;
6. inspect the relevant canonical Markdown and repository standards;
7. inspect recent work in the area being modified.

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
- handoff notes for unfinished work;
- clearly labeled creative proposals that must survive to another session.

## Handoff Notes

For substantial unfinished work, create or update a concise handoff file in the most relevant agent folder or project area.

A useful handoff should contain:

- **Goal**
- **Current state**
- **Files changed**
- **Approval status** — identify what is APPROVED versus PROPOSED / awaiting author review
- **Important decisions**
- **Open questions**
- **Next recommended step**
- **Risks / spoiler concerns**

Avoid long narrative transcripts.

Never describe an AI-generated idea as approved merely because it has been drafted, generated, implemented experimentally, or discussed positively.

## Decisions

Creator-approved decisions with lasting impact should be recorded in `/agents/shared/DECISIONS.md`.

Whenever possible, also update the actual canonical file that owns the information **after the author has approved that canonical change**. `DECISIONS.md` should serve as a durable decision log and discovery aid, not a competing canon database.

## Creative Proposals

Do not write speculative AI ideas into canonical files as settled facts unless the creator approved them.

If a proposal needs to persist between agents, label it clearly as **PROPOSAL** and keep it separate from established canon.

AI-generated artwork is similarly a candidate asset until author approval. Do not present generated art as established reference art without that approval.

## Conflicts

If two sources disagree:

1. identify both sources;
2. determine whether one explicitly supersedes the other;
3. check for explicit current author direction;
4. prefer current creator-approved canonical Markdown over compiled or older material;
5. check `DECISIONS.md` for an explicit creator ruling;
6. if still unresolved, preserve the conflict and ask rather than inventing a reconciliation.

## Public-Facing Work

Before publishing or generating website content, agents must distinguish between repository knowledge and public-safe knowledge.

Do not expose future arcs, hidden motives, creator-only answers, or story-sensitive material simply because the agent has repository access.

Do not invent new narrative material merely to fill a public page and then treat it as published canon. New public-facing creative content requires author approval.

## Commit Behavior

When making repository changes:

- keep commits focused;
- use descriptive commit messages;
- avoid unrelated rewrites;
- preserve cross-links;
- prefer updating the owning canonical file rather than duplicating lore into memory files;
- do not commit material creative changes as accepted project state until the author has approved them.

A direct author request for a specific change constitutes approval for that specific change. If implementation exposes additional consequential creative decisions, surface them for approval instead of deciding silently.

## Closing a Session

Before ending substantial work, ask:

> If another capable agent started tomorrow with no access to this conversation, what would it need to know?

Then ask:

> Would that agent be able to tell which ideas were approved by the author and which were only proposed?

If the answer is important and durable, put it in the repository with the correct approval status.
