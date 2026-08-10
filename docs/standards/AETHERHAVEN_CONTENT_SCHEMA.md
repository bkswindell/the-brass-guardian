# Aetherhaven Content Schema

**Schema:** Aetherhaven Canon Content Model  
**Current version:** `0.1.0`  
**Status:** **DESIGN PHASE — GOVERNANCE ACTIVE / FIELD MODEL NOT YET FROZEN**  
**Authority:** Author-approved schema governance  
**Applies to:** Canonical Markdown, website content ingestion, public Archive projections, derived indexes, validators, and future tools that consume repository canon

> This document is the governing contract for the structured content model used by *The Brass Guardian / Aetherhaven* repository. The final Version 1 field dictionary will be completed only after the current Astro website implementation has been audited against the canonical Markdown and publication system. The change-control rules in this document are active now.

## 1. Purpose

The repository must maintain **one authoritative body of world content** rather than parallel copies of lore in Markdown, website source code, JSON catalogs, databases, or generated indexes.

The target architecture is:

```text
creator-approved canon and public-safe projections
                ↓
canonical Markdown + active canonical assets
                ↓
validated Aetherhaven content model
                ↓
Astro / tools / search / derived indexes / publication projection
```

Canonical content must not be maintained independently inside website code merely because the website needs structured data.

The website is a **consumer and presenter** of the repository's content model. It is not a second canon database.

## 2. Governing Principles

### 2.1 Canon Markdown owns world content

Canonical Markdown files remain the durable source of truth for approved characters, locations, organizations, artifacts, vessels, historical events, stories, story arcs, and other approved world records.

Structured metadata exists to make that canon reliably machine-readable. Metadata must not become a competing narrative layer that silently disagrees with the prose it describes.

### 2.2 Publication approval is separate from content

A record being canonical or containing public-safe fields does **not** itself authorize publication.

The public website must retain a separate fail-closed author-approval mechanism. The intended long-term role of the publication manifest or its successor is to act as an **approval ledger**, not as a duplicate content database.

An AI agent must never be able to publish a record merely by changing a canon file's visibility or classification metadata.

### 2.3 Presentation data is not automatically canon metadata

Website implementation details must remain website-side unless they describe a durable property of the fictional-world record itself.

Examples that normally remain presentation data:

- SVG hit regions for a raster map;
- pixel coordinates and responsive overlay geometry;
- CSS classes;
- animation timing;
- drawer order or panel layout;
- breakpoints and responsive image derivatives;
- route-transition behavior;
- Curator's Route ordering and other exhibition choreography, unless explicitly promoted to canon for a separate reason.

Examples that normally belong to the content model:

- stable record identity;
- canonical name and aliases;
- record type;
- canon status;
- canonical relationships;
- public-safe title or summary when explicitly approved as content;
- spoiler/publication classification;
- map reference number or letter when it is an in-world/cartographic fact;
- canonical asset references;
- historical chronology and uncertainty;
- archival catalog numbers and other in-world identifiers.

### 2.4 Derived data may be duplicated; authored content may not

Indexes, search documents, optimized images, route manifests, relationship graphs, sitemaps, cached projections, and build artifacts may be generated from the source model.

Generated output is disposable and must be reproducible from authoritative repository sources.

Do not hand-maintain derived files when they can be generated deterministically.

### 2.5 Stable identity outranks website presentation

A canonical entity must retain one stable identity regardless of where or how the Archive presents it.

A location does not become a different entity because the website places it in Hidden Archives. A character does not receive a second identity because a public projection is restricted. A district remains a location even if the website uses a specialized route or component for districts.

Website categories may project or subtype canonical entities; they must not create competing canonical identities.

## 3. Schema Authority and Change Control

Once Version 1.0.0 is declared **LOCKED**, this schema is infrastructure.

No AI agent, website implementation, build script, migration utility, or convenience refactor may change the schema contract unilaterally.

**The author must explicitly approve material schema changes.**

Agents may identify limitations, prepare proposals, estimate migration scope, and implement an approved migration. They may not silently add, rename, reinterpret, remove, or repurpose schema fields merely to make an implementation easier.

### 3.1 Valid reasons to propose a schema change

A schema change may be warranted when:

- an established canonical concept cannot be represented correctly;
- a first-class record type or relationship is genuinely missing;
- a field's current meaning is ambiguous enough to threaten canon integrity;
- publication or spoiler safety cannot be enforced reliably with the existing model;
- durable asset, chronology, provenance, or relationship information cannot be represented without duplication or loss;
- a new repository consumer has a durable content requirement that belongs to the content itself rather than to that consumer's presentation layer;
- validation reveals a structural defect that cannot be solved without modifying the contract.

### 3.2 Reasons that are not sufficient by themselves

Do not change the schema merely because:

- a component would be easier to write with another field;
- an agent prefers a different naming convention;
- a page needs temporary layout data;
- a JavaScript object currently uses a convenient property name;
- a new visual treatment needs CSS or geometric configuration;
- generated output would be simpler if canon were reshaped around it;
- an AI believes the alternative is more elegant;
- one isolated record could avoid a local adapter by adding global metadata.

