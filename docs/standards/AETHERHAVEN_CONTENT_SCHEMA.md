# Aetherhaven Content Schema

**Schema:** Aetherhaven Canon Content Model  
**Current version:** `1.0.0`  
**Status:** **LOCKED — AUTHOR APPROVED**  
**Authority:** Author-approved Version 1 schema contract  
**Applies to:** Canonical Markdown, website content ingestion, public Archive projections, derived indexes, validators, and future tools that consume repository canon

> This document is the governing contract for structured content in *The Brass Guardian / Aetherhaven* repository. The website/content audit is complete and the Version 1 field contract was explicitly approved by the author on 2026-08-10. **Bulk profile migration may begin only after executable validators and templates are updated to this locked contract.**

See [`docs/development/AETHERHAVEN_CONTENT_MODEL_V1_AUDIT.md`](../development/AETHERHAVEN_CONTENT_MODEL_V1_AUDIT.md) for the implementation audit that produced this schema.

---

## 1. Purpose

The repository must maintain **one authoritative body of authored world content** rather than parallel copies of lore in Markdown, website source code, JSON catalogs, databases, or generated indexes.

The target architecture is:

```text
creator-approved canon
        ↓
canonical Markdown + active canonical assets
        ↓
validated Aetherhaven content model
        ↓
public-safe projection stored with the owning record
        ↓
separate author approval ledger
        ↓
Astro / search / indexes / public Archive
```

The website is a **consumer and presenter** of the repository's content model. It is not a second canon database.

---

## 2. Four Ownership Domains

Every structured value must belong to one of four domains.

### 2.1 Canon content

Facts or durable editorial metadata about the fictional world and its owning record.

Examples:

- stable record identity;
- canonical name and aliases;
- subject type;
- canon authority and development state;
- canonical relationships;
- map reference number or letter;
- chronology and uncertainty;
- artifact catalog number;
- canonical asset references;
- provenance/source basis.

**Owner:** canonical Markdown.

### 2.2 Public projection content

Deliberately reader-safe text and metadata derived from, but narrower than, the full canon record.

Examples:

- public title;
- public summary;
- `public` versus `teaser` classification;
- public visitor access label;
- public-safe tags;
- curated public related-record links;
- selected public-safe canonical image.

**Owner:** the same canonical Markdown file under `public_projection`.

A public projection is **not publication approval**.

### 2.3 Publication approval

The creator's authorization to publish an exact projection.

Examples:

- approved record ID;
- deterministic public-projection hash;
- approval date;
- first publication date;
- release switch.

**Owner:** website publication ledger/release controls.

Canonical content must never self-authorize publication.

### 2.4 Presentation and derived data

Technical or exhibition information that does not describe the fictional subject itself.

Examples:

- SVG map hit geometry;
- Curator Route ordering and notes;
- CSS/layout values;
- responsive derivative filenames;
- generated image dimensions;
- search indexes;
- sitemaps;
- route manifests;
- cached relationship graphs.

**Owner:** website presentation configuration or generated build output.

Derived output must be disposable and reproducible from authoritative sources.

---

## 3. Governing Principles

### 3.1 Canonical Markdown owns authored content

Canonical Markdown remains the durable source for approved characters, locations, organizations, artifacts, vessels, historical events, stories, story arcs, and public projections of those records.

Do not maintain an independent copy of that content in JavaScript, JSON, a CMS, a database, or generated output.

### 3.2 One canonical identity per subject

A canonical entity retains one stable `id` regardless of how the Archive presents it.

A location does not receive a new identity because it is placed in Hidden Archives. A district remains a location. A hidden character remains the same character. Website categories may project canonical records but may not create competing canonical identities.

### 3.3 Public projection is narrower than the source record

A full internal profile may be story-sensitive while still carrying a small safe teaser.

The existence of a safe public projection does not imply that the rest of the file is public.

### 3.4 Publication fails closed

Production may render a public projection only when a separate author-approved ledger entry matches the current deterministic projection fingerprint.

Changing front matter cannot by itself publish content.

### 3.5 Presentation requirements do not automatically change the schema

A frontend convenience is not sufficient reason for a new canonical field.

Use adapters, presentation configuration, or derived data when the requirement belongs to a consumer rather than the world model.

### 3.6 Stable fields; flexible vocabularies where appropriate

The schema keeps the structural contract strict while allowing safe vocabularies such as relationship type, asset role, subtype, and provenance kind to use lowercase kebab-case strings.

This prevents routine world growth from requiring a schema revision merely to add a new relationship label or location subtype.

---

## 4. Schema Authority and Change Control

Version `1.0.0` is **LOCKED** and is infrastructure.

No AI agent, website implementation, build script, migration utility, or convenience refactor may change the schema contract unilaterally.

**The author must explicitly approve material schema changes.**

Agents may identify limitations, prepare proposals, estimate migration scope, and implement an approved migration. They may not silently add, rename, reinterpret, remove, or repurpose schema fields.

### 4.1 Valid reasons to propose a schema change

A change may be warranted when:

- an established canonical concept cannot be represented correctly;
- a genuinely new first-class record family is needed;
- current semantics threaten canon integrity;
- publication/spoiler safety cannot be enforced with the existing model;
- durable asset, chronology, provenance, or relationship information cannot be represented without loss;
- a new consumer has a durable requirement that belongs to content rather than presentation;
- validation exposes a structural defect that cannot be solved by an adapter.

### 4.2 Insufficient reasons by themselves

Do not change the schema merely because:

- a component is easier to write with another field;
- an agent prefers another naming convention;
- a page needs temporary layout data;
- JavaScript currently uses another property name;
- a visual treatment needs coordinates or CSS configuration;
- generated output would be easier if canon mirrored the frontend;
- an isolated record could avoid a small adapter by expanding the global schema.

### 4.3 Required proposal

After lock, use `/templates/Aetherhaven_Schema_Change_Proposal.md` for any material schema change.

---

## 5. Semantic Versioning

The governing document uses semantic versioning.

### PATCH — `1.0.x`

Clarification or documentation only. Valid data does not change.

**Repository migration:** none.

### MINOR — `1.x.0`

Backward-compatible additive change.

Examples:

- genuinely useful optional field;
- optional nested property;
- new optional enum value that does not reinterpret existing values.

**Repository migration:** targeted enrichment only when useful; existing compliant records remain valid.

### MAJOR — `x.0.0`

