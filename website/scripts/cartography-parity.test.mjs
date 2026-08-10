import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

import { JSON_SCHEMA, load as parseYaml } from "js-yaml";

import legacyManifest from "../content/public/manifest.json" with { type: "json" };
import legacyPresentation from "../content/public/archive-presentation.json" with { type: "json" };

const repositoryRoot = resolve(process.cwd(), "..");
const locationsRoot = resolve(repositoryRoot, "locations");
const frontmatterPattern = /^---\s*\n([\s\S]*?)\n---(?:\s*\n|$)/u;

const parseFrontmatter = (source, path) => {
  const match = frontmatterPattern.exec(source);
  assert.ok(match, `${path}: missing YAML front matter.`);
  const parsed = parseYaml(match[1], { schema: JSON_SCHEMA });
  assert.ok(parsed && typeof parsed === "object" && !Array.isArray(parsed));
  return parsed;
};

const loadLocationsBySlug = async () => {
  const bySlug = new Map();
  for (const entry of await readdir(locationsRoot, { withFileTypes: true })) {
    if (!entry.isFile() || !entry.name.endsWith(".md") || entry.name === "README.md") continue;
    const path = resolve(locationsRoot, entry.name);
    const record = parseFrontmatter(await readFile(path, "utf8"), path);
    if (record.schema_version === 1 && typeof record.slug === "string") {
      bySlug.set(record.slug, { path, record });
    }
  }
  return bySlug;
};

test("all 30 approved C1 map markers are owned by canonical Markdown cartography", async () => {
  const bySlug = await loadLocationsBySlug();
  const legacyById = new Map(legacyManifest.entries.map((entry) => [entry.id, entry]));
  const failures = [];

  for (const mapEntry of legacyPresentation.mapEntries) {
    const legacy = legacyById.get(mapEntry.id);
    if (!legacy) {
      failures.push(`${mapEntry.id}: missing from legacy approved publication manifest`);
      continue;
    }
    const found = bySlug.get(legacy.slug);
    if (!found) {
      failures.push(`${mapEntry.id}: no Schema v1 location owns slug ${legacy.slug}`);
      continue;
    }

    const { record } = found;
    const canonical = (record.cartography ?? []).find(
      (candidate) =>
        candidate.map_id === "aetherhaven-city" &&
        candidate.category !== "unlisted",
    );
    const expectedCategory = /^[A-F]$/u.test(mapEntry.mapMarker)
      ? "restricted"
      : "numbered";

    if (!canonical) {
      failures.push(
        `${record.id} (${record.slug}): missing aetherhaven-city ${expectedCategory} reference ${mapEntry.mapMarker}`,
      );
      continue;
    }
    if (
      canonical.category !== expectedCategory ||
      canonical.reference !== mapEntry.mapMarker
    ) {
      failures.push(
        `${record.id} (${record.slug}): expected ${expectedCategory} ${mapEntry.mapMarker}; found ${canonical.category} ${canonical.reference}`,
      );
    }
  }

  assert.deepEqual(failures, []);
});
