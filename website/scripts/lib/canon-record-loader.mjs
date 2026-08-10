import { readdir, readFile } from "node:fs/promises";
import { relative, resolve, sep } from "node:path";

import { JSON_SCHEMA, load as parseYaml } from "js-yaml";

import { validateCanonRecords } from "./canon-schema-v1.mjs";

export const canonicalRecordRoots = Object.freeze([
  "characters",
  "locations",
  "organizations",
  "artifacts",
  "vessels",
  "historical_events",
  "story_drafts",
  "story_arcs",
]);

const frontmatterPattern = /^---\s*\n([\s\S]*?)\n---(?:\s*\n|$)/u;

export const parseCanonFrontmatter = (source, path = "canonical Markdown") => {
  const match = frontmatterPattern.exec(source);
  if (!match) throw new Error(`${path}: missing YAML front matter.`);
  const parsed = parseYaml(match[1], { schema: JSON_SCHEMA });
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error(`${path}: front matter must parse to an object.`);
  }
  return parsed;
};

export const loadCanonRecordSources = async ({ repositoryRoot }) => {
  const sources = [];
  for (const directory of canonicalRecordRoots) {
    const directoryPath = resolve(repositoryRoot, directory);
    const entries = await readdir(directoryPath, { withFileTypes: true });
    for (const entry of entries) {
      if (!entry.isFile() || !entry.name.endsWith(".md") || entry.name === "README.md") {
        continue;
      }
      const path = resolve(directoryPath, entry.name);
      sources.push({
        path,
        relativePath: relative(repositoryRoot, path).split(sep).join("/"),
      });
    }
  }
  return sources;
};

export const loadCanonRecords = async ({ repositoryRoot }) => {
  const sources = await loadCanonRecordSources({ repositoryRoot });
  const records = [];
  for (const source of sources) {
    const record = parseCanonFrontmatter(
      await readFile(source.path, "utf8"),
      source.path,
    );
    records.push(record);
  }
  validateCanonRecords(records);
  return records;
};
