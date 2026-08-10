# Aetherhaven Content Model Version 1 Handoff

**Goal:** Replace duplicated/hard-coded Archive record content with schema-governed canonical Markdown while preserving the approved C1 website layout, routes, public copy, map behavior, Hidden Archives behavior, accessibility, and fail-closed publication controls.

**Branch:** `schema/content-model-v1-audit`  
**Branch status:** **APPROVED / READY TO MERGE — DO NOT BEGIN BULK PROFILE MIGRATION ON THIS BRANCH**

## Approval status

- **APPROVED:** schema governance and the requirement that GitHub Markdown become the authoritative authored content source.
- **APPROVED:** preserve author publication control and the current website user experience during the source-of-truth realignment.
- **APPROVED / LOCKED:** Aetherhaven Content Schema Version `1.0.0`, explicitly approved by the author on 2026-08-10.
- **NEXT AUTHORIZED PHASE:** build executable validators, update templates, and pressure-test them against the locked schema.
- **NOT YET STARTED:** repository-wide profile migration, Version 2 publication-manifest cutover, Astro content-loader implementation, or removal of current hard-coded content sources.

## Work completed

- Audited final C1 production/publication architecture after Hermes completed the website pass.
- Confirmed the current public manifest inventories 95 approved projections: 67 ordinary records plus 28 Hidden Archive teasers.
- Audited publication validation, Archive presentation data, release controls, Preview loading, record routing, Open Catalog, Map Room, Hidden Archives, and record image handling.
- Audited current canonical Markdown families and representative records across characters, locations, organizations, artifacts, historical events, story arcs, and story drafts.
- Identified The Wayfinder as a first-class vessel record gap.
- Added `docs/development/AETHERHAVEN_CONTENT_MODEL_V1_AUDIT.md`.
- Expanded and then locked `docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md` as Version `1.0.0`.

## Locked architecture

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

## Locked Version 1 decisions

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

## Required next phase

1. Merge this schema/audit checkpoint into `main`.
2. Build executable Version 1 validators.
3. Update all canonical profile templates to emit the locked Version 1 structure.
4. Pressure-test representative records against the executable validator and templates.
5. Only after that prerequisite passes, create a focused migration branch for the repository-wide metadata migration.
6. Realign Astro/publication ingestion only after migrated Markdown validates and the C1 parity gate can be proven.

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