import assert from "node:assert/strict";
import test from "node:test";

import {
  validateCanonRecord,
  validateCanonRecords,
} from "./lib/canon-schema-v1.mjs";

const base = (overrides = {}) => ({
  schema_version: 1,
  id: "AH-TEST-001",
  record_type: "location",
  name: "Example Place",
  slug: "example-place",
  aliases: [],
  last_updated: "2026-08-10",
  canon: { status: "canonical", scope: ["aetherhaven-volumes"] },
  development: { status: "working" },
  disclosure: { level: "public" },
  ...overrides,
});

const amelia = base({
  id: "AH-CHAR-002",
  record_type: "character",
  name: "Amelia Hawthorne",
  slug: "amelia-hawthorne",
  aliases: ["Amelia", "The Bearer", "Bearer of the Living Key"],
  development: { status: "working", temporal_relevance: "very-high" },
  disclosure: { level: "story-sensitive" },
  character: {
    titles: ["The Clockwork Explorer"],
    age_status: "Exact series chronology unresolved",
  },
  relationships: [
    { target: "AH-CHAR-001", type: "daughter-of", visibility: "public" },
    { target: "AH-VESSEL-WAYFINDER", type: "travels-aboard", visibility: "public" },
  ],
  assets: [
    {
      id: "primary-reference",
      path: "art/AH-1-004_The_Aether_Gauntlet-Exterior_Study.png",
      role: "reference",
      visibility: "teaser",
      alt: "Aetherhaven Archives study of Amelia Hawthorne's Aether Gauntlet.",
    },
  ],
  public_projection: {
    title: "Amelia Hawthorne",
    summary:
      "Amelia Hawthorne is a young mechanic and apprentice explorer who lives and travels aboard the Wayfinder with her father, Professor Elias Hawthorne.",
    classification: "public",
    archive_section: "catalog",
    access_label: "public",
    tags: ["character"],
    related: ["AH-CHAR-001", "AH-VESSEL-WAYFINDER"],
    image: { asset: "primary-reference" },
  },
});

const elias = base({
  id: "AH-CHAR-001",
  record_type: "character",
  name: "Professor Elias Hawthorne",
  slug: "professor-elias-hawthorne",
  aliases: ["Elias Hawthorne", "Elias", "Professor Hawthorne"],
  disclosure: { level: "public" },
  character: { titles: ["The Brass Guardian"] },
  relationships: [
    { target: "AH-CHAR-002", type: "father-of", visibility: "public" },
    { target: "AH-VESSEL-WAYFINDER", type: "travels-aboard", visibility: "public" },
  ],
});

const wayfinder = base({
  id: "AH-VESSEL-WAYFINDER",
  record_type: "vessel",
  name: "The Wayfinder",
  slug: "wayfinder",
  aliases: ["Wayfinder"],
  disclosure: { level: "public" },
  vessel: { class: "explorer-airship", status: "active" },
  relationships: [
    { target: "AH-CHAR-001", type: "crew", visibility: "public" },
    { target: "AH-CHAR-002", type: "crew", visibility: "public" },
  ],
});

const nullZone = base({
  id: "AH-LOC-PLACEHOLDER-027",
  name: "The Null Zone",
  slug: "null-zone",
  aliases: ["Null Zone"],
  development: { status: "placeholder", temporal_relevance: "unresolved" },
  disclosure: { level: "story-sensitive" },
  cartography: [
    { map_id: "aetherhaven-city", category: "restricted", reference: "F" },
  ],
  public_projection: {
    title: "The Null Zone",
    summary: "Map annotation: “Machines fail here.” Further record sealed.",
    classification: "teaser",
    archive_section: "hidden",
    access_label: "restricted",
    tags: ["restricted-location"],
    related: [],
  },
});

const governmentDistrict = base({
  id: "AH-LOC-GOVERNMENT-DISTRICT",
  name: "The Government District",
  slug: "government-district",
  subtype: "district",
  descriptor: "Civic district",
  disclosure: { level: "public" },
  cartography: [
    { map_id: "aetherhaven-city", category: "numbered", reference: "11" },
  ],
});

