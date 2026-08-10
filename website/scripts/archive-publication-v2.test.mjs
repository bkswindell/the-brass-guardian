import assert from "node:assert/strict";
import { resolve } from "node:path";
import test from "node:test";

import publicationLedger from "../content/public/manifest.json" with { type: "json" };
import archivePresentation from "../content/public/archive-presentation.json" with { type: "json" };
import archiveRelease from "../content/public/archive-release.json" with { type: "json" };
import assetRegistry from "../content/public/archive-assets.json" with { type: "json" };

import { loadCanonRecords } from "./lib/canon-record-loader.mjs";
import { buildArchivePublicationV2 } from "./lib/archive-publication-v2-model.mjs";
import { validateArchivePresentationV2 } from "./lib/archive-presentation-v2.mjs";
import { validatePublicationLedgerV2 } from "./lib/publication-boundary-v2.mjs";

const repositoryRoot = resolve(process.cwd(), "..");
const records = await loadCanonRecords({ repositoryRoot });

test("v2 ledger and presentation validate their approved closed shapes", () => {
  assert.equal(validatePublicationLedgerV2(publicationLedger).entries.length, 95);
  const presentation = validateArchivePresentationV2(archivePresentation);
  assert.equal(presentation.mapEntries.length, 30);
  assert.equal(presentation.curatorRoute.length, 8);
});

test("v2 ledger rejects unknown fields, duplicate IDs, malformed hashes, and malformed dates", () => {
  const unknown = structuredClone(publicationLedger);
  unknown.entries[0].sourcePaths = ["characters/Amelia_Hawthorne.md"];
  assert.throws(() => validatePublicationLedgerV2(unknown), /unrecognized field/u);

  const duplicate = structuredClone(publicationLedger);
  duplicate.entries[1].id = duplicate.entries[0].id;
  assert.throws(() => validatePublicationLedgerV2(duplicate), /duplicate publication ledger id/u);

  const badHash = structuredClone(publicationLedger);
  badHash.entries[0].projectionHash = "sha256:not-a-digest";
  assert.throws(() => validatePublicationLedgerV2(badHash), /invalid projectionHash/u);

  const badDate = structuredClone(publicationLedger);
  badDate.entries[0].approvedOn = "2026-02-31";
  assert.throws(() => validatePublicationLedgerV2(badDate), /approvedOn/u);
});

test("v2 presentation rejects duplicate canonical IDs, unsafe geometry, and extra fields", () => {
  const duplicate = structuredClone(archivePresentation);
  duplicate.mapEntries[1].id = duplicate.mapEntries[0].id;
  assert.throws(() => validateArchivePresentationV2(duplicate), /duplicate map entry id/u);

  const geometry = structuredClone(archivePresentation);
  geometry.mapEntries[0].mapRegion.cx = 1540;
  assert.throws(() => validateArchivePresentationV2(geometry), /geometry cx/u);

  const markerLeak = structuredClone(archivePresentation);
  markerLeak.mapEntries[0].mapMarker = "1";
  assert.throws(() => validateArchivePresentationV2(markerLeak), /unrecognized map entry field/u);
});

test("published v2 model resolves the exact C1-sized projection from Schema v1 Markdown", async () => {
  const archive = await buildArchivePublicationV2({
    records,
    ledger: publicationLedger,
    presentation: archivePresentation,
    release: archiveRelease,
    assetRegistry,
    repositoryRoot,
    preview: false,
  });

  assert.equal(records.length, 210);
  assert.equal(archive.entries.length, 67);
  assert.equal(archive.hiddenEntries.length, 28);
  assert.equal(archive.mapEntries.length, 24);
  assert.equal(archive.hiddenMapEntries.length, 6);
  assert.equal(archive.curatorRoute.length, 8);
  assert.deepEqual(
    [...archive.mapEntries, ...archive.hiddenMapEntries]
      .map((entry) => entry.mapMarker)
      .sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
    [
      ...Array.from({ length: 24 }, (_, index) => String(index + 1)),
      "A",
      "B",
      "C",
      "D",
      "E",
      "F",
    ].sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
  );
});

test("changing approved public Markdown invalidates the projection fingerprint", async () => {
  const changedRecords = structuredClone(records);
  const target = changedRecords.find((record) => record.id === publicationLedger.entries[0].id);
  target.public_projection.summary += " Unauthorized change.";

  await assert.rejects(
    buildArchivePublicationV2({
      records: changedRecords,
      ledger: publicationLedger,
      presentation: archivePresentation,
      release: archiveRelease,
      assetRegistry,
      repositoryRoot,
      preview: false,
    }),
    /public projection changed after author approval/u,
  );
});

test("sealed mode fails closed while Preview uses the same Markdown projections without ledger authorization", async () => {
  const sealed = await buildArchivePublicationV2({
    records,
    ledger: publicationLedger,
    presentation: archivePresentation,
    release: {
      schemaVersion: 1,
      status: "sealed",
      approvedBy: "author",
      approvedOn: "2026-08-10",
      includeHiddenArchives: false,
    },
    assetRegistry,
    repositoryRoot,
    preview: false,
  });
  assert.equal(sealed.enabled, false);
  assert.deepEqual(sealed.entries, []);

  const preview = await buildArchivePublicationV2({
    records,
    ledger: { schemaVersion: 2, entries: [] },
    presentation: archivePresentation,
    release: archiveRelease,
    assetRegistry,
    repositoryRoot,
    preview: true,
  });
  assert.equal(preview.enabled, true);
  assert.equal(preview.isPreview, true);
  assert.equal(preview.noindex, true);
  assert.equal(preview.entries.length, 67);
  assert.equal(preview.hiddenEntries.length, 28);
});