Breaking structural or semantic change.

Examples:

- rename/remove field;
- change field meaning;
- change stable-ID semantics;
- make an optional field required;
- incompatible relationship/asset restructuring;
- redefine record families;
- alter publication/security semantics in a way that requires reclassification.

**Repository migration:** mandatory migration plan, implementation, validation, and post-migration audit.

### Record-level `schema_version`

Canonical Markdown records store only the compatible **major** schema version:

```yaml
schema_version: 1
```

PATCH and MINOR documentation changes therefore do not require touching every profile solely to change a version string.

---

# PART I — VERSION 1 CANONICAL RECORD CONTRACT

## 6. Canonical Record Roots

Version 1 recognizes these canonical record families:

- `characters/`
- `locations/`
- `organizations/`
- `artifacts/`
- `vessels/`
- `historical_events/`
- `story_arcs/`
- `story_drafts/` during the initial migration

The initial migration adds `vessels/` and creates an owning Wayfinder record from already-approved canon.

`media_reactions/`, `/agents/proposals/`, `unused/`, templates, development documents, compiled exports, and website files are not canonical content records under this schema.

---

## 7. Closed Canonical `record_type` Values

Version 1 canonical record types are:

- `character`
- `location`
- `organization`
- `artifact`
- `vessel`
- `historical_event`
- `story`
- `story_arc`

### Important distinctions

- A **district** is `record_type: location` with `subtype: district`.
- A restricted location remains `record_type: location`.
- A canonical story draft is `record_type: story` with appropriate development metadata.
- `archive-record` is a website presentation category, not a canonical record type.
- `rumor` is not a Version 1 canonical family. A future durable need for a standalone rumor family must be evaluated rather than preemptively expanding the ontology.

Adding a new first-class `record_type` after lock is at least a MINOR schema change and may be MAJOR if it changes existing interpretation.

---

## 8. Universal Required Fields

Every schema-governed canonical Markdown record must contain these fields after migration.

| Field | Type | Required | Owner | Validation / meaning | Migration source |
|---|---|---|---|---|---|
| `schema_version` | integer | yes | schema | Must be `1` for Version 1 records. | new |
| `id` | string | yes | canon | Unique immutable canonical ID. Preserve existing canonical IDs. | type-specific `*_id` |
| `record_type` | enum | yes | canon | One of the eight Version 1 record types. | directory/template type |
| `name` | string | yes | canon | Canonical subject name/title. | `name` or story/arc `title` |
| `slug` | string | yes | durable routing | Lowercase kebab-case; globally unique among active records. | generated from current public slug or canonical name |
| `aliases` | list[string] | yes | canon | May be empty. | existing `aliases` or `[]` |
| `last_updated` | ISO date | yes | repository metadata | `YYYY-MM-DD`. | existing `last_updated` |
| `canon` | object | yes | canon | Authority and scope; see below. | `canon_status`, `canonical_scope` |
| `development` | object | yes | editorial metadata | Profile maturity; see below. | current status wording / placeholder state |
| `disclosure` | object | yes | editorial safety | Maximum sensitivity of the full record. | hidden/spoiler status + manual review |

### Optional universal fields

| Field | Type | Owner | Meaning |
|---|---|---|---|
| `subtype` | kebab-case string | canon | Machine-readable subtype such as `district`; open vocabulary. |
| `descriptor` | string | canon/editorial | Human-readable subject classification preserving useful current `type` text. |
| `provenance` | object | canon/editorial | Source basis. |
| `relationships` | list[object] | canon | Structured canonical links. |
| `assets` | list[object] | canon/visual canon | Active canonical assets. |
| `cartography` | list[object] | canon | In-world/cartographic references; normally locations. |
| `chronology` | object | canon/editorial | Exact, relative, disputed, or anomalous chronology. |
| `public_projection` | object | public projection | Reader-safe candidate projection. Presence never authorizes publication. |
| `character` | object | canon/editorial | Character-specific fields. |
| `location` | object | canon | Location-specific fields. |
| `organization` | object | canon | Organization-specific fields. |
| `artifact` | object | canon | Artifact-specific fields. |
| `historical_event` | object | canon/editorial | Historical-event-specific archival status. |
| `story` | object | editorial/canon | Story-specific metadata. |
| `vessel` | object | canon | Vessel-specific metadata. |
| `production` | object | production metadata | Artifact/image production workflow fields. |

Unknown top-level fields are invalid after migration unless the schema is changed through the approved process.

---

## 9. Stable Canonical Identity

### 9.1 `id`

`id` is the durable canonical identity.

Rules:

- unique across every canonical record family;
- immutable once established except through an explicitly approved migration;
- may contain uppercase letters, digits, and hyphens following existing `AH-*` conventions;
- website placement does not alter it;
- completion of a placeholder does not alter it;
- internal IDs such as `AH-ORG-PLACEHOLDER-004` remain stable even when the profile later becomes complete, unless the author separately approves an ID migration.

The migration replaces type-specific keys such as:

- `character_id`
- `location_id`
- `organization_id`
- `artifact_id`
- `historical_event_id`
- `story_arc_id`
- `story_draft_id`

with universal `id`.

### 9.2 `slug`

`slug` is a durable routing/search key, not a fictional-world identity.

Rules:

- lowercase kebab-case;
- globally unique among active records;
- stable after public publication whenever practical;
- a slug change after publication requires redirect/route review and public-projection reapproval, but does not by itself change canonical identity.

Existing public URLs must be preserved during migration.

---

## 10. `canon` Object

```yaml
canon:
  status: canonical
  scope:
    - aetherhaven-volumes
```

### Fields

| Field | Type | Required | Allowed values / rule |
|---|---|---|---|
| `status` | enum | yes | `canonical`, `proposed`, `superseded` |
| `scope` | list[string] | yes | lowercase kebab-case scope labels; may be empty only for `proposed` |

### Meaning

`canon.status` expresses **authority**, not completeness or secrecy.

Examples:

- a source-grounded placeholder that preserves approved facts → `canonical`;
- a canonical story draft with working wording → `canonical`;
- a hidden antagonist profile approved by the author → `canonical`;
- unapproved creative material → `proposed` and should normally remain outside active canon roots;
- retained record explicitly replaced by later canon → `superseded`.

Do not encode `hidden`, `working`, `placeholder`, `draft`, or `long-range` inside `canon.status`.

