import publicationManifest from "../../content/public/manifest.json" with { type: "json" };
import archiveRelease from "../../content/public/archive-release.json" with { type: "json" };
import archivePresentation from "../../content/public/archive-presentation.json" with { type: "json" };
import { toPublicArchiveEntry } from "../../scripts/lib/publication-boundary.mjs";
import { validateArchiveRelease } from "../../scripts/lib/archive-release.mjs";
import { validateArchivePresentation } from "../../scripts/lib/archive-presentation.mjs";

const release = validateArchiveRelease(archiveRelease);
const presentation = validateArchivePresentation(
  archivePresentation,
  publicationManifest,
);
const approvedEntries = publicationManifest.entries.map(toPublicArchiveEntry);
const presentationById = new Map(
  presentation.mapEntries.map((entry) => [entry.id, entry]),
);

const withPresentationMetadata = (entry) => {
  const presentationEntry = presentationById.get(entry.id);

  return {
    ...entry,
    ...(presentationEntry ?? {}),
    archiveSection: entry.tags.includes("hidden-archive") ? "hidden" : "public",
  };
};

const publishedEntries = approvedEntries
  .filter((entry) => !entry.tags.includes("hidden-archive"))
  .map(withPresentationMetadata);
const publishedHiddenEntries = approvedEntries
  .filter((entry) => entry.tags.includes("hidden-archive"))
  .map(withPresentationMetadata);
const publishedMapEntries = publishedEntries.filter(
  (entry) => entry.mapMarker && entry.mapRegion && entry.mapLabel,
);
const publishedHiddenMapEntries = publishedHiddenEntries.filter(
  (entry) => entry.mapMarker && entry.mapRegion && entry.mapLabel,
);
const publishedById = new Map(publishedEntries.map((entry) => [entry.id, entry]));
const entryHref = (entry) => `/archive/${entry.entityType}/${entry.slug}/`;
const publishedCuratorRoute = presentation.curatorRoute.map((step) => {
  if (step.kind === "room") return step;
  const entry = publishedById.get(step.id);
  if (!entry) throw new Error(`Curator route record is not approved: ${step.id}`);
  return {
    ...step,
    title: entry.publicTitle,
    href: entryHref(entry),
    entityType: entry.entityType,
  };
});

export const isArchivePublished = (candidateRelease = release) =>
  validateArchiveRelease(candidateRelease).status === "published";

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

export const getArchivePublication = async (
  env = process.env,
  candidateRelease = release,
) => {
  const resolvedRelease = validateArchiveRelease(candidateRelease);
  const production = env.VERCEL_ENV === "production";
  const preview =
    !production &&
    (env.PUBLICATION_PREVIEW === "1" || env.VERCEL_ENV === "preview");

  if (preview) {
    const { getWorldEntrancePreview } = await import("./archive-preview.mjs");
    const proposal = getWorldEntrancePreview(env);
    return {
      ...proposal,
      mode: "preview",
      isPublic: false,
      isPreview: true,
      noindex: true,
    };
  }

  if (!isArchivePublished(resolvedRelease)) return sealedArchive;

  const hiddenEntries = resolvedRelease.includeHiddenArchives
    ? publishedHiddenEntries
    : [];
  const hiddenMapEntries = resolvedRelease.includeHiddenArchives
    ? publishedHiddenMapEntries
    : [];

  return {
    enabled: true,
    mode: "public",
    isPublic: true,
    isPreview: false,
    noindex: false,
    entries: publishedEntries,
    mapEntries: publishedMapEntries,
    hiddenEntries,
    hiddenMapEntries,
    curatorRoute: publishedCuratorRoute,
  };
};
