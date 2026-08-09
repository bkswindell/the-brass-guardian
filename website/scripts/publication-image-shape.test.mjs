import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";

import { validatePublicationManifest } from "./lib/publication-boundary.mjs";

const makeEntry = (image) => ({
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
  image,
});

test("rejects every malformed value explicitly supplied as image", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-image-shape-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(join(repositoryRoot, "characters", "Example.md"), "# Fixture\n");

  for (const image of [null, false, 0, "", []]) {
    await assert.rejects(
      validatePublicationManifest(
        { schemaVersion: 1, entries: [makeEntry(image)] },
        { repositoryRoot },
      ),
      /image must be a non-null object/,
    );
  }
});

test("accepts a complete image record backed by a real public file", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-valid-image-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(join(repositoryRoot, "characters", "Example.md"), "# Fixture\n");
  const publicRoot = join(repositoryRoot, "website", "public");
  await mkdir(join(publicRoot, "images"), { recursive: true });
  await writeFile(join(publicRoot, "images", "example.webp"), "fixture");

  const image = {
    src: "/images/example.webp",
    alt: "A neutral fixture image.",
    width: 640,
    height: 480,
  };
  const validated = await validatePublicationManifest(
    { schemaVersion: 1, entries: [makeEntry(image)] },
    { repositoryRoot, publicRoot },
  );

  assert.deepEqual(validated.entries[0].image, image);
});

test("rejects image URLs whose browser and filesystem paths can diverge", async (t) => {
  const repositoryRoot = await mkdtemp(
    join(tmpdir(), "aetherhaven-publication-image-url-"),
  );
  t.after(() => rm(repositoryRoot, { recursive: true, force: true }));
  await mkdir(join(repositoryRoot, "characters"), { recursive: true });
  await writeFile(join(repositoryRoot, "characters", "Example.md"), "# Fixture\n");
  const publicRoot = join(repositoryRoot, "website", "public");

  for (const src of [
    "/images/%2e%2e/secret.webp",
    "/images/example.webp?download=1",
    "/images/example.webp#fragment",
  ]) {
    const literalFile = join(publicRoot, src.slice(1));
    await mkdir(dirname(literalFile), { recursive: true });
    await writeFile(literalFile, "fixture");

    await assert.rejects(
      validatePublicationManifest(
        {
          schemaVersion: 1,
          entries: [
            makeEntry({
              src,
              alt: "A neutral fixture image.",
              width: 640,
              height: 480,
            }),
          ],
        },
        { repositoryRoot, publicRoot },
      ),
      /image src must be a canonical public asset URL/,
    );
  }
});
