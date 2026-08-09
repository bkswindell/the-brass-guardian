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
- The Astro website is implemented under `website/` and deploys automatically from GitHub to Vercel.
- Vercel Web Analytics and Speed Insights are installed and verified.
- The author approved the public-safe Coming Soon page, including responsive cover-art derivatives, a brass archive display stand, and an accessible cover reader.
- The production Coming Soon page is live at canonical **TheBrassGuardian.com** (`https://thebrassguardian.com/`). The `www.thebrassguardian.com`, `brassguardian.com`, `www.brassguardian.com`, and stable Vercel production hostnames permanently redirect to the canonical apex; branch and deployment-specific Vercel URLs remain available only for review. HTTPS, certificates, final GET behavior, canonical metadata, and absence of GitHub routing were verified after cutover.
- Vercel Hobby remains approved for the initial non-commercial deployment.
- Milestone A establishes an empty explicit public manifest, a fail-closed publication validator and test suite, and a reusable Astro site layout. No public lore or archive record routes were added, and the Coming Soon presentation remains unchanged.

### Next Recommended Step

Select and author-review the first exact public archive projection as a separate milestone. Do not populate the manifest by copying internal canon wholesale.
