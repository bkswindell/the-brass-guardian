import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { validatePublicationManifest } from "./lib/publication-boundary.mjs";

const makeEntry = (overrides = {}) => ({
  id: "character-example",
  slug: "example",
  entityType: "character",
  canonicalName: "Example Record",
  publicTitle: "Example Record",
  publicSummary: "A neutral public projection fixture.",
  sourcePaths: ["characters/Example.md"],
  publicationStatus: "approved",
  spoilerClassification: "public",
  approval: { approvedBy: "author", approvedOn: "2026-08-09" },
  relatedEntryIds: [],
  tags: [],
  ...overrides,
});

const validate = (entry, repositoryRoot, options = {}) =>
  validatePublicationManifest(
    { schemaVersion: 1, entries: [entry] },
    { repositoryRoot, ...options },
  );

test("rejects canonical-root traversal through an allowed raw prefix", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-traversal-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await mkdir(join(repositoryRoot, "agents", "shared"), { recursive: true });
  await writeFile(
    join(repositoryRoot, "agents", "shared", "CURRENT_WORK.md"),
    "# Private fixture\n",
  );

  await assert.rejects(
    validate(
      makeEntry({
        sourcePaths: ["characters/../agents/shared/CURRENT_WORK.md"],
      }),
      repositoryRoot,
    ),
    /source path must use an approved canonical source root/,
  );
});

test("rejects a canonical source path that resolves to a directory", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-source-directory-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters", "Example.md"), {
    recursive: true,
  });

  await assert.rejects(
    validate(makeEntry(), repositoryRoot),
    /canonical source must be a regular file/,
  );
});

test("rejects a public image path that resolves to a directory", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-image-directory-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(join(repositoryRoot, "characters", "Example.md"), "# Fixture\n");
  const publicRoot = join(repositoryRoot, "website", "public");
  await mkdir(join(publicRoot, "images", "example.webp"), { recursive: true });

  await assert.rejects(
    validate(
      makeEntry({
        image: {
          src: "/images/example.webp",
          alt: "A neutral fixture.",
          width: 640,
          height: 480,
        },
      }),
      repositoryRoot,
      { publicRoot },
    ),
    /public image must be a regular file/,
  );
});

test("rejects a canonical source symlink that resolves outside the repository", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-source-symlink-"),
  );
  const externalRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-external-source-"),
  );
  t.after(async () => {
    await rm(repositoryRoot, { recursive: true, force: true });
    await rm(externalRoot, { recursive: true, force: true });
  });
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  const externalSource = join(externalRoot, "Private.md");
  await writeFile(externalSource, "# Private fixture\n");
  await symlink(externalSource, join(repositoryRoot, "characters", "Example.md"));

  await assert.rejects(
    validate(makeEntry(), repositoryRoot),
    /canonical source resolves outside the repository root/,
  );
});

test("rejects a public image symlink that resolves outside the public root", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-image-symlink-"),
  );
  const externalRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-external-image-"),
  );
  t.after(async () => {
    await rm(repositoryRoot, { recursive: true, force: true });
    await rm(externalRoot, { recursive: true, force: true });
  });
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(join(repositoryRoot, "characters", "Example.md"), "# Fixture\n");
  const publicRoot = join(repositoryRoot, "website", "public");
  await mkdir(join(publicRoot, "images"), { recursive: true });
  const externalImage = join(externalRoot, "private.webp");
  await writeFile(externalImage, "not really an image");
  await symlink(externalImage, join(publicRoot, "images", "example.webp"));

  await assert.rejects(
    validate(
      makeEntry({
        image: {
          src: "/images/example.webp",
          alt: "A neutral fixture.",
          width: 640,
          height: 480,
        },
      }),
      repositoryRoot,
      { publicRoot },
    ),
    /public image resolves outside the public root/,
  );
});

test("rejects a canonical source symlink into a restricted repository area", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-restricted-symlink-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await mkdir(join(repositoryRoot, "agents", "shared"), { recursive: true });
  const restrictedSource = join(repositoryRoot, "agents", "shared", "PRIVATE.md");
  await writeFile(restrictedSource, "# Private fixture\n");
  await symlink(restrictedSource, join(repositoryRoot, "characters", "Example.md"));

  await assert.rejects(
    validate(makeEntry(), repositoryRoot),
    /canonical source resolves outside an approved source root/,
  );
});
