# Canon Markdown and Visual Integration Standard

## Purpose

This standard keeps *The Brass Guardian* repository interconnected, visually grounded, low in duplication, and easy for people and AI agents to navigate.

## Structured Content Schema Governance

Structured front matter and machine-readable canon are governed by [AETHERHAVEN_CONTENT_SCHEMA.md](AETHERHAVEN_CONTENT_SCHEMA.md).

**Aetherhaven Content Schema Version `1.0.0` is LOCKED and author-approved.** It is now the authoritative structured-content contract.

Rules:

- new canonical records must use the Version 1 structure defined by the schema and the current templates;
- existing legacy front matter remains valid only until the controlled Version 1 migration reaches that record;
- do not introduce new global metadata conventions outside the locked schema;
- do not duplicate canonical/public-projection content into website code as a permanent source;
- keep presentation configuration and derived output outside canon metadata;
- publication approval remains separate from a record's `public_projection`;
- any material schema change must use [Aetherhaven_Schema_Change_Proposal.md](../../templates/Aetherhaven_Schema_Change_Proposal.md) and receive explicit author approval before implementation;
- before bulk migration, executable validators and templates must match the locked contract and representative pressure tests must pass.

This standard continues to govern Markdown organization, visual evidence, cross-linking, duplication, and editorial practices while the schema governs structured metadata.

## Historical-Event Records

Historical events belong in `historical_events/` and use [Historical_Event_Profile_Template.md](../../templates/Historical_Event_Profile_Template.md).

A historical-event file owns:

- the objective event,
- public and restricted accounts,
- participants and institutions,
- the known timeline,
- conflicting testimony,
- physical evidence and provenance,
- institutional consequences,
- continuity constraints,
- and unresolved historical questions.

A story arc owns how Amelia and the reader discover, experience, or interpret that history.

Profiles and artifacts should link to the event rather than repeat its full chronology. Historical records must preserve uncertainty and must not convert rumor into fact.

Every historical event ends with an **Archival Status** section containing:

- Public Record,
- Restricted Record,
- Primary Sources,
- and Outstanding Historical Questions.

Artifacts should link to relevant historical events through a **Related Historical Events** section. Provenance belongs in the artifact record; the complete event chronology belongs in the historical-event record.

## Source Priority

1. Latest explicit canon decision in active Markdown.
2. Canonical Markdown profiles, story drafts, and artifact files.
3. Active artwork in `art/`, interpreted through its Markdown record.
4. Owner-managed compiled manuscript only where active Markdown has a genuine gap.
5. `unused/` is excluded and must never be consulted unless the project owner explicitly restores a named item.
6. `media_reactions/` is non-canonical audience evidence and cannot override active canon.

## Required Structure

After migration to Version 1, every schema-governed canonical Markdown record must contain the universal fields required by `AETHERHAVEN_CONTENT_SCHEMA.md`, including:

- `schema_version: 1`;
- one stable canonical `id`;
- one canonical `record_type`;
- canonical `name`, durable `slug`, aliases, and real `last_updated` date;
- separate `canon`, `development`, and `disclosure` objects;
- type-specific extensions only where permitted by the locked schema;
- canonical-ID `relationships` for machine links when target records exist;
- structured active `assets` rather than legacy image lists;
- `cartography` and `chronology` when applicable;
- an optional `public_projection` only when reader-safe content has been deliberately prepared.

The Markdown body should continue to contain:

- a concise canonical summary;
- a **Visual Reference** section when visual canon exists;
- direct relative hyperlinks for human GitHub navigation;
- a **Continuity Notes** section defining what the file owns;
- a **TODO / Production Checklist**;
- open questions or intentionally unresolved canon where appropriate.

Do not mechanically rewrite narrative prose merely to normalize metadata.

## Visual Requirements by File Type

### Locations

- Include a callout to the [Map of Aetherhaven](../../art/Map_of_Aetherhaven.png) when the location appears on the city map.
- Include at least one active approved location asset when available.
- Until location art exists, include a checked or unchecked TODO rather than using substitute or unused art.
- Store the in-world map reference in `cartography`; website pixel geometry remains presentation data.

### Characters

- Include an approved portrait, photograph, silhouette, or clearly identified visual reference when available.
- Do not use a group image as a permanent substitute unless the character is clearly identifiable and the file says it is a temporary reference.

### Organizations

- Include an approved crest, seal, badge, document, artifact, uniform element, headquarters image, or other relevant visual asset when available.
- Link to the authoritative artifact file for an artifact rather than repeating its full history.

### Artifacts

- Embed every active image associated with the artifact.
- Preserve image variants only when their distinct purpose is documented.
- Include a **Plate Text Transcription — Visual Evidence Only** section that records every readable heading, label, date, signature, seal, stamp, handwritten note, redaction, name, place, measurement, catalog number, and identifying mark.
- Mark uncertain text as illegible, partially illegible, abraded, struck through, or redacted. Never reconstruct text merely because later canon suggests what it might say.
- Include a **Complete Plate Description — Visual Evidence Only** section describing the entire visible composition without importing unseen story facts.
- Include a separate **Non-Visual Canon References and Story Context** section for broader history, interpretation, and links.
- Preserve visible plate text even when it conflicts with newer canon; document the conflict and let active linked Markdown control the broader story.
- Keep recovery details, form, canonical purpose, production status, and unresolved questions in the artifact file.

### Historical Events

- Link the event's public and restricted evidence, involved profiles, related story arcs, and authoritative artifact records.
- Include an approved historical illustration, evidence collage, photograph, document, map, or artifact set when one exists.
- Do not depict an unresolved witness account, mediator identity, chronology, or disputed action as settled fact.
- Treat the historical-event file as the authoritative owner of the event chronology.

