import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import { getWorldEntrancePreview } from "../src/lib/archive-preview.mjs";

const mapPageUrl = new URL("../src/pages/archive/map/index.astro", import.meta.url);
const hiddenPageUrl = new URL("../src/pages/archive/hidden/index.astro", import.meta.url);
const entrancePageUrl = new URL("../src/pages/archive/index.astro", import.meta.url);
const recordPageUrl = new URL(
  "../src/pages/archive/[entityType]/[slug].astro",
  import.meta.url,
);
const layoutUrl = new URL("../src/layouts/ArchiveLayout.astro", import.meta.url);

const expectedPublicCharacters = [
  "Amelia Hawthorne",
  "Barnaby Wren",
  "Beatrice Pike",
  "Captain Mara Voss",
  "Chancellor Octavia Vale",
  "Chief Inspector Beatrice Thorne",
  "Doctor Elara Quill",
  "Euphemia Pike",
  "Juniper Bell",
  "Lucian Wren",
  "Madame Celestine Mirrow",
  "Master Gideon Brasswell",
  "Orin Flint",
  "Pip",
  "Professor Elias Hawthorne",
  "Tamsin Pike",
].sort();

const expectedPublicOrganizations = [
  "The Academy of Invention",
  "The Aerial Mariners’ Union",
  "The Aetherhaven Archives",
  "The Brass Watch",
  "The Conclave of Eight",
  "The Conservancy of Living Mechanisms",
  "The Eight Founding Engineering Guilds",
  "The Free Spring Assembly",
  "The Guild of Aetherwrights",
  "The Guild of Artificers",
  "The Guild of Canalwrights",
  "The Guild of Clockwrights",
  "The Guild of Enginewrights",
  "The Guild of Framewrights",
  "The Guild of Skywrights",
  "The Guild of Verdant Mechanists",
  "The Handwright Circles",
  "The High Council of Aetherhaven",
  "The Lamplighters’ Fellowship",
  "The Mechanists’ Guild",
  "The Miners’ Guild",
  "The Order of the Mended Hand",
  "The Severed Coil",
  "The Society of Explorers",
  "The Unwound",
].sort();

const expectedHiddenFigures = [
  "Keeper Thirteen",
  "Silas Rook",
  "The Ashen Cartographer",
  "The Bellmaker",
  "The Cinder Regent",
  "The Curator",
  "The First Mechanist",
  "The First Tender",
  "The Hidden Architect",
  "The Lady in the Water",
  "The Null Shepherd",
  "The Passenger of Dock Zero",
].sort();

const expectedHiddenOrganizations = [
  "The Ash Detail",
  "The Cinder Wardens",
  "The Clockkeepers Without Hours",
  "The Furnace Court",
  "The Inner Compass",
  "The Keepers of Time",
  "The Ninth Guild",
  "The Order of the Closed Eye",
  "The Quiet Choir",
  "The Underclock",
].sort();

const titles = (entries) => entries.map((entry) => entry.publicTitle).sort();

test("preview catalog exposes all 24 numbered map locations and six restricted references", () => {
  const archive = getWorldEntrancePreview({ PUBLICATION_PREVIEW: "1" });

  assert.deepEqual(
    archive.mapEntries.map((entry) => entry.mapMarker),
    Array.from({ length: 24 }, (_, index) => String(index + 1)),
  );
  assert.deepEqual(
    archive.hiddenMapEntries.map((entry) => entry.mapMarker),
    ["A", "B", "C", "D", "E", "F"],
  );

  for (const entry of [...archive.mapEntries, ...archive.hiddenMapEntries]) {
    assert.ok(entry.mapRegion, `${entry.mapMarker} must define a clickable region`);
    assert.ok(entry.mapLabel, `${entry.mapMarker} must define a clickable label plate`);
  }
});

test("public catalog includes every source-classified public character and organization", () => {
  const archive = getWorldEntrancePreview({ PUBLICATION_PREVIEW: "1" });
  const publicCharacters = archive.entries.filter((entry) => entry.entityType === "character");
  const publicOrganizations = archive.entries.filter((entry) => entry.entityType === "organization");

  assert.deepEqual(titles(publicCharacters), expectedPublicCharacters);
  assert.deepEqual(titles(publicOrganizations), expectedPublicOrganizations);
  assert.ok(publicCharacters.every((entry) => entry.archiveSection === "public"));
  assert.ok(publicOrganizations.every((entry) => entry.archiveSection === "public"));
});

