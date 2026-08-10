import { createHash } from "node:crypto";

const projectionFields = Object.freeze([
  "title",
  "summary",
  "classification",
  "archive_section",
  "access_label",
  "tags",
  "related",
  "image",
]);

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

export const derivePublicEntityType = (record) => {
  switch (record.record_type) {
    case "character":
      return "character";
    case "location":
      return record.subtype === "district" ? "district" : "location";
    case "organization":
      return "organization";
    case "artifact":
      return "artifact";
    case "vessel":
      return "vessel";
    case "historical_event":
      return "event";
    case "story":
      return "story";
    case "story_arc":
      return "story-arc";
    default:
      throw new Error(`Unsupported canonical record type: ${record.record_type}`);
  }
};

export const getAetherhavenMapReference = (record) => {
  const entry = (record.cartography ?? []).find(
    (candidate) =>
      candidate.map_id === "aetherhaven-city" &&
      candidate.category !== "unlisted",
  );
  return entry?.reference;
};

export const selectedProjectionAsset = (record) => {
  const selection = record.public_projection?.image;
  if (!selection) return undefined;
  const asset = (record.assets ?? []).find(
    (candidate) => candidate.id === selection.asset,
  );
  assert(asset, `${record.id}: selected public asset does not exist: ${selection.asset}`);
  assert(
    asset.visibility === "public" || asset.visibility === "teaser",
    `${record.id}: selected public asset is not safe for publication: ${selection.asset}`,
  );
  return asset;
};

export const normalizeProjectionFingerprint = (
  record,
  { sourceAssetSha256 = null } = {},
) => {
  const projection = record.public_projection;
  assert(projection, `${record.id}: public projection is required.`);
  const unknown = Object.keys(projection).find(
    (field) => !projectionFields.includes(field),
  );
  assert(!unknown, `${record.id}: unknown public projection field: ${unknown}`);

  const asset = selectedProjectionAsset(record);
  const imageAlt = projection.image
    ? projection.image.alt ?? asset?.alt
    : null;

  if (asset) {
    assert(
      typeof sourceAssetSha256 === "string" && /^[a-f0-9]{64}$/u.test(sourceAssetSha256),
      `${record.id}: selected public image requires its source SHA-256 digest.`,
    );
  }

  return {
    id: record.id,
    slug: record.slug,
    entityType: derivePublicEntityType(record),
    canonicalName: record.name,
    publicTitle: projection.title,
    publicSummary: projection.summary,
    spoilerClassification: projection.classification,
    publicAccessLabel: projection.access_label,
    archiveSection: projection.archive_section,
    tags: [...projection.tags],
    relatedEntryIds: [...projection.related],
    image: asset
      ? {
          assetId: asset.id,
          alt: imageAlt,
          sourceSha256,
        }
      : null,
  };
};

export const projectionHash = (normalizedProjection) =>
  `sha256:${createHash("sha256")
    .update(JSON.stringify(normalizedProjection), "utf8")
    .digest("hex")}`;

export const resolvePublishedImage = (record, assetRegistry) => {
  const asset = selectedProjectionAsset(record);
  if (!asset) return undefined;
  const published = assetRegistry?.assets?.[asset.path];
  assert(
    published,
    `${record.id}: selected public asset has no generated Archive derivative registry entry: ${asset.path}`,
  );
  const alt = record.public_projection.image?.alt ?? asset.alt;
  return {
    src: published.src,
    alt,
    width: published.width,
    height: published.height,
    sources: [...(published.sources ?? [])],
    sourcePath: asset.path,
    assetId: asset.id,
  };
};

export const toArchiveEntry = (record, assetRegistry) => {
  const projection = record.public_projection;
  assert(projection, `${record.id}: public projection is required.`);
  return {
    id: record.id,
    slug: record.slug,
    entityType: derivePublicEntityType(record),
    canonicalName: record.name,
    publicTitle: projection.title,
    publicSummary: projection.summary,
    spoilerClassification: projection.classification,
    publicAccessLabel: projection.access_label,
    archiveSection: projection.archive_section,
    relatedEntryIds: [...projection.related],
    tags: [...projection.tags],
    ...(projection.image
      ? { image: resolvePublishedImage(record, assetRegistry) }
      : {}),
    ...(getAetherhavenMapReference(record)
      ? { mapMarker: getAetherhavenMapReference(record) }
      : {}),
  };
};

export const archiveEntryHref = (entry) =>
  `/archive/${entry.entityType}/${entry.slug}/`;
