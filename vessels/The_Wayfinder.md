---
schema_version: 1
id: AH-VESSEL-WAYFINDER
record_type: vessel
name: The Wayfinder
slug: wayfinder
aliases:
- Wayfinder
last_updated: '2026-08-10'
canon:
  status: canonical
  scope:
  - aetherhaven-volumes
development:
  status: working
disclosure:
  level: story-sensitive
provenance:
  sources:
  - kind: canonical-record
    ref: artifacts/007_The_Wayfinder_Technical_Plate.md
  - kind: canonical-record
    ref: locations/The_Gardens_Airship_Landing.md
  - kind: canonical-record
    ref: story_drafts/The_Brass_Guardian_and_the_Clockwork_Explorer.md
assets:
- id: reference-1
  path: art/Wayfinder_Above_the_Clouds.png
  role: reference
  visibility: public
  alt: The Wayfinder, a brass explorer airship with a silver envelope, sailing above sunlit clouds and mountain peaks.
vessel:
  class: explorer-airship
  status: active
public_projection:
  title: The Wayfinder
  summary: 'The Wayfinder is Elias and Amelia Hawthorne’s exploration airship: part vessel, part workshop, and part home above the clouds. She is frequently moored at the Gardens Airship Landing, where expedition equipment, repairs, and questions collect between journeys. Her hull shows the care of many voyages, and her systems combine practical engineering with older mechanisms that do not surrender their secrets easily. The Hawthornes trust her not merely as a machine, but as a companion.'
  classification: public
  archive_section: catalog
  access_label: public
  tags:
  - airship
  - exploration
  - hawthorne
  related:
  - AH-LOC-PLACEHOLDER-001
  - AH-LOC-AIRSHIP-LANDING
  image:
    asset: reference-1
    alt: The Wayfinder, a brass explorer airship with a silver envelope, sailing above sunlit clouds and mountain peaks.
relationships:
- target: AH-CHAR-001
  type: connected-to
  visibility: story-sensitive
- target: AH-CHAR-002
  type: connected-to
  visibility: story-sensitive
- target: AH-LOC-AIRSHIP-LANDING
  type: connected-to
  visibility: teaser
- target: AH-ART-007
  type: connected-to
  visibility: story-sensitive
- target: AH-LOC-PLACEHOLDER-001
  type: public-related
  visibility: teaser
---
# The Wayfinder

> **Canonical vessel profile.** This record owns the *Wayfinder* as a first-class vessel. The technical plate remains authoritative for the plate and visible technical evidence; location records remain authoritative for individual berths and facilities.

## Canonical Summary

The *Wayfinder* is [Professor Elias Hawthorne](../characters/Professor_Elias_Hawthorne.md) and [Amelia Hawthorne](../characters/Amelia_Hawthorne.md)'s exploration airship: part vessel, part workshop, and part home above the clouds.

She is frequently moored at [the Gardens Airship Landing](../locations/The_Gardens_Airship_Landing.md), where expedition equipment, repairs, and questions collect between journeys. Her hull shows the care of many voyages, and her systems combine practical engineering with older mechanisms that do not surrender their secrets easily.

The Hawthornes trust the *Wayfinder* not merely as a machine, but as a companion and home.

## Visual Reference

![The Wayfinder above the clouds](../art/Wayfinder_Above_the_Clouds.png)

## Relationships

- [Professor Elias Hawthorne](../characters/Professor_Elias_Hawthorne.md) — explorer, engineer, and keeper of the vessel.
- [Amelia Hawthorne](../characters/Amelia_Hawthorne.md) — explorer, mechanic, and resident aboard the vessel.
- [The Gardens Airship Landing](../locations/The_Gardens_Airship_Landing.md) — familiar home berth between expeditions.
- [The Wayfinder Technical Plate](../artifacts/007_The_Wayfinder_Technical_Plate.md) — authoritative artifact record for the existing technical plate.

## Continuity Notes

- This profile consolidates already-approved Wayfinder canon; it does not establish new specifications.
- The vessel is both transportation and a lived-in Hawthorne home.
- Older or unexplained mechanisms aboard the vessel should remain unexplained unless separately established.
- Technical artifact details belong in the linked artifact record rather than being duplicated here.

## Development Checklist

- [x] First-class vessel record established by Schema Version 1 migration.
- [x] Existing public projection preserved.
- [x] Existing canonical visual reference linked.
- [ ] Expand technical and operational details only as canon establishes them.
