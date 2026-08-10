# Aetherhaven Content Schema Version 1 — Semantic Migration Audit

**Audit date:** 2026-08-10  
**Schema:** `1.0.0 — LOCKED`

This pass runs after the deterministic legacy-field migration and corrects semantic issues that structural validation alone cannot detect. It uses the pre-migration `main` records only to recover already-existing metadata; it does not generate new canon.

## Summary

- Additional canonical relationships recovered: **0**
- Legacy fields fully modeled and removed from preservation notes: **23**
- Legacy fields partially modeled while preserving the original note: **2**
- Character asset roles corrected from assumed portrait to neutral reference: **0**
- Artifact catalog-number corrections/removals: **0**
- Story chronology states corrected to relative placement: **0**

## Catalog Number Corrections

- None.

## Partial Relationship Enrichment

- `characters/The_Hidden_Architect_Unassigned.md` — `unknown_to`: modeled 5 of 7; original preservation note retained.
- `organizations/The_Order_of_the_Mended_Hand.md` — `primary_connections`: modeled 12 of 13; original preservation note retained.

## Safety Rule

No unresolved or ambiguous value is promoted to a canonical-ID relationship. Partial or unresolved legacy content remains visible in the owning Markdown preservation notes until separately modeled or resolved.