Prefer adapters and presentation configuration over contaminating the canonical schema with consumer-specific implementation state.

## 4. Semantic Versioning

The locked schema will use semantic versioning.

### PATCH — `1.0.x`

Clarification or documentation change that does not alter valid structured data.

Examples:

- clarify wording;
- add examples;
- document an already-existing validation rule;
- correct a typo without changing field semantics.

**Migration requirement:** none.

### MINOR — `1.x.0`

Backward-compatible additive change.

Examples:

- add a genuinely useful optional field;
- add a new optional relationship attribute with a safe default;
- add an optional enum value that does not reinterpret existing values.

Existing compliant profiles must remain valid.

**Migration requirement:** targeted enrichment may occur, but a repository-wide rewrite is not required solely because the minor version changed.

### MAJOR — `x.0.0`

Breaking structural or semantic change.

Examples:

- rename or remove a field;
- change a field's meaning;
- change stable-ID semantics;
- make a previously optional field required;
- restructure relationships or assets incompatibly;
- split or merge record types in a way that changes existing interpretation;
- change publication/security semantics in a way that requires existing records to be reclassified.

**Migration requirement:** a migration plan, compatibility analysis, validation changes, repository migration, and post-migration audit are mandatory.

## 5. Required Schema-Change Lifecycle

Any proposed material change after schema lock follows this sequence:

1. **Identify the problem.** State what the existing schema cannot represent safely or accurately.
2. **Verify ownership.** Determine whether the requirement truly belongs to canon/content rather than website presentation, build output, or publication approval.
3. **Prepare a Schema Change Proposal.** Use `/templates/Aetherhaven_Schema_Change_Proposal.md`.
4. **Assess blast radius.** Identify record types, files, validators, Astro loaders, tests, publication controls, generated indexes, and tools affected.
5. **Consider alternatives.** Prefer a local adapter or presentation configuration when it avoids unnecessary schema expansion.
6. **Assign semantic version impact.** PATCH, MINOR, or MAJOR.
7. **Obtain explicit author approval.** Proposal status remains `PROPOSED` until approved.
8. **Update this document first.** The authoritative schema must describe the approved new contract before dependent code or profiles rely on it.
9. **Update validators and templates.** Validation and new-record templates must agree with the new contract.
10. **Migrate affected records.** Use deterministic automation where safe; flag substantive canon questions for human/creative review.
11. **Realign website ingestion.** Website code consumes the new schema rather than maintaining compatibility by silently duplicating content.
12. **Validate the whole repository.** No profile may remain unknowingly stranded between schema versions.
13. **Record completion and migration notes.** Future agents must be able to understand why the change occurred.

A schema proposal must not be implemented as accepted repository state before approval merely because a working branch makes experimentation possible.

## 6. Migration Safety Rules

### 6.1 Metadata migration must not rewrite canon prose unnecessarily

A deterministic metadata change may be automated when meaning is preserved.

Do not mechanically rewrite narrative sections, resolve open questions, invent missing facts, or reinterpret uncertain history merely to satisfy a new schema field.

When a migration exposes a substantive canon question, leave the record valid using an approved unresolved/unknown representation where possible and flag the question for author review.

### 6.2 No silent defaults that create facts

A validator or migration may supply technical defaults only when the schema explicitly defines them as non-semantic.

Do not default a character to public, an event to confirmed, a relationship to canonical, an image to approved, or a mystery to resolved merely because a value is absent.

Fail closed or preserve uncertainty.

### 6.3 One migration pass should leave one schema version

After a breaking migration is declared complete, active canonical profiles should not remain on mixed incompatible versions unless a documented transition mechanism explicitly supports it.

### 6.4 Rollback must be possible

Breaking migrations should be performed on a focused branch with a clear pre-migration base. Automated transformation should be reproducible and reviewable. Do not destroy information solely because the new schema no longer has the same field shape.

## 7. AI-Agent Rules

All agents working with structured canon must follow these rules:

- read this document before creating or modifying schema-governed metadata;
- do not introduce undocumented schema fields into canonical profiles;
- do not redefine an existing field locally for one file;
- do not copy canonical summaries or relationships into website code as a permanent source;
- do not treat website hard-coding as a reason to duplicate content into Markdown and JavaScript simultaneously;
- do not infer publication approval from canon status;
- do not expose internal relationships simply because both endpoints are canonical;
- do not change this schema without following the change-control lifecycle;
- when a consumer needs information that is not modeled, first determine whether the information is canon, publication approval, derived data, or presentation configuration;
- when uncertain, propose rather than expanding the schema silently.

## 8. Website Guardrails

The Astro website should ultimately load canonical records through a schema-aware ingestion layer such as Astro Content Collections or an equivalent build-time adapter.

The migration must preserve the approved Archive layout and user experience unless a separate design change is explicitly requested.

Website-side code may contain:

- rendering logic;
- route logic;
- presentation configuration;
- map interaction geometry;
- exhibition ordering;
- responsive behavior;
- accessibility behavior;
- derived caches or indexes;
- publication-gate enforcement.

