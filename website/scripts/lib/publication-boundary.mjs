import { realpath, stat } from "node:fs/promises";
import { isAbsolute, relative, resolve, sep } from "node:path";

const allowedManifestFields = new Set(["schemaVersion", "entries"]);
const allowedEntryFields = new Set([
  "id",
  "slug",
  "entityType",
  "canonicalName",
  "publicTitle",
  "publicSummary",
  "sourcePaths",
  "publicationStatus",
  "spoilerClassification",
  "approval",
  "image",
  "relatedEntryIds",
  "tags",
  "publicationDate",
]);
const allowedApprovalFields = new Set(["approvedBy", "approvedOn"]);
const allowedImageFields = new Set(["src", "alt", "width", "height"]);
const allowedCanonicalSourceRoots = new Set([
  "characters",
  "organizations",
  "locations",
  "historical_events",
  "story_arcs",
  "story_drafts",
  "artifacts",
]);
const kebabCasePattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const isoDatePattern = /^\d{4}-\d{2}-\d{2}$/;
const publicImageUrlPattern =
  /^\/(?:[A-Za-z0-9._-]+\/)*[A-Za-z0-9._-]+\.(?:avif|gif|jpe?g|png|svg|webp)$/i;
const isIsoDate = (value) => {
  if (typeof value !== "string" || !isoDatePattern.test(value)) {
    return false;
  }
  const [year, month, day] = value.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return (
    date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day
  );
};
export const publicEntityTypes = Object.freeze([
  "character",
  "location",
  "district",
  "organization",
  "artifact",
  "story",
  "archive-record",
  "vessel",
  "event",
  "rumor",
]);
const publicEntityTypeSet = new Set(publicEntityTypes);

const invalidField = (entryId, field) =>
  new Error(`${entryId ?? "entry"}: invalid publication field: ${field}`);

export const toPublicArchiveEntry = (entry) => ({
  id: entry.id,
  slug: entry.slug,
  entityType: entry.entityType,
  canonicalName: entry.canonicalName,
  publicTitle: entry.publicTitle,
  publicSummary: entry.publicSummary,
  spoilerClassification: entry.spoilerClassification,
  relatedEntryIds: [...entry.relatedEntryIds],
  tags: [...entry.tags],
  ...(entry.image
    ? {
        image: {
          src: entry.image.src,
          alt: entry.image.alt,
          width: entry.image.width,
          height: entry.image.height,
        },
      }
    : {}),
  ...(entry.publicationDate
    ? { publicationDate: entry.publicationDate }
    : {}),
});

