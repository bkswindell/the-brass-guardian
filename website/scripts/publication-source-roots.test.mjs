import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { validatePublicationManifest } from "./lib/publication-boundary.mjs";

test("rejects source paths outside approved canonical source roots", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-source-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "website"), { recursive: true });
  await writeFile(join(repositoryRoot, "website", "README.md"), "# Internal\n");

  const entry = {
    id: "archive-record-example",
    slug: "example",
    entityType: "archive-record",
    canonicalName: "Example Record",
    publicTitle: "Example Record",
    publicSummary: "A neutral public projection fixture.",
    sourcePaths: ["website/README.md"],
    publicationStatus: "approved",
    spoilerClassification: "public",
    approval: { approvedBy: "author", approvedOn: "2026-08-09" },
    relatedEntryIds: [],
    tags: [],
  };

  await assert.rejects(
    validatePublicationManifest(
      { schemaVersion: 1, entries: [entry] },
      { repositoryRoot },
    ),
    /source path must use an approved canonical source root/,
  );
});
