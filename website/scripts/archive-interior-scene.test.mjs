import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const layoutUrl = new URL("../src/layouts/ArchiveLayout.astro", import.meta.url);
const entranceUrl = new URL("../src/pages/archive/index.astro", import.meta.url);

test("Archive routes share a Preview-gated responsive interior scene", async () => {
  const source = await readFile(layoutUrl, "utf8");

  assert.match(source, /getWorldEntrancePreview/);
  assert.match(source, /archive\.enabled\s*&&/);
  assert.match(source, /class="archive-interior-scene"/);
  assert.match(
    source,
    /aetherhaven-archive-threshold-768\.webp 768w,\s*\/images\/archive\/aetherhaven-archive-threshold-1024\.webp 1024w/,
  );
  assert.match(source, /aria-hidden="true"/);
  assert.match(source, /class:list=\{\["archive-shell", \{ "archive-shell-open": archive\.enabled \}\]\}/);
});

test("Archive interior styling makes the scene spatially dominant without obscuring content", async () => {
  const source = await readFile(layoutUrl, "utf8");

  assert.match(source, /\.archive-interior-scene\s*\{/);
  assert.match(source, /\.archive-interior-scene img\s*\{/);
  assert.match(source, /\.archive-shell-open \.archive-header\s*\{/);
  assert.match(source, /\.archive-room-floor\s*\{/);
  assert.match(source, /prefers-reduced-motion:\s*reduce/);
});

test("Archive entrance leaves an architectural sightline and roots its controls in an arrival desk", async () => {
  const source = await readFile(entranceUrl, "utf8");
  const layoutSource = await readFile(layoutUrl, "utf8");

  assert.match(source, /class="arrival-desk"/);
  assert.match(source, /\.entrance-hero\s*\{[^}]*min-height:/s);
  assert.match(source, /\.arrival-desk\s*\{/);
  assert.match(source, /\.route-list a::before\s*\{/);
  assert.match(source, /\.record-card::before\s*\{/);
  assert.match(source, /scroll-margin-top:\s*7(?:\.5)?rem/);
  assert.match(
    layoutSource,
    /@media \(max-width: 44rem\)[\s\S]*?\.archive-header\s*\{[^}]*position:\s*relative;[^}]*top:\s*auto;/,
  );
});
