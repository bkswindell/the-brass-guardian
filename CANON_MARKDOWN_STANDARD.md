# Canon Markdown and Visual Integration Standard

## Purpose

This standard keeps *The Brass Guardian* repository interconnected, visually grounded, low in duplication, and easy for people and AI agents to navigate.

## Source Priority

1. Latest explicit canon decision in active Markdown.
2. Canonical Markdown profiles and artifact files.
3. Active artwork in `art/`, interpreted through its Markdown record.
4. Owner-managed compiled manuscript only where active Markdown has a genuine gap.
5. `unused/` is excluded and must never be consulted unless the project owner explicitly restores a named item.

## Required Structure

Every canonical Markdown file should contain:

- YAML front matter with a stable ID, canon status, last-updated date, related Markdown paths, and image paths.
- A concise canonical summary.
- A **Visual Reference** section using active compiled art when available.
- Direct relative hyperlinks whenever another character, location, organization, artifact, or story arc is named as a meaningful relationship.
- A **Continuity Notes** section defining what the file owns and what belongs in linked files.
- A **TODO / Production Checklist** using Markdown checkboxes.
- Open questions or intentionally unresolved canon where appropriate.

## Visual Requirements by File Type

### Locations

- Include a callout to the [Map of Aetherhaven](art/Map_of_Aetherhaven.png) when the location appears on the city map.
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

### Story Arcs

- Link to the involved characters, organizations, locations, and artifacts.
- Use a representative canonical image only when it does not spoil more than the arc file already reveals.

## Hyperlinking Rule

Whenever a Markdown file makes a meaningful named reference to another documented entity, use a relative Markdown link on the first important occurrence in that section. Repeated links in every sentence are unnecessary.

Use an artifact file as the authoritative source for an object or image. Use character, location, organization, and arc files as the authoritative sources for their broader subjects.

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
- [ ] Add visual-reference sections to every existing character profile.
- [ ] Add map and location-art sections to every existing location profile.
- [ ] Add crest, seal, or representative-art sections to every existing organization profile.
- [ ] Add representative art and complete cross-links to every story-arc profile.
- [ ] Add backlinks from existing profiles to all directly referenced artifact files.
- [ ] Review the repository periodically for broken links and duplicated canon text.
