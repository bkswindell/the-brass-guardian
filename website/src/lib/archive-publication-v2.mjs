import { resolve } from "node:path";

import { getCollection } from "astro:content";

import publicationLedger from "../../content/public/manifest.json" with { type: "json" };
import archiveRelease from "../../content/public/archive-release.json" with { type: "json" };
import archivePresentation from "../../content/public/archive-presentation.json" with { type: "json" };
import assetRegistry from "../../content/public/archive-assets.json" with { type: "json" };

import { validateCanonRecords } from "../../scripts/lib/canon-schema-v1.mjs";
import {
  buildArchivePublicationV2,
  projectionFingerprintForRecord,
} from "../../scripts/lib/archive-publication-v2-model.mjs";

const repositoryRoot = resolve(process.cwd(), "..");

const loadCanon = async () => {
  const entries = await getCollection("canon");
  const records = entries.map((entry) => entry.data);
  validateCanonRecords(records);
  return records;
};

export const getArchivePublicationV2 = async (
  env = process.env,
  candidateRelease = archiveRelease,
) => {
  const production = env.VERCEL_ENV === "production";
  const preview =
    !production &&
    (env.PUBLICATION_PREVIEW === "1" || env.VERCEL_ENV === "preview");

  return buildArchivePublicationV2({
    records: await loadCanon(),
    ledger: publicationLedger,
    presentation: archivePresentation,
    release: candidateRelease,
    assetRegistry,
    repositoryRoot,
    preview,
  });
};

export const getArchiveProjectionFingerprintV2 = async (record) =>
  projectionFingerprintForRecord(record, { repositoryRoot });
