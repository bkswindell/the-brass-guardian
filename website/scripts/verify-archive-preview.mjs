import { readFile, stat } from "node:fs/promises";

const root = new URL("../dist-preview/", import.meta.url);
const failures = [];

const expect = (condition, message) => {
  if (!condition) failures.push(message);
};

const readText = async (path) =>
  readFile(new URL(path, root), "utf8").catch(() => "");

const exists = async (path) =>
  stat(new URL(path, root))
    .then((entry) => entry.isFile())
    .catch(() => false);

const routes = [
  ["archive/index.html", "Explore Aetherhaven"],
  ["archive/map/index.html", "Map of Aetherhaven"],
  ["archive/hidden/index.html", "Hidden Archives"],
  ["archive/location/aetherhaven/index.html", "Aetherhaven"],
  ["archive/location/clockwork-gardens/index.html", "The Clockwork Gardens"],
  [
    "archive/location/gardens-airship-landing/index.html",
    "The Gardens Airship Landing",
  ],
  ["archive/district/merchant-district/index.html", "The Merchant District"],
  ["archive/district/inventors-district/index.html", "The Inventors’ District"],
  ["archive/location/aerial-docks/index.html", "The Aerial Docks"],
  ["archive/vessel/wayfinder/index.html", "The Wayfinder"],
  ["archive/character/amelia-hawthorne/index.html", "Amelia Hawthorne"],
  ["archive/organization/aetherhaven-archives/index.html", "The Aetherhaven Archives"],
];

for (const [path, expectedHeading] of routes) {
  const html = await readText(path);
  expect(Boolean(html), `Preview route must be generated: ${path}`);
  expect(html.includes(expectedHeading), `${path} must include ${expectedHeading}.`);
  expect(
    html.includes('<meta name="robots" content="noindex, nofollow">'),
    `${path} must remain noindex during preview refinement.`,
  );
  expect(
    html.includes("Proposal preview") ||
      html.includes("Preview only") ||
      path === "archive/map/index.html",
    `${path} must identify non-canonical proposal content.`,
  );
  expect(
    html.includes("archive-shell-open") &&
      html.includes("archive-interior-scene") &&
      html.includes("aetherhaven-archive-threshold-768.webp") &&
      html.includes("aetherhaven-archive-threshold-1024.webp"),
    `${path} must render inside the responsive Archive interior scene.`,
  );
}

const archiveHtml = await readText("archive/index.html");
const homeHtml = await readText("index.html");
const manifestText = await readText("site.webmanifest");
expect(
  homeHtml.includes("Enter Archive") && homeHtml.includes('href="/archive/"'),
  "Preview landing page must provide a primary entrance into the Archive.",
);
expect(
  homeHtml.includes('class="archive-invitation"') &&
    homeHtml.includes("aetherhaven-archive-threshold-768.webp") &&
    homeHtml.includes("aetherhaven-archive-threshold-1024.webp") &&
    homeHtml.includes("Invitation Waiting") &&
    homeHtml.includes("Lock Released") &&
    !homeHtml.includes("ArchiveLockExperience") &&
    !homeHtml.includes("react-three-fiber"),
  "Preview landing must render the simple Archive invitation over the responsive scene backdrop.",
);
expect(
  !homeHtml.includes("Coming Soon") &&
    !homeHtml.includes("Archive preparations underway") &&
    !homeHtml.includes("Return soon"),
  "Preview landing page must remove obsolete Coming Soon language.",
);
expect(
  manifestText.includes(
    '"description": "An entrance to The Brass Guardian and the Aetherhaven Archives."',
  ),
  "Preview web manifest must describe the active Archive entrance.",
);
expect(
  archiveHtml.includes('href="/archive/map/"'),
  "Archive entrance must link clearly to the map.",
);
expect(
  archiveHtml.includes("67 public records are indexed for this Preview"),
  "Archive entrance must report the preview record count.",
);
expect(
  archiveHtml.includes("Curator’s Route") &&
    archiveHtml.includes("Begin curated route"),
  "Archive entrance must offer a clearly curated discovery path.",
);
expect(
  archiveHtml.includes("Open Catalog") &&
  archiveHtml.includes('id="catalog-search"') &&
  archiveHtml.includes('id="catalog-result-count"') &&
  archiveHtml.includes('data-catalog-filter="character"') &&
  archiveHtml.includes('data-catalog-filter="organization"'),
  "Archive entrance must also offer a searchable, accessible open catalog.",
  );
  expect(
  archiveHtml.includes('href="/archive/hidden/"') &&
  archiveHtml.includes("Enter with spoiler warning"),
  "Archive entrance must separate sensitive records behind a warned Hidden Archives doorway.",
  );