export const validatePublicationManifest = async (
  manifest,
  { repositoryRoot, publicRoot = resolve(repositoryRoot, "website", "public") },
) => {
  if (manifest?.schemaVersion !== 1) {
    throw new Error("publication manifest schemaVersion must be 1.");
  }
  if (!Array.isArray(manifest.entries)) {
    throw new Error("publication manifest entries must be an array.");
  }
  const unrecognizedManifestField = Object.keys(manifest).find(
    (field) => !allowedManifestFields.has(field),
  );
  if (unrecognizedManifestField) {
    throw new Error(`unrecognized manifest field: ${unrecognizedManifestField}`);
  }

  const seenIds = new Set();
  const seenSlugs = new Set();

  for (const entry of manifest.entries) {
    const hasImage = Object.hasOwn(entry, "image");
    for (const field of ["canonicalName", "publicTitle", "publicSummary"]) {
      if (typeof entry[field] !== "string" || !entry[field].trim()) {
        throw invalidField(entry.id, field);
      }
    }
    if (!Array.isArray(entry.sourcePaths) || entry.sourcePaths.length === 0) {
      throw invalidField(entry.id, "sourcePaths");
    }
    if (!Array.isArray(entry.relatedEntryIds)) {
      throw invalidField(entry.id, "relatedEntryIds");
    }
    if (!Array.isArray(entry.tags)) {
      throw invalidField(entry.id, "tags");
    }
    for (const field of ["sourcePaths", "relatedEntryIds", "tags"]) {
      if (entry[field].some((value) => typeof value !== "string")) {
        throw invalidField(entry.id, field);
      }
    }
    if (
      new Set(entry.tags).size !== entry.tags.length ||
      new Set(entry.relatedEntryIds).size !== entry.relatedEntryIds.length
    ) {
      throw new Error(
        `${entry.id}: tags and relatedEntryIds must contain unique values.`,
      );
    }
    if (entry.relatedEntryIds.includes(entry.id)) {
      throw new Error(`${entry.id}: a public record cannot relate to itself.`);
    }
    if (
      entry.approval?.approvedBy !== "author" ||
      !isIsoDate(entry.approval?.approvedOn)
    ) {
      throw invalidField(entry.id, "approval");
    }
    if (!publicEntityTypeSet.has(entry.entityType)) {
      throw new Error(
        `${entry.id}: unsupported public entity type: ${entry.entityType}`,
      );
    }
    if (
      entry.publicationDate !== undefined &&
      !isIsoDate(entry.publicationDate)
    ) {
      throw new Error(`${entry.id}: publicationDate must use YYYY-MM-DD.`);
    }

    const unrecognizedField = Object.keys(entry).find(
      (field) => !allowedEntryFields.has(field),
    );
    if (unrecognizedField) {
      throw new Error(`${entry.id}: unrecognized field: ${unrecognizedField}`);
    }
    const unrecognizedApprovalField = Object.keys(entry.approval).find(
      (field) => !allowedApprovalFields.has(field),
    );
    if (unrecognizedApprovalField) {
      throw new Error(
        `${entry.id}: unrecognized approval field: ${unrecognizedApprovalField}`,
      );
    }
    if (
      hasImage &&
      (entry.image === null ||
        typeof entry.image !== "object" ||
        Array.isArray(entry.image))
    ) {
      throw new Error(`${entry.id}: image must be a non-null object.`);
    }
    const unrecognizedImageField = hasImage
      ? Object.keys(entry.image).find((field) => !allowedImageFields.has(field))
      : undefined;
    if (unrecognizedImageField) {
      throw new Error(
        `${entry.id}: unrecognized image field: ${unrecognizedImageField}`,
      );
    }

    for (const field of ["id", "slug"]) {
      if (!kebabCasePattern.test(entry[field])) {
        throw new Error(`${field} must be lowercase kebab-case: ${entry[field]}`);
      }
    }

    if (seenIds.has(entry.id)) {
      throw new Error(`duplicate public ID: ${entry.id}`);
    }
    if (seenSlugs.has(entry.slug)) {
      throw new Error(`duplicate public slug: ${entry.slug}`);
    }
    seenIds.add(entry.id);
    seenSlugs.add(entry.slug);

    if (entry.publicationStatus !== "approved") {
      throw new Error(
        `${entry.id}: publicationStatus must be approved for the public projection.`,
      );
    }

    if (!new Set(["public", "teaser"]).has(entry.spoilerClassification)) {
      throw new Error(
        `${entry.id}: spoilerClassification must be public or teaser.`,
      );
    }

    if (
      hasImage &&
      (typeof entry.image.alt !== "string" || !entry.image.alt.trim())
    ) {
      throw new Error(`${entry.id}: image alt text is required.`);
    }
    if (hasImage) {
      if (
        !Number.isInteger(entry.image.width) ||
        entry.image.width <= 0 ||
        !Number.isInteger(entry.image.height) ||
        entry.image.height <= 0
      ) {
        throw new Error(
          `${entry.id}: image width and height must be positive integers.`,
        );
      }
      if (typeof entry.image.src !== "string") {
        throw new Error(`${entry.id}: image src must be a safe public asset path.`);
      }
      const imageUrlSegments = entry.image.src.split("/").slice(1);
      if (
        !publicImageUrlPattern.test(entry.image.src) ||
        imageUrlSegments.some((segment) => segment === "." || segment === "..")
      ) {
        throw new Error(
          `${entry.id}: image src must be a canonical public asset URL: ${entry.image.src}`,
        );
      }
      const imagePath = resolve(publicRoot, entry.image.src.slice(1));
      const relativeImagePath = relative(publicRoot, imagePath);
      const isSafeImagePath =
        typeof entry.image.src === "string" &&
        entry.image.src.startsWith("/") &&
        !entry.image.src.startsWith("//") &&
        !entry.image.src.includes("\\") &&
        !relativeImagePath.startsWith("..") &&
        !isAbsolute(relativeImagePath);
      if (!isSafeImagePath) {
        throw new Error(
          `${entry.id}: image src must be a safe public asset path: ${entry.image.src}`,
        );
      }

      let realImagePath;
      let imageStats;
      try {
        realImagePath = await realpath(imagePath);
        imageStats = await stat(realImagePath);
      } catch {
        throw new Error(
          `${entry.id}: public image does not exist: ${entry.image.src}`,
        );
      }
      const realPublicRoot = await realpath(publicRoot);
      const realImageRelativePath = relative(realPublicRoot, realImagePath);
      if (
        realImageRelativePath.startsWith("..") ||
        isAbsolute(realImageRelativePath)
      ) {
        throw new Error(
          `${entry.id}: public image resolves outside the public root: ${entry.image.src}`,
        );
      }
      if (!imageStats.isFile()) {
        throw new Error(
          `${entry.id}: public image must be a regular file: ${entry.image.src}`,
        );
      }
    }

    for (const sourcePath of entry.sourcePaths) {
      const resolvedSourcePath = resolve(repositoryRoot, sourcePath);
      const relativeSourcePath = relative(repositoryRoot, resolvedSourcePath);
      const isSafeSourcePath =
        typeof sourcePath === "string" &&
        sourcePath.endsWith(".md") &&
        !sourcePath.includes("\\") &&
        !isAbsolute(sourcePath) &&
        !relativeSourcePath.startsWith("..") &&
        !isAbsolute(relativeSourcePath);

      if (!isSafeSourcePath) {
        throw new Error(
          `${entry.id}: source path must be a safe repository-relative Markdown path: ${sourcePath}`,
        );
      }
      const sourceRoot = relativeSourcePath.split(sep, 1)[0];
      if (
        relativeSourcePath !== "README.md" &&
        !allowedCanonicalSourceRoots.has(sourceRoot)
      ) {
        throw new Error(
          `${entry.id}: source path must use an approved canonical source root: ${sourcePath}`,
        );
      }

      let realSourcePath;
      let sourceStats;
      try {
        realSourcePath = await realpath(resolvedSourcePath);
        sourceStats = await stat(realSourcePath);
      } catch {
        throw new Error(`${entry.id}: source path does not exist: ${sourcePath}`);
      }
      const realRepositoryRoot = await realpath(repositoryRoot);
      const realSourceRelativePath = relative(realRepositoryRoot, realSourcePath);
      if (
        realSourceRelativePath.startsWith("..") ||
        isAbsolute(realSourceRelativePath)
      ) {
        throw new Error(
          `${entry.id}: canonical source resolves outside the repository root: ${sourcePath}`,
        );
      }
      const realSourceRoot = realSourceRelativePath.split(sep, 1)[0];
      if (
        realSourceRelativePath !== "README.md" &&
        !allowedCanonicalSourceRoots.has(realSourceRoot)
      ) {
        throw new Error(
          `${entry.id}: canonical source resolves outside an approved source root: ${sourcePath}`,
        );
      }
      if (!sourceStats.isFile()) {
        throw new Error(
          `${entry.id}: canonical source must be a regular file: ${sourcePath}`,
        );
      }
    }
  }

  for (const entry of manifest.entries) {
    for (const relatedEntryId of entry.relatedEntryIds) {
      if (!seenIds.has(relatedEntryId)) {
        throw new Error(
          `${entry.id}: relatedEntryIds contains an unpublished record: ${relatedEntryId}`,
        );
      }
    }
  }

  return manifest;
};
