import assert from "node:assert/strict";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { readOutputDirectory } from "./lib/build-output.mjs";

const withWebsite = async (run) => {
  const websiteRoot = await mkdtemp(join(tmpdir(), "tbg-build-output-"));
  try {
    await run(websiteRoot);
  } finally {
    await rm(websiteRoot, { recursive: true, force: true });
  }
};

test("resolves both CLI outDir forms relative to the website root", async () => {
  await withWebsite(async (websiteRoot) => {
    assert.equal(
      await readOutputDirectory({ args: ["--outDir", "one"], websiteRoot }),
      join(websiteRoot, "one"),
    );
    assert.equal(
      await readOutputDirectory({ args: ["--outDir=two"], websiteRoot }),
      join(websiteRoot, "two"),
    );
  });
});

test("uses configuration-level outDir when the CLI does not override it", async () => {
  await withWebsite(async (websiteRoot) => {
    await writeFile(
      join(websiteRoot, "astro.config.mjs"),
      'export default { outDir: "configured-output" };\n',
    );

    assert.equal(
      await readOutputDirectory({ args: [], websiteRoot }),
      join(websiteRoot, "configured-output"),
    );
  });
});

test("CLI outDir takes precedence over a configured output directory", async () => {
  await withWebsite(async (websiteRoot) => {
    await writeFile(
      join(websiteRoot, "astro.config.mjs"),
      'export default { outDir: "configured-output" };\n',
    );

    assert.equal(
      await readOutputDirectory({
        args: ["--outDir", "cli-output"],
        websiteRoot,
      }),
      join(websiteRoot, "cli-output"),
    );
  });
});