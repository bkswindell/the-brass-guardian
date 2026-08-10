# Aetherhaven Content Schema Version 1 — Migration Report

**Migration date:** 2026-08-10  
**Schema:** `1.0.0 — LOCKED`  
**Branch:** `migration/content-schema-v1`

## First-Pass Migration Summary

- Schema-governed records discovered: **210**
- Legacy records migrated: **209**
- First-class records created: **1**
- Existing Version 1 records encountered at first pass: **0**
- Current C1 public projections copied into owning Markdown: **95**
- Relationship-like legacy values that could not be safely converted during the first generic pass and were preserved verbatim for later semantic review: **96**
- Other nonblank legacy fields preserved verbatim for later semantic review: **75**
- Missing/invalid active asset references skipped: **0**

The migration rewrote structured front matter and preserved the existing Markdown narrative body. When a legacy structured value could not be converted safely, the value was retained under `Schema Migration Preservation Notes` instead of being discarded or guessed.

The follow-up semantic audit subsequently recovered additional safe relationships and normalized semantic issues. See [`AETHERHAVEN_CONTENT_SCHEMA_V1_SEMANTIC_AUDIT.md`](AETHERHAVEN_CONTENT_SCHEMA_V1_SEMANTIC_AUDIT.md) for the final review.

## Public Projection Preservation

All **95** currently approved C1 projections were copied from the existing publication manifest into their owning canonical Markdown records as `public_projection` without creative rewriting.

The migration preserved:

- public title;
- public summary;
- public/teaser classification;
- visitor access label;
- public-safe tags;
- approved related-record set, mapped to canonical IDs;
- current public slug;
- selected public image context.

Publication approval itself remains separate. The existing website manifest continues to control production until the later Version 2 approval-ledger cutover passes the C1 parity gate.

## First-Class Record Created

- `vessels/The_Wayfinder.md`

The Wayfinder record consolidates already-approved vessel canon distributed across the technical plate, Gardens Airship Landing, Hawthorne profiles, and canonical story draft. No new vessel specifications were invented.

## Non-Public Slug Collision

One internal slug collision was resolved deterministically:

- `story_arcs/The_Disappearance_of_Prototype_I.md`: `the-disappearance-of-prototype-i` → `the-disappearance-of-prototype-i-story-arc`

The public URL set is unchanged.

## Legacy Data Preservation

The first generic conversion deliberately failed closed when a value did not resolve to one unique canonical record. This included unresolved people, unnamed groups, places that do not yet have their own records, uncertain affiliations, descriptive relationship text, and development-only fields.

Those values were retained in their owning Markdown rather than silently discarded. The semantic follow-up pass converted additional fields only when the existing pre-migration data resolved safely and uniquely.

## Validation State

The migration workflow requires:

- unique canonical IDs;
- unique slugs;
- valid locked Version 1 record shapes;
- valid canon/development/disclosure states;
- resolvable canonical relationship targets;
- safe public-related relationships;
- valid active asset paths outside `unused/`;
- valid and unique Aetherhaven cartography references;
- valid chronology structures;
- valid public projections.

The complete migrated metadata set is exported transiently and validated with the repository's locked `validateCanonRecords()` implementation before migration output is accepted.

## Website Boundary

This phase does **not** change the production Archive data source. The existing C1 manifest, presentation manifest, and release controls remain active until the subsequent Astro/publication realignment reproduces the current public release exactly.