Website-side code should not permanently own:

- canonical record names;
- canonical biographies or descriptions;
- canonical relationships;
- canonical location summaries;
- canonical organization summaries;
- spoiler classifications that belong to the record model;
- canonical asset descriptions;
- in-world map identifiers;
- duplicated public projection prose that already has an owning canonical record.

Temporary migration adapters are permitted when clearly marked and scheduled for removal.

## 9. Publication Boundary Guardrails

The current project intentionally uses a fail-closed public publication boundary.

The final content architecture must preserve or strengthen that property.

The preferred separation is:

```text
canonical record
    ↓
public-safe projection defined by the content model
    ↓
author approval ledger / publication fingerprint
    ↓
production website
```

The final schema audit must determine the precise approval-ledger design. A content record must not be able to self-authorize its own publication.

Where practical, publication approval should be invalidated when approved public-facing content materially changes. A deterministic projection hash or equivalent mechanism should be evaluated during the Version 1 design review.

## 10. Validation Requirements for Version 1

Before the repository-wide migration begins, the final schema must be capable of supporting validation for at least:

- allowed record types and subtypes;
- unique stable IDs;
- unique or intentionally scoped slugs;
- required fields by record type;
- enumerated canon/publication classifications;
- relationship target existence;
- relationship visibility/security rules;
- canonical asset path validity;
- map-reference validity;
- chronology representation and unresolved/disputed dates;
- source/provenance references where applicable;
- no references to `unused/` as active canon;
- schema-version compatibility;
- publication projection safety;
- separation of creator-only data from public output.

Validation should eventually run in CI and fail before malformed structured canon reaches production or becomes the basis for generated indexes.

## 11. Provisional Content Domains — Not Yet the Final Field Dictionary

The Version 1 audit is expected to determine the final representation for these domains:

- record identity and schema version;
- canonical name, aliases, title, and subtype;
- canon status and canonical scope;
- public-safe title, summary, tags, and classification;
- Archive section/access treatment;
- relationships and relationship visibility;
- canonical assets and public-safe asset presentation;
- map references;
- historical chronology, certainty, and temporal anomalies;
- provenance/source basis;
- artifact cataloging;
- story and story-arc metadata;
- publication approval linkage without self-authorization.

The presence of a domain in this list does **not** approve a particular field name or YAML structure. Do not begin the repository-wide metadata migration from this provisional list.

## 12. Version 1 Freeze Criteria

Version 1.0.0 must not be declared locked until all of the following have occurred:

1. Hermes completes the current website implementation pass.
2. The final website code is audited for every piece of content or metadata it consumes.
3. The current publication manifest and publication validator are reconciled with the source-of-truth design.
4. Canonical Markdown structures across all record families are inventoried.
5. Content, publication approval, derived data, and presentation-only data are explicitly separated.
6. Representative edge cases are modeled successfully.
7. The data dictionary is complete, including types, required/optional status, allowed values, ownership, public behavior, examples, and migration source.
8. Validators and templates can express the final contract.
9. The author explicitly approves the Version 1 schema.

## 13. Required Representative Records Before Repository-Wide Migration

The final schema must be pressure-tested against representative examples, including at minimum:

- **Amelia Hawthorne** — character;
- **The Clockwork Gardens** — location with hidden/restricted implications;
- **The Government District** — district/location subtype;
- **The Null Zone** — restricted location whose website treatment must not redefine its identity;
- **The Brass Watch** — organization;
- **The Aether Gauntlet: Exterior Study** — artifact with canonical image and transcription evidence;
- **The Wayfinder** — vessel / first-class-entity question;
- **The Clockwork Jungle Expedition** — historical event with unresolved chronology and restricted information;
- at least one story draft;
- at least one story arc;
- at least one placeholder profile;
- at least one record with creator-only relationships but a public-safe projection.

If these records require incompatible local exceptions, the schema is not ready to freeze.

## 14. Planned Version 1 Data Dictionary

**Not yet defined.**

This section will be completed after the website/content audit. It will define, for every approved field:

| Property | Definition |
|---|---|
| Field | Canonical field/path name |
| Type | String, enum, list, object, reference, date, etc. |
| Required | Universal, record-type-specific, optional, or conditional |
| Allowed values | Closed enum or validation rule where applicable |
| Owner | Canon content, publication approval, derived data, or presentation configuration |
| Public behavior | How the value may participate in a public projection |
| Example | Valid representative value |
| Migration source | Existing YAML, Markdown section, manifest field, website catalog field, or derived value |

No repository-wide profile migration begins until this section is complete and Version 1 is explicitly approved.

## 15. Change History

### 0.1.0 — 2026-08-10

**Status:** Governance approved; final field model pending.

Established:

- Markdown as the intended single authoritative content source;
- separation of canon content, publication approval, derived data, and presentation configuration;
- author approval requirement for material schema changes;
- semantic versioning and migration expectations;
- schema-change proposal workflow;
- AI-agent and website guardrails;
- Version 1 freeze criteria;
- representative-record pressure testing.

No canonical profile migration is authorized by this version.