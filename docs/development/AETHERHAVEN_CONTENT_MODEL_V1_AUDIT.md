# Aetherhaven Content Model Version 1 Audit

**Status:** COMPLETE IMPLEMENTATION AUDIT / SCHEMA CANDIDATE PREPARATION  
**Branch:** `schema/content-model-v1-audit`  
**Audit date:** 2026-08-10  
**Governing schema:** [`docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md`](../standards/AETHERHAVEN_CONTENT_SCHEMA.md)

## Purpose

This audit records the final website/content state that must be represented by the Version 1 Aetherhaven content model before any repository-wide Markdown migration begins.

The audit is intentionally about **data ownership and completeness**, not redesigning the approved Aetherhaven Archives user experience.

The target remains:

```text
canonical Markdown + active canonical assets
        ↓
schema-aware content ingestion
        ↓
public-safe projection
        ↓
separate author approval ledger
        ↓
existing Archive presentation and release controls
```

The website must stop serving as a second content database while preserving its current public behavior.

---

## 1. Final Website State Audited

The completed C1 implementation on `main` uses three distinct website data layers:

1. `website/content/public/manifest.json`
   - 95 author-approved public projections;
   - 67 ordinary catalog records;
   - 28 Hidden Archive teasers;
   - currently duplicates names, titles, summaries, source paths, classifications, access labels, relationships, tags, image data, approval data, and publication dates.

2. `website/content/public/archive-presentation.json`
   - 30 map interaction records covering references 1–24 and A–F;
   - SVG region geometry and label hitboxes;
   - eight Curator Route annotations;
   - author approval for this presentation configuration.

3. `website/content/public/archive-release.json`
   - explicit `published` / `sealed` release switch;
   - author approval date;
   - controls whether Hidden Archives are included.

Production renders only validated public manifests. Preview additionally loads proposal content from hard-coded JavaScript catalogs.

---

## 2. Current Public Manifest Inventory

The current approved manifest contains **95 records**.

### By current website entity type

| Website type | Count |
|---|---:|
| organization | 35 |
| character | 28 |
| location | 19 |
| district | 6 |
| archive-record | 6 |
| vessel | 1 |
| **Total** | **95** |

### By public safety classification

| Classification | Count |
|---|---:|
| public | 63 |
| teaser | 32 |

### By visitor access label

| Access label | Count |
|---|---:|
| public | 63 |
| restricted | 20 |
| mysterious | 6 |
| teaser | 4 |
| major spoiler | 1 |
| ultimate spoiler | 1 |

Only three current public records carry record-specific images in the manifest:

- Aetherhaven;
- the Clockwork Gardens;
- the Wayfinder.

The current manifest relationship graph is intentionally sparse: most entries have no `relatedEntryIds`, while a small set of featured records carries the approved C1 cross-links.

This sparse public cross-link set must be preserved exactly during migration rather than replaced automatically by every internal canon relationship.

---

## 3. Fields Currently Required by the Website

The current record manifest requires:

- `id`
- `slug`
- `entityType`
- `canonicalName`
- `publicTitle`
- `publicSummary`
- `sourcePaths`
- `publicationStatus`
- `spoilerClassification`
- `publicAccessLabel`
- `approval`
- `relatedEntryIds`
- `tags`
- `publicationDate`
- optional `image` with `src`, `alt`, `width`, and `height`

These fields do **not** all belong to the same owner.

### Target ownership classification

| Current field | Target owner |
|---|---|
| `id` | canonical Markdown stable identity |
| `slug` | canonical Markdown durable routing key |
| `entityType` | derived from canonical `record_type` / subtype |
| `canonicalName` | canonical Markdown `name` |
| `publicTitle` | canonical Markdown public projection |
| `publicSummary` | canonical Markdown public projection |
| `sourcePaths` | derived from owning canonical record; not duplicated |
| `publicationStatus` | publication approval/release system; not canon metadata |
| `spoilerClassification` | canonical Markdown public projection |
| `publicAccessLabel` | canonical Markdown public projection |
| `approval` | publication approval ledger |
| `relatedEntryIds` | canonical Markdown public projection, referencing canonical relationships |
| `tags` | canonical Markdown public projection |
| `publicationDate` | publication approval ledger |
| image `src` | derived website asset output |
| image `alt` | canonical Markdown public projection / selected asset metadata |
| image dimensions | derived from generated website asset |

---

## 4. Presentation Data That Must Stay Website-Side

The following are approved website presentation data and must **not** be copied into canonical front matter:

- SVG map-circle coordinates;
- map-label rectangle coordinates;
- percentage map positions used by presentation code;
- responsive zoom behavior;
- CSS and layout details;
- Archive room background treatment;
- Curator Route order;
- Curator Route visitor labels and notes;
- the Map Room route step;
- presentation approval metadata;
- release switch state;
- responsive image derivative filenames and widths.