const aetherhavenHtml = await readText("archive/location/aetherhaven/index.html");
expect(
  aetherhavenHtml.includes('aria-label="Curator’s Route"') &&
    aetherhavenHtml.includes("Next stop: The Map Room"),
  "Record pages must preserve the suggested route without trapping free exploration.",
);

const mapHtml = await readText("archive/map/index.html");
for (const marker of [...Array.from({ length: 24 }, (_, index) => String(index + 1)), "A", "B", "C", "D", "E", "F"]) {
  expect(
    mapHtml.includes(`data-map-marker="${marker}"`),
    `Interactive map must expose linked region ${marker}.`,
  );
}
expect(
  mapHtml.includes('class="map-link-overlay"') &&
    mapHtml.includes('viewBox="0 0 1539 1152"') &&
    !mapHtml.includes("map-hotspot"),
  "Map must use responsive semantic region-and-label links instead of floating marker buttons.",
);
expect(
  mapHtml.includes("map-of-aetherhaven-768.webp") &&
    mapHtml.includes("map-of-aetherhaven-1539.webp"),
  "Map must provide responsive derivatives while preserving the complete artwork.",
);
expect(
  mapHtml.includes("Map controls") && mapHtml.includes("Reset view"),
  "Map must expose understandable zoom controls.",
);
expect(
  mapHtml.includes(
    'id="map-zoom-level" for="map-zoom-in map-zoom-out" aria-live="polite" aria-atomic="true"',
  ),
  "Map must announce zoom-level changes to assistive technology.",
);
expect(
  mapHtml.includes("Accessible map index") &&
    mapHtml.includes("Public locations • 1–24") &&
    mapHtml.includes("Restricted references • A–F"),
  "Map must provide a non-visual index equivalent to its linked regions.",
);

const hiddenHtml = await readText("archive/hidden/index.html");
expect(
  hiddenHtml.includes("Spoiler and sensitive-material warning") &&
    hiddenHtml.includes("Hidden and mysterious figures") &&
    hiddenHtml.includes("Concealed and sensitive organizations"),
  "Hidden Archives must warn visitors and separate restricted locations, figures, and organizations.",
);
expect(
  (hiddenHtml.match(/<details /g) ?? []).length === 28,
  "Hidden Archives must emit all 28 closed restricted record stubs.",
);
expect(
  await exists("images/archive/map-of-aetherhaven-1539.webp"),
  "Preview builds must emit the staged proposal map asset.",
);
expect(
  (await exists("images/archive/aetherhaven-archive-threshold-768.webp")) &&
    (await exists("images/archive/aetherhaven-archive-threshold-1024.webp")),
  "Preview builds must emit both responsive Archive threshold backdrop derivatives.",
);
expect(
  mapHtml.includes("Continue to The Clockwork Gardens"),
  "The Map Room must offer the next curated stop.",
);

if (failures.length > 0) {
  console.error(`Archive preview verification failed (${failures.length}):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(
  "Archive preview verification passed: 67 public records, 30 direct map links, 28 closed Hidden Archive records, noindex controls, responsive art, and accessible navigation.",
);