---

## 11. `development` Object

```yaml
development:
  status: working
  temporal_relevance: very-high
```

### Fields

| Field | Type | Required | Allowed values |
|---|---|---|---|
| `status` | enum | yes | `complete`, `working`, `placeholder`, `concept` |
| `temporal_relevance` | enum | no | `none`, `low`, `moderate`, `high`, `very-high`, `critical`, `unresolved` |

`development.status` describes how complete the profile is, independently of whether its existing contents are canon.

Mapping examples:

- `Canonical working profile` → canon `canonical`, development `working`;
- `Source-grounded placeholder` → canon `canonical`, development `placeholder`;
- `Canonical future story concept` → canon `canonical`, development `concept`;
- completed finalized profile → canon `canonical`, development `complete`.

---

## 12. `disclosure` Object

```yaml
disclosure:
  level: story-sensitive
```

### `level` values

- `public`
- `teaser`
- `story-sensitive`
- `creator-only`

This field classifies the **full canonical record**, not its public projection.

A record with `disclosure.level: creator-only` may still carry a deliberately tiny `public_projection` teaser if the author wants the existence of the subject revealed without exposing the file.

Migration of `disclosure.level` requires review. Do not infer that an entire source file is public merely because the current website publishes a safe summary of it.

---

## 13. `provenance` Object

```yaml
provenance:
  sources:
    - kind: manuscript
      ref: Aetherhaven v3.pdf
    - kind: author-decision
      ref: 2026-08-10 Archive canon approval
```

### Source fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `kind` | kebab-case string | yes | Open controlled vocabulary. |
| `ref` | string | yes | Repository path, source label, decision reference, or external citation label. |
| `note` | string | no | Clarification only. |

Recommended `kind` values include:

- `manuscript`
- `canonical-record`
- `author-decision`
- `artwork`
- `artifact-evidence`
- `external`

Adding a new provenance `kind` does **not** require a schema change when it conforms to the open kebab-case rule.

Existing `source_basis`, `source`, and `source_scope` migrate here where appropriate.

---

## 14. `relationships` — Canonical Knowledge Graph

```yaml
relationships:
  - target: AH-CHAR-001
    type: father
    visibility: public
  - target: AH-ORG-SECRET-001
    type: interest-from
    visibility: creator-only
```

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `target` | canonical ID | yes | Must resolve to an active canonical record. |
| `type` | kebab-case string | yes | Directional open vocabulary. |
| `visibility` | enum | yes | Same four values as `disclosure.level`. |
| `note` | string | no | Internal clarification; never public automatically. |

### Rules

- Relationship types are directional.
- Backlinks are generated; reciprocal entries are not required unless the reverse relation carries different meaning.
- A relationship target must exist.
- Do not create placeholder relationship targets solely to satisfy a link unless the subject genuinely deserves a record.
- Open relationship vocabulary prevents routine new relationship labels from forcing schema changes.
- `public_projection.related` must be a subset of relationship targets whose relationship visibility is `public` or `teaser`.

Existing `primary_locations`, `affiliations`, `key_connections`, `headquarters`, `leadership`, `governing_authority`, `primary_connections`, `points_of_interest`, event participants, story entities, `related_markdown`, and similar structured links should migrate into this graph where they reference actual canonical records.

Unresolved names without an owning record remain in prose until a record exists.

---

## 15. `assets` — Active Canonical Assets

```yaml
assets:
  - id: primary-portrait
    path: art/characters/Example.png
    role: portrait
    visibility: public
    alt: Portrait of Example Character in established Aetherhaven reference style.
```

### Asset fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `id` | kebab-case string | yes | Unique within the owning record. |
| `path` | repository-relative path | yes | Active asset; must not resolve under `unused/`. |
| `role` | kebab-case string | yes | Open vocabulary such as `portrait`, `plate`, `map`, `cover`, `inline`, `reference`. |
| `visibility` | enum | yes | `public`, `teaser`, `story-sensitive`, `creator-only`. |
| `alt` | string | yes | Neutral meaningful visual description. |
| `caption` | string | no | Optional reusable caption. |
| `placement` | string | no | Optional story/production placement instruction. |

### Rules

- Canonical records contain only active project assets appropriate to that record.
- Candidate/rejected visual experiments remain outside canonical asset metadata until approved.
- A public projection may select only an asset whose visibility is `public` or `teaser`.
- Website derivative filenames, widths, heights, `srcset`, formats, and optimization details are generated data and do not belong here.
- A selected asset’s source-file digest participates in publication fingerprinting.

Existing `canonical_images` and story `artwork` migrate into structured assets.

---

## 16. `cartography` — Canonical Map References

A record may appear on more than one map, so cartography is a list.

```yaml
cartography:
  - map_id: aetherhaven-city
    category: numbered
    reference: "22"
```

Restricted example:

```yaml
cartography:
  - map_id: aetherhaven-city
    category: restricted
    reference: F
```

Unlisted interior example:

```yaml
cartography:
  - map_id: aetherhaven-city
    category: unlisted
    parent_reference: "11"
```

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `map_id` | kebab-case string | yes | Stable map identity, e.g. `aetherhaven-city`. |
| `category` | enum | yes | `numbered`, `restricted`, `unlisted`. |
| `reference` | string | conditional | Required for numbered/restricted; omitted for unlisted. |
| `parent_reference` | string | no | May identify the mapped parent of an unlisted interior/site. |

### Rules

- Map reference is canon/content.
- Pixel geometry is presentation data.
- `map_reference_category` and `map_number` migrate here.
- The website presentation manifest joins geometry to canonical map records by canonical ID and resolves the marker from this content rather than owning a second copy.

---

## 17. `chronology` — Time Without False Precision

Aetherhaven chronology may be exact, relative, disputed, contradictory, or anomalous.

```yaml
chronology:
  status: relative
  display: Before Volume 1
```

Disputed example:

```yaml
chronology:
  status: disputed
  display: Date unresolved
  accounts:
    - label: civic-record
      value: Seven civic months elapsed
      certainty: confirmed
    - label: shipboard-account
      value: Nineteen days elapsed aboard
      certainty: confirmed
```

### Fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `status` | enum | yes when chronology exists | `exact`, `approximate`, `range`, `relative`, `disputed`, `unknown`, `anomalous` |
| `display` | string | yes | Human-readable chronology without forced ISO conversion. |
| `sort_key` | integer | no | Internal ordering aid only; omission preserves uncertainty. |
| `accounts` | list[object] | no | Conflicting or parallel chronology accounts. |
| `note` | string | no | Context. |

