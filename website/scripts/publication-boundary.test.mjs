import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  toPublicArchiveEntry,
  validatePublicationManifest,
} from "./lib/publication-boundary.mjs";

const makeRepository = async () => {
  const repositoryRoot = await mkdtemp(join(tmpdir(), "aetherhaven-publication-"));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(
    join(repositoryRoot, "characters", "Example.md"),
    "# Approved source fixture\n",
  );
  return repositoryRoot;
};

const makeEntry = (overrides = {}) => ({
  id: "character-example",
  slug: "example",
  entityType: "character",
  canonicalName: "Example Record",
  publicTitle: "Example Record",
  publicSummary: "A deliberately neutral public projection used only by the automated test suite.",
  sourcePaths: ["characters/Example.md"],
  publicationStatus: "approved",
  spoilerClassification: "public",
  approval: {
    approvedBy: "author",
    approvedOn: "2026-08-09",
  },
  relatedEntryIds: [],
  tags: ["fixture"],
  ...overrides,
});

const makeManifest = (entries) => ({
  schemaVersion: 1,
  entries,
});

test("accepts an explicitly approved public projection with an existing source", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  const result = await validatePublicationManifest(
    makeManifest([makeEntry()]),
    { repositoryRoot },
  );

  assert.equal(result.entries.length, 1);
  assert.equal(result.entries[0].id, "character-example");
});

test("rejects a draft record from the public projection", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([makeEntry({ publicationStatus: "draft" })]),
      { repositoryRoot },
    ),
    /publicationStatus must be approved/,
  );
});

test("rejects restricted spoiler classifications from the public projection", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  for (const spoilerClassification of ["story-sensitive", "creator-only"]) {
    await assert.rejects(
      validatePublicationManifest(
        makeManifest([makeEntry({ spoilerClassification })]),
        { repositoryRoot },
      ),
      /spoilerClassification must be public or teaser/,
    );
  }
});

test("rejects undeclared internal fields from a public record", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([makeEntry({ privateNotes: "Never publish this field." })]),
      { repositoryRoot },
    ),
    /unrecognized field: privateNotes/,
  );
});

test("rejects a record whose owning source path is missing", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([
        makeEntry({ sourcePaths: ["characters/Missing_Record.md"] }),
      ]),
      { repositoryRoot },
    ),
    /source path does not exist: characters\/Missing_Record\.md/,
  );
});

test("rejects source paths that escape the canonical repository boundary", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([makeEntry({ sourcePaths: ["../private-notes.md"] })]),
      { repositoryRoot },
    ),
    /source path must be a safe repository-relative Markdown path/,
  );
});

test("rejects an image without meaningful alternative text", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([
        makeEntry({
          image: {
            src: "/images/example.webp",
            width: 640,
            height: 480,
          },
        }),
      ]),
      { repositoryRoot },
    ),
    /image alt text is required/,
  );
});

test("rejects non-string image alternative text without crashing", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([
        makeEntry({
          image: {
            src: "/images/example.webp",
            alt: 42,
            width: 640,
            height: 480,
          },
        }),
      ]),
      { repositoryRoot },
    ),
    /image alt text is required/,
  );
});

test("rejects identifiers that are not lowercase kebab-case", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  for (const overrides of [
    { id: "Character Example" },
    { slug: "Example Record" },
  ]) {
    await assert.rejects(
      validatePublicationManifest(
        makeManifest([makeEntry(overrides)]),
        { repositoryRoot },
      ),
      /must be lowercase kebab-case/,
    );
  }
});

test("rejects duplicate public IDs and slugs", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  for (const duplicate of [
    makeEntry({ slug: "second-record" }),
    makeEntry({ id: "character-second" }),
  ]) {
    await assert.rejects(
      validatePublicationManifest(
        makeManifest([makeEntry(), duplicate]),
        { repositoryRoot },
      ),
      /duplicate public (ID|slug)/,
    );
  }
});

test("rejects relationships to records outside the approved manifest", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([
        makeEntry({ relatedEntryIds: ["location-not-approved"] }),
      ]),
      { repositoryRoot },
    ),
    /relatedEntryIds contains an unpublished record: location-not-approved/,
  );
});

