import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const sourceUrl = new URL("../src/pages/index.astro", import.meta.url);

test("Archive gateway is an accessible functional mechanism", async () => {
  const source = await readFile(sourceUrl, "utf8");
  assert.match(source, /data-archive-gateway="mechanical"/);
  assert.match(source, /aria-describedby="archive-gateway-note"/);
  assert.match(source, /class="gear gear-primary"/);
  assert.match(source, /class="gear gear-secondary"/);
  assert.match(source, /class="clock-dial"/);
  assert.match(source, /class="aether-core"/);
  assert.match(source, /class="state-rest">Invitation waiting/);
  assert.match(source, /class="state-active"[^>]*>Lock released/);
  assert.match(source, /\.archive-gateway:hover/);
  assert.match(source, /\.archive-gateway:focus-visible/);
  assert.match(source, /\.archive-gateway:hover \.state-active/);
});

test("Archive gateway respects reduced-motion preferences", async () => {
  const source = await readFile(sourceUrl, "utf8");
  const reducedMotion = source.match(
    /@media \(prefers-reduced-motion: reduce\) \{([\s\S]+)\n  \}/,
  )?.[1];
  assert.ok(reducedMotion, "Expected a reduced-motion media query.");
  assert.match(reducedMotion, /\.gear/);
  assert.match(reducedMotion, /\.clock-hand/);
  assert.match(reducedMotion, /animation: none/);
  assert.match(reducedMotion, /transition: none/);
});