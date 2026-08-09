# Current Cross-Agent Work

This file tracks active work that may span multiple AI agents or sessions. Keep it concise and current.

## Active Priority — Public Website

**Project:** `thebrassguardian.com`

**Goal:** Build a public-facing website that transforms the repository into a fun, immersive way to explore Aetherhaven and The Brass Guardian canon without exposing the main plot or answers to central mysteries.

### Desired Experience

The site should feel like an entrance into the **Aetherhaven Archives** rather than a conventional wiki or corporate author site.

Visitors should be able to discover:

- Aetherhaven and its districts;
- Elias and Amelia Hawthorne;
- the Wayfinder;
- the Clockwork Gardens;
- public-safe organizations and figures;
- artifact records and archival plates;
- maps and recovered documents;
- canon-compatible short stories and micro-fiction;
- rumors, unresolved clues, and optional deeper discoveries.

### Public Content Rule

Repository access includes material that is not appropriate for first-time visitors.

Before publishing any content, classify it as approximately:

- PUBLIC
- TEASER
- STORY-SENSITIVE
- CREATOR-ONLY

Only PUBLIC and deliberately selected TEASER material should appear on the public site without explicit creator approval.

### Initial Engineering Direction

Before choosing or changing the web stack, the implementing agent should inspect the repository for existing website code, deployment configuration, package manifests, current branches, and asset organization.

Prefer a content-driven architecture that can reuse canonical Markdown and structured metadata rather than duplicating lore into hard-coded pages.

The approved initial hosting target is the Vercel Hobby plan for the project's current non-commercial phase. Publish and review the site at a temporary Vercel deployment URL before connecting either custom domain. Domain connection is a separate creator-approved cutover step.

### Initial Content/UX Direction

Useful first-release areas likely include:

1. immersive landing page / introduction;
2. Explore Aetherhaven;
3. interactive or navigable city map;
4. character introductions;
5. artifact/archive gallery;
6. the Wayfinder;
7. short public stories;
8. an Archive-style discovery layer with cross-links and subtle mysteries.

These are directional, not yet a locked sitemap.

### Current State

- Shared `/agents/` durable-memory architecture established.
- Hermes Aetherhaven `SOUL.md` established.
- GPT collaboration profile established.
- Vercel account established and connected to the official GitHub account.
- `thebrassguardian.com` and `www.thebrassguardian.com` currently redirect to the official GitHub repository as placeholders.
- Vercel Hobby approved for the initial non-commercial deployment, with preview-first review before domain connection.
- Website implementation has not yet been architected in this shared memory file.

### Next Recommended Step

Have the implementing agent inspect the repository's current technical structure and produce a concise website architecture proposal before large-scale code generation.

The proposal should identify:

- existing web code, if any;
- recommended stack based on what is already present;
- content ingestion strategy for Markdown canon;
- public/spoiler filtering strategy;
- image/asset strategy;
- proposed sitemap;
- deployment approach;
- first implementation milestone.

Do not begin by copying all canon to the public site.
