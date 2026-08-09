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
- Milestone C1 is active on `feat/world-entrance-map`. The branch is an author-approved iterative workspace: agents may commit, push, and refresh its Vercel Preview without per-change approval, but may not merge to `main` or publish to production without explicit approval.
- C1 currently contains a proposal-only Archive entrance, interactive Aetherhaven map, and seven preview records. Proposal records are enabled only by `PUBLICATION_PREVIEW=1` or Vercel's `VERCEL_ENV=preview`; the production build keeps the approved public manifest empty and excludes proposal record routes, copy, and artwork. Candidate derivatives live outside Astro's unconditional `public/` tree and are staged only during preview builds.
- Production isolation is fail-closed: `VERCEL_ENV=production` overrides a conflicting Preview flag, successful production builds remove the static Archive route tree and every build artifact unreachable from retained public HTML, and the build fails if any remaining production page can reach a Preview-sensitive artifact. CLI and Astro-configured output directories are both resolved before cleanup or asset staging. Production verification asserts that no Archive route directory, candidate artwork, route-only styles, or Archive layout artifact remains.
- C1 navigation now follows the approved dual model: an eight-stop Curator’s Route provides intentional orientation while the searchable Open Catalog, Map Room, and record cross-references support free exploration. Every record preserves both a recommended next stop and an obvious way to leave the route.
- Preview-enabled landing builds now replace preparation/Coming Soon language with **Enter Archive** and link directly to `/archive/`; preview-disabled production-safe builds retain the sealed landing page and emit no Archive link.
- The author rejected the Flash-style procedural 3D lock and superseded its React/Three.js/GSAP presentation. The current C1 direction is Astro-only and scene-first: a generated, non-canonical Aetherhaven Archive environment sits behind the central editorial frame as a washed atmospheric backdrop, while one simple real `/archive/` invitation changes **Invitation Waiting** to **Lock Released** through restrained CSS light/copy feedback. Gears, gauges, Canvas, WebGL, and complex mechanism animation are removed. Responsive 1024px/768px backdrop derivatives remain Preview-only; production must emit no Archive routes, candidate art, or entrance link.
- The author likes the washed/darkened scene on the main landing and directed the Archive interior to make that environment more focal. The current interior checkpoint carries the responsive scene across every Archive route, leaves an architectural sightline above the arrival desk and framed map, presents desktop navigation as a translucent wayfinding rail, keeps mobile navigation non-sticky, and reduces panel opacity so Curator notes, route drawers, catalog cards, map workbench, and record sheets feel placed within the room. Anchor targets clear the sticky desktop rail. The visual treatment remains proposal-only pending live author review.
- Branch status: **PRESERVE TEMPORARILY / AWAITING REVIEW**. `feat/world-entrance-map` supports the active C1 Vercel Preview and should remain until the author approves a merge or requests further refinement. After an approved merge to `main` is verified, delete the feature branch.

### Next Recommended Step

Refine the C1 World Entrance through local and Vercel Preview review. Keep its map, copy, classifications, and images labeled as proposals until the author approves the final production projection; then move only the accepted records through the approved public manifest and merge gate.
