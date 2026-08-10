import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import {
  getArchivePublication,
  isArchivePublished,
} from "../src/lib/archive-publication.mjs";

const publicationSourceUrl = new URL(
  "../src/lib/archive-publication.mjs",
  import.meta.url,
);

test("production publication has no static dependency on raw Preview catalogs", async () => {
  const source = await readFile(publicationSourceUrl, "utf8");

  assert.doesNotMatch(source, /from\s+["']\.\/archive-preview\.mjs["']/u);
  assert.match(source, /await\s+import\(["']\.\/archive-preview\.mjs["']\)/u);
  assert.ok(
    source.indexOf("await import") > source.indexOf("if (preview)"),
    "Preview data must be imported only after entering the Preview branch.",
  );
});

test("publishes only the approved projection in production", async () => {
  assert.equal(isArchivePublished(), true);

  const archive = await getArchivePublication({
    VERCEL_ENV: "production",
    PUBLICATION_PREVIEW: "1",
  });

  assert.equal(archive.enabled, true);
  assert.equal(archive.mode, "public");
  assert.equal(archive.isPublic, true);
  assert.equal(archive.isPreview, false);
  assert.equal(archive.noindex, false);
  assert.equal(archive.entries.length, 67);
  assert.equal(archive.mapEntries.length, 24);
  assert.equal(archive.hiddenEntries.length, 28);
  assert.equal(archive.hiddenMapEntries.length, 6);
  assert.ok(
    [...archive.entries, ...archive.hiddenEntries].every(
      (entry) =>
        !("sourcePaths" in entry) &&
        !("approval" in entry) &&
        !("publicationStatus" in entry) &&
        !("previewStatus" in entry),
    ),
  );
});

test("keeps proposal data isolated to explicit Preview builds", async () => {
  const archive = await getArchivePublication({ VERCEL_ENV: "preview" });

  assert.equal(archive.enabled, true);
  assert.equal(archive.mode, "preview");
  assert.equal(archive.isPublic, false);
  assert.equal(archive.isPreview, true);
  assert.equal(archive.noindex, true);
  assert.equal(archive.entries.length, 67);
  assert.equal(archive.hiddenEntries.length, 28);
  assert.ok(archive.entries.every((entry) => entry.previewStatus === "proposal"));
});

test("uses the published projection for ordinary local production builds", async () => {
  const archive = await getArchivePublication({});
  assert.equal(archive.mode, "public");
  assert.equal(archive.noindex, false);
});

test("supports an explicit version-controlled rollback to a sealed Archive", async () => {
  const archive = await getArchivePublication(
    { VERCEL_ENV: "production", PUBLICATION_PREVIEW: "1" },
    {
      schemaVersion: 1,
      status: "sealed",
      approvedBy: "author",
      approvedOn: "2026-08-10",
      includeHiddenArchives: false,
    },
  );

  assert.equal(archive.enabled, false);
  assert.equal(archive.mode, "sealed");
  assert.deepEqual(archive.entries, []);
  assert.deepEqual(archive.hiddenEntries, []);
});
