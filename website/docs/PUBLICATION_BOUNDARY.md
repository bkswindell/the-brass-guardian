# Public Publication Boundary

## Status

**C1 public Archive release — 95 author-approved projections are enabled.**

This document defines the curated projection boundary between the internal Brass Guardian repository and the public website. It does not grant publication approval to any story, character, location, artifact, image, or other repository material.

## Governing Rule

**Repository presence is not publication approval.**

The website must never import or render the internal canon library wholesale. Public routes may consume only records deliberately added to `content/public/manifest.json` and presentation metadata deliberately added to `content/public/archive-presentation.json` after the author approves the exact public projection.

The record manifest contains 67 ordinary public records and 28 Hidden Archive teasers approved by the author on 2026-08-10. The presentation manifest contains the exact 30 map geometries and eight Curator Route annotations approved on the same date. Production may render only these client-safe projections. The deeper canonical sources and restricted answers remain outside the public output.

## Executable Contract

The build-time contract is implemented by:

- `scripts/lib/publication-boundary.mjs` — validation and safe client projection;
- `scripts/lib/archive-release.mjs` — strict validation for the version-controlled release state;
- `scripts/lib/archive-presentation.mjs` — strict validation for public map and Curator Route metadata;
- `scripts/verify-publication-boundary.mjs` — validates the real record, presentation, and release manifests;
- `scripts/verify-archive-publication.mjs` — verifies approved values within their owning record page, map anchor, route step, or Hidden Archive drawer; scans every non-binary emitted artifact for internal markers; and enforces the nine-file Archive image inventory;
- `scripts/sealed-build.test.mjs` — runs the real build in an isolated sealed copy and proves Archive routes and images are pruned;
- `scripts/publication-boundary.test.mjs`, `scripts/publication-date.test.mjs`, `scripts/publication-image-shape.test.mjs`, `scripts/publication-manifest-shape.test.mjs`, `scripts/publication-path-hardening.test.mjs`, and `scripts/publication-source-roots.test.mjs` — positive, negative, and path-hardening contract tests;
- `content/public/manifest.json` — the explicit public allowlist;
- `content/public/archive-presentation.json` — the approved 30-link map geometry and eight-step Curator Route contract;
- `content/public/archive-release.json` — the explicit `published` or `sealed` release state.

`npm run build` invokes `npm run verify:publication` first. Vercel therefore rejects a production build when the public record, presentation, or release manifests violate the boundary.

## Manifest Shape

The top-level object uses `schemaVersion: 1` and an `entries` array. Every entry must provide:

| Field | Requirement |
|---|---|
| `id` | Stable, unique, lowercase kebab-case public ID. |
| `slug` | Unique, lowercase kebab-case URL slug. |
| `entityType` | One of the supported public archive entity types. |
| `canonicalName` | Canonical subject name used for continuity checks. |
| `publicTitle` | Author-approved title presented to visitors. |
| `publicSummary` | Deliberately written public-safe summary; never copied automatically from an internal profile. |
| `sourcePaths` | One or more existing repository-relative Markdown sources used for audit and continuity. |
| `publicationStatus` | Must be exactly `approved`. Drafts cannot enter the public manifest. |
| `spoilerClassification` | Must be `public` or deliberately approved `teaser`. |
| `approval` | Must record `approvedBy: "author"` and an ISO `approvedOn` date. |
| `relatedEntryIds` | Public cross-references only; each target must exist in the same approved manifest. |
| `tags` | Unique public-safe tags. |

Optional fields:

| Field | Requirement |
|---|---|
| `image` | Canonical root-relative image URL, meaningful alt text, and positive integer width and height. The URL cannot contain encoding, query, or fragment syntax, and the asset must exist under `public/`. |
| `publicationDate` | ISO date in `YYYY-MM-DD` form. |
| `publicAccessLabel` | Short author-approved visitor label. This does not weaken the validated `public`/`teaser` safety classification. |

Unknown top-level, approval, and image fields are rejected so private notes cannot silently enter generated client data.

## Presentation Manifest Shape

`content/public/archive-presentation.json` contains only public interaction metadata. It requires `schemaVersion: 1`, a dated author approval, exactly 30 unique map entries covering markers `1–24` and `A–F`, and exactly eight unique Curator Route annotations. Map entries may contain only an approved record ID, marker, bounded SVG region and label geometry, and an optional bounded percentage position. Route record steps may contain only an approved public record ID, label, and note; the Map Room step additionally carries its public title and Archive-local href.

The validator rejects unknown nested fields, invalid geometry, duplicate IDs or markers, missing record references, hidden/public marker mismatches, altered route length, and any Map Room href that is not a canonical lowercase path beneath `/archive/` (including traversal, encoding, query, fragment, or doubled-slash forms).

Owning sources are restricted to the root `README.md` or Markdown under `characters/`, `organizations/`, `locations/`, `historical_events/`, `story_arcs/`, `story_drafts/`, and `artifacts/`. Website files, agent proposals, audience reactions, and `unused/` material cannot be declared as canonical provenance.

## Supported Public Entity Types

- `character`
- `location`
- `district`
- `organization`
- `artifact`
- `story`
- `archive-record`
- `vessel`
- `event`
- `rumor`

These are presentation categories, not new canon classifications.

## Public Projection Safety

`toPublicArchiveEntry()` produces the object allowed to reach page rendering. It excludes:

- `sourcePaths`;
- `publicationStatus`;
- the complete `approval` record;
- any undeclared fields.

The retained spoiler classification is limited by validation to `public` or `teaser`. The optional `publicAccessLabel` preserves approved visitor-facing labels such as `restricted` or `major spoiler` without allowing the underlying restricted classification or source material into the public projection.

Production resolves manifest IDs against the separately approved presentation manifest for map geometry and Curator Route annotations. Titles, summaries, relationships, images, and record routes still come only from the approved record projection. The raw Preview catalog is dynamically imported only after the non-production Preview branch is selected; a production environment cannot load it or be forced into proposal mode by setting `PUBLICATION_PREVIEW=1`.

## Approval Workflow

1. Identify the owning canonical Markdown source or sources.
2. Draft a concise public title and summary separately from the internal source text.
3. Classify the exact projection as `public` or `teaser`.
4. Select only approved web imagery and write accurate alt text.
5. Obtain explicit author approval for the exact text, classification, relationships, and imagery.
6. Add the entry to `content/public/manifest.json` with the approval date.
7. Add approved map geometry and Curator Route annotations to `content/public/archive-presentation.json` when the release needs them.
8. Set `content/public/archive-release.json` to the approved scope only after the exact collection is accepted.
9. Run `npm run verify` and `npm run verify:archive-preview`.
10. Review the generated branch Preview before merging or exposing a route.

Changing an internal canonical source does not automatically update or authorize its public projection. Public summaries should be re-audited when owning sources materially change.

## Route Convention

Public archive records use stable routes of the form:

`/archive/{entityType}/{slug}/`

The current C1 release emits 67 routes under this convention. Hidden Archive teasers remain closed drawers at `/archive/hidden/` rather than receiving unrestricted standalone record routes.

## Explicitly Rejected Inputs

The validator rejects:

- draft, story-sensitive, or creator-only records;
- missing or unsafe source paths;
- missing or unsafe public image paths;
- non-file paths and symbolic links that resolve outside their approved roots;
- missing image alt text or invalid dimensions;
- duplicate IDs, slugs, tags, or relationships;
- relationships to unpublished records or to the record itself;
- malformed approvals and publication dates;
- undeclared fields that could carry internal notes.

Internal profiles, story arcs, story drafts, proposal files, and artwork are not public simply because they are available to the build environment.
