import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import { isArchivePublished } from "../src/lib/archive-publication.mjs";
import { validatePublicationLedgerV2 } from "./lib/publication-boundary-v2.mjs";
import { validateArchivePresentationV2 } from "./lib/archive-presentation-v2.mjs";
import { validateArchiveRelease } from "./lib/archive-release.mjs";

const publicationSourceUrl = new URL(
  "../src/lib/archive-publication.mjs",
  import.meta.url,
);
const v2SourceUrl = new URL(
  "../src/lib/archive-publication-v2.mjs",
  import.meta.url,
);
const ledgerUrl = new URL("../content/public/manifest.json", import.meta.url);
const presentationUrl = new URL(
  "../content/public/archive-presentation.json",
  import.meta.url,
);
const releaseUrl = new URL(
  "../content/public/archive-release.json",
  import.meta.url,
);

const readJson = async (url) => JSON.parse(await readFile(url, "utf8"));

test("Archive facade routes through Schema v1/v2 without raw Preview catalogs", async () => {
  const [facade, v2] = await Promise.all([
    readFile(publicationSourceUrl, "utf8"),
    readFile(v2SourceUrl, "utf8"),
  ]);

  assert.match(
    facade,
    /await\s+import\(["']\.\/archive-publication-v2\.mjs["']\)/u,
  );
  assert.doesNotMatch(facade, /archive-preview|archive-catalog/u);
  assert.doesNotMatch(v2, /archive-preview|archive-catalog/u);
  assert.match(v2, /getCollection\(["']canon["']\)/u);
  assert.match(v2, /projectionFingerprintForRecord/u);
});

test("active Version 2 approval ledger contains the exact 95-record C1 approval set", async () => {
  const ledger = validatePublicationLedgerV2(await readJson(ledgerUrl));
  assert.equal(ledger.entries.length, 95);
  assert.equal(new Set(ledger.entries.map((entry) => entry.id)).size, 95);
  assert.ok(
    ledger.entries.every(
      (entry) =>
        entry.approvedBy === "author" &&
        /^sha256:[a-f0-9]{64}$/u.test(entry.projectionHash),
    ),
  );
});

test("active Version 2 presentation keeps 30 map geometries and eight Curator Route steps", async () => {
  const presentation = validateArchivePresentationV2(
    await readJson(presentationUrl),
  );
  assert.equal(presentation.mapEntries.length, 30);
  assert.equal(presentation.curatorRoute.length, 8);
  assert.ok(
    presentation.mapEntries.every((entry) => !Object.hasOwn(entry, "mapMarker")),
    "Map marker ownership must come from canonical Markdown cartography.",
  );
});

test("release state remains independently fail-closed", async () => {
  const release = validateArchiveRelease(await readJson(releaseUrl));
  assert.equal(release.status, "published");
  assert.equal(isArchivePublished(), true);

  const sealed = validateArchiveRelease({
    schemaVersion: 1,
    status: "sealed",
    approvedBy: "author",
    approvedOn: "2026-08-10",
    includeHiddenArchives: false,
  });
  assert.equal(sealed.status, "sealed");
});
