import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { validatePublicationManifest } from "./lib/publication-boundary.mjs";

const scriptsRoot = dirname(fileURLToPath(import.meta.url));
const websiteRoot = resolve(scriptsRoot, "..");
const repositoryRoot = resolve(websiteRoot, "..");
const manifestPath = resolve(websiteRoot, "content", "public", "manifest.json");
const publicRoot = resolve(websiteRoot, "public");

try {
  const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  const validated = await validatePublicationManifest(manifest, {
    repositoryRoot,
    publicRoot,
  });
  console.log(
    `Publication boundary passed: ${validated.entries.length} explicitly approved public record(s).`,
  );
} catch (error) {
  console.error(`Publication boundary failed: ${error.message}`);
  process.exit(1);
}