Account fields:

- `label`: non-empty string;
- `value`: non-empty string;
- `certainty`: `confirmed`, `probable`, `disputed`, or `unknown`;
- `note`: optional string.

### Rules

- Never invent an exact date to satisfy sorting.
- Conflicting accounts remain separate.
- ISO dates are used only for real repository metadata such as `last_updated` and publication approval dates, not forced onto fictional chronology.

Existing historical `date_status`, event `chronology`, and story placement chronology migrate here.

---

# PART II — RECORD-TYPE EXTENSIONS

## 18. Character Extension

Optional `character` object:

```yaml
character:
  titles:
    - The Clockwork Explorer
  age_status: Exact series chronology unresolved
  public_identity: Known explorer
  former_roles: []
  current_roles: []
```

Fields:

- `titles`: list[string]
- `age_status`: optional string
- `public_identity`: optional string
- `former_roles`: optional list[string]
- `current_roles`: optional list[string]

Existing character `title`, `age_status`, `public_identity`, `former_role`, and `current_role` migrate here.

Locations, affiliations, and character connections migrate to `relationships`.

---

## 19. Location Extension

Optional `location` object:

```yaml
location:
  jurisdiction:
    - Aetherhaven Archives
  access_status:
    - Open Archive
    - Public access
```

Fields:

- `jurisdiction`: optional list[string]
- `access_status`: optional list[string]

`subtype: district` identifies civic districts.

Parent location, governing organizations, recurring characters, and points of interest migrate to relationships.

**Important:** `location.access_status` describes in-world access. It is not the same field as website `public_projection.access_label`.

---

## 20. Organization Extension

Optional `organization` object:

```yaml
organization:
  jurisdiction:
    - Official civic records and historical collections
  access_classes:
    - Open Archives
    - Scholarly Archives
    - Restricted Archives
    - Hidden Archives
    - Lost Archives
```

Fields:

- `jurisdiction`: optional list[string]
- `access_classes`: optional list[string]

Headquarters, leadership, governing authority, institutional allies/rivals, and other record relationships migrate to `relationships`.

`access_classes` is available for organizations such as the Aetherhaven Archives whose internal access taxonomy is itself a durable institutional property. It does not control website publication.

---

## 21. Artifact Extension

Optional `artifact` object:

```yaml
artifact:
  category: Amelia and the Aether Gauntlet
  catalog_number: AH-1-004
```

Fields:

- `category`: optional string
- `catalog_number`: optional string

### Identity distinction

- `id` is the repository's stable canonical record identity.
- `artifact.catalog_number` is an in-world archival/catalog identifier visible on or assigned to the artifact.

They must not be conflated.

### Production metadata

Artifact production workflow moves to optional `production`:

```yaml
production:
  slate_number: 9
  image_status: image-linked
  visual_transcription_status: complete
```

Fields:

- `slate_number`: optional integer
- `image_status`: optional kebab-case/string status
- `visual_transcription_status`: optional kebab-case/string status

The artifact body remains authoritative for visible plate transcription and visual-only evidence.

---

## 22. Historical Event Extension

Optional `historical_event` object:

```yaml
historical_event:
  public_record_status: simplified and incomplete
  restricted_record_status: fragmented, contradictory, and partly withheld
```

Fields:

- `public_record_status`: optional string
- `restricted_record_status`: optional string

Participants, locations, organizations, related artifacts, story arcs, and institutional interest migrate to `relationships`.

Chronology uses the universal `chronology` object.

---

## 23. Story Extension

Canonical story drafts use `record_type: story`.

Optional `story` object:

```yaml
story:
  subtitle: A Day Aboard the Wayfinder
  title_status: Working title
  proposed_book: Book One
  proposed_placement:
    - Opening story
    - First chapter
```

Fields:

- `subtitle`: optional string
- `title_status`: optional string
- `proposed_book`: optional string
- `proposed_placement`: optional list[string]

Characters, locations, artifacts, and other connections migrate to relationships.

Cover and inline artwork migrate to `assets`, using `role` and optional `placement`.

Story chronology uses the universal chronology object.

---

## 24. Story Arc

Story arcs use:

```yaml
record_type: story_arc
```

No additional required namespace is needed in Version 1.

The existing arc premise, progression, emotional stakes, resolution requirements, and open questions remain in Markdown prose.

Primary characters, locations, organizations, artifacts, story drafts, and other dependencies migrate to `relationships`.

Delayed-reveal or hidden status is represented by `disclosure`, not by changing the record type.

---

## 25. Vessel Extension

Version 1 introduces first-class vessels.

Optional `vessel` object:

```yaml
vessel:
  class: explorer-airship
  status: active
```

Fields:

- `class`: optional kebab-case/string
- `status`: optional kebab-case/string

Ownership, crew, home berth, technical artifacts, and recurring locations are relationships.

### Wayfinder migration rule

The migration creates a dedicated Wayfinder canonical record from already-approved material currently distributed across the technical artifact, Gardens Airship Landing, characters, and story draft.

Do not invent new Wayfinder specifications merely to populate optional vessel fields.

---

# PART III — PUBLIC PROJECTION CONTRACT

## 26. `public_projection`

A canonical record may optionally carry one public projection.

```yaml
public_projection:
  title: Amelia Hawthorne
  summary: >-
    Amelia Hawthorne is a young mechanic and apprentice explorer who lives and
    travels aboard the Wayfinder with her father, Professor Elias Hawthorne.
  classification: public
  archive_section: catalog
  access_label: public
  tags:
    - character
  related: []
```

### Required fields when `public_projection` exists

| Field | Type | Allowed values / rule | Migration source |
|---|---|---|---|
| `title` | string | non-empty | current `publicTitle` |
| `summary` | string | non-empty | current `publicSummary` |
| `classification` | enum | `public` or `teaser` only | current `spoilerClassification` |
| `archive_section` | enum | `catalog` or `hidden` | current normal/Hidden placement; replaces `hidden-archive` tag semantics |
| `access_label` | string | non-empty, max 40 chars | current `publicAccessLabel` |
| `tags` | list[string] | unique public-safe strings | current public `tags` |
| `related` | list[canonical ID] | unique; must be safe relationships | current `relatedEntryIds` mapped to canonical IDs |

