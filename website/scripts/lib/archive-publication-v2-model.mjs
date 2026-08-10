import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

import { validateArchiveRelease } from "./archive-release.mjs";
import { validatePublicationLedgerV2 } from "./publication-boundary-v2.mjs";
import { validateArchivePresentationV2 } from "./archive-presentation-v2.mjs";
import {
  archiveEntryHref,
  normalizeProjectionFingerprint,
  projectionHash,
  selectedProjectionAsset,
  toArchiveEntry,
} from "../../src/lib/archive-content-model.mjs";

const expectedMapMarkers = Object.freeze([
  ...Array.from({ length: 24 }, (_, index) => String(index + 1)),
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
]);

export const sealedArchiveProjection = Object.freeze({
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
});

const sha256File = async (repositoryRoot, path) => {
  const bytes = await readFile(resolve(repositoryRoot, path));
  return createHash("sha256").update(bytes).digest("hex");
};

export const projectionFingerprintForRecord = async (
  record,
  { repositoryRoot },
) => {
  const asset = selectedProjectionAsset(record);
  const sourceAssetSha256 = asset
    ? await sha256File(repositoryRoot, asset.path)
    : null;
  return projectionHash(
    normalizeProjectionFingerprint(record, { sourceAssetSha256 }),
  );
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
      throw new Error(
        `Curator Route record is not available in the public catalog: ${step.id}`,
      );
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

export const buildArchivePublicationV2 = async ({
  records,
  ledger,
  presentation,
  release,
  assetRegistry,
  repositoryRoot,
  preview = false,
}) => {
  const resolvedRelease = validateArchiveRelease(release);
  const resolvedPresentation = validateArchivePresentationV2(presentation);
  const resolvedLedger = validatePublicationLedgerV2(ledger);
  const recordsWithProjection = records.filter((record) => record.public_projection);

  if (!preview && resolvedRelease.status !== "published") {
    return sealedArchiveProjection;
  }

  const recordsById = new Map(
    recordsWithProjection.map((record) => [record.id, record]),
  );
  let selectedRecords;

  if (preview) {
    selectedRecords = recordsWithProjection;
  } else {
    const approved = new Map();
    for (const approval of resolvedLedger.entries) {
      const record = recordsById.get(approval.id);
      if (!record) {
        throw new Error(
          `Publication approval has no matching canonical public projection: ${approval.id}`,
        );
      }
      const actualHash = await projectionFingerprintForRecord(record, {
        repositoryRoot,
      });
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
  const archiveEntriesById = new Map(
    archiveEntries.map((entry) => [entry.id, entry]),
  );
  const { mapEntries: resolvedMapEntries, curatorRoute } = resolvePresentation(
    archiveEntriesById,
    resolvedPresentation,
  );
  const mapById = new Map(
    resolvedMapEntries.map((entry) => [entry.id, entry]),
  );

  const enriched = archiveEntries.map((entry) => mapById.get(entry.id) ?? entry);
  const catalogEntries = enriched.filter(
    (entry) => entry.archiveSection === "catalog",
  );
  const allHiddenEntries = enriched.filter(
    (entry) => entry.archiveSection === "hidden",
  );
  const hiddenEntries =
    resolvedRelease.includeHiddenArchives || preview ? allHiddenEntries : [];
  const mapEntries = catalogEntries.filter(
    (entry) => entry.mapRegion && entry.mapLabel,
  );
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
