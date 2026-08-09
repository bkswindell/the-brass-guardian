import assert from "node:assert/strict";
import test from "node:test";

import {
  getWorldEntrancePreview,
  isArchivePreviewEnabled,
} from "../src/lib/archive-preview.mjs";

test("keeps proposal records disabled for production builds", () => {
  assert.equal(isArchivePreviewEnabled({ VERCEL_ENV: "production" }), false);
  assert.equal(
    isArchivePreviewEnabled({
      VERCEL_ENV: "production",
      PUBLICATION_PREVIEW: "1",
    }),
    false,
  );
  assert.equal(isArchivePreviewEnabled({}), false);

  const preview = getWorldEntrancePreview({ VERCEL_ENV: "production" });
  assert.equal(preview.enabled, false);
  assert.deepEqual(preview.entries, []);
  assert.deepEqual(preview.curatorRoute, []);

  const conflictingPreview = getWorldEntrancePreview({
    VERCEL_ENV: "production",
    PUBLICATION_PREVIEW: "1",
  });
  assert.equal(conflictingPreview.enabled, false);
  assert.deepEqual(conflictingPreview.entries, []);
});

test("enables proposal records only for explicit local or Vercel preview builds", () => {
  assert.equal(isArchivePreviewEnabled({ PUBLICATION_PREVIEW: "1" }), true);
  assert.equal(isArchivePreviewEnabled({ VERCEL_ENV: "preview" }), true);
  assert.equal(isArchivePreviewEnabled({ PUBLICATION_PREVIEW: "0" }), false);

  const preview = getWorldEntrancePreview({ VERCEL_ENV: "preview" });
  assert.equal(preview.enabled, true);
  assert.equal(preview.entries.length, 7);
  assert.deepEqual(
    preview.curatorRoute.map((step) => step.id),
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
  assert.ok(preview.curatorRoute.every((step) => step.href.startsWith("/archive/")));
});

test("marks every preview record as a non-canonical proposal", () => {
  const { entries } = getWorldEntrancePreview({ PUBLICATION_PREVIEW: "1" });
  const ids = entries.map((entry) => entry.id);
  const slugs = entries.map((entry) => entry.slug);

  assert.equal(new Set(ids).size, entries.length);
  assert.equal(new Set(slugs).size, entries.length);
  assert.ok(entries.every((entry) => entry.previewStatus === "proposal"));
  assert.ok(entries.every((entry) => !("approval" in entry)));
  assert.ok(entries.every((entry) => !("publicationStatus" in entry)));
  assert.ok(
    entries.every((entry) =>
      entry.relatedEntryIds.every((relatedId) => ids.includes(relatedId)),
    ),
  );

  const markerPositions = Object.fromEntries(
    entries
      .filter((entry) => entry.mapMarker)
      .map((entry) => [entry.mapMarker, entry.mapPosition]),
  );
  assert.deepEqual(markerPositions[8], { x: 28, y: 59 });
  assert.deepEqual(markerPositions[13], { x: 57, y: 23.4 });
});
