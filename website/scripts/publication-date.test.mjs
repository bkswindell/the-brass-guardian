import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { validatePublicationManifest } from "./lib/publication-boundary.mjs";

test("rejects a malformed optional publication date", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-date-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(join(repositoryRoot, "characters", "Example.md"), "# Fixture\n");

  const entry = {
    id: "character-example",
    slug: "example",
    entityType: "character",
    canonicalName: "Example Record",
    publicTitle: "Example Record",
    publicSummary: "A neutral public projection fixture.",
    sourcePaths: ["characters/Example.md"],
    publicationStatus: "approved",
    spoilerClassification: "public",
    approval: { approvedBy: "author", approvedOn: "2026-08-09" },
    relatedEntryIds: [],
    tags: [],
    publicationDate: "2026-13-40",
  };

  await assert.rejects(
    validatePublicationManifest(
      { schemaVersion: 1, entries: [entry] },
      { repositoryRoot },
    ),
    /publicationDate must use YYYY-MM-DD/,
  );
});

test("rejects an impossible author approval date", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-approval-date-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(join(repositoryRoot, "characters", "Example.md"), "# Fixture\n");

  const entry = {
    id: "character-example",
    slug: "example",
    entityType: "character",
    canonicalName: "Example Record",
    publicTitle: "Example Record",
    publicSummary: "A neutral public projection fixture.",
    sourcePaths: ["characters/Example.md"],
    publicationStatus: "approved",
    spoilerClassification: "public",
    approval: { approvedBy: "author", approvedOn: "2026-02-30" },
    relatedEntryIds: [],
    tags: [],
  };

  await assert.rejects(
    validatePublicationManifest(
      { schemaVersion: 1, entries: [entry] },
      { repositoryRoot },
    ),
    /invalid publication field: approval/,
  );
});

test("accepts valid leap-day approval and publication dates", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-leap-date-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(join(repositoryRoot, "characters", "Example.md"), "# Fixture\n");

  const entry = {
    id: "character-example",
    slug: "example",
    entityType: "character",
    canonicalName: "Example Record",
    publicTitle: "Example Record",
    publicSummary: "A neutral public projection fixture.",
    sourcePaths: ["characters/Example.md"],
    publicationStatus: "approved",
    spoilerClassification: "public",
    approval: { approvedBy: "author", approvedOn: "2024-02-29" },
    relatedEntryIds: [],
    tags: [],
    publicationDate: "2024-02-29",
  };

  const validated = await validatePublicationManifest(
    { schemaVersion: 1, entries: [entry] },
    { repositoryRoot },
  );

  assert.equal(validated.entries[0].publicationDate, "2024-02-29");
});
