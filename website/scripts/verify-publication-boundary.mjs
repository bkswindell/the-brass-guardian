import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import publicationLedger from "../content/public/manifest.json" with { type: "json" };
import archivePresentation from "../content/public/archive-presentation.json" with { type: "json" };
import archiveRelease from "../content/public/archive-release.json" with { type: "json" };
import assetRegistry from "../content/public/archive-assets.json" with { type: "json" };

import { loadCanonRecords } from "./lib/canon-record-loader.mjs";
import { buildArchivePublicationV2 } from "./lib/archive-publication-v2-model.mjs";

const scriptsRoot = dirname(fileURLToPath(import.meta.url));
const websiteRoot = resolve(scriptsRoot, "..");
const repositoryRoot = resolve(websiteRoot, "..");

try {
  const records = await loadCanonRecords({ repositoryRoot });
  const archive = await buildArchivePublicationV2({
    records,
    ledger: publicationLedger,
    presentation: archivePresentation,
    release: archiveRelease,
    assetRegistry,
    repositoryRoot,
    preview: false,
  });

  if (archiveRelease.status === "published") {
    if (records.length !== 210) {
      throw new Error(`expected 210 Schema v1 canonical records; found ${records.length}.`);
    }
    if (publicationLedger.entries.length !== 95) {
      throw new Error(
        `published Archive requires 95 approved projection fingerprints; found ${publicationLedger.entries.length}.`,
      );
    }
    if (archive.entries.length !== 67) {
      throw new Error(
        `published Archive requires 67 public catalog records; found ${archive.entries.length}.`,
      );
    }
    if (archive.hiddenEntries.length !== 28) {
      throw new Error(
        `published Archive requires 28 Hidden Archive teasers; found ${archive.hiddenEntries.length}.`,
      );
    }
    if (archive.mapEntries.length + archive.hiddenMapEntries.length !== 30) {
      throw new Error("published Archive requires 30 canonical map references.");
    }
    if (archive.curatorRoute.length !== 8) {
      throw new Error("published Archive requires the approved eight-stop Curator Route.");
    }
  }

  console.log(
    `Publication boundary passed: ${records.length} Schema v1 canon record(s), ${publicationLedger.entries.length} exact approved projection fingerprint(s), ${archive.entries.length} public catalog record(s), ${archive.hiddenEntries.length} Hidden Archive teaser(s), ${archive.mapEntries.length + archive.hiddenMapEntries.length} canonical map link(s), release ${archiveRelease.status}.`,
  );
} catch (error) {
  console.error(`Publication boundary failed: ${error.message}`);
  process.exit(1);
}