Optional:

```yaml
public_projection:
  image:
    asset: primary-map
    alt: Optional context-specific override
```

Image fields:

- `asset`: required local asset ID when image exists;
- `alt`: optional public-context override; otherwise use asset `alt`.

### Rules

- Presence does not mean approved or published.
- `classification` is only `public` or `teaser`; full-file secrecy belongs to `disclosure`.
- `archive_section` is **website/editorial placement**, not an in-world Aetherhaven Archives access class.
- `related` is intentionally curated. Do not expose every safe internal relationship automatically.
- Every `related` target must exist in canonical relationships and have `visibility` `public` or `teaser`.
- Production additionally requires every related target to have a matching approved projection ledger entry.
- A selected image asset must be `public` or `teaser` visibility.
- Public projection text may be more concise than the canonical summary/body and may intentionally withhold deeper facts.

---

## 27. Public Website Entity Type Is Derived

`entityType` is not stored as duplicate public content.

The website derives its presentation category from canonical data.

| Canonical record | Derived current public category |
|---|---|
| `character` | `character` |
| `location` + `subtype: district` | `district` |
| other ordinary `location` | `location` |
| hidden/restricted location drawer | treated as location content; website may use drawer presentation without changing canonical type |
| `organization` | `organization` |
| `artifact` | `artifact` |
| `vessel` | `vessel` |
| `historical_event` | `event` |
| `story` | `story` |
| `story_arc` | no public category required until a public projection needs one; implementation may use an Archive presentation adapter rather than changing canonical type |

Current visitor-facing URLs must remain stable during the migration. District routes therefore continue to use `/archive/district/{slug}/` even though district is canonically a location subtype.

---

## 28. Exact C1 Projection Preservation

The current published C1 manifest contains 95 author-approved projections.

During migration:

- copy the current approved public title, summary, classification, access label, tags, relationships, and image selection into the owning Markdown `public_projection` without creative rewriting;
- map current website-only IDs to canonical IDs;
- do not expand or reduce the current public related-record set unless separately approved;
- do not silently replace public stubs with richer internal canon text;
- do not reinterpret Hidden Archive teaser copy;
- preserve existing slugs and public routes;
- prove that the generated public output is materially equivalent before replacing the current manifest architecture.

This is a data-source migration, not an automatic public-copy rewrite.

---

# PART IV — PUBLICATION APPROVAL AND PRESENTATION

## 29. Publication Manifest Version 2 — Approval Ledger

Target `website/content/public/manifest.json` Version 2 contains approvals, not duplicate record content.

Candidate shape:

```json
{
  "schemaVersion": 2,
  "entries": [
    {
      "id": "AH-CHAR-002",
      "projectionHash": "sha256:<digest>",
      "approvedBy": "author",
      "approvedOn": "2026-08-10",
      "publicationDate": "2026-08-10"
    }
  ]
}
```

### Ledger fields

| Field | Type | Required | Rule |
|---|---|---|---|
| `id` | canonical ID | yes | Must resolve to exactly one canonical record with `public_projection`. |
| `projectionHash` | SHA-256 string | yes | Must match current deterministic public projection. |
| `approvedBy` | string | yes | Must be `author`. |
| `approvedOn` | ISO date | yes | `YYYY-MM-DD`. |
| `publicationDate` | ISO date | yes | Preserve current publication date; update only when intentionally republished as a new first-publication event if policy later requires. |

Unknown ledger fields are rejected.

### No `publicationStatus`

An entry's presence with a valid matching hash is the per-record approval. Global release state remains separate.

---

## 30. Publication Fingerprint

The public projection fingerprint is a deterministic SHA-256 over a normalized object containing every reader-facing value derived from the canonical record.

At minimum it covers:

- canonical ID;
- slug;
- derived public entity type/category;
- canonical name shown publicly;
- public title;
- public summary;
- classification;
- access label;
- Archive section;
- public tags;
- public related canonical IDs;
- selected public image asset ID;
- selected image alt text;
- cryptographic digest of the selected source asset bytes.

It does **not** include:

- creator-only notes;
- source provenance not rendered publicly;
- unrelated internal relationships;
- Markdown prose outside the projection;
- presentation geometry;
- generated derivative filenames.

### Result

- Editing internal canon without changing the public projection does not automatically revoke publication.
- Editing any public-facing field does revoke the matching approval until the author approves the new fingerprint.
- Replacing an approved selected image at the same path also revokes approval because its asset digest changes.

---

## 31. Release Manifest

`website/content/public/archive-release.json` remains a separate release control.

Its current `published` / `sealed` semantics and fail-closed production behavior should remain unless a separately approved publication architecture change is proposed.

Record approval and release state solve different problems:

- ledger: **is this exact projection approved?**
- release manifest: **should the approved Archive currently be exposed?**

---

## 32. Archive Presentation Manifest

`website/content/public/archive-presentation.json` remains website-side because it owns presentation, not canon.

It may continue to contain:

- author approval for presentation configuration;
- map hit geometry;
- label hit geometry;
- optional percentage positioning if actually used;
- Curator Route ordering;
- Curator Route labels/notes;
- the Map Room step.

### Target changes during migration

- change presentation IDs from website-only IDs to canonical IDs;
- stop using `hidden-archive` tags to infer Archive section;
- resolve public/hidden placement from `public_projection.archive_section`;
- resolve map marker from canonical `cartography` rather than requiring a second authored marker field in the presentation file;
- retain geometry and route copy unchanged unless separately approved.

Presentation metadata must not become a backdoor for titles, lore summaries, biographies, relationships, or canonical map identifiers.

---

# PART V — EXECUTABLE INGESTION AND VALIDATION

## 33. Astro Content Ingestion

The website should introduce a schema-aware build-time content loader, preferably Astro Content Collections / Content Layer with Zod validation.

The schema document remains technology-neutral; Astro is the current executable consumer.

### Recommended logical collection

One logical `canon` collection over the approved record roots is preferred because canonical relationships use one ID namespace.

A practical loader may scan repository roots using a brace glob or custom build-time loader, then validate by `record_type`.

The website must not require a hard-coded record list to discover a new schema-valid Markdown record.

### Preview behavior

Preview loads Markdown records that contain `public_projection`, regardless of publication-ledger approval, and clearly marks them as proposals/unapproved projections.

### Production behavior