const brassWatch = base({
  id: "AH-ORG-BRASS-WATCH",
  record_type: "organization",
  name: "The Brass Watch",
  slug: "brass-watch",
  aliases: ["The Watch", "Aetherhaven Brass Watch"],
  development: { status: "working", temporal_relevance: "critical" },
  disclosure: { level: "public" },
  organization: {
    jurisdiction: ["Public safety", "Criminal investigations", "Emergency response"],
  },
});

const gauntlet = base({
  id: "AH-ART-009",
  record_type: "artifact",
  name: "The Aether Gauntlet: Exterior Study",
  slug: "aether-gauntlet-exterior-study",
  aliases: [],
  disclosure: { level: "teaser" },
  artifact: {
    category: "Amelia and the Aether Gauntlet",
    catalog_number: "AH-1-004",
  },
  production: {
    slate_number: 9,
    image_status: "image-linked",
    visual_transcription_status: "complete",
  },
  assets: [
    {
      id: "primary-plate",
      path: "art/AH-1-004_The_Aether_Gauntlet-Exterior_Study.png",
      role: "plate",
      visibility: "teaser",
      alt: "Aetherhaven Archives exterior study of Amelia Hawthorne's Aether Gauntlet.",
    },
  ],
});

const clockworkJungleExpedition = base({
  id: "AH-HIST-016",
  record_type: "historical_event",
  name: "The Clockwork Jungle Expedition",
  slug: "clockwork-jungle-expedition",
  aliases: ["The Clockwork Jungle Accident", "The Vault Awakening"],
  disclosure: { level: "story-sensitive" },
  chronology: {
    status: "relative",
    display: "Before Volume 1",
    note: "Exact date unresolved.",
  },
  historical_event: {
    public_record_status: "simplified and incomplete",
    restricted_record_status: "fragmented, contradictory, and partly withheld",
  },
});

const dayAboard = base({
  id: "AH-STORY-DRAFT-002",
  record_type: "story",
  name: "The Brass Guardian and the Clockwork Explorer",
  slug: "the-brass-guardian-and-the-clockwork-explorer",
  aliases: [],
  development: { status: "working" },
  disclosure: { level: "teaser" },
  chronology: {
    status: "relative",
    display: "Present-day Hawthorne life before the primary Book One conflict",
  },
  story: {
    subtitle: "A Day Aboard the Wayfinder",
    title_status: "Working title",
    proposed_book: "Book One",
    proposed_placement: ["Opening story", "First chapter"],
  },
});

const keeperOfDreams = base({
  id: "AH-ARC-KEEPER-OF-DREAMS",
  record_type: "story_arc",
  name: "The Keeper of Dreams",
  slug: "keeper-of-dreams",
  aliases: [],
  development: { status: "working", temporal_relevance: "high" },
  disclosure: { level: "story-sensitive" },
});

const silas = base({
  id: "AH-CHAR-SILAS-ROOK",
  record_type: "character",
  name: "Silas Rook",
  slug: "silas-rook",
  aliases: ["The Stillmaker", "The First Cut", "S. Rook", "The Man Between Hours"],
  development: { status: "working", temporal_relevance: "critical" },
  disclosure: { level: "creator-only" },
  character: {
    titles: ["The Stillmaker"],
    public_identity: "Unknown",
  },
  public_projection: {
    title: "Silas Rook",
    summary:
      "Silas Rook is indexed as a major spoiler figure. Identity and fuller context remain sealed or withheld from the public catalog.",
    classification: "teaser",
    archive_section: "hidden",
    access_label: "major spoiler",
    tags: ["character"],
    related: [],
  },
});

test("accepts representative Version 1 record families without schema exceptions", () => {
  const records = [
    amelia,
    elias,
    wayfinder,
    nullZone,
    governmentDistrict,
    brassWatch,
    gauntlet,
    clockworkJungleExpedition,
    dayAboard,
    keeperOfDreams,
    silas,
  ];
  assert.equal(validateCanonRecords(records), records);
});

