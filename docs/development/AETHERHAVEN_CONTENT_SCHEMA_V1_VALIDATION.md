# Aetherhaven Content Schema Version 1 — Validation and Template Gate

**Schema:** `1.0.0 — LOCKED`  
**Status:** **PASS — BULK-MIGRATION PREREQUISITE SATISFIED**  
**Validation date:** 2026-08-10  
**Branch:** `schema/content-model-v1-validation`

## Purpose

This checkpoint proves that the locked Version 1 content contract has an executable validator, reusable templates for every Version 1 record family, and representative automated pressure tests before any repository-wide canonical-profile migration begins.

## Executable Validator

`website/scripts/lib/canon-schema-v1.mjs` validates parsed Version 1 canonical-record metadata and enforces the locked contract, including:

- schema major version;
- stable canonical ID shape;
- closed canonical record types;
- durable slugs and real metadata dates;
- separate canon, development, and disclosure semantics;
- allowed top-level fields;
- provenance shape;
- canonical-ID relationships and relationship disclosure;
- active asset metadata and `unused/` exclusion;
- cartography reference rules;
- chronology and disputed-account representation;
- type-specific extension ownership;
- public-projection fields and safe-related-record constraints;
- public image selection from public/teaser assets;
- repository-wide duplicate ID/slug checks;
- relationship-target existence;
- unique Aetherhaven map references.

The validator is dependency-free and accepts already-parsed front matter objects. The later Astro/content-ingestion layer will parse Markdown and pass its structured data through this contract rather than redefining schema semantics.

## Pressure Tests

`website/scripts/canon-schema-v1.test.mjs` exercises representative Version 1 shapes for:

- Amelia Hawthorne — character;
- Professor Elias Hawthorne — character relationship target;
- The Wayfinder — first-class vessel;
- The Null Zone — restricted mapped placeholder with Hidden Archive teaser;
- The Government District — location with district subtype;
- The Brass Watch — organization;
- The Aether Gauntlet: Exterior Study — artifact with separate canonical ID and in-world catalog number;
- The Clockwork Jungle Expedition — historical event with unresolved relative chronology;
- *A Day Aboard the Wayfinder* — story;
- *The Keeper of Dreams* — delayed-reveal story arc;
- Silas Rook — creator-only full record with a narrow public teaser.

Negative tests explicitly reject:

- `archive-record` as a canonical record type;
- `district` as a canonical record type;
- unsafe creator-only relationships exposed through `public_projection.related`;
- active assets under `unused/`;
- malformed cartography;
- duplicate canonical IDs, slugs, and Aetherhaven map references;
- unknown top-level fields that would silently drift the schema.

## Template Coverage

All eight locked record families now have reusable Version 1 templates:

- `templates/Character_Profile_Template.md`
- `templates/Location_Profile_Template.md`
- `templates/Organization_Profile_Template.md`
- `templates/Artifact_Profile_Template.md`
- `templates/Historical_Event_Profile_Template.md`
- `templates/Story_Profile_Template.md`
- `templates/Story_Arc_Profile_Template.md`
- `templates/Vessel_Profile_Template.md`

`website/scripts/canon-schema-v1-templates.test.mjs` verifies that all eight templates declare Version 1, use the correct record type, use the safe proposed/creator-only new-record defaults, and do not retain legacy top-level ID/status/image fields.

## Build Gate

`website/package.json` now runs:

```text
prebuild
  → verify:content-schema
  → verify:publication
  → build
```

This means schema/template regressions fail before the existing publication-boundary validation and before Astro production output is generated.

## Verification Result

GitHub/Vercel reported **success** for the branch head after the new prebuild gate was introduced. Therefore:

- Version 1 schema pressure tests passed;
- Version 1 template tests passed;
- the existing publication-boundary verification still passed;
- the website build still completed successfully;
- no public Archive content or UX change was required.

## Migration Authorization Boundary

This PASS satisfies the locked schema's validator/template prerequisite for beginning the controlled metadata migration.

It does **not** authorize creative rewriting of canon or public copy. The migration must:

- preserve existing canonical meaning;
- preserve exact approved C1 public projections unless the author separately approves edits;
- preserve stable public routes;
- fail closed on unclear disclosure/publication decisions;
- maintain the C1 parity gate before website cutover;
- create the first-class Wayfinder vessel record only from already-approved source material.

The next work should occur on a dedicated migration branch created from the verified `main` checkpoint after this validation PR is merged.
