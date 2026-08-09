# Durable Creator Decisions

This file records creator-approved decisions that should survive individual AI conversations and be discoverable by all agents.

It is a decision log, not a substitute for the canonical Markdown files. When a decision belongs in a character, location, organization, timeline, story, or artifact file, update that owning canon file as well **only after the author has approved that canonical change**.

---

## 2026-08-08 — Author Retains Final Artistic and Canonical Control

**Status:** APPROVED / GOVERNING PRINCIPLE

The human author retains final and exclusive artistic control over **The Brass Guardian / Aetherhaven** project.

AI is an important part of the creative process and may be used for artistic guidance, brainstorming, continuity analysis, prose drafting, story and plot ideas, world-building proposals, illustration concepts, generative artwork, editing, organization, technical implementation, and public-experience development.

However, AI does not have authority to decide what becomes canon.

All material canonical changes must be explicitly approved by the author before they are adopted or committed as accepted project state. This includes changes to story, characters, relationships, world-building, lore, chronology, mysteries, organizations, fictional rules, visual canon, and other creative elements that materially affect the project.

AI-generated prose, artwork, concepts, plots, interpretations, and designs remain **proposals or candidate assets** until the author approves them.

Brainstorming discussion does not establish canon.

A direct author instruction to make a specific creative change constitutes approval for that specific change, but does not grant an agent authority to invent consequential surrounding details without review.

The author expects AI collaborators to provide genuine creative judgment, criticism, alternatives, and guidance. The author may accept, revise, combine, or reject any AI-generated material.

When approval is ambiguous, agents must not assume approval.

The full operating policy is maintained in:

`/agents/shared/AUTHORSHIP_AND_ARTISTIC_CONTROL.md`

This principle overrides any agent-specific instruction or workflow that would otherwise allow autonomous canonical decision-making.

---

## 2026-08-08 — Creative Proposal Staging Area

**Status:** APPROVED

The repository will maintain `/agents/proposals/` as a durable staging area for useful **unapproved creative ideas** shared between AI collaborators and the author.

The purpose of this area is to preserve possible story plots, characters, locations, organizations, artifacts, illustration concepts, mystery interpretations, terminology, motifs, and other creative possibilities without making them appear canonical.

Material stored under `/agents/proposals/` is not canon unless the author later explicitly approves it and the approved scope is promoted into the appropriate canonical or project files.

The active proposal index is:

`/agents/proposals/ACTIVE_CREATIVE_PROPOSALS.md`

Rejected or parked proposals may remain in the proposal area as development history, provided their status is unmistakable.

Agents must not move proposal material into canon merely because it appears useful, internally consistent, or has been discussed repeatedly.

---

## 2026-08-08 — Shared AI Memory Architecture

**Status:** APPROVED

The repository will contain an `/agents/` section used as durable shared memory and operating guidance for AI collaborators.

Agent-specific subfolders may include:

- `/agents/hermes/`
- `/agents/gpt/`
- `/agents/gemini/`
- `/agents/claude/`

Shared information belongs under `/agents/shared/` so different agents can exchange durable context through GitHub rather than relying on private chat history.

The repository remains the source of truth. Agent memory files must not become an alternative canon database.

---

## 2026-08-08 — Repository Documentation and Template Layout

**Status:** APPROVED

The repository root should remain intentionally clean and contain only files that conventionally belong at the project entry point, including the public `README.md`, `AGENTS.md`, the compiled PDF/DOCX manuscript exports, and any future conventional root metadata such as a license or contribution guide.

Reusable project Markdown templates are centralized under:

`/templates/`

Project-wide internal documentation is centralized under:

`/docs/`

The principal development paths are:

- `/docs/PROJECT_INDEX.md` — internal canon and repository index;
- `/docs/standards/CANON_MARKDOWN_STANDARD.md` — Markdown and visual integration standard;
- `/docs/standards/Map_Location_Reference_Style_Guide.md` — map-location public-reference guidance;
- `/docs/development/CANON_DEVELOPMENT_TODO.md` — active development queue;
- `/docs/development/PLACEHOLDER_PROFILE_INDEX.md` — placeholder inventory;
- `/templates/` — reusable character, organization, location, artifact, story-arc, and historical-event profile templates.

AI agents, scripts, and workflows must use these current paths rather than recreating obsolete root-level copies.

---

## 2026-08-08 — Public Website Direction

**Status:** APPROVED

The first major task for the Hermes agent is development of **thebrassguardian.com**.

The site should transform the GitHub repository into an immersive public experience for exploring Aetherhaven and The Brass Guardian universe.

It should introduce visitors to the world through public-safe lore, artwork, locations, characters, artifacts, archival material, and short canon-compatible stories without revealing the central plots or answers to major mysteries.

The experience should feel like entering and exploring the Aetherhaven Archives rather than browsing a conventional spoiler-heavy wiki.

---

## 2026-08-08 — Initial Website Hosting and Domain Cutover