test("keeps canon authority separate from placeholder maturity", () => {
  assert.equal(validateCanonRecord(nullZone), nullZone);
  assert.equal(nullZone.canon.status, "canonical");
  assert.equal(nullZone.development.status, "placeholder");
});

test("allows a creator-only full record with a narrow teaser projection", () => {
  assert.equal(validateCanonRecord(silas), silas);
  assert.equal(silas.disclosure.level, "creator-only");
  assert.equal(silas.public_projection.classification, "teaser");
});

test("rejects website presentation categories as canonical record types", () => {
  assert.throws(
    () => validateCanonRecord(base({ id: "AH-TEST-ARCHIVE", record_type: "archive-record" })),
    /record_type is invalid/,
  );
});

test("rejects district as a canonical record type and accepts location subtype instead", () => {
  assert.throws(
    () => validateCanonRecord(base({ id: "AH-TEST-DISTRICT", record_type: "district" })),
    /record_type is invalid/,
  );
  assert.doesNotThrow(() => validateCanonRecord(governmentDistrict));
});

test("rejects public relationships that are not explicitly safe relationships", () => {
  const unsafe = structuredClone(amelia);
  unsafe.relationships.push({
    target: "AH-ORG-SECRET-001",
    type: "interest-from",
    visibility: "creator-only",
  });
  unsafe.public_projection.related.push("AH-ORG-SECRET-001");
  assert.throws(() => validateCanonRecord(unsafe), /not backed by a public\/teaser relationship/);
});

test("rejects active canonical assets under unused", () => {
  const invalid = structuredClone(gauntlet);
  invalid.assets[0].path = "unused/old-gauntlet.png";
  assert.throws(() => validateCanonRecord(invalid), /must not reference unused/);
});

test("requires map references for numbered and restricted cartography", () => {
  const invalid = structuredClone(nullZone);
  delete invalid.cartography[0].reference;
  assert.throws(() => validateCanonRecord(invalid), /reference must be a non-empty string/);
});

test("requires unlisted cartography to omit a direct reference", () => {
  const invalid = base({
    id: "AH-LOC-INTERIOR",
    name: "Interior Room",
    slug: "interior-room",
    cartography: [
      {
        map_id: "aetherhaven-city",
        category: "unlisted",
        reference: "11",
        parent_reference: "11",
      },
    ],
  });
  assert.throws(() => validateCanonRecord(invalid), /reference must be omitted/);
});

test("preserves disputed chronology as parallel accounts", () => {
  const disputed = base({
    id: "AH-HIST-DISPUTED",
    record_type: "historical_event",
    name: "Disputed Event",
    slug: "disputed-event",
    chronology: {
      status: "disputed",
      display: "Records disagree",
      accounts: [
        { label: "civic-record", value: "Seven months", certainty: "confirmed" },
        { label: "shipboard-account", value: "Nineteen days", certainty: "confirmed" },
      ],
    },
  });
  assert.doesNotThrow(() => validateCanonRecord(disputed));
});

test("rejects duplicate canonical IDs, slugs, and Aetherhaven map references", () => {
  assert.throws(() => validateCanonRecords([amelia, { ...elias, id: amelia.id }]), /duplicate canonical id/);
  assert.throws(() => validateCanonRecords([amelia, { ...elias, slug: amelia.slug }]), /duplicate canonical slug/);
  const duplicateMap = {
    ...governmentDistrict,
    id: "AH-LOC-OTHER-DISTRICT",
    slug: "other-district",
  };
  assert.throws(() => validateCanonRecords([governmentDistrict, duplicateMap]), /duplicate map reference/);
});

test("rejects unknown top-level fields so the schema cannot drift silently", () => {
  assert.throws(
    () => validateCanonRecord({ ...base(), frontendWidget: "drawer" }),
    /unknown top-level field/,
  );
});