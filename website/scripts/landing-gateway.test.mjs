import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const pageUrl = new URL("../src/pages/index.astro", import.meta.url);

test("Archive gateway is a simple semantic invitation", async () => {
  const source = await readFile(pageUrl, "utf8");

  assert.match(source, /class="archive-invitation"/);
  assert.match(source, /href="\/archive\/"/);
  assert.match(source, /Enter Archive/);
  assert.match(source, /Invitation Waiting/);
  assert.match(source, /Lock Released/);
  assert.match(source, /\.archive-invitation:hover/);
  assert.match(source, /\.archive-invitation:focus-visible/);
  assert.doesNotMatch(source, /ArchiveLockExperience|client:idle|react-three-fiber/);
});

test("Archive scene is Preview-gated and responsive", async () => {
  const source = await readFile(pageUrl, "utf8");

  assert.match(source, /archive\.enabled && \(/);
  assert.match(source, /aetherhaven-archive-threshold-768\.webp/);
  assert.match(source, /aetherhaven-archive-threshold-1024\.webp/);
  assert.match(source, /media="\(max-width: 48rem\)"/);
  assert.match(source, /class="archive-backdrop"/);
});

test("Archive invitation respects reduced-motion preferences", async () => {
  const source = await readFile(pageUrl, "utf8");
  const reducedMotion = source.match(
    /@media \(prefers-reduced-motion: reduce\) \{([\s\S]+)\n  \}/,
  )?.[1];

  assert.ok(reducedMotion, "Expected a reduced-motion media query.");
  assert.match(reducedMotion, /\.archive-invitation/);
  assert.match(reducedMotion, /transition: none !important/);
});
