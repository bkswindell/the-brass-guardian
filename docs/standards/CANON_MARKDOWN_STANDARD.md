# Canon Markdown and Visual Integration Standard

## Purpose

This standard keeps *The Brass Guardian* repository interconnected, visually grounded, low in duplication, and easy for people and AI agents to navigate.


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
- Order Interest,
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

Every canonical Markdown file should contain:

- YAML front matter with a stable ID, canon status, last-updated date, related Markdown paths, and image paths.
- A concise canonical summary.
- A **Visual Reference** section using active compiled art when available.
- Direct relative hyperlinks whenever another character, location, organization, artifact, historical event, or story arc is named as a meaningful relationship.
- A **Continuity Notes** section defining what the file owns and what belongs in linked files.
- A **TODO / Production Checklist** using Markdown checkboxes.
- Open questions or intentionally unresolved canon where appropriate.

## Visual Requirements by File Type

### Locations

- Include a callout to the [Map of Aetherhaven](../../art/Map_of_Aetherhaven.png) when the location appears on the city map.
- Include at least one canonical image of the location when available.
- Until location art exists, include a checked or unchecked TODO rather than using substitute or unused art.

### Characters

- Include a canonical portrait, photograph, silhouette, or clearly identified visual reference when available.
- Do not use a group image as a permanent substitute unless the character is clearly identifiable and the file says it is a temporary reference.

### Organizations

- Include a crest, seal, badge, document, artifact, uniform element, headquarters image, or other relevant visual asset.
- Link to the authoritative artifact file for the asset rather than repeating its full history.

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
- Include a canonical historical illustration, evidence collage, photograph, document, map, or artifact set when one exists.
- Do not depict an unresolved witness account, mediator identity, chronology, or disputed action as settled fact.
- Treat the historical-event file as the authoritative owner of the event chronology.

#### Story Drafts

- Story prose belongs in `story_drafts/`; long-range plotting and reveal planning belong in `story_arcs/`.
- A file marked **Canonical story draft** is authoritative for its character relationships, events, emotional truth, and explicitly stated continuity even while the title and wording remain under revision.
- Preserve the current full prose before making structural revisions.
- Separate exact draft text from editorial notes, continuity notes, placement options, and unresolved terminology.
- Working titles may change without changing the story's canonical status.
- Do not treat every fairy-tale explanation, metaphor, remembered detail, or narrator simplification as settled technical lore when the draft explicitly preserves that ambiguity.
- Opening stories should avoid premature exposition when their purpose is to establish present-day character attachment, wonder, domestic life, or tone.
- Link the draft to the character, location, artifact, historical-event, and story-arc records that own its deeper continuity.

## Story Arcs

- Link to the involved characters, organizations, locations, and artifacts.
- Use a representative canonical image only when it does not spoil more than the arc file already reveals.

## Public Reaction Records

Files in `media_reactions/` are non-canonical development evidence.

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

Use an artifact file as the authoritative source for an object or image. Use character, location, organization, historical-event, and arc files as the authoritative sources for their broader subjects.

## Duplication Rule

Summarize and link; do not copy full sections between files. A local file may contain the facts necessary to understand its own subject, but detailed history should live only in the profile that owns that history.

## AI-Agent Optimization

- Prefer explicit names over pronouns in summaries and relationship lists.
- Use stable IDs and relative paths in YAML.
- Separate established canon, staged revelations, proposed concepts, and open questions.
- Never allow a TODO, theory, or original slate recommendation to appear indistinguishable from confirmed canon.
- Keep headings predictable across files.

## Repository Migration Checklist

- [x] Create an artifact profile template.
- [x] Create one Markdown record for every entry in the original Artifact Image Slate.
- [x] Link existing active artifact art where confidently matched.
- [x] Transcribe and fully describe every completed active artifact plate currently available.
- [x] Create the historical-event template and `historical_events/` index.
- [x] Separate objective historical events from story arcs that reveal or revisit them.
- [ ] Add visual-reference sections to every existing character profile.
- [ ] Add map and location-art sections to every existing location profile.
- [ ] Add crest, seal, or representative-art sections to every existing organization profile.
- [ ] Add representative art and complete cross-links to every story-arc profile.
- [ ] Add backlinks from existing profiles to all directly referenced artifact files.
- [ ] Review the repository periodically for broken links and duplicated canon text.
