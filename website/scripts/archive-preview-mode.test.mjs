import assert from "node:assert/strict";
import test from "node:test";

import {
  getWorldEntrancePreview,
  isArchivePreviewEnabled,
} from "../src/lib/archive-preview.mjs";

test("keeps proposal records disabled for production builds", () => {
  assert.equal(isArchivePreviewEnabled({ VERCEL_ENV: "production" }), false);
  assert.equal(isArchivePreviewEnabled({}), false);

  const preview = getWorldEntrancePreview({ VERCEL_ENV: "production" });
  assert.equal(preview.enabled, false);
  assert.deepEqual(preview.entries, []);
});

test("enables proposal records only for explicit local or Vercel preview builds", () => {
  assert.equal(isArchivePreviewEnabled({ PUBLICATION_PREVIEW: "1" }), true);
  assert.equal(isArchivePreviewEnabled({ VERCEL_ENV: "preview" }), true);
  assert.equal(isArchivePreviewEnabled({ PUBLICATION_PREVIEW: "0" }), false);

  const preview = getWorldEntrancePreview({ VERCEL_ENV: "preview" });
  assert.equal(preview.enabled, true);
  assert.equal(preview.entries.length, 7);
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
});