`archive-presentation.json` is therefore a legitimate durable website configuration file. It is not a second canon database when it contains only presentation data keyed to canonical record IDs.

### Map reference distinction

The **fact** that the Gearbreaker Mines are map reference `22`, or the Null Zone is reference `F`, belongs to canonical Markdown.

The **pixel geometry** that makes that printed region clickable belongs to the website presentation manifest.

The target presentation validator should resolve the map marker from canonical content rather than hand-maintaining the marker in both places.

---

## 5. Current Hard-Coded Content That Must Be Removed

### `website/src/lib/archive-catalog.mjs`

Currently owns duplicate public records for:

- 24 numbered map locations;
- six restricted map locations;
- public characters;
- public organizations;
- hidden characters;
- hidden organizations.

This file duplicates canonical names, summaries, source paths, classifications, tags, and IDs. It must cease to be a content source.

### `website/src/lib/archive-preview.mjs`

Currently hard-codes featured public projections for:

- Aetherhaven;
- Clockwork Gardens;
- Gardens Airship Landing;
- Merchant District;
- Inventors’ District;
- Aerial Docks;
- Wayfinder.

It also hard-codes the Curator Route definition before merging it with catalog data.

After migration, Preview must consume the **same Markdown public projections** as production. The difference between Preview and production is author approval, not a second body of text.

### Record page responsive image table

`website/src/pages/archive/[entityType]/[slug].astro` currently contains an ID-keyed `responsiveSources` object for the three illustrated records.

This is acceptable only as a temporary implementation. Record-specific responsive image data should be generated from the selected canonical asset and build output so adding a fourth illustrated record does not require editing an Astro component.

---

## 6. Current Astro Page Consumers

### Public Archive entrance

`website/src/pages/archive/index.astro` consumes:

- record title;
- public summary;
- record type;
- tags;
- map marker;
- public access label / classification;
- route slug;
- Curator Route title/label/note/href.

Search currently indexes only public title plus public tags.

Record-class filter buttons are currently hard-coded for location, district, character, organization, and vessel. Future implementation should derive available filter classes from the loaded public dataset while preserving the present labels and layout.

### Record viewer

`website/src/pages/archive/[entityType]/[slug].astro` consumes:

- stable ID;
- slug;
- website entity type;
- canonical name;
- public title;
- public summary;
- access label / classification;
- public tags;
- selected image plus alt/dimensions;
- map marker;
- public related records;
- Curator Route membership.

### Map Room

`website/src/pages/archive/map/index.astro` consumes:

- public title;
- map reference;
- record route or Hidden Archive anchor;
- presentation geometry;
- Archive section/public-vs-hidden placement.

The canonical map reference and website geometry must be joined by stable canonical ID.

### Hidden Archives

`website/src/pages/archive/hidden/index.astro` currently assumes three groups:

- restricted map locations;
- hidden characters;
- hidden organizations.

The target loader should classify records from structured metadata rather than from the special `hidden-archive` tag. The current group headings and UX may remain unchanged for the present dataset.

---

## 7. Current Canonical Markdown Families

The repository already contains distinct Markdown record families with partly inconsistent YAML conventions.

### Characters

Common current fields include:

- type-specific `character_id`;
- `name`;
- `title`;
- aliases;
- canon status and scope;
- primary locations;
- affiliations;
- key connections;
- temporal relevance;
- source basis;
- canonical images.

Hidden profiles additionally use fields such as spoiler level, public identity, former role, and current role.

### Locations

Common current fields include:

- `location_id`;
- `name`;
- descriptive `type`;
- aliases;
- canon status and scope;
- jurisdiction;
- access status;
- map category and reference;
- parent location;
- primary connections;
- points of interest;
- temporal relevance;
- source basis;
- canonical images.

### Organizations

Common current fields include:

- `organization_id`;
- `name`;
- descriptive `type`;
- aliases;
- canon status and scope;
- headquarters;
- jurisdiction;
- leadership;
- governing authority in some records;
- key relationships;
- source/cross-link data;
- canonical images;
- temporal relevance.

### Artifacts

Common current fields include:

- `artifact_id`;
- original slate number;
- name;
- category;
- canon status;
- image status;
- source and source scope;
- transcription status;
- related Markdown;
- canonical images.

The in-world archival catalog number is conceptually distinct from the internal `artifact_id` and must remain distinct in Version 1.

### Historical events

Common current fields include:

- `historical_event_id`;
- name and aliases;
- descriptive event type;
- canon status and scope;
- date status;
- chronology;
- locations;
- participants;
- organizations;
- artifacts;
- story arcs;
- public/restricted record status;
- institutional interest;
- source basis.

