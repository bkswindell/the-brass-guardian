import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";

const script = new URL("generate-archive-assets.py", import.meta.url);

const expectedOutputs = new Map([
  ["map-of-aetherhaven-768.webp", 768],
  ["map-of-aetherhaven-1152.webp", 1152],
  ["map-of-aetherhaven-1539.webp", 1539],
  ["clockwork-gardens-at-night-480.webp", 480],
  ["clockwork-gardens-at-night-767.webp", 767],
  ["wayfinder-above-clouds-640.webp", 640],
  ["wayfinder-above-clouds-1024.webp", 1024],
]);

test("generates responsive archive WebP derivatives from repository artwork", async (t) => {
  const outputRoot = await mkdtemp(join(tmpdir(), "aetherhaven-archive-assets-"));
  t.after(() => rm(outputRoot, { recursive: true, force: true }));

  const generation = spawnSync(
    "python3",
    [script.pathname, "--output-root", outputRoot],
    { encoding: "utf8" },
  );

  assert.equal(generation.status, 0, generation.stderr || generation.stdout);

  for (const [filename, expectedWidth] of expectedOutputs) {
    const outputPath = join(outputRoot, filename);
    const bytes = await readFile(outputPath);
    assert.equal(bytes.toString("ascii", 0, 4), "RIFF", `${filename} is not WebP`);
    assert.equal(bytes.toString("ascii", 8, 12), "WEBP", `${filename} is not WebP`);

    const inspection = spawnSync(
      "python3",
      [
        "-c",
        "from PIL import Image; import sys; im=Image.open(sys.argv[1]); print(im.format, im.width, im.height)",
        outputPath,
      ],
      { encoding: "utf8" },
    );
    assert.equal(inspection.status, 0, inspection.stderr);
    const [format, width, height] = inspection.stdout.trim().split(" ");
    assert.equal(format, "WEBP");
    assert.equal(Number(width), expectedWidth);
    assert.ok(Number(height) > 0);
  }
});
