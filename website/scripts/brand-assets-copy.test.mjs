import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

test("social artwork generator uses the active Archive invitation", async () => {
  const generator = await readFile(
    new URL("generate-brand-assets.py", import.meta.url),
    "utf8",
  );
  assert.match(generator, /ENTER ARCHIVE/);
  assert.doesNotMatch(generator, /COMING SOON/);
  assert.doesNotMatch(generator, /prepared for public access/);
});