### Story Drafts

- Story prose belongs in `story_drafts/` during the initial migration; long-range plotting and reveal planning belong in `story_arcs/`.
- Schema Version 1 uses `record_type: story` for canonical story drafts.
- A canonical story draft may have working wording/title/placement while retaining `canon.status: canonical`; development state and canon authority are separate.
- Preserve the current full prose before structural revisions.
- Separate exact draft text from editorial notes, continuity notes, placement options, and unresolved terminology.
- Working titles may change without changing the story's canonical authority.
- Do not treat every fairy-tale explanation, metaphor, remembered detail, or narrator simplification as settled technical lore when the draft explicitly preserves that ambiguity.
- Opening stories should avoid premature exposition when their purpose is to establish present-day character attachment, wonder, domestic life, or tone.
- Link the draft to the records that own deeper character, location, vessel, artifact, event, and story-arc continuity.

## Story Arcs

- Use `record_type: story_arc`.
- Link involved characters, organizations, locations, vessels, artifacts, events, and stories through canonical-ID relationships where records exist.
- Use a representative approved asset only when it does not spoil more than the arc file already reveals.
- Delayed-reveal/hidden status belongs in `disclosure`, not canon authority or record type.

## Public Reaction Records

Files in `media_reactions/` are non-canonical development evidence and are outside the Version 1 canonical-record roots.

- Preserve source transcripts, articles, blogs, and reviews exactly between `<!-- SOURCE CONTENT START: IMMUTABLE PUBLIC REACTION -->` and `<!-- SOURCE CONTENT END: IMMUTABLE PUBLIC REACTION -->`.
- Store a SHA-256 checksum for each immutable source block.
- Editorial metadata, interpretation audits, summaries, tags, and canon links may be updated.
- Do not silently correct misspelled names, inaccurate claims, or speculative statements inside source content; those errors are useful evidence of audience understanding.
- Never promote a reaction theory into canon without a separate explicit canon decision.
- When a reaction conflicts with canon, link to the authoritative active Markdown and describe the conflict outside the source block.
- Aggregate conclusions must identify the sample size and avoid treating a limited test audience as broad market evidence.

## Organization Naming Collision Rule

Aetherhaven contains two distinct organizations whose formal names begin with **Order**:

- [The Order of the Mended Hand](../../organizations/The_Order_of_the_Mended_Hand.md) is a public, highly visible hospitaller and medical organization. Its normal shorthand is **the Hand**.
- [The Order of the Closed Eye](../../organizations/The_Order_of_the_Closed_Eye.md) is a secret containment organization. Canon prose normally uses **the Closed Eye** or its full name.

Do not use bare **the Order** as shorthand for the Mended Hand.

Bare **the Order** may refer to the Closed Eye only in clearly established internal speech, restricted records, or deliberately obscured dialogue. Never use bare **the Order** where both organizations appear in the same passage.

On first meaningful reference in a file or scene, use the appropriate full formal name before using its approved shorthand.

## Hyperlinking Rule

Whenever a Markdown file makes a meaningful named reference to another documented entity, use a relative Markdown link on the first important occurrence in that section. Repeated links in every sentence are unnecessary.

Relative Markdown links serve humans reading GitHub. Version 1 `relationships` use stable canonical IDs for machine-readable structure. Keep both where useful; they serve different purposes.

Use an artifact file as the authoritative source for an object or image. Use character, location, organization, vessel, historical-event, story, and story-arc files as the authoritative sources for their broader subjects.

## Duplication Rule

Summarize and link; do not copy full sections between files. A local file may contain the facts necessary to understand its own subject, but detailed history should live only in the profile that owns that history.

The same principle applies to downstream consumers: website code, approval ledgers, presentation manifests, indexes, and generated data must not become permanent second owners of canonical prose or relationships.

## AI-Agent Optimization

- Prefer explicit names over pronouns in summaries and relationship lists.
- Use stable canonical IDs in structured relationships and relative Markdown paths for human links.
- Separate canon authority, development maturity, disclosure sensitivity, public projection, and publication approval.
- Never allow a TODO, theory, or recommendation to appear indistinguishable from confirmed canon.
- Keep headings predictable across files.
- Follow `AETHERHAVEN_CONTENT_SCHEMA.md` for all structured metadata and schema-change governance.
- When a new content need does not fit Version 1, use the schema-change process rather than inventing a field locally.

## Repository Migration Checklist

- [x] Create an artifact profile template.
- [x] Create one Markdown record for every entry in the original Artifact Image Slate.
- [x] Link existing active artifact art where confidently matched.
- [x] Transcribe and fully describe every completed active artifact plate currently available.
- [x] Create the historical-event template and `historical_events/` index.
- [x] Separate objective historical events from story arcs that reveal or revisit them.
- [x] Complete, approve, and lock Aetherhaven Content Schema Version `1.0.0`.
- [x] Add Version 1 story and vessel templates.
- [x] Align existing reusable profile templates with Version 1.
- [ ] Complete executable validator pressure tests before bulk migration.
- [ ] Migrate active canonical profile front matter to Version 1.
- [ ] Create the first-class Wayfinder vessel record from already-approved canon.
- [ ] Realign Astro/publication ingestion after migrated Markdown validates and C1 parity can be proven.
- [ ] Add visual-reference sections to every existing character profile where needed.
- [ ] Add map and location-art sections to every existing location profile where needed.
- [ ] Add crest, seal, or representative-art sections to every existing organization profile where needed.
- [ ] Add representative art and complete cross-links to every story-arc profile where useful.
- [ ] Review the repository periodically for broken links and duplicated canon text.
