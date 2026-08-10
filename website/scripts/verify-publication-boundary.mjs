import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { validatePublicationManifest } from "./lib/publication-boundary.mjs";
import { validateArchiveRelease } from "./lib/archive-release.mjs";
import { validateArchivePresentation } from "./lib/archive-presentation.mjs";

const scriptsRoot = dirname(fileURLToPath(import.meta.url));
const websiteRoot = resolve(scriptsRoot, "..");
const repositoryRoot = resolve(websiteRoot, "..");
const manifestPath = resolve(websiteRoot, "content", "public", "manifest.json");
const releasePath = resolve(
  websiteRoot,
  "content",
  "public",
  "archive-release.json",
);
const presentationPath = resolve(
  websiteRoot,
  "content",
  "public",
  "archive-presentation.json",
);
const publicRoot = resolve(websiteRoot, "public");

try {
  const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  const release = validateArchiveRelease(
    JSON.parse(await readFile(releasePath, "utf8")),
  );
  const presentation = JSON.parse(await readFile(presentationPath, "utf8"));
  const validated = await validatePublicationManifest(manifest, {
    repositoryRoot,
    publicRoot,
  });
  validateArchivePresentation(presentation, validated);
  if (release.status === "published" && validated.entries.length === 0) {
    throw new Error("published Archive release requires approved manifest entries.");
  }
  const hiddenEntries = validated.entries.filter((entry) =>
    entry.tags.includes("hidden-archive"),
  );
  if (
    release.status === "published" &&
    !release.includeHiddenArchives &&
    hiddenEntries.length > 0
  ) {
    throw new Error(
      "sealed Hidden Archives cannot remain in the published manifest projection.",
    );
  }
  console.log(
    `Publication boundary passed: ${validated.entries.length} approved record(s), ${presentation.mapEntries.length} approved map presentation(s), ${hiddenEntries.length} Hidden Archive teaser(s), release ${release.status}.`,
  );
} catch (error) {
  console.error(`Publication boundary failed: ${error.message}`);
  process.exit(1);
}