Production loads the same Markdown projections but renders only records whose Version 2 approval-ledger fingerprint matches and whose release controls allow exposure.

Preview and production therefore share one authored content source.

---

## 34. Validation Requirements

Version 1 validation must enforce at least:

### Universal integrity

- valid `schema_version`;
- allowed top-level fields;
- unique canonical IDs;
- unique slugs;
- valid record type;
- valid canon/development/disclosure enums;
- valid real metadata dates;
- no active canonical asset path under `unused/`.

### Relationships

- target exists;
- no duplicate identical target/type pair unless explicitly allowed by a later extension;
- visibility is valid;
- public related target is an existing relationship;
- public related relationship is `public` or `teaser`.

### Assets

- local asset IDs unique within record;
- source path exists and resolves safely under approved active asset roots;
- source is a regular file;
- no symbolic/path traversal escape;
- meaningful alt text;
- public selected asset exists and is safe.

### Cartography

- map ID valid kebab-case;
- numbered/restricted reference present;
- unlisted reference omitted;
- unique `aetherhaven-city` numbered/restricted marker among active mapped records;
- presentation geometry references a canonical mapped record.

### Chronology

- valid status;
- display string present;
- no forced sort key;
- account certainty valid;
- conflicting accounts preserved.

### Public projection

- required fields present;
- classification only public/teaser;
- Archive section valid;
- access label length limit;
- tags unique;
- related IDs unique and safe;
- image asset valid;
- no unknown projection fields.

### Publication

- approval ID resolves;
- projection hash matches;
- every public relationship target approved in production;
- current release manifest valid;
- production cannot import raw unapproved preview content as an alternate source.

---

## 35. Source Root and File Rules

Schema-governed canonical Markdown must:

- remain plain `.md` unless a future approved schema change explicitly permits another format;
- remain human-readable in GitHub;
- use YAML front matter;
- keep narrative canon in Markdown prose;
- avoid Astro/React component syntax in canonical content;
- retain relative Markdown links for human GitHub navigation;
- use structured IDs in metadata for machine relationships.

Astro may transform relative `.md` links when rendering, but canonical Markdown must not be written around Astro-specific route syntax.

---

## 36. No Manual Index Requirement

Folders plus schema metadata are the machine index.

`PROJECT_INDEX.md` and other human-facing indexes may remain useful, but any complete machine inventory should be generated from canonical records rather than manually maintained as the website's source of truth.

Generated indexes must be reproducible.

---

# PART VI — LEGACY MIGRATION MAP

## 37. Universal Legacy Field Mapping

| Current field/pattern | Version 1 target |
|---|---|
| `character_id`, `location_id`, `organization_id`, `artifact_id`, `historical_event_id`, `story_arc_id`, `story_draft_id` | `id` |
| current directory/profile family | `record_type` |
| descriptive `type` | `descriptor` and, when useful, machine `subtype` |
| `name` | `name` |
| story/arc `title` | `name` |
| `aliases` | `aliases` |
| `canon_status` | split into `canon.status`, `development.status`, and `disclosure.level` |
| `canonical_scope` | `canon.scope` |
| `last_updated` | `last_updated` |
| `temporal_relevance` | `development.temporal_relevance` |
| `source_basis`, `source`, `source_scope` | `provenance.sources` |
| `related_markdown` and structured named relationships | `relationships` where target has a canonical record |
| `canonical_images` | `assets` |
| map category/number | `cartography` |
| event/story chronology | `chronology` |

---

## 38. Character Legacy Mapping

| Current | Target |
|---|---|
| `title` | `character.titles[]` |
| `age_status` | `character.age_status` |
| `public_identity` | `character.public_identity` |
| `former_role` | `character.former_roles` |
| `current_role` | `character.current_roles` |
| `primary_locations` | relationships |
| `affiliations` | relationships when target record exists; otherwise retain in prose until modeled |
| `key_connections` | relationships when target record exists |
| spoiler text in `canon_status` / `spoiler_level` | `disclosure.level` plus prose; do not expose automatically |

---

## 39. Location Legacy Mapping

| Current | Target |
|---|---|
| `jurisdiction` | `location.jurisdiction` and/or relationships where canonical target exists |
| `access_status` | `location.access_status` |
| `map_reference_category` + `map_number` | `cartography` |
| `parent_location` | relationship type `parent-location` |
| `primary_connections` | relationships |
| `points_of_interest` | relationships such as `contains` / `point-of-interest` |

---

## 40. Organization Legacy Mapping

| Current | Target |
|---|---|
| `primary_jurisdiction` | `organization.jurisdiction` |
| `headquarters` | relationships such as `headquartered-at` |
| `leadership` | relationships such as `led-by` |
| `governing_authority` | relationships such as `governed-by` |
| `key_relationships` | relationships |

---

## 41. Artifact Legacy Mapping

| Current | Target |
|---|---|
| `category` | `artifact.category` |
| in-world catalog number | `artifact.catalog_number` |
| `slate_number` | `production.slate_number` |
| `image_status` | `production.image_status` |
| `visual_transcription_status` | `production.visual_transcription_status` |
| current active images | `assets` |

The plate transcription and complete visual description remain Markdown body sections.

---

## 42. Historical Event Legacy Mapping

| Current | Target |
|---|---|
| `date_status` + `chronology` | universal `chronology` |
| `locations` | relationships |
| `participants` | relationships |
| `organizations` | relationships |
| `related_artifacts` | relationships |
| `related_story_arcs` | relationships |
| `public_record_status` | `historical_event.public_record_status` |
| `restricted_record_status` | `historical_event.restricted_record_status` |
| `order_interest` | relationship to appropriate organization when established; preserve uncertainty in note/prose |

---

## 43. Story and Story Arc Legacy Mapping

Story draft:

| Current | Target |
|---|---|
| `title` | `name` |
| `subtitle` | `story.subtitle` |
| `title_status` | `story.title_status` |
| `proposed_book` | `story.proposed_book` |
| `proposed_placement` | `story.proposed_placement` |
| chronology string | universal `chronology` |
| characters/locations/connections | relationships |
| cover/inline artwork | assets with role/placement |

Story arc:

- `title` → `name`;
- primary characters, locations, organizations, artifacts, related story drafts → relationships;
- delayed reveal / hidden nature → disclosure and prose;
- progression and narrative planning remain in Markdown body.

---

