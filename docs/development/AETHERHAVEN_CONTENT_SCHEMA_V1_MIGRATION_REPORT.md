# Aetherhaven Content Schema Version 1 — Migration Report

**Migration date:** 2026-08-10  
**Schema:** `1.0.0 — LOCKED`  
**Branch:** `migration/content-schema-v1`

## Summary

- Schema-governed records discovered: **210**
- Legacy records migrated: **0**
- First-class records created: **0**
- Existing Version 1 records encountered: **210**
- Current C1 public projections copied into owning Markdown: **0**
- Unresolved relationship-like legacy values preserved in prose: **0**
- Other legacy fields preserved in prose: **0**
- Missing/invalid legacy asset references skipped: **0**

The migration rewrote front matter only, except when a legacy structured value could not be converted safely. Such values were appended verbatim under `Schema Migration Preservation Notes` in the owning Markdown record rather than being discarded or interpreted.

## Public Projection Preservation

The exact current C1 `publicTitle`, `publicSummary`, classification, access label, tags, related-record set, slug, and selected image context were copied from the approved Version 1 website manifest into each owning canonical record as `public_projection`. Publication approval remains in the existing website manifest until the later Version 2 ledger cutover.

## Created First-Class Records


## Slug Adjustments for Non-Public Records

- `story_arcs/The_Disappearance_of_Prototype_I.md`: `the-disappearance-of-prototype-i` → `the-disappearance-of-prototype-i-story-arc`

## Preserved Unresolved Legacy Relationship Values

- None.

## Other Preserved Legacy Fields

- None.

## Skipped Legacy Asset References

- None.

## Scope Fallbacks

- None.

## Validation State

- Ruby migration checks require unique IDs/slugs, resolved relationship targets, safe public relationships, and existing active asset files.
- The workflow exports every migrated metadata object and runs the repository’s locked JavaScript `validateCanonRecords()` implementation over the complete set.
- Website publication/Preview parity is **not** cut over in this migration; the existing C1 website data sources remain active until the later source-of-truth realignment passes the explicit C1 parity gate.

