# Branch Lifecycle and Cleanup Policy

This repository uses short-lived working branches. Branches are implementation workspaces, not durable project memory.

## Governing Rule

**Once a pull request has been successfully merged into `main`, its working branch should be deleted promptly unless the author has explicitly approved keeping that branch for an active operational reason.**

The durable record of completed work is the merged commit history, pull request history, canonical files, and `/agents/` durable memory—not a collection of old branches.

## Normal Lifecycle

1. Start from the current `main` branch.
2. Create one focused working branch for the task.
3. Make and validate the intended changes.
4. Open a pull request into `main` when review is appropriate.
5. Confirm the final scope and any required author approval.
6. Merge the approved work into `main`.
7. Verify that the merged result exists correctly on `main`.
8. **Delete the merged working branch.**

Agents should treat branch deletion as part of completing the task, not as optional housekeeping for someone else later.

## Exceptions

A branch may remain temporarily after a merge only when there is a specific active reason, such as:

- an external preview or deployment test still depends on that branch;
- unfinished material exists on the branch that has not yet been reviewed or salvaged;
- a migration or recovery procedure explicitly requires the branch to remain available;
- the author explicitly instructs the team to preserve the branch.

The exception should be documented in the relevant handoff with:

- the branch name;
- why it must remain;
- what is still needed;
- the condition that allows it to be deleted.

Do not keep merged branches merely "just in case." Git history already preserves the merged work.

## Abandoned or Superseded Branches

If a pull request is intentionally closed without merge because the work was rejected or superseded, delete the branch once any useful material has been safely preserved elsewhere.

Before deleting an unmerged branch, compare it to `main` and verify that it contains no unique work that still needs review or recovery.

## AI Agent Responsibilities

Any AI agent that creates a branch owns its lifecycle until handoff.

Before ending work involving a branch, record whether the branch is:

- **ACTIVE** — work is still underway;
- **AWAITING REVIEW** — PR or author review is pending;
- **MERGED — DELETE** — merged and no longer needed;
- **PRESERVE TEMPORARILY** — still required for a documented reason;
- **ABANDONED — REVIEW BEFORE DELETE** — unmerged work may need salvage review.

If an agent merges a pull request and has the technical ability to delete the branch, it should do so immediately after verifying `main`.

If the current toolset cannot delete remote branches, the agent must explicitly flag the branch for deletion in its handoff rather than silently leaving it behind.

## Branch Count Discipline

Keep the active branch list small and understandable. Normally, the repository should contain:

- `main`;
- a small number of genuinely active task branches;
- temporary branches with clearly documented purposes.

A large accumulation of merged, superseded, or abandoned branches should be treated as repository maintenance debt and audited promptly.

## Final Principle

**Merge it, verify it, remove the branch.**

Branches are temporary workspaces. `main` and the repository's durable documentation are the lasting record.