**Status:** APPROVED

The initial non-commercial version of **thebrassguardian.com** will use the Vercel Hobby plan. The author has created a Vercel account connected to the official GitHub account.

Development should be published first to a temporary Vercel deployment URL for review. The custom domains should remain forwarded to the official GitHub repository until a production build is approved and ready for connection.

Connecting the domains is a separate cutover step and must not be performed merely because a preview deployment exists. If the site's purpose later becomes commercial, review the hosting plan against Vercel's then-current terms before continuing to use the Hobby tier.

---

## 2026-08-08 — Public Coming Soon Cutover

**Status:** APPROVED

The author approved replacing the temporary GitHub redirects for `thebrassguardian.com` and `www.thebrassguardian.com` with the reviewed Vercel-hosted Coming Soon page. The page may use the approved cover artwork as a prominent archive display with an accessible cover reader, while remaining public-safe and free of unreleased story material.

Deploy the approved page to Vercel production before changing DNS. **TheBrassGuardian.com** is the branded canonical website, represented technically as `https://thebrassguardian.com/`; permanently redirect `www.thebrassguardian.com`, `brassguardian.com`, `www.brassguardian.com`, and the stable Vercel production hostname to that canonical apex. Preserve unrelated DNS records, and verify HTTPS and redirect behavior after cutover. Branch and deployment-specific Vercel URLs remain available only for deployment review.

---

## 2026-08-09 — Curated Publication Boundary

**Status:** APPROVED

The public website uses `website/content/public/manifest.json` as its explicit publication allowlist. The manifest begins empty. Repository presence, internal canon status, or build-system access does not grant publication approval.

Every future public record must use separately curated public-facing fields, reference an owning canonical source, carry explicit author approval, and be classified `public` or deliberately approved `teaser`. Draft, story-sensitive, creator-only, malformed, or undeclared material must fail the production build rather than render.

Public image references must resolve to approved regular files under the website's public asset root, use meaningful alternative text and explicit dimensions, and pass canonical URL, traversal, and symbolic-link containment checks. Internal provenance and approval metadata must not enter client-facing projections.

Future archive records reserve stable routes of the form `/archive/{entityType}/{slug}/`, but no archive record routes or public lore are approved by this decision. Each exact text and image projection still requires author review before publication.

---

## 2026-08-09 — Dedicated Website Preview Branch Workflow

**Status:** APPROVED

Once the author approves a dedicated website feature branch, agents may iteratively implement, commit, push, and update that branch and its Vercel Preview deployment without requesting approval for every individual change. The branch and Preview deployment are the normal shared refinement workspace.

Preview copy, classifications, imagery, and interactions remain proposals rather than approved canon or production publication. Preview routes must remain clearly labeled, `noindex`, and separate from the production navigation until the author approves launch.

Explicit author approval is still required before merging the dedicated branch into `main`, promoting or publishing the work to production, or treating proposed creative material as accepted canon. This workflow does not relax spoiler discipline, publication-boundary validation, security review, accessibility, or responsive-quality requirements.

---

## 2026-08-08 — Moon Garden Canon

**Status:** APPROVED

The Moon Garden is a rare, hidden nocturnal layer of the Clockwork Gardens rather than a distant ordinary location.

It is not publicly mapped or generally known. Rumors may disagree about its location and contents.

Access depends on invitation or recognition by the Gardens and cannot be reliably forced or mapped.

Juniper Bell pays special attention to the Moon Garden and other hidden gardens nested within the Clockwork Gardens. She can work with the Gardens to reveal, conceal, redirect, or close paths, but does not command them.

Amelia's early visit was by invitation.

It remains unresolved whether Juniper chose Amelia because she believed Amelia could help, whether the Gardens instructed Juniper to summon her, or whether another explanation applies.

Preserve that ambiguity.

---

## 2026-08-08 — "Clockwork Princess" Usage

**Status:** APPROVED

Juniper Bell is the only character who calls Amelia **"the Clockwork Princess."**

The phrase is affectionate, distinctive, and connected to Juniper's possible identity as the Keeper of Dreams and to the early story title *The Brass Guardian and the Clockwork Princess*.

No other character should routinely use the title.

It does not establish Amelia as literal royalty or grant political authority.

---

## Existing Visual Canon — Amelia's Aether Heart

**Status:** APPROVED / ESTABLISHED

The Aether Heart is a persistent visible component of Amelia Hawthorne's mechanical arm near the wrist/forearm and should appear as glowing aetheric energy when the arm is visibly depicted unless a scene provides a deliberate reason otherwise.

---

## Maintaining This File

Add new decisions chronologically.

Use one of these statuses when useful:

- **APPROVED**
- **SUPERSEDED**
- **PROVISIONAL**
- **REJECTED**

When superseding a decision, retain the old entry for history and link or point to the new ruling rather than silently deleting the prior record.

Do not use **APPROVED** unless the author actually approved the decision.
