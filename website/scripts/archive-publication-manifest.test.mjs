import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const readJson = async (path) => JSON.parse(await readFile(new URL(path, import.meta.url), "utf8"));

test("approves the exact C1 public and Hidden Archive projection", async () => {
  const release = await readJson("../content/public/archive-release.json");
  const manifest = await readJson("../content/public/manifest.json");
  const presentation = await readJson("../content/public/archive-presentation.json");

  assert.deepEqual(release, {
    schemaVersion: 1,
    status: "published",
    approvedBy: "author",
    approvedOn: "2026-08-10",
    includeHiddenArchives: true,
  });

  assert.equal(manifest.schemaVersion, 1);
  assert.equal(manifest.entries.length, 95);
  assert.equal(new Set(manifest.entries.map((entry) => entry.id)).size, 95);
  assert.equal(new Set(manifest.entries.map((entry) => entry.slug)).size, 95);
  assert.equal(
    manifest.entries.filter((entry) => entry.tags.includes("hidden-archive")).length,
    28,
  );
  assert.ok(
    manifest.entries.every(
      (entry) =>
        entry.publicationStatus === "approved" &&
        entry.approval.approvedBy === "author" &&
        entry.approval.approvedOn === "2026-08-10" &&
        ["public", "teaser"].includes(entry.spoilerClassification),
    ),
  );

  assert.deepEqual(presentation.approval, {
    approvedBy: "author",
    approvedOn: "2026-08-10",
  });
  assert.equal(presentation.schemaVersion, 1);
  assert.equal(presentation.mapEntries.length, 30);
  assert.deepEqual(
    presentation.mapEntries.map((entry) => entry.mapMarker),
    [...Array.from({ length: 24 }, (_, index) => String(index + 1)), "A", "B", "C", "D", "E", "F"],
  );
  assert.equal(presentation.curatorRoute.length, 8);
  assert.deepEqual(
    presentation.curatorRoute.map((step) => step.id),
    [
      "location-aetherhaven",
      "map-room",
      "location-clockwork-gardens",
      "location-gardens-airship-landing",
      "vessel-wayfinder",
      "location-aerial-docks",
      "district-merchant",
      "district-inventors",
    ],
  );
});
