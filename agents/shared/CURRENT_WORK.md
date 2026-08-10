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
- Milestone C1 was approved by the author and merged into `main` from `feat/world-entrance-map` on 2026-08-10. The author subsequently directed the complete reviewed C1 experience to be published, including the warned Hidden Archives index and all 28 closed teaser drawers. This approves the exact public projection for website release; it does not declare the records or generated Archive art to be canon and does not authorize revealing deeper restricted source content.
- The reviewed C1 production release is live on `main` at `https://thebrassguardian.com/`. `content/public/manifest.json` contains 95 dated author-approved projections: 67 ordinary public records and 28 Hidden Archive teasers. `content/public/archive-presentation.json` separately contains the approved 30 map geometries and eight Curator Route annotations. The six restricted map references, 12 mysterious or spoiler-sensitive figures, and 10 concealed organizations remain separated from the ordinary catalog and closed by default.
- `content/public/archive-release.json` is the version-controlled release switch. `published` renders only the safe record and presentation projections in production; `sealed` returns the Archive to an empty model and triggers route/asset pruning. `VERCEL_ENV=production` always defeats a conflicting Preview flag, and production has no static dependency on the raw Preview catalog. Vercel branch Previews dynamically load proposal data and continue to use proposal labels and `noindex`.
- The nine reviewed Archive derivatives now live under `website/public/images/archive/` for production delivery. This includes responsive derivatives of the accepted `AA-2` environment, canonical map, Clockwork Gardens art, and Wayfinder art. Website-publication approval for `AA-2` does not establish it as visual canon.
- C1 navigation now follows the approved dual model: an eight-stop Curator’s Route provides intentional orientation while the searchable Open Catalog, Map Room, and record cross-references support free exploration. Every record preserves both a recommended next stop and an obvious way to leave the route.
- Published and Preview landing builds replace preparation/Coming Soon language with **Enter Archive** and link directly to `/archive/`; only an explicit `sealed` release returns the production landing page to the closed state.
- The author rejected the Flash-style procedural 3D lock and superseded its React/Three.js/GSAP presentation. The current C1 direction is Astro-only and scene-first: the creator-approved `art/locations/aetherhaven_archive/AA-2.png` environment sits behind the central editorial frame as a washed atmospheric backdrop, while one simple real `/archive/` invitation changes **Invitation Waiting** to **Lock Released** through restrained CSS light/copy feedback. Gears, gauges, Canvas, WebGL, and complex mechanism animation are removed. The separate production-publication gate for the responsive derivatives, Archive routes, and entrance link was approved on 2026-08-10 as recorded above.
- The author accepted `AA-2.png` as the permanent active Archive environment image and selected it to replace the generic website threshold. Rejected `AA-*` variants and the superseded generic source are stored under `unused/aetherhaven_archive/`. The current interior checkpoint carries the responsive scene across every Archive route, leaves an architectural sightline above the arrival desk and framed map, presents desktop navigation as a translucent wayfinding rail, keeps mobile navigation non-sticky, and reduces panel opacity so Curator notes, route drawers, catalog cards, map workbench, and record sheets feel placed within the room. Anchor targets clear the sticky desktop rail.
- The first independent release review failed closed because production recovered presentation metadata from raw Preview objects, sealed rollback failed the real prebuild gate, and artifact verification did not prove an exact projection. Those blockers were remediated before commit: production now consumes only the two approved public manifests, the sealed configuration passes an isolated real prebuild/build and prunes routes/images, and verification reconstructs the exact projection, scans all emitted text types for internal markers, and enforces the nine-file asset inventory.
- A second independent review timed out before returning a verdict but demonstrated three further fail-closed gaps: a traversal-shaped Map Room href passed validation, approved record/map/route values could be reassociated in emitted HTML while global containment checks still passed, and provenance markers in SVG or webmanifest output were not scanned. Regression tests and production checks now reject canonical-path violations, enforce values within each owning record/map/route/drawer element, and scan every non-binary artifact. The corrected verifier rejects the reviewer’s exact tampered artifact tree.
- A third narrow review failed closed because the emitted-element matcher accepted suffixed attribute names such as `data-href`, `x-data-map-marker`, and `data-id` as ownership attributes. The matcher now requires whitespace before each exact attribute name. Regression tests cover all three suffix bypasses, Hidden Archive drawer reassociation, safe text artifacts, and marker-like bytes in approved binary extensions.
- A fourth surgical review confirmed the ASCII suffix fix but found that JavaScript `\s` also accepts Unicode whitespace that HTML does not treat as an attribute separator, and that the map href/marker mutation test masked one check with the other. The matcher now uses the exact HTML ASCII-whitespace class `[\t\n\f\r ]`; href and marker mutations are independently asserted, with additional non-breaking-space prefix regressions for href, marker, and drawer ID.
- The fifth surgical re-review passed with no findings. It confirmed the exact HTML whitespace boundary, exclusion of Unicode-whitespace attribute prefixes, independent href/marker regression coverage, and non-vacuous route/drawer ownership checks. The independent pre-commit release gate is satisfied.
- The remediated C1 publication checkpoint passes 82 tests, renders and verifies 72 pages in both production and Preview modes, confirms 67 public record routes, 30 direct semantic map links, 28 closed Hidden Archive drawers, canonical/indexable production routes, `noindex` Previews, approved assets, valid internal links/fragments, and zero browser QA errors. The resolved production map geometry and Curator Route projection retains the pre-remediation SHA-256 fingerprint `596a90098ba01e1b9f7a8c442c696ebde91e357e194a1835ef442b2e55ea5f92`; visual layout did not change.
- Live production verification on 2026-08-10 confirmed Vercel `Ready`, canonical `200` responses, 67/67 record routes, 30 direct map links, 28 closed Hidden Archive drawers, all nine approved Archive assets, indexable canonical metadata, 308 secondary-domain redirects, desktop/mobile/keyboard/no-JavaScript behavior, and zero browser errors. The generated Vercel deployment URL is authentication-protected; Vercel CLI status and the public canonical domain were therefore used for authoritative deployment and content verification respectively.
- Branch status: **MERGED / DELETED**. `release/publish-c1-archive` was verified to contain no unique commits and was deleted locally and remotely after the reviewed release and closeout state reached `main`.
- Branch status: **MERGED / DELETED**. After pushed `main` and its production-safe deployment were verified, `feat/world-entrance-map` was confirmed to contain no unique commits and was deleted locally and remotely in accordance with the branch lifecycle policy.

