import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const assetRoot = new URL("../content/preview/assets/archive/", import.meta.url);

const expectedOutputs = new Map([
  ["map-of-aetherhaven-768.webp", 768],
  ["map-of-aetherhaven-1152.webp", 1152],
  ["map-of-aetherhaven-1539.webp", 1539],
  ["clockwork-gardens-at-night-480.webp", 480],
  ["clockwork-gardens-at-night-767.webp", 767],
  ["wayfinder-above-clouds-640.webp", 640],
  ["wayfinder-above-clouds-1024.webp", 1024],
]);

const readUint24LE = (bytes, offset) =>
  bytes[offset] | (bytes[offset + 1] << 8) | (bytes[offset + 2] << 16);

const readWebpDimensions = (bytes) => {
  assert.equal(bytes.toString("ascii", 0, 4), "RIFF");
  assert.equal(bytes.toString("ascii", 8, 12), "WEBP");

  const chunk = bytes.toString("ascii", 12, 16);
  if (chunk === "VP8X") {
    return {
      width: readUint24LE(bytes, 24) + 1,
      height: readUint24LE(bytes, 27) + 1,
    };
  }

  if (chunk === "VP8 ") {
    assert.equal(bytes.toString("hex", 23, 26), "9d012a");
    return {
      width: bytes.readUInt16LE(26) & 0x3fff,
      height: bytes.readUInt16LE(28) & 0x3fff,
    };
  }

  if (chunk === "VP8L") {
    assert.equal(bytes[20], 0x2f);
    return {
      width: 1 + bytes[21] + ((bytes[22] & 0x3f) << 8),
      height:
        1 +
        (bytes[22] >> 6) +
        (bytes[23] << 2) +
        ((bytes[24] & 0x0f) << 10),
    };
  }

  assert.fail(`Unsupported WebP chunk ${JSON.stringify(chunk)}`);
};

test("committed proposal archive assets are valid responsive WebP files", async () => {
  for (const [filename, expectedWidth] of expectedOutputs) {
    const bytes = await readFile(new URL(filename, assetRoot));
    const dimensions = readWebpDimensions(bytes);
    assert.equal(dimensions.width, expectedWidth, filename);
    assert.ok(dimensions.height > 0, filename);
  }
});