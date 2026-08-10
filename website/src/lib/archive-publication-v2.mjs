import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";

import { getCollection } from "astro:content";

import publicationLedger from "../../content/public/manifest.v2.json" with { type: "json" };
import archiveRelease from "../../content/public/archive-release.json" with { type: "json" };
import archivePresentation from "../../content/public/archive-presentation.v2.json" with { type: "json" };
import assetRegistry from "../../content/public/archive-assets.json" with { type: "json" };

import { validateCanonRecords } from "../../scripts/lib/canon-schema-v1.mjs";
import { validateArchiveRelease } from "../../scripts/lib/archive-release.mjs";
import { validatePublicationLedgerV2 } from "../../scripts/lib/publication-boundary-v2.mjs";
import { validateArchivePresentationV2 } from "../../scripts/lib/archive-presentation-v2.mjs";
import {
  archiveEntryHref,
  getAetherhavenMapReference,
  normalizeProjectionFingerprint,
  projectionHash,
  selectedProjectionAsset,
  toArchiveEntry,
} from "./archive-content-model.mjs";

const repositoryRoot = fileURLToPath(new URL("../../../", import.meta.url));
const expectedMapMarkers = [
  ...Array.from({ length: 24 }, (_, index) => String(index + 1)),
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
];

const sealedArchive = {
  enabled: false,
  mode: "sealed",
  isPublic: false,
  isPreview: false,
  noindex: true,
  entries: [],
  mapEntries: [],
  hiddenEntries: [],
  hiddenMapEntries: [],
  curatorRoute: [],
};

const sha256File = async (path) => {
  const bytes = await readFile(resolve(repositoryRoot, path));
  return createHash("sha256").update(bytes).digest("hex");
};

const projectionFingerprintForRecord = async (record) => {
  const asset = selectedProjectionAsset(record);
  const sourceAssetSha256 = asset ? await sha256File(asset.path) : null;
  return projectionHash(
    normalizeProjectionFingerprint(record, { sourceAssetSha256 }),
  );
};

const loadCanon = async () => {
  const entries = await getCollection("canon");
  const records = entries.map((entry) => entry.data);
  validateCanonRecords(records);
  return records;
};

const resolvePresentation = (archiveEntriesById, presentation) => {
  const mapEntries = presentation.mapEntries.map((presentationEntry) => {
    const entry = archiveEntriesById.get(presentationEntry.id);
    if (!entry) {
      throw new Error(
        `Archive presentation references a record unavailable in this projection: ${presentationEntry.id}`,
      );
    }
    const marker = entry.mapMarker;
    if (!marker) {
      throw new Error(
        `Archive presentation record has no canonical Aetherhaven map reference: ${presentationEntry.id}`,
      );
    }
    return { ...entry, ...presentationEntry, mapMarker: marker };
  });

  const markerSet = new Set(mapEntries.map((entry) => entry.mapMarker));
  for (const marker of expectedMapMarkers) {
    if (!markerSet.has(marker)) {
      throw new Error(`Archive presentation is missing canonical map reference ${marker}.`);
    }
  }
  if (markerSet.size !== expectedMapMarkers.length) {
    throw new Error("Archive presentation contains an unexpected canonical map reference.");
  }

  for (const entry of mapEntries) {
    const restricted = /^[A-F]$/u.test(entry.mapMarker);
    if (restricted !== (entry.archiveSection === "hidden")) {
      throw new Error(
        `${entry.id}: canonical map reference conflicts with Archive public/hidden placement.`,
      );
    }
  }

  const curatorRoute = presentation.curatorRoute.map((step) => {
    if (step.kind === "room") return step;
    const entry = archiveEntriesById.get(step.id);
    if (!entry || entry.archiveSection !== "catalog") {
      throw new Error(`Curator Route record is not available in the public catalog: ${step.id}`);
    }
    return {
      ...step,
      title: entry.publicTitle,
      href: archiveEntryHref(entry),
      entityType: entry.entityType,
    };
  });

  return { mapEntries, curatorRoute };
};

export const isArchivePublishedV2 = (candidateRelease = archiveRelease) =>
  validateArchiveRelease(candidateRelease).status === "published";

export const getArchivePublicationV2 = async (
  env = process.env,
  candidateRelease = archiveRelease,
) => {
  const release = validateArchiveRelease(candidateRelease);
  const presentation = validateArchivePresentationV2(archivePresentation);
  const ledger = validatePublicationLedgerV2(publicationLedger);
  const records = await loadCanon();
  const recordsWithProjection = records.filter((record) => record.public_projection);

  const production = env.VERCEL_ENV === "production";
  const preview =
    !production &&
    (env.PUBLICATION_PREVIEW === "1" || env.VERCEL_ENV === "preview");

  if (!preview && release.status !== "published") return sealedArchive;

  const recordsById = new Map(recordsWithProjection.map((record) => [record.id, record]));
  let selectedRecords;

  if (preview) {
    selectedRecords = recordsWithProjection;
  } else {
    const approved = new Map();
    for (const approval of ledger.entries) {
      const record = recordsById.get(approval.id);
      if (!record) {
        throw new Error(
          `Publication approval has no matching canonical public projection: ${approval.id}`,
        );
      }
      const actualHash = await projectionFingerprintForRecord(record);
      if (actualHash !== approval.projectionHash) {
        throw new Error(
          `${approval.id}: public projection changed after author approval. Expected ${approval.projectionHash}; received ${actualHash}.`,
        );
      }
      approved.set(record.id, record);
    }

    for (const record of approved.values()) {
      for (const relatedId of record.public_projection.related ?? []) {
        if (!approved.has(relatedId)) {
          throw new Error(
            `${record.id}: approved public relationship targets an unapproved projection: ${relatedId}`,
          );
        }
      }
    }
    selectedRecords = [...approved.values()];
  }

  const archiveEntries = selectedRecords.map((record) => ({
    ...toArchiveEntry(record, assetRegistry),
    ...(preview ? { previewStatus: "proposal" } : {}),
  }));
  const archiveEntriesById = new Map(archiveEntries.map((entry) => [entry.id, entry]));
  const { mapEntries: resolvedMapEntries, curatorRoute } = resolvePresentation(
    archiveEntriesById,
    presentation,
  );
  const mapById = new Map(resolvedMapEntries.map((entry) => [entry.id, entry]));

  const enriched = archiveEntries.map((entry) => mapById.get(entry.id) ?? entry);
  const catalogEntries = enriched.filter(
    (entry) => entry.archiveSection === "catalog",
  );
  const allHiddenEntries = enriched.filter(
    (entry) => entry.archiveSection === "hidden",
  );
  const hiddenEntries = release.includeHiddenArchives || preview ? allHiddenEntries : [];
  const mapEntries = catalogEntries.filter((entry) => entry.mapRegion && entry.mapLabel);
  const hiddenMapEntries = hiddenEntries.filter(
    (entry) => entry.mapRegion && entry.mapLabel,
  );

  return {
    enabled: true,
    mode: preview ? "preview" : "public",
    isPublic: !preview,
    isPreview: preview,
    noindex: preview,
    entries: catalogEntries,
    mapEntries,
    hiddenEntries,
    hiddenMapEntries,
    curatorRoute,
  };
};

export const getArchiveProjectionFingerprintV2 = projectionFingerprintForRecord;
