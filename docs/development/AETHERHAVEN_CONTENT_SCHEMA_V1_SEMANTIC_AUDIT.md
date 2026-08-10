# Aetherhaven Content Schema Version 1 — Semantic Migration Audit

**Audit date:** 2026-08-10  
**Schema:** `1.0.0 — LOCKED`  
**Migration branch:** `migration/content-schema-v1`

This audit records semantic and legacy-data corrections made after the deterministic front-matter migration. It exists because structural schema validation can prove shape and references, but cannot by itself prove that a value such as a catalog number, chronology classification, or asset role was interpreted correctly.

No new story canon was created by this audit.

## Summary

- Schema-governed records after migration: **210**
- Existing canonical records migrated: **209**
- New first-class vessel record created from already-approved canon: **1** (`vessels/The_Wayfinder.md`)
- Existing C1 public projections copied into their owning Markdown records: **95**
- Additional canonical relationships recovered from legacy metadata: **67**
- Legacy fields fully modeled and removed from preservation notes: **24**
- Legacy fields partially modeled while preserving the original note: **2**
- Character asset roles corrected from assumed portrait to neutral reference: **2**
- Artifact catalog-number corrections: **12**
- Story chronology states corrected to relative placement: **2**
- Missing active asset references after migration: **0**

## Legacy Syntax Repairs

Six existing profiles used the malformed YAML form `aliases:[]`. The migration normalized that exact syntax to `aliases: []` before strict parsing. No alias value changed.

Affected files:

- `characters/Beatrice_Pike.md`
- `characters/Euphemia_Pike.md`
- `characters/Keeper_Thirteen.md`
- `locations/Cloudspire.md`
- `locations/Dock_Zero.md`
- `locations/Pike_Bridge.md`

## Canonical-ID Collision Repair

Preflight found two existing location records using `AH-LOC-PLACEHOLDER-049`.

- `locations/Rootglass_Cloister.md` retains `AH-LOC-PLACEHOLDER-049` because it occupies the original sequential placeholder position between Mariners' Hall (`048`) and the later medical-location additions.
- `locations/The_Hall_of_Vital_Mechanics.md` receives the durable collision-repair ID `AH-LOC-HALL-VITAL-MECHANICS`.
- `locations/The_Cauldron_Recovery_House.md` retains its existing `AH-LOC-PLACEHOLDER-050`.

This is an identity-integrity repair required by Schema Version 1 uniqueness rules; it does not change the Hall's canon, name, or narrative content.

## Artifact Catalog-Number Corrections

The first migration pass exposed a Markdown-formatting bug in the legacy catalog-number extractor. The semantic pass accepts only exact in-body identifiers and corrected these artifact records:

- `artifacts/001_The_Hawthorne_Explorers_Crest.md` → `AH-1-001`
- `artifacts/002_Seal_of_the_Society_of_Explorers.md` → `SE-1-002`
- `artifacts/003_The_Six_Key_Sigil.md` → `AH-1-002`
- `artifacts/004_The_First_Mechanists_Mark.md` → `AH-1-003`
- `artifacts/007_The_Wayfinder_Technical_Plate.md` → `AH-1-006`
- `artifacts/009_The_Aether_Gauntlet_Exterior_Study.md` → `AH-1-004`
- `artifacts/011_Prototype_II_Cabinet_Photograph.md` → `AH-1-005`
- `artifacts/012_The_Missing_Prototype_I_Catalog_Card.md` → `AH-1-014`
- `artifacts/015_Botanical_Plate_of_the_Dream_Blossom.md` → `AH-1-006`
- `artifacts/018_The_Changing_Paths_of_the_Gardens.md` → `AH-1-008`
- `artifacts/021_Tamsin_Pikes_Brass_Key.md` → `AH-1-017`
- `artifacts/025_The_Passengers_Future_Dated_Ticket.md` → `AH-1-018`

The corrected values are derived from text already visible in the owning artifact records; no catalog identifier was invented.

## Relationship Enrichment

The semantic pass recovered **67** additional canonical-ID relationships from legacy fields that were recognizable but not part of the first generic mapping, including fields such as:

- `key_relationships`
- `primary_location`
- `affiliation` / `public_affiliation`
- `known_leadership`
- `primary_connections`
- `governing_body`
- `meeting_place`
- `member_guilds`
- `primary_guardian`
- `known_to` / `unknown_to`

Only unique, existing canonical targets were converted.

Two fields were only partially resolvable and therefore keep their original preservation note:

- `characters/The_Hidden_Architect_Unassigned.md` — `unknown_to`: 5 of 7 values resolve to canonical records.
- `organizations/The_Order_of_the_Mended_Hand.md` — `primary_connections`: 12 of 13 values resolve to canonical records.

## Asset Role Correction

Legacy `canonical_images` identified visual references but did not assert that the first character image was a dedicated portrait. The first migration pass inferred `portrait` for two character assets. The semantic audit changed those roles to neutral `reference` rather than inventing portrait semantics.

Public image selections are unaffected.

## Story Chronology Correction

Both canonical story drafts use relative placement in the series. A first-pass keyword heuristic mistakenly read the word “conflict” in one placement description as evidence of conflicting chronology. Both story records now correctly use:

`chronology.status: relative`

Their human-readable chronology text is unchanged.

## Preservation Rule

Values that cannot be mapped safely remain verbatim under `Schema Migration Preservation Notes` in the owning Markdown file. They are not discarded, silently normalized, or promoted to canonical-ID relationships by guesswork.

This preserves uncertainty until the relevant subject receives a canonical record or a later approved content/schema decision makes the relationship machine-resolvable.

## Validation Result

After the deterministic migration and semantic audit:

- all **210** records validate against the locked executable Schema Version 1 contract;
- canonical IDs are unique;
- slugs are unique;
- relationship targets resolve;
- public related-record targets are backed by public/teaser relationships;
- active asset paths resolve and do not use `unused/`;
- Aetherhaven map references are unique;
- all **95** currently approved C1 projections exist in owning Markdown records;
- the production website continues to use the existing C1 publication source during this phase, so this migration does not alter the live Archive presentation.
