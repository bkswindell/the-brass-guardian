import { readdir, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { join } from "node:path";

import { JSON_SCHEMA, load as parseYaml } from "js-yaml";
import type { Loader } from "astro/loaders";

const canonicalDirectories = [
  "characters",
  "locations",
  "organizations",
  "artifacts",
  "vessels",
  "historical_events",
  "story_drafts",
  "story_arcs",
] as const;

const frontmatterPattern = /^---\s*\n([\s\S]*?)\n---(?:\s*\n|$)/u;

type CanonRecord = Record<string, unknown> & { id?: unknown; schema_version?: unknown };

const parseFrontmatter = (source: string, path: string): CanonRecord => {
  const match = frontmatterPattern.exec(source);
  if (!match) throw new Error(`${path}: missing YAML front matter.`);

  const parsed = parseYaml(match[1], { schema: JSON_SCHEMA });
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error(`${path}: front matter must parse to an object.`);
  }
  return parsed as CanonRecord;
};

export function canonFrontmatterLoader(repositoryRoot: URL): Loader {
  const rootPath = fileURLToPath(repositoryRoot);

  return {
    name: "aetherhaven-canon-frontmatter",
    load: async ({ store, parseData, generateDigest, watcher, logger }) => {
      store.clear();
      let count = 0;

      for (const directory of canonicalDirectories) {
        const directoryPath = join(rootPath, directory);
        watcher?.add(directoryPath);
        const entries = await readdir(directoryPath, { withFileTypes: true });

        for (const entry of entries) {
          if (!entry.isFile() || !entry.name.endsWith(".md") || entry.name === "README.md") {
            continue;
          }

          const path = join(directoryPath, entry.name);
          const source = await readFile(path, "utf8");
          const rawData = parseFrontmatter(source, path);

          if (rawData.schema_version !== 1) {
            throw new Error(`${path}: expected schema_version: 1.`);
          }
          if (typeof rawData.id !== "string" || rawData.id.length === 0) {
            throw new Error(`${path}: missing Schema v1 stable id.`);
          }

          const id = rawData.id;
          const data = await parseData({ id, data: rawData });
          store.set({ id, data, digest: generateDigest(data) });
          count += 1;
        }
      }

      logger.info(`Loaded ${count} Schema v1 canonical records from repository Markdown frontmatter.`);
    },
  } satisfies Loader;
}
