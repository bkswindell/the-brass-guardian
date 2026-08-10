# Hermes Handoff — Aetherhaven Archive Schema v1 Website Architecture

**Status:** APPROVED / ACTIVE ARCHITECTURE  
**Date:** 2026-08-10  
**Author authority:** Creator-approved direction  
**Website cutover:** PR #34 merged to `main`  
**Schema:** `docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md` — Version `1.0.0 — LOCKED`

## Goal

Preserve the existing Aetherhaven Archive visitor experience while making the repository's canonical Markdown the authoritative content source for the website.

Hermes should continue developing the website as an immersive **Aetherhaven Archive** experience, but website code must not become a second lore database.

The governing direction is:

```text
Canonical Markdown + Schema v1 frontmatter
        ↓
Astro frontmatter-only content collection
        ↓
public_projection from owning Markdown records
        ↓
hash-based author approval ledger
        ↓
Archive publication model
        ↓
existing Astro layouts / routes / interactions
```

The **content may evolve frequently**. The **schema should evolve rarely**.

---

## Current State

The source-of-truth cutover is complete and merged into `main`.

The repository currently contains **210 Schema v1 canonical records** across:

- `characters/`
- `locations/`
- `organizations/`
- `artifacts/`
- `vessels/`
- `historical_events/`
- `story_drafts/`
- `story_arcs/`

The current approved public Archive projection contains:

- **95** author-approved public/teaser projections;
- **67** public record routes;
- **28** closed Hidden Archive teaser records;
- **30** canonical city-map references;
- **8** Curator's Route stops;
- **72** generated HTML pages in the current published C1 experience.

These counts are current parity expectations, not permanent schema constants. If the creator approves new public records later, the counts should grow naturally rather than being treated as immutable world rules.

---

## What Changed From the Original Website Implementation

The first Archive implementation maintained record content in website-side JavaScript and JSON, especially the old catalog/preview model.

That architecture has been retired.

The following duplicate content sources were removed and **must not be recreated**:

- `website/src/lib/archive-catalog.mjs`
- `website/src/lib/archive-preview.mjs`
- the old content-heavy Version 1 `website/content/public/manifest.json`
- the old website-owned record IDs such as `character-amelia-hawthorne`, `hidden-character-*`, and `restricted-*`

Canonical entities now keep their stable Schema v1 `AH-*` IDs regardless of how the Archive presents them.

Examples:

- Amelia remains `AH-CHAR-002` whether shown in a dossier, search result, or cross-reference.
- A restricted location remains a `location`; "restricted" is disclosure/presentation state, not a new entity identity.
- A district is a location subtype, not a separate website-only ontology.
- The Wayfinder now has its own first-class vessel record under `vessels/`.

---

## Authoritative Content Source

For entity facts and reader-facing Archive copy, **the owning Markdown file is authoritative**.

A Schema v1 record may contain:

- canonical identity and record type;
- canon/development/disclosure state;
- relationships using stable canonical IDs;
- asset references and alt text;
- cartographic reference where it is a durable world fact;
- chronology where applicable;
- `public_projection` containing the reader-safe Archive projection approved for potential publication.

Website templates should render these records. They should not duplicate their titles, summaries, classifications, relationships, tags, image descriptions, map marker identities, or other lore-bearing content in JavaScript.

When canon changes, update the owning Markdown record first.

---

## Astro Content Ingestion

The website reads Schema v1 Markdown through:

- `website/src/content.config.ts`
- `website/src/loaders/canon-frontmatter-loader.ts`

The loader is intentionally **frontmatter-only**.

Do not casually replace it with normal Markdown rendering for the entire canon library. The public Archive does not need to compile every internal Markdown body, inline image, private note, or story-sensitive illustration merely to obtain structured record metadata.

This separation reduces accidental publication coupling and keeps private/internal prose out of the public content pipeline.

The loader uses stable canonical IDs as collection entry IDs and requires `schema_version: 1`.

---

## Public Projection

Public and Hidden Archive reader-facing record content now comes from each owning Markdown record's `public_projection`.

The website publication model converts that projection into the presentation shape used by the existing Astro pages.

Primary implementation files:

- `website/src/lib/archive-publication.mjs`
- `website/src/lib/archive-publication-v2.mjs`
- `website/src/lib/archive-content-model.mjs`
- `website/scripts/lib/archive-publication-v2-model.mjs`
- `website/scripts/lib/canon-record-loader.mjs`