### Story arcs

Common current fields include:

- `story_arc_id`;
- title;
- canon status and scope;
- primary characters, locations, organizations, and artifacts;
- related Markdown;
- canonical images;
- temporal relevance.

Actual story arcs also contain specialized variants such as `primary_character`, `primary_protagonist`, and `related_story_drafts`.

### Story drafts

Current story-draft metadata includes:

- `story_draft_id`;
- title and subtitle;
- title status;
- canon status;
- proposed book and placement;
- chronology;
- primary characters and locations;
- primary connections;
- source basis;
- last-updated date;
- cover and inline artwork with placement instructions.

### Vessels

The website already treats **The Wayfinder** as a first-class vessel, but the repository does not yet contain a dedicated vessel-owning canonical Markdown profile. Its public record currently cites the Wayfinder technical artifact and Gardens Airship Landing.

Version 1 therefore needs a first-class `vessel` record family, and the migration needs to create an owning Wayfinder profile from already-approved canon without inventing new vessel lore.

---

## 8. Identity Findings

The website currently creates parallel IDs such as:

- `character-amelia-hawthorne`;
- `restricted-null-zone`;
- `hidden-character-first-mechanist`.

Canonical Markdown already has stable IDs such as:

- `AH-CHAR-002`;
- `AH-LOC-PLACEHOLDER-027`;
- the relevant First Mechanist canonical ID.

Version 1 must use **one canonical identity**.

Website placement must never create a second identity. A restricted location remains the same location; a hidden character remains the same character.

Existing public URLs are protected by `slug`, not by the current website-only ID. The internal public IDs can therefore be migrated to canonical IDs without changing visitor URLs.

Existing canonical IDs containing words such as `PLACEHOLDER` remain stable unless the author separately approves an ID migration. Completion of a placeholder profile is not sufficient reason to change its ID.

---

## 9. Type Findings

Current website `entityType` mixes canonical subject type with presentation behavior.

Version 1 should separate them.

### Canonical record types

Candidate stable record families:

- `character`
- `location`
- `organization`
- `artifact`
- `vessel`
- `historical_event`
- `story`
- `story_arc`

A canonical story draft is a `story` with working/development metadata rather than a permanent separate ontology.

A district is a `location` subtype.

A restricted map location is still a `location`.

`archive-record` is a website presentation category and should not become a canonical record type merely because Hidden Archives uses drawer presentation.

Public website route/entity categories can be **derived** from canonical type and subtype so current routes such as `/archive/district/.../` remain unchanged.

---

## 10. Public Projection Findings

The exact C1 public copy should move into the owning canonical Markdown files under a clearly separated **public projection** object.

A public projection is not the same thing as the complete canonical record.

It should contain only deliberately reader-safe material needed to generate the current Archive record:

- public title;
- public summary;
- `public` or `teaser` classification;
- visitor access label;
- Archive section (`catalog` or `hidden`);
- public-safe tags;
- the exact curated public related-record set;
- optional selected canonical asset and public alt text.

Presence of a public projection **must not publish the record**.

Preview may render an unapproved projection for author review. Production may render it only when a separate approval-ledger entry matches its deterministic fingerprint.

---

## 11. Relationship Findings

Internal canonical relationships and public website cross-links are related but not identical.

Version 1 needs:

1. a canonical relationship graph using stable canonical IDs;
2. disclosure level on each relationship;
3. a curated public-related list that must reference safe canonical relationships.

This allows the full internal graph to be richer than the public website without either duplicating relationship facts in JavaScript or accidentally exposing a hidden connection.

Backlinks should be generated. They should not require manually maintaining reciprocal relationship entries unless the reverse relationship carries distinct meaning.

---

## 12. Asset Findings

Canonical Markdown currently uses flat image paths while the public website uses generated WebP derivative paths and dimensions.

Version 1 should store structured **canonical asset references** in Markdown:

- local asset ID;
- active repository source path;
- role;
- disclosure level;
- meaningful alt text;
- optional caption or story-placement instruction.

The website should derive:

- WebP/AVIF derivatives;
- dimensions;
- responsive `srcset` values;
- final public URLs.

A public projection selects an asset by local asset ID instead of hand-maintaining a derivative URL.

Publication fingerprinting should incorporate the selected source asset’s content digest so silently replacing an approved image invalidates the approval.

Presentation-only images that are not canonical record assets may remain in website presentation configuration.

---

## 13. Chronology Findings

Aetherhaven chronology cannot safely be reduced to ISO dates.

Version 1 needs an optional structured chronology object that can represent:

- exact dates;
- approximate dates;
- ranges;
- relative chronology;
- disputed chronology;
- unknown dates;
- anomalous or contradictory temporal evidence.

Human-readable in-world dates remain strings.

An optional internal sort key may support timelines without claiming that uncertain dates are exact.

Conflicting accounts must be representable as separate accounts rather than overwritten by one normalized date.

---

## 14. Publication Approval Findings

The current manifest correctly fails closed, but it duplicates the content being approved.

Target Version 2 of `website/content/public/manifest.json` should become an **approval ledger** only.

A candidate entry should contain approximately:

```json
{
  "id": "AH-CHAR-002",
  "projectionHash": "sha256:<digest>",
  "approvedBy": "author",
  "approvedOn": "2026-08-10",
  "publicationDate": "2026-08-10"
}
```

The projection hash should cover every public-facing value derived from Markdown, including the digest of any selected canonical public asset.

Production must fail if:

- a projection changed after approval;
- a selected asset changed after approval;
- an approved ID no longer resolves;
- an approved relationship target is no longer approved;
- an approved projection violates the public schema.

The existing global `archive-release.json` remains a separate release switch.

---

## 15. Astro Ingestion Findings

There is currently no `website/src/content.config.ts`.

The target implementation should introduce a schema-aware Astro content collection or equivalent build-time loader over the repository canonical roots.

A practical target is one logical `canon` collection loaded from the repository roots so all relationships resolve through one stable canonical-ID namespace.

Candidate source roots after migration:

- `characters/`
- `locations/`
- `organizations/`
- `artifacts/`
- `vessels/`
- `historical_events/`
- `story_arcs/`
- `story_drafts/` or a later normalized story root

The content model remains technology-neutral even if Astro/Zod is used as the executable website validator.

---

## 16. Representative Pressure Tests

The candidate Version 1 model was checked conceptually against the required representative records.

| Representative record | Required capabilities confirmed |
|---|---|
| Amelia Hawthorne | stable identity, title/aliases, relationships, public projection, assets, disclosure separate from public copy |
| Clockwork Gardens | placeholder development state, map reference, public projection, location subtype, relationships |
| Government District | location with `district` subtype while preserving `/archive/district/.../` route behavior |
| Null Zone | same location identity despite restricted map treatment; map `F`; Hidden Archive public projection |
| Brass Watch | organization jurisdiction plus richer internal relationships and simpler public projection |
| Aether Gauntlet Exterior Study | artifact internal ID, separate archival catalog number, production/transcription metadata, canonical plate asset |
| Wayfinder | new first-class vessel owner; existing artifact and berth become relationships rather than co-owning public content |
| Clockwork Jungle Expedition | unresolved chronology, participants, restricted/public record distinction, story connections |
| Day Aboard the Wayfinder | story title/subtitle/status, relative chronology, cover and placed inline assets |
| Keeper of Dreams | canonical story arc with delayed-reveal disclosure and linked story/location/character records |
| source-grounded placeholder | canonical authority separated from profile completion status |
| Silas Rook | creator/story-sensitive full profile with only a deliberately minimal teaser projection |

No representative case requires a second website content database.

---

## 17. Required Website Realignment After Schema Approval

After Version 1 is locked and Markdown migration is complete, the website implementation should:

1. load canonical Markdown through the schema-aware content loader;
2. derive the Preview catalog from Markdown public projections;
3. derive production projections from the same Markdown data;
4. replace the current full public manifest with the approval-ledger format;
5. change presentation-manifest IDs to canonical IDs;
6. resolve map markers from canonical cartography metadata while retaining geometry website-side;
7. remove hard-coded lore from `archive-catalog.mjs` and `archive-preview.mjs`;
8. remove the record-page hard-coded responsive image table;
9. derive image output metadata from the asset pipeline;
10. make catalog type filters data-driven while retaining current UX;
11. make Hidden Archive grouping data-driven while retaining current UX;
12. preserve the current 67 record routes, 28 closed Hidden Archive drawers, 30 map links, eight-stop Curator Route, layout, accessibility behavior, and release controls;
13. prove that the final generated public projection is materially equivalent to the currently approved C1 projection unless the author separately approves content changes.

---

## 18. Audit Conclusion

The final website pass confirms the original architecture decision:

**Canonical Markdown should become the only authored record source.**

The website still needs two non-canonical durable configuration layers:

- presentation configuration;
- publication/release approval.

Those layers are not duplicate canon when they contain only information that belongs to presentation or approval.

The Version 1 schema must therefore govern four explicitly different ownership domains:

1. canonical content;
2. public projection content stored with its owning canonical record;
3. publication approval;
4. website presentation / derived output.

The next step is to complete the candidate field dictionary in `AETHERHAVEN_CONTENT_SCHEMA.md` and present Version 1 for explicit author approval. **No canonical profile migration is authorized by this audit alone.**