test("hidden figures and organizations remain separate from the public catalog", () => {
  const archive = getWorldEntrancePreview({ PUBLICATION_PREVIEW: "1" });
  const hiddenFigures = archive.hiddenEntries.filter((entry) => entry.entityType === "character");
  const hiddenOrganizations = archive.hiddenEntries.filter(
    (entry) => entry.entityType === "organization",
  );

  assert.deepEqual(titles(hiddenFigures), expectedHiddenFigures);
  assert.deepEqual(titles(hiddenOrganizations), expectedHiddenOrganizations);
  assert.ok(archive.hiddenEntries.every((entry) => entry.archiveSection === "hidden"));
  assert.ok(
    archive.entries.every(
      (entry) => !archive.hiddenEntries.some((hidden) => hidden.id === entry.id),
    ),
  );
});

test("map uses one semantic SVG link for each region and label instead of floating buttons", async () => {
  const source = await readFile(mapPageUrl, "utf8");

  assert.match(source, /class="map-link-overlay"/);
  assert.match(source, /viewBox="0 0 1539 1152"/);
  assert.match(source, /class="map-region-target"/);
  assert.match(source, /class="map-label-target"/);
  assert.match(source, /mapEntries\.map/);
  assert.match(source, /hiddenMapEntries\.map/);
  assert.doesNotMatch(source, /class="map-hotspot"/);
  assert.doesNotMatch(source, /aria-controls="map-record-detail"/);
  assert.doesNotMatch(source, /id="map-record-detail"/);
});

test("Hidden Archives is a warned Archive subsection and preserves sealed identities", async () => {
  const source = await readFile(hiddenPageUrl, "utf8").catch(() => "");

  assert.match(source, /Hidden Archives/);
  assert.match(source, /spoiler/i);
  assert.match(source, /sensitive/i);
  assert.match(source, /identity remains (?:sealed|withheld)/i);
  assert.match(source, /archive\.hiddenEntries/);
});

test("public Archive catalog exposes entity filters and a warned Hidden Archives doorway", async () => {
  const [entranceSource, layoutSource] = await Promise.all([
    readFile(entrancePageUrl, "utf8"),
    readFile(layoutUrl, "utf8"),
  ]);

  assert.match(entranceSource, /\{entries\.length\} public records/);
  assert.match(entranceSource, /data-catalog-filter="character"/);
  assert.match(entranceSource, /data-catalog-filter="organization"/);
  assert.match(entranceSource, /class="hidden-archive-callout"/);
  assert.match(entranceSource, /href="\/archive\/hidden\/"/);
  assert.match(layoutSource, /href="\/archive\/hidden\/"/);
});

test("non-curated stub records browse the catalog without claiming to be route stop zero", async () => {
  const source = await readFile(recordPageUrl, "utf8");

  assert.match(source, /routeIndex >= 0 \?/);
  assert.match(source, /class="catalog-record-nav"/);
  assert.match(source, /Return to the Open Catalog/);
});

test("mobile map targets stay readable and Hidden Archive drawers show disclosure affordances", async () => {
  const [mapSource, hiddenSource] = await Promise.all([
    readFile(mapPageUrl, "utf8"),
    readFile(hiddenPageUrl, "utf8"),
  ]);

  assert.match(mapSource, /swipe to move across the chart/i);
  assert.match(mapSource, /\.map-canvas \{\s*min-width: 48rem;/);
  assert.match(hiddenSource, /class="drawer-state"/);
  assert.match(hiddenSource, /\.hidden-record\[open\] \.drawer-state/);
});

test("production-safe archive data remains empty", () => {
  const archive = getWorldEntrancePreview({ VERCEL_ENV: "production", PUBLICATION_PREVIEW: "1" });

  assert.deepEqual(archive.entries, []);
  assert.deepEqual(archive.mapEntries, []);
  assert.deepEqual(archive.hiddenEntries, []);
  assert.deepEqual(archive.hiddenMapEntries, []);
});