Production and Archive Preview use the **same Markdown projections**.

The difference is authorization:

- Preview may render current public projections for review and is noindex/noncanonical.
- Production requires an exact matching author-approved projection fingerprint.

Do not create a separate Preview lore/catalog database again.

---

## Publication Approval Is Separate From Content

The active approval ledger is:

`website/content/public/manifest.json`

It is now **Schema Version 2** and intentionally small.

It contains publication authorization data such as:

- canonical `id`;
- `projectionHash`;
- `approvedBy`;
- `approvedOn`;
- publication date.

It must **not** become another copy of titles, summaries, tags, relationships, image descriptions, or canon facts.

A Markdown record declaring something public does not authorize itself for production publication.

### Fingerprint behavior

The SHA-256 publication fingerprint covers the reader-facing projection and the selected source artwork digest.

Therefore, if someone changes approved public Markdown or replaces its selected source artwork, the previous approval becomes stale and production validation fails closed.

This is intentional.

**Do not work around a fingerprint failure by weakening validation or blindly regenerating hashes.**

A changed projection requires author review/approval before the approval ledger is updated.

---

## Release State Is Also Separate

The Archive's overall release switch remains:

`website/content/public/archive-release.json`

This answers a different question from content approval:

> Is the Archive currently published at all?

The release system remains fail-closed and supports sealed behavior independently of individual record approvals.

Do not merge release state into canonical Markdown.

---

## Presentation Data That Correctly Remains Website-Side

The active presentation file is:

`website/content/public/archive-presentation.json`

It is Schema Version 2 and is keyed by canonical IDs.

It currently owns presentation-only information such as:

- SVG/map hit geometry;
- clickable label geometry;
- Curator's Route ordering;
- Curator's Route labels and visitor-navigation notes.

This is intentionally **not canon content**.

Example boundary:

- `Map 17` being the Entertainment District is a durable cartographic fact and belongs in canonical Markdown.
- the SVG `cx`, `cy`, radius, and clickable label rectangle for Map 17 belong to the website presentation layer.

Do not move pixel geometry into the canon schema.

---

## Derived Web Assets

The generated web-derivative registry is:

`website/content/public/archive-assets.json`

It maps canonical source asset paths to optimized website derivatives and responsive source sets.

Canonical Markdown owns the source asset reference, semantic role, visibility, and alt information.

The website may own derived values such as:

- WebP derivative path;
- output width/height;
- responsive variants;
- deployment-specific asset paths.

Do not copy those generated web details back into canon unless they become durable source-asset facts.

---

## Schema Change Guardrail

The authoritative schema is:

`docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md`

Version `1.0.0` is **LOCKED**.

Hermes is a **consumer and implementer** of the schema, not its unilateral owner.

If the website needs a value the schema does not provide, first classify the requirement:

1. **canon content** — belongs in canonical Markdown if the existing schema can represent it;
2. **publication approval** — belongs in the approval/publication system;
3. **derived data** — calculate it from canonical data where possible;
4. **presentation configuration** — keep it website-side.

A frontend convenience is not sufficient reason to change the schema.

If the current schema genuinely cannot represent a durable project concept, do **not** add an ad-hoc global field. Use:

`templates/Aetherhaven_Schema_Change_Proposal.md`

The proposal remains `PROPOSED` until the creator approves it.

A breaking schema change may require a repository-wide migration. Treat it accordingly.

---

## Website UX Direction

The source-of-truth migration was **not a redesign**.

The existing Archive visual design and visitor experience remain the approved baseline unless the creator separately requests changes.

Preserve the established experience, including:

- Archive entrance/navigation model;
- Open Catalog;
- Hidden Archives and spoiler warning behavior;
- closed Hidden Archive drawers by default;
- interactive city map;
- Curator's Route;
- record viewer layouts;
- responsive behavior;
- accessibility semantics;
- current atmospheric Aetherhaven design language.

Future UX improvements are welcome, but they should be intentional product/design changes rather than accidental side effects of content architecture work.

Mystery must not become bad usability.

---

## Adding a New Canonical Record to the Website

The intended workflow is now:

1. Create or update the owning canonical Markdown record using Schema v1.
2. Add durable relationships/assets/cartography to that record as appropriate.
3. Add or revise `public_projection` only with creator-approved or explicitly reviewable public copy.
4. If presentation-specific map geometry or curated-route placement is needed, add that separately to `archive-presentation.json`.
5. Generate/prepare web derivatives when a newly approved source image requires them and update `archive-assets.json` as derived data.
6. Preview the result through the same Markdown-backed publication model.
7. Obtain creator approval for the exact public projection.
8. Update the approval ledger fingerprint only after that approval.
9. Run the full validation suite.
10. Merge and promptly delete the working branch.

Do not add a record by hard-coding another object into a website catalog.

---

## Changing an Existing Public Record

If canon changes but the approved `public_projection` does not change, the public site may not need a new publication approval.

If the reader-facing projection or selected public image changes:

1. make the change in the owning Markdown record/source asset;
2. preview it;
3. obtain creator approval;
4. update the matching approval fingerprint;
5. validate production and Preview;
6. merge.

A failed fingerprint after an intentional public-copy change is expected behavior, not a bug.

---

## Validation Requirements

Website/content work should be verified from `website/` using the repository's existing scripts.

At minimum:

```bash
npm ci
npm run verify
npm run verify:archive-preview
```

The current validation system checks the important boundaries, including:

- Schema v1 record validity;
- complete canonical ID/relationship integrity;
- exact approval fingerprints;
- release state;
- public vs Hidden Archive projection;
- expected map references and geometry joins;
- Curator's Route resolution;
- generated routes and internal links;
- publication leakage of internal content;
- approved Archive asset inventory;
- sealed-release behavior;
- production and Preview rendering.

GitHub also contains read-only validation workflows for the canon library and website.

Do not weaken a failing gate merely to make a PR green. Determine whether the failure indicates canon, approval, presentation, asset, or implementation drift.

---

## Historical Migration Files

The Schema v1 and publication-v2 migrations have completed.

One-time migration scaffolding used to perform the cutover was removed from the active website architecture when it was no longer needed.

Do not restore old migration scripts/workflows as normal runtime architecture.

Historical reports under `docs/development/` may still describe the migration process and are useful for audit/history, but the current standards and active implementation on `main` are authoritative.

---

## Important Files to Read Before Future Archive Work

Always read the relevant portions of:

1. `docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md`
2. `docs/standards/CANON_MARKDOWN_STANDARD.md`
3. `agents/hermes/SOUL.md`
4. this handoff file
5. `website/src/content.config.ts`
6. `website/src/loaders/canon-frontmatter-loader.ts`
7. `website/src/lib/archive-publication.mjs`
8. `website/src/lib/archive-publication-v2.mjs`
9. `website/scripts/lib/archive-publication-v2-model.mjs`
10. `website/content/public/manifest.json`
11. `website/content/public/archive-presentation.json`
12. `website/content/public/archive-release.json`
13. `website/content/public/archive-assets.json`
14. the canonical Markdown records involved in the task.

Inspect current `main`; do not rely on old branch implementations or remembered chat context.

---

## Approval Status

The following architecture is **APPROVED**:

- Schema v1 Markdown is the canonical website content source.
- Version 1.0.0 schema change control is active.
- public record copy is owned by Markdown `public_projection`.
- production publication requires a separate exact approval fingerprint.
- release state remains separate and fail-closed.
- map geometry/Curator Route configuration remain website presentation data.
- optimized web assets are derived data.
- the existing C1 Archive UX remains the baseline experience.

Any substantial reversal of these decisions is an architectural/schema proposal and requires creator approval.

---

## Branch Status

PR #34 — **MERGED**.

The `website/schema-v1-content-source` branch contains no unique work after merge and may be deleted if it still exists.

The unrelated `replace-dock-zero-artifact` branch is intentionally outside this handoff and should not be modified or deleted solely because of the website migration.

Future work should use short-lived task branches and delete them promptly after merge in accordance with `agents/shared/BRANCH_LIFECYCLE.md`.

---

## Next Recommended Direction

With the source-of-truth architecture established, Hermes can focus again on the actual visitor experience:

- improving Archive exploration;
- adding newly approved canonical records automatically through the Markdown pipeline;
- building richer relationship-driven discovery;
- improving maps, artifact viewing, search/indexing, timelines, and Archive atmosphere;
- supporting future public stories and exhibits without duplicating canon;
- keeping hidden/story-sensitive material protected by the publication boundary.

The goal is not to make the data architecture visible to visitors.

The goal is for the architecture to make the Archive **easier to grow without losing canon control**.
