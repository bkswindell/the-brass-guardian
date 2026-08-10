# Aetherhaven Content Schema Version 1 — Semantic Migration Audit

**Audit date:** 2026-08-10  
**Schema:** `1.0.0 — LOCKED`

This pass runs after the deterministic legacy-field migration and corrects semantic issues that structural validation alone cannot detect. It uses the pre-migration `main` records only to recover already-existing metadata; it does not generate new canon.

## Summary

- Additional canonical relationships recovered: **67**
- Legacy fields fully modeled and removed from preservation notes: **24**
- Legacy fields partially modeled while preserving the original note: **2**
- Character asset roles corrected from assumed portrait to neutral reference: **2**
- Artifact catalog-number corrections/removals: **12**
- Story chronology states corrected to relative placement: **2**

## Catalog Number Corrections

- `artifacts/001_The_Hawthorne_Explorers_Crest.md`: `- **The Hawthorne Explorer’s Crest**

### Printed description

> Family crest and expedition seal of Professor Elias Hawthorne and the Hawthorne line. Commonly found on documents, instrument cases, field journals, and the Wayfinder.

### Recovery information

- **DATE DISCOVERED:**` → `AH-1-001`
- `artifacts/002_Seal_of_the_Society_of_Explorers.md`: `- **Seal of [the Society of Explorers](../organizations/The_Society_of_Explorers.md)**

### Printed description

> Official seal of [the Society of Explorers](../organizations/The_Society_of_Explorers.md) of [Aetherhaven](../locations/Aetherhaven.md). Impression found on authenticated expedition documents, charter licenses, and field dispatches. First issued in the Year 769 A.H. Current iteration adopted in the Year 1043 A.H.

### Recovery information

- **DATE RECOVERED:**` → `SE-1-002`
- `artifacts/003_The_Six_Key_Sigil.md`: `- **The Six-Key Sigil**

### Printed description

> Ancient symbol discovered carved into basalt slab beneath debris field in the Null Zone, Sector F-12. Associated with references to the “Six Keys” in early Aetherhaven texts. Purpose unknown.

### Recovery and condition information

- **DATE DISCOVERED:**` → `AH-1-002`
- `artifacts/004_The_First_Mechanists_Mark.md`: `- **The First Mechanist’s Mark**

### Printed description

> Maker’s mark attributed to the First Mechanist, legendary architect of the Heart Engine and creator of the Six Keys.

> Found on machines, structures, documents, and stone throughout Aetherhaven and beneath.

### Recovery and condition information

- **DATE DISCOVERED:**` → `AH-1-003`
- `artifacts/007_The_Wayfinder_Technical_Plate.md`: `- **The Wayfinder**
- **HAWTHORNE MODEL W-7A • EXPLORER CLASS AIRSHIP**

### Quotation

> “Not just a machine, but a companion.”  
> “She has carried us farther than any map.”  
> — A. Hawthorne

### Specifications

- **Length:**` → `AH-1-006`
- `artifacts/009_The_Aether_Gauntlet_Exterior_Study.md`: `- **The Aether Gauntlet — Exterior Study**

### Printed description

> Primary interface and receptacle for the Aether Heart. Designed and constructed by Prof. Elias Hawthorne for his daughter, Amelia Hawthorne. Purpose: Channel, protect, and amplify Aetheric power through precision mechanisms.

### Quotation

> “It is not merely a machine, but a bridge between flesh and force.”  
> — E.H.

### Date tag

- **DATE:**` → `AH-1-004`
- `artifacts/011_Prototype_II_Cabinet_Photograph.md`: `### Cabinet label

> **PROTOTYPE II**  
> Property of Aetherhaven Academy  
> For Study and Preservation Only

### Catalog data card

- **DESIGNATION:**` → `AH-1-005`
- `artifacts/012_The_Missing_Prototype_I_Catalog_Card.md`: `- **RECORD TYPE:**` → `AH-1-014`
- `artifacts/015_Botanical_Plate_of_the_Dream_Blossom.md`: `### Specimen card

- **SPECIMEN:**` → `AH-1-006`
- `artifacts/018_The_Changing_Paths_of_the_Gardens.md`: `- **The Changing Paths of the Gardens**
- **THREE SURVEYS OF AETHERHAVEN’S [CLOCKWORK GARDENS](../locations/The_Clockwork_Gardens.md)**

### Introductory statement

> The layout of the paths is not static but follows unknown laws. When aligned to true north, the arrangement of the third survey forms [the Six-Key Sigil](003_The_Six_Key_Sigil.md).

### Survey I

- **SURVEY I**
- **Pre-Rising**
-` → `AH-1-008`
- `artifacts/021_Tamsin_Pikes_Brass_Key.md`: `- **TAMSIN PIKE’S BRASS KEY**

### Family identification

- **Family Heirloom — Pike Line**
-` → `AH-1-017`
- `artifacts/025_The_Passengers_Future_Dated_Ticket.md`: `- **TITLE:**` → `AH-1-018`

## Partial Relationship Enrichment

- `characters/The_Hidden_Architect_Unassigned.md` — `unknown_to`: modeled 5 of 7; original preservation note retained.
- `organizations/The_Order_of_the_Mended_Hand.md` — `primary_connections`: modeled 12 of 13; original preservation note retained.

## Safety Rule

No unresolved or ambiguous value is promoted to a canonical-ID relationship. Partial or unresolved legacy content remains visible in the owning Markdown preservation notes until separately modeled or resolved.