test("removes approval and source provenance from client-facing records", () => {
  const entry = makeEntry({
    image: {
      src: "/images/example.webp",
      alt: "A neutral test image.",
      width: 640,
      height: 480,
      internalCaption: "This must never reach a client projection.",
    },
  });

  const publicEntry = toPublicArchiveEntry(entry);

  assert.deepEqual(Object.keys(publicEntry).sort(), [
    "canonicalName",
    "entityType",
    "id",
    "image",
    "publicAccessLabel",
    "publicSummary",
    "publicTitle",
    "relatedEntryIds",
    "slug",
    "spoilerClassification",
    "tags",
  ]);
  assert.equal("approval" in publicEntry, false);
  assert.equal("sourcePaths" in publicEntry, false);
  assert.equal("publicationStatus" in publicEntry, false);
  assert.deepEqual(publicEntry.image, {
    src: "/images/example.webp",
    alt: "A neutral test image.",
    width: 640,
    height: 480,
  });
});

test("requires complete public metadata and an author approval record", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  for (const overrides of [
    { canonicalName: "" },
    { publicTitle: "" },
    { publicSummary: "" },
    { sourcePaths: [] },
    { relatedEntryIds: undefined },
    { tags: undefined },
    { approval: { approvedBy: "agent", approvedOn: "2026-08-09" } },
    { approval: { approvedBy: "author", approvedOn: "08/09/2026" } },
  ]) {
    await assert.rejects(
      validatePublicationManifest(
        makeManifest([makeEntry(overrides)]),
        { repositoryRoot },
      ),
      /invalid publication field/,
    );
  }
});

test("rejects entity types outside the public archive vocabulary", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([makeEntry({ entityType: "secret-answer" })]),
      { repositoryRoot },
    ),
    /unsupported public entity type/,
  );
});

test("rejects an image path that is missing from the public asset directory", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([
        makeEntry({
          image: {
            src: "/images/missing.webp",
            alt: "A neutral test image.",
            width: 640,
            height: 480,
          },
        }),
      ]),
      {
        repositoryRoot,
        publicRoot: join(repositoryRoot, "website", "public"),
      },
    ),
    /public image does not exist: \/images\/missing\.webp/,
  );
});

test("rejects an image path that escapes the public asset directory", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      makeManifest([
        makeEntry({
          image: {
            src: "/../../private.webp",
            alt: "A neutral test image.",
            width: 640,
            height: 480,
          },
        }),
      ]),
      { repositoryRoot },
    ),
    /image src must be a canonical public asset URL/,
  );
});

test("rejects an unsupported publication-manifest schema version", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  await assert.rejects(
    validatePublicationManifest(
      { schemaVersion: 2, entries: [makeEntry()] },
      { repositoryRoot },
    ),
    /schemaVersion must be 1/,
  );
});

test("rejects undeclared fields nested inside image and approval metadata", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  for (const overrides of [
    {
      image: {
        src: "/images/example.webp",
        alt: "A neutral test image.",
        width: 640,
        height: 480,
        privateNotes: "Do not expose this.",
      },
    },
    {
      approval: {
        approvedBy: "author",
        approvedOn: "2026-08-09",
        internalComment: "Not public metadata.",
      },
    },
  ]) {
    await assert.rejects(
      validatePublicationManifest(
        makeManifest([makeEntry(overrides)]),
        { repositoryRoot },
      ),
      /unrecognized (image|approval) field/,
    );
  }
});

test("rejects invalid image dimensions before checking the asset", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  for (const dimensions of [
    { width: 0, height: 480 },
    { width: 640, height: "480" },
  ]) {
    await assert.rejects(
      validatePublicationManifest(
        makeManifest([
          makeEntry({
            image: {
              src: "/images/example.webp",
              alt: "A neutral test image.",
              ...dimensions,
            },
          }),
        ]),
        { repositoryRoot },
      ),
      /image width and height must be positive integers/,
    );
  }
});

test("rejects duplicate tags, duplicate relationships, and self-links", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  for (const overrides of [
    { tags: ["fixture", "fixture"] },
    { relatedEntryIds: ["character-example", "character-example"] },
    { relatedEntryIds: ["character-example"] },
  ]) {
    await assert.rejects(
      validatePublicationManifest(
        makeManifest([makeEntry(overrides)]),
        { repositoryRoot },
      ),
      /(tags and relatedEntryIds must contain unique values|cannot relate to itself)/,
    );
  }
});

test("rejects non-string values in public metadata lists", async (t) => {
  const repositoryRoot = await makeRepository();
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));

  for (const overrides of [
    { tags: [{ privateNote: "hidden" }] },
    { relatedEntryIds: [42] },
    { sourcePaths: [42] },
  ]) {
    await assert.rejects(
      validatePublicationManifest(
        makeManifest([makeEntry(overrides)]),
        { repositoryRoot },
      ),
      /invalid publication field/,
    );
  }
});
