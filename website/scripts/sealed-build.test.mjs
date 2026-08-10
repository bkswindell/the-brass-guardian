import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import {
  cp,
  lstat,
  mkdtemp,
  readFile,
  rm,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { basename, join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const websiteRoot = new URL("../", import.meta.url);
const repositoryRoot = new URL("../../", import.meta.url);
const canonicalSourcePaths = [
  "README.md",
  "characters",
  "organizations",
  "locations",
  "historical_events",
  "story_arcs",
  "story_drafts",
  "artifacts",
];
const excludedDirectories = new Set([
  "node_modules",
  "dist",
  "dist-preview",
  ".astro",
]);

const pathExists = (path) =>
  lstat(path)
    .then(() => true)
    .catch(() => false);

test(
  "sealed release passes the real prebuild/build wrapper and prunes Archive output",
  { timeout: 120_000 },
  async (t) => {
    const temporaryRoot = await mkdtemp(join(tmpdir(), "tbg-sealed-build-"));
    const isolatedWebsite = join(temporaryRoot, "website");
    t.after(() => rm(temporaryRoot, { recursive: true, force: true }));

    await cp(websiteRoot, isolatedWebsite, {
      recursive: true,
      filter: (source) => !excludedDirectories.has(basename(source)),
    });
    await cp(
      new URL("../node_modules", import.meta.url),
      join(isolatedWebsite, "node_modules"),
      { recursive: true },
    );
    for (const sourcePath of canonicalSourcePaths) {
      await cp(
        new URL(sourcePath, repositoryRoot),
        join(temporaryRoot, sourcePath),
        { recursive: true },
      );
    }

    const isolatedReleasePath = join(
      isolatedWebsite,
      "content",
      "public",
      "archive-release.json",
    );
    await writeFile(
      isolatedReleasePath,
      `${JSON.stringify(
        {
          schemaVersion: 1,
          status: "sealed",
          approvedBy: "author",
          approvedOn: "2026-08-10",
          includeHiddenArchives: false,
        },
        null,
        2,
      )}\n`,
    );

    const { stdout, stderr } = await execFileAsync("npm", ["run", "build"], {
      cwd: isolatedWebsite,
      env: {
        ...process.env,
        VERCEL_ENV: "production",
        PUBLICATION_PREVIEW: "1",
      },
      maxBuffer: 10 * 1024 * 1024,
    });

    assert.match(stdout, /Publication boundary passed/);
    assert.doesNotMatch(`${stdout}\n${stderr}`, /Publication boundary failed/);
    assert.equal(await pathExists(join(isolatedWebsite, "dist", "archive")), false);
    assert.equal(
      await pathExists(join(isolatedWebsite, "dist", "images", "archive")),
      false,
    );

    const actualRelease = JSON.parse(
      await readFile(new URL("../content/public/archive-release.json", import.meta.url)),
    );
    assert.equal(actualRelease.status, "published");
    assert.equal(actualRelease.includeHiddenArchives, true);
  },
);
