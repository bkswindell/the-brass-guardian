import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { syncPreviewAssets } from "./lib/preview-assets.mjs";

test("stages proposal assets only for an explicitly enabled preview build", async (t) => {
  const root = await mkdtemp(join(tmpdir(), "aetherhaven-preview-assets-"));
  t.after(() => rm(root, { recursive: true, force: true }));

  const sourceRoot = join(root, "source");
  const publicRoot = join(root, "public");
  await mkdir(sourceRoot, { recursive: true });
  await writeFile(join(sourceRoot, "map.webp"), "proposal-map");

  await syncPreviewAssets({ enabled: true, sourceRoot, publicRoot });
  assert.equal(
    await readFile(join(publicRoot, "map.webp"), "utf8"),
    "proposal-map",
  );

  await syncPreviewAssets({ enabled: false, sourceRoot, publicRoot });
  await assert.rejects(readFile(join(publicRoot, "map.webp")), {
    code: "ENOENT",
  });
});