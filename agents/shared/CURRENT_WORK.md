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
- Milestone C1 was approved by the author and merged into `main` from `feat/world-entrance-map` on 2026-08-10. The implementation is now durable on `main`, while its proposal records, Hidden Archives, and Archive artwork remain publication-gated and excluded from production until an exact public projection is separately approved.
- C1 now contains a proposal-only Archive entrance, a directly interactive Aetherhaven map, 67 public Preview records, and a separately warned Hidden Archives subsection. The map provides 24 numbered public destination links and six lettered restricted links; each responsive SVG link combines its district geometry and raster-label hit area into one keyboard focus stop rather than restoring floating marker buttons. The public catalog includes source-grounded stubs for all 16 public character profiles and 25 public organization profiles. Hidden Archives keeps 12 mysterious or spoiler-sensitive figures and 10 concealed or sensitive organizations outside the ordinary catalog, with 28 restricted records closed by default. Proposal records are enabled only by `PUBLICATION_PREVIEW=1` or Vercel's `VERCEL_ENV=preview`; the production build keeps the approved public manifest empty and excludes proposal record routes, copy, and artwork. Candidate derivatives live outside Astro's unconditional `public/` tree and are staged only during preview builds.
- Production isolation is fail-closed: `VERCEL_ENV=production` overrides a conflicting Preview flag, successful production builds remove the static Archive route tree and every build artifact unreachable from retained public HTML, and the build fails if any remaining production page can reach a Preview-sensitive artifact. CLI and Astro-configured output directories are both resolved before cleanup or asset staging. Production verification asserts that no Archive route directory, candidate artwork, route-only styles, or Archive layout artifact remains.
- C1 navigation now follows the approved dual model: an eight-stop Curator’s Route provides intentional orientation while the searchable Open Catalog, Map Room, and record cross-references support free exploration. Every record preserves both a recommended next stop and an obvious way to leave the route.
- Preview-enabled landing builds now replace preparation/Coming Soon language with **Enter Archive** and link directly to `/archive/`; preview-disabled production-safe builds retain the sealed landing page and emit no Archive link.
- The author rejected the Flash-style procedural 3D lock and superseded its React/Three.js/GSAP presentation. The current C1 direction is Astro-only and scene-first: the creator-approved `art/locations/aetherhaven_archive/AA-2.png` environment sits behind the central editorial frame as a washed atmospheric backdrop, while one simple real `/archive/` invitation changes **Invitation Waiting** to **Lock Released** through restrained CSS light/copy feedback. Gears, gauges, Canvas, WebGL, and complex mechanism animation are removed. Responsive 1024px/768px derivatives remain Preview-only until production publication is separately approved; production must emit no Archive routes, Archive art, or entrance link.
- The author accepted `AA-2.png` as the permanent active Archive environment image and selected it to replace the generic website threshold. Rejected `AA-*` variants and the superseded generic source are stored under `unused/aetherhaven_archive/`. The current interior checkpoint carries the responsive scene across every Archive route, leaves an architectural sightline above the arrival desk and framed map, presents desktop navigation as a translucent wayfinding rail, keeps mobile navigation non-sticky, and reduces panel opacity so Curator notes, route drawers, catalog cards, map workbench, and record sheets feel placed within the room. Anchor targets clear the sticky desktop rail.
- The expanded C1 local checkpoint passes 64 tests, renders and verifies 72 Preview pages, confirms 30 direct semantic map links and 28 closed Hidden Archive drawers, passes desktop/mobile Chromium review, reports zero high-severity npm vulnerabilities, and preserves exact overlay alignment at both 1406×1052 and 768×575 rendered map sizes. The final production output contains only the sealed landing and 404 HTML surfaces; no Archive route directory, Preview artwork directory, Archive copy, map overlay markup, or route-only implementation remains.
- Branch status: **MERGED / DELETED**. After pushed `main` and its production-safe deployment were verified, `feat/world-entrance-map` was confirmed to contain no unique commits and was deleted locally and remotely in accordance with the branch lifecycle policy.

### Next Recommended Step

Begin Milestone C2 with the Amelia and Elias Core Introduction slice. Keep C1 map copy, classifications, Hidden Archives, and Archive images labeled as proposals until the author approves the final production projection; move only exact accepted records through the approved public manifest and publication gate.