## 44. Current Website Manifest Mapping

| Manifest Version 1 field | Version 1 source / Version 2 target |
|---|---|
| `id` | replaced by canonical Markdown `id` |
| `slug` | Markdown `slug` |
| `entityType` | derived |
| `canonicalName` | Markdown `name` |
| `publicTitle` | `public_projection.title` |
| `publicSummary` | `public_projection.summary` |
| `sourcePaths` | derived from owning Markdown record; removed from approval ledger |
| `publicationStatus` | removed; ledger match + release state replaces it |
| `spoilerClassification` | `public_projection.classification` |
| `publicAccessLabel` | `public_projection.access_label` |
| `approval` | Version 2 approval ledger |
| `relatedEntryIds` | `public_projection.related` using canonical IDs |
| `tags` | `public_projection.tags` |
| `publicationDate` | Version 2 approval ledger |
| image URL | generated from selected canonical asset |
| image alt | selected asset alt or projection override |
| image width/height | derived build output |

---

# PART VII — WEBSITE REALIGNMENT REQUIREMENTS

## 45. Required Post-Migration Website Changes

After Version 1 approval and Markdown migration, the website must be realigned without changing the approved user experience unless separately requested.

Required architecture work:

1. create schema-aware Astro content ingestion;
2. derive Preview records from Markdown `public_projection`;
3. derive production records from the same projection plus the Version 2 approval ledger;
4. convert `manifest.json` to approval-only Version 2;
5. convert presentation IDs to canonical IDs;
6. resolve map markers from canonical cartography;
7. remove canonical/public content ownership from `archive-catalog.mjs`;
8. remove featured public copy ownership from `archive-preview.mjs`;
9. replace ID-specific record responsive-image tables with generated asset metadata;
10. make available record filters derive from loaded data while preserving the current controls/labels;
11. make Hidden Archive classification derive from explicit projection metadata rather than a magic tag;
12. preserve the current release/sealed fail-closed controls;
13. preserve all currently approved routes, map links, drawers, Curator Route behavior, accessibility, and layout;
14. regression-test the generated public projection against the existing C1 public release before cutover.

### What may remain hard-coded

Presentation logic may still contain:

- Archive headings and instructional UI copy;
- global room/exhibit artwork configuration;
- CSS/layout;
- map geometry;
- Curator Route presentation;
- labels for known record-type filters;
- release behavior;
- accessibility mechanics.

It must not contain record-specific lore that belongs in Markdown.

---

## 46. Public Output Parity Gate

Before the old hard-coded/public-manifest content sources are removed, the migration branch must prove parity with the currently approved C1 release.

At minimum verify:

- 95 approved projections accounted for;
- 67 ordinary public records;
- 28 Hidden Archive teasers;
- same current 67 standalone record routes;
- same 30 map links and markers;
- same 28 closed Hidden Archive drawers;
- same eight-stop Curator Route;
- same approved titles/summaries/classifications/access labels/tags/related links unless separately approved;
- same public images and visual behavior;
- production remains indexable only when published;
- Preview remains `noindex`;
- sealed mode still prunes Archive routes/assets according to current release policy.

Any content difference is a publication change and requires author review rather than being dismissed as a migration artifact.

---

# PART VIII — FREEZE AND MIGRATION GOVERNANCE

## 47. Version 1 Freeze Criteria

Version `1.0.0` is **LOCKED**. The freeze criteria are:

- [x] Hermes completed the current website implementation pass.
- [x] Final website content consumers were audited.
- [x] Current publication manifest, presentation manifest, and release controls were audited.
- [x] Existing canonical Markdown record families were inventoried against templates and representative files.
- [x] Canon content, public projection, publication approval, presentation data, and derived data were explicitly separated.
- [x] Required representative edge cases were pressure-tested conceptually.
- [x] Candidate Version 1 data dictionary is complete in this document.
- [x] Author reviewed and approved the field contract on 2026-08-10.
- [x] Document version promoted to `1.0.0 — LOCKED`.
- [ ] Executable validators/templates are updated to the locked contract before the bulk profile migration begins.

**No bulk profile migration begins until the remaining validator/template prerequisite is complete.**

---

## 48. Representative Record Pressure Tests

Version 1 must support, without record-specific schema exceptions:

- **Amelia Hawthorne** — character, aliases/title, relationships, public projection, asset references, deeper internal disclosure.
- **The Clockwork Gardens** — location, placeholder maturity, map reference, public projection, hidden implications.
- **The Government District** — canonical location with district subtype and existing district URL behavior.
- **The Null Zone** — one location identity, restricted map `F`, Hidden Archive teaser projection.
- **The Brass Watch** — organization jurisdiction, leadership/relationships, concise public projection.
- **The Aether Gauntlet: Exterior Study** — artifact ID, separate in-world catalog number, plate asset, production/transcription status.
- **The Wayfinder** — first-class vessel owner with artifact/berth/character relationships.
- **The Clockwork Jungle Expedition** — unresolved/relative chronology, participants, evidence, restricted/public record distinction.
- **A Day Aboard the Wayfinder** — story title/subtitle, working placement, relative chronology, cover and placed inline assets.
- **The Keeper of Dreams** — delayed-reveal story arc, relationships, disclosure separate from canon status.
- **Source-grounded placeholders** — canonical authority separated from profile completeness.
- **Silas Rook** — highly sensitive full record with an intentionally minimal approved public teaser.

The completed audit found no representative case that requires duplicate website lore.

---

## 49. Required Schema-Change Lifecycle After Lock

1. Identify the problem.
2. Verify the requirement belongs to content rather than presentation/derived output.
3. Prepare `/templates/Aetherhaven_Schema_Change_Proposal.md`.
4. Assess blast radius across records, validators, website, tests, approvals, and generated outputs.
5. Consider adapters/alternatives.
6. Assign PATCH/MINOR/MAJOR impact.
7. Obtain explicit author approval.
8. Update this schema first.
9. Update executable validators and templates.
10. Migrate affected records deterministically where safe.
11. Flag substantive canon questions rather than inventing values.
12. Realign consumers.
13. Validate the complete repository.
14. Record migration completion and branch lifecycle.

---

## 50. Migration Safety Rules

### Metadata changes must not rewrite prose unnecessarily

A deterministic metadata transformation may be automated when meaning is preserved.

Do not mechanically rewrite narrative sections, resolve open questions, invent facts, or normalize disputed history merely to fill fields.

