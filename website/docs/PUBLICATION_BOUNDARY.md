# Public Publication Boundary

## Status

**Milestone A technical foundation — no public archive records are enabled.**

This document defines the curated projection boundary between the internal Brass Guardian repository and the public website. It does not grant publication approval to any story, character, location, artifact, image, or other repository material.

## Governing Rule

**Repository presence is not publication approval.**

The website must never import or render the internal canon library wholesale. Public routes may consume only records deliberately added to `content/public/manifest.json` after the author approves the exact public projection.

The manifest currently contains an empty `entries` array. The production Coming Soon page therefore remains the only substantive public page.

## Executable Contract

The build-time contract is implemented by:

- `scripts/lib/publication-boundary.mjs` — validation and safe client projection;
- `scripts/verify-publication-boundary.mjs` — validates the real manifest;
- `scripts/publication-boundary.test.mjs`, `scripts/publication-date.test.mjs`, `scripts/publication-image-shape.test.mjs`, `scripts/publication-manifest-shape.test.mjs`, `scripts/publication-path-hardening.test.mjs`, and `scripts/publication-source-roots.test.mjs` — positive, negative, and path-hardening contract tests;
- `content/public/manifest.json` — the explicit public allowlist.

`npm run build` invokes `npm run verify:publication` first. Vercel therefore rejects a production build when the public manifest violates the boundary.

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

Unknown top-level, approval, and image fields are rejected so private notes cannot silently enter generated client data.

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

`toPublicArchiveEntry()` produces the object allowed to reach future page rendering. It excludes:

- `sourcePaths`;
- `publicationStatus`;
- the complete `approval` record;
- any undeclared fields.

The retained spoiler classification is limited by validation to `public` or `teaser` and may support future visitor-facing labels.

## Approval Workflow

1. Identify the owning canonical Markdown source or sources.
2. Draft a concise public title and summary separately from the internal source text.
3. Classify the exact projection as `public` or `teaser`.
4. Select only approved web imagery and write accurate alt text.
5. Obtain explicit author approval for the exact text, classification, relationships, and imagery.
6. Add the entry to `content/public/manifest.json` with the approval date.
7. Run `npm run verify`.
8. Review the generated branch preview before merging or exposing a route.

Changing an internal canonical source does not automatically update or authorize its public projection. Public summaries should be re-audited when owning sources materially change.

## Reserved Route Convention

Future archive records should use stable routes of the form:

`/archive/{entityType}/{slug}/`

No archive record routes are implemented in this milestone. The convention is reserved for review so content population and public navigation can remain separate, approval-gated work.

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
