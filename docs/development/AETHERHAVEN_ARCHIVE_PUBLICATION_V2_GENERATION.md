# Aetherhaven Archive Publication Version 2 — Cutover Report

**Completed:** 2026-08-10  
**Source:** Aetherhaven Content Schema `1.0.0` canonical Markdown  
**Status:** COMPLETE — ACTIVE PUBLICATION CONTRACT

## Result

- Canonical Schema v1 records loaded from Markdown: **210**
- Existing approved C1 public/Hidden Archive projections preserved: **95**
- Active approval-ledger entries: **95**
- Public catalog routes: **67**
- Hidden Archive teaser records: **28**
- Canonical city-map references: **30**
- Curator Route steps: **8**
- Production HTML pages: **72**

The C1 public experience was used as the migration parity baseline. Public titles, summaries, classifications, access labels, tags, public relationships, image selections, image alt text, map geometry, Hidden Archive behavior, and Curator Route behavior were preserved through the cutover.

## Active Ownership

Canonical Markdown is now the authoritative source for record identity, public projection copy, public-safe relationships, asset selection, and canonical cartography.

The website retains only presentation/release data that does not belong in canon:

- `website/content/public/manifest.json` — Version 2 author-approval ledger containing canonical IDs and SHA-256 projection fingerprints;
- `website/content/public/archive-presentation.json` — Version 2 map geometry and Curator Route presentation data keyed by canonical IDs;
- `website/content/public/archive-release.json` — independent fail-closed release state;
- `website/content/public/archive-assets.json` — generated web-derivative registry for approved source artwork.

## Publication Guardrail

Each approval fingerprint covers the canonical ID, stable slug, public entity type, canonical name, reader-facing projection, public relationship IDs, selected source asset, alt text, and SHA-256 digest of the selected source-image bytes. A change to approved public Markdown or its selected source image invalidates the existing approval until the author approves a new fingerprint.

Preview and production now consume the same canonical Markdown projection. Production additionally requires a matching approval fingerprint and a published release state.

## Retired Duplicate Sources

The cutover removes the former JavaScript content stores and Version 1 publication manifest as content authorities. `archive-catalog.mjs`, `archive-preview.mjs`, and the duplicated Version 1 publication-validation path are no longer part of the active website architecture.

The one-time v2 candidate generator, legacy cartography parity harness, and candidate `.v2.json` files were removed after successful cutover validation.