### No silent semantic defaults

Do not default:

- a full record to public;
- an event to confirmed;
- a relationship to public;
- an image to public;
- a mystery to resolved.

Where a safe technical default is explicitly defined, it must not create fictional facts.

### Fail closed on uncertainty

When disclosure/publication classification is unclear, choose no public projection or require review rather than exposing the record.

### One breaking migration, one compatible active schema

After the Version 1 migration is complete, active canonical profiles should not remain split across incompatible metadata shapes.

### Preserve rollback

Bulk migration occurs on a focused branch from a known base. Transformation must be reproducible and reviewable. Do not destroy source information merely because the target schema no longer uses the same field name.

---

## 51. AI-Agent Rules

All agents working with structured canon must:

- read this document before modifying schema-governed metadata;
- preserve author authority over canon and public publication;
- use canonical IDs for machine relationships;
- avoid undocumented fields;
- avoid local field reinterpretations;
- keep record-specific lore out of website source;
- keep presentation geometry out of canon front matter;
- keep publication approval separate from public projection;
- never infer full-file publicity from a safe public summary;
- propose schema changes rather than expanding the contract silently;
- preserve exact approved public copy during source-of-truth migrations unless the author approves content edits.

---

# PART IX — ILLUSTRATIVE SHAPES

## 52. Illustrative Character Shape

This is structural illustration only; it does not authorize migration values not already established.

```yaml
---
schema_version: 1
id: AH-CHAR-002
record_type: character
name: Amelia Hawthorne
slug: amelia-hawthorne
aliases:
  - Amelia
  - The Bearer
  - Bearer of the Living Key
last_updated: 2026-08-10
canon:
  status: canonical
  scope:
    - aetherhaven-volumes
development:
  status: working
  temporal_relevance: very-high
disclosure:
  level: story-sensitive
character:
  titles:
    - The Clockwork Explorer
relationships:
  - target: AH-CHAR-001
    type: father
    visibility: public
public_projection:
  title: Amelia Hawthorne
  summary: >-
    Amelia Hawthorne is a young mechanic and apprentice explorer who lives and
    travels aboard the Wayfinder with her father, Professor Elias Hawthorne.
  classification: public
  archive_section: catalog
  access_label: public
  tags:
    - character
  related: []
---
```

The exact `disclosure`, complete relationships, and asset assignments are reviewed during migration; the public projection text shown above is the already-approved C1 public summary.

---

## 53. Illustrative Restricted Location Shape

```yaml
---
schema_version: 1
id: AH-LOC-PLACEHOLDER-027
record_type: location
name: The Null Zone
slug: null-zone
aliases:
  - Null Zone
last_updated: 2026-08-10
canon:
  status: canonical
  scope:
    - aetherhaven-volumes
development:
  status: placeholder
  temporal_relevance: unresolved
disclosure:
  level: story-sensitive
cartography:
  - map_id: aetherhaven-city
    category: restricted
    reference: F
public_projection:
  title: The Null Zone
  summary: 'Map annotation: “Machines fail here.” Further record sealed.'
  classification: teaser
  archive_section: hidden
  access_label: restricted
  tags:
    - restricted-location
  related: []
---
```

Again, this demonstrates structure and preservation of the currently approved C1 teaser. It does not broaden the public source file.

---

## 54. Illustrative Artifact Shape

```yaml
---
schema_version: 1
id: AH-ART-009
record_type: artifact
name: The Aether Gauntlet: Exterior Study
slug: aether-gauntlet-exterior-study
aliases: []
last_updated: 2026-08-10
canon:
  status: canonical
  scope:
    - aetherhaven-volumes
development:
  status: working
disclosure:
  level: teaser
artifact:
  category: Amelia and the Aether Gauntlet
  catalog_number: AH-1-004
production:
  slate_number: 9
  image_status: image-linked
  visual_transcription_status: complete
assets:
  - id: primary-plate
    path: art/AH-1-004_The_Aether_Gauntlet-Exterior_Study.png
    role: plate
    visibility: teaser
    alt: Aetherhaven Archives exterior study of Amelia Hawthorne's Aether Gauntlet.
---
```

The visible plate transcription remains below the front matter in Markdown.

---

# PART X — CHANGE HISTORY

## 55. Change History

### 1.0.0 — 2026-08-10

**Status:** LOCKED / AUTHOR APPROVED.

The author explicitly approved the complete Version 1 field contract represented by the `0.2.0` candidate. Version 1 is now the governing structured-content contract for the repository.

This lock authorizes the next implementation phase in this order:

1. update executable validators to the Version 1 contract;
2. update canonical record templates;
3. pressure-test validator/template behavior;
4. then begin the controlled repository-wide metadata migration;
5. realign Astro/publication ingestion only after migrated Markdown validates and the C1 public-output parity gate can be enforced.

The lock does **not** authorize changing canon prose, public copy, publication scope, website layout, routes, map behavior, Hidden Archive behavior, or other reader-facing content outside the approved migration/parity work.

### 0.2.0 — 2026-08-10

**Status:** Historical candidate; superseded by approved Version `1.0.0`.

Added after the final Hermes/C1 website audit:

- complete ownership model;
- closed canonical record families;
- universal frontmatter contract;
- canon/development/disclosure separation;
- stable canonical identity and durable slug rules;
- structured provenance;
- structured canonical relationships with disclosure levels;
- structured canonical assets and derived-image boundary;
- multi-map cartography model;
- chronology model supporting disputed/anomalous time;
- type-specific extensions;
- `public_projection` contract;
- derived public entity-type rules;
- Version 2 publication approval ledger design;
- deterministic publication fingerprint requirements;
- presentation-manifest boundary;
- Astro ingestion target;
- complete validation requirements;
- legacy field migration maps;
- C1 public-output parity gate;
- freeze checklist and illustrative shapes.

No canonical profile migration was performed under Version `0.2.0`.

### 0.1.0 — 2026-08-10

**Status:** Governance approved; field model pending.

Established:

- Markdown as intended single authoritative content source;
- separation of canon content, publication approval, derived data, and presentation configuration;
- author approval requirement for material schema changes;
- semantic versioning and migration expectations;
- schema-change proposal workflow;
- AI-agent and website guardrails;
- Version 1 freeze criteria;
- representative-record pressure testing.

No canonical profile migration was authorized by Version `0.1.0`.