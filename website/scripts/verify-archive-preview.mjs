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
    html.includes("Proposal preview") || path === "archive/map/index.html",
    `${path} must identify non-canonical proposal content.`,
  );
}

const archiveHtml = await readText("archive/index.html");
expect(
  archiveHtml.includes('href="/archive/map/"'),
  "Archive entrance must link clearly to the map.",
);
expect(
  archiveHtml.includes("7 records cleared for preview"),
  "Archive entrance must report the preview record count.",
);

const mapHtml = await readText("archive/map/index.html");
for (const marker of ["2", "8", "12", "13", "19"]) {
  expect(
    mapHtml.includes(`data-map-marker="${marker}"`),
    `Interactive map must expose marker ${marker}.`,
  );
}
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
  mapHtml.includes("Accessible map records"),
  "Map must provide a non-visual record list equivalent to the hotspots.",
);
expect(
  await exists("images/archive/map-of-aetherhaven-1539.webp"),
  "Preview builds must emit the staged proposal map asset.",
);

if (failures.length > 0) {
  console.error(`Archive preview verification failed (${failures.length}):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(
  "Archive preview verification passed: entrance, interactive map, seven proposal records, noindex controls, responsive map art, and accessible navigation.",
);