### Next Recommended Step

Begin Milestone C2 with the Amelia and Elias Core Introduction slice, preserving C1's publication boundary and the distinction between approved public presentation and canon.

---

## Active Parallel Work — Aetherhaven Content Schema

**Branch:** `content/archive-source-of-truth`  
**Branch status:** **AWAITING MERGE / RECONCILED WITH COMPLETED C1 RELEASE**

The author approved establishing schema governance before the final website/content audit is complete.

Current staged work on this branch:

- `docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md` created as Version `0.1.0`, with governance active but the field dictionary intentionally unfrozen;
- `/templates/Aetherhaven_Schema_Change_Proposal.md` created for future controlled schema changes;
- `AGENTS.md`, the canon Markdown standard, and Hermes instructions updated to require schema-change control;
- no canonical profile metadata has been migrated;
- no website code has been realigned on this branch.

Hermes has now completed the C1 website publication pass. Before beginning the source-of-truth migration:

1. merge these governance rules into current `main`;
2. audit the final Astro implementation, manifest/publication boundary, catalog data, map data, route generation, assets, and content consumers;
3. complete the Version 1 data dictionary;
4. pressure-test representative record families;
5. obtain explicit author approval to mark Version `1.0.0` **LOCKED**;
6. only then begin the repository-wide canonical Markdown metadata migration.

The final source-of-truth migration must preserve the existing approved site layout and user experience unless the author separately requests a design change.