# Aetherhaven Content Model Version 1 Handoff

**Goal:** Replace duplicated/hard-coded Archive record content with schema-governed canonical Markdown while preserving the approved C1 website layout, routes, public copy, map behavior, Hidden Archives behavior, accessibility, and fail-closed publication controls.

**Branch:** `schema/content-model-v1-audit`  
**Branch status:** **AWAITING AUTHOR REVIEW — DO NOT BEGIN BULK PROFILE MIGRATION**

## Approval status

- **APPROVED:** schema governance and the requirement that GitHub Markdown become the authoritative authored content source.
- **APPROVED:** preserve author publication control and the current website user experience during the source-of-truth realignment.
- **CANDIDATE / AWAITING AUTHOR APPROVAL:** the complete Version 1 field contract now documented as schema `0.2.0`.
- **NOT YET AUTHORIZED:** repository-wide profile migration, Version 2 publication-manifest cutover, Astro content-loader implementation, or removal of current hard-coded content sources.

## Work completed

- Audited final C1 production/publication architecture after Hermes completed the website pass.
- Confirmed the current public manifest is the exact user-supplied 95-record manifest and inventories 67 ordinary records plus 28 Hidden Archive teasers.
- Audited publication validation, Archive presentation data, release controls, Preview loading, record routing, Open Catalog, Map Room, Hidden Archives, and record image handling.
- Audited current canonical Markdown families and representative records across characters, locations, organizations, artifacts, historical events, story arcs, and story drafts.
- Identified The Wayfinder as a first-class vessel record gap.
- Added `docs/development/AETHERHAVEN_CONTENT_MODEL_V1_AUDIT.md`.
- Expanded `docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md` to Version `0.2.0`, a complete Version 1 candidate field model.

## Candidate architecture

```text
canonical Markdown
    + public_projection in owning record
        ↓
schema-aware Astro ingestion
        ↓
Version 2 approval ledger with projection hash
        ↓
existing Archive presentation manifest
        ↓
existing published/sealed release switch
        ↓
public website
```

## Major candidate decisions

- One canonical ID per subject; website-hidden/public placement does not create another identity.
- Universal canonical record types: character, location, organization, artifact, vessel, historical_event, story, story_arc.
- District is a location subtype; restricted locations remain locations.
- Canon authority, profile maturity, and spoiler sensitivity are separate fields.
- Canonical relationships become stable-ID references with disclosure levels.
- Public cross-links remain explicitly curated and do not automatically expose all canon relationships.
- Active canonical art becomes structured asset metadata; responsive derivatives remain generated website data.
- Canonical map reference belongs in Markdown; map hit geometry stays website-side.
- Chronology supports exact, approximate, range, relative, disputed, unknown, and anomalous states without forcing ISO fictional dates.
- The 95 current C1 public projections move into owning Markdown unchanged during migration.
- Publication approval moves to a minimal hash-based ledger; public projections cannot self-authorize.
- Asset bytes participate in the public projection fingerprint when an image is selected.
- Preview and production consume the same Markdown public projection; only approval differs.

## Required next step

1. Author reviews Version `0.2.0` candidate.
2. Resolve any field-model concerns.
3. On explicit author approval, promote the document to `1.0.0 — LOCKED`.
4. Update executable validators/templates to the locked contract.
5. Only then begin the repository-wide metadata migration and website source-of-truth realignment on a focused migration branch.

## Important migration parity gate

The eventual cutover must preserve, absent separate author-approved content changes:

- all 95 current approved projections;
- 67 standalone public record routes;
- 28 closed Hidden Archive teaser drawers;
- 30 direct map links;
- eight Curator Route stops;
- current slugs and visitor routes;
- approved public titles, summaries, classifications, labels, tags, relationships, and images;
- current production indexability, Preview `noindex`, and sealed rollback behavior.

## Files changed on this branch

- `docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md`
- `docs/development/AETHERHAVEN_CONTENT_MODEL_V1_AUDIT.md`
- `agents/gpt/HANDOFF_CONTENT_MODEL_V1.md`

No canonical profile or website production source has been changed on this branch.
