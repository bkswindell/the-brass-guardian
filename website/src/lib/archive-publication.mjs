import archiveRelease from "../../content/public/archive-release.json" with { type: "json" };
import { validateArchiveRelease } from "../../scripts/lib/archive-release.mjs";

const release = validateArchiveRelease(archiveRelease);

export const isArchivePublished = (candidateRelease = release) =>
  validateArchiveRelease(candidateRelease).status === "published";

export const getArchivePublication = async (
  env = process.env,
  candidateRelease = release,
) => {
  const { getArchivePublicationV2 } = await import("./archive-publication-v2.mjs");
  return getArchivePublicationV2(env, candidateRelease);
};
