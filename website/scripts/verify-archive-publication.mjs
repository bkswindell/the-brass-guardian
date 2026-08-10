import { readFile, readdir, stat } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { join, relative, resolve, sep } from "node:path";

import publicationLedger from "../content/public/manifest.v2.json" with { type: "json" };
import archivePresentation from "../content/public/archive-presentation.v2.json" with { type: "json" };
import archiveRelease from "../content/public/archive-release.json" with { type: "json" };
import assetRegistry from "../content/public/archive-assets.json" with { type: "json" };

import {
  loadCanonRecords,
  loadCanonRecordSources,
} from "./lib/canon-record-loader.mjs";
import { buildArchivePublicationV2 } from "./lib/archive-publication-v2-model.mjs";
import {
  approvedArchiveAssetFilesV2,
  findInternalPublicationLeaksV2,
  verifyArchiveAssetInventoryV2,
  verifyEmittedArchiveProjectionV2,
} from "./lib/archive-publication-verifier-v2.mjs";

const root = fileURLToPath(new URL("../dist/", import.meta.url));
const websiteRoot = fileURLToPath(new URL("../", import.meta.url));
const repositoryRoot = resolve(websiteRoot, "..");
const siteOrigin = "https://thebrassguardian.com";
const failures = [];

const expect = (condition, message) => {
  if (!condition) failures.push(message);
};

const records = await loadCanonRecords({ repositoryRoot });
const sources = await loadCanonRecordSources({ repositoryRoot });
const archive = await buildArchivePublicationV2({
  records,
  ledger: publicationLedger,
  presentation: archivePresentation,
  release: archiveRelease,
  assetRegistry,
  repositoryRoot,
  preview: false,
});

const paths = (await readdir(root, { recursive: true, withFileTypes: true }))
  .filter((entry) => entry.isFile())
  .map((entry) =>
    relative(root, join(entry.parentPath, entry.name)).split(sep).join("/"),
  )
  .sort();
const htmlPaths = paths.filter((path) => path.endsWith(".html"));
const htmlByPath = new Map(
  await Promise.all(
    htmlPaths.map(async (path) => [path, await readFile(join(root, path), "utf8")]),
  ),
);

const archivePaths = htmlPaths.filter((path) => path.startsWith("archive/"));
const recordPaths = archivePaths.filter(
  (path) => path.split("/").length === 4 && path.endsWith("/index.html"),
);

expect(records.length === 210, `Expected 210 Schema v1 canon records; found ${records.length}.`);
expect(publicationLedger.entries.length === 95, `Expected 95 approved projection fingerprints; found ${publicationLedger.entries.length}.`);
expect(htmlPaths.length === 72, `Production must emit 72 HTML pages; found ${htmlPaths.length}.`);
expect(archivePaths.length === 70, `Production must emit 70 Archive pages; found ${archivePaths.length}.`);
expect(recordPaths.length === 67, `Production must emit 67 public record routes; found ${recordPaths.length}.`);
expect(archive.entries.length === 67, `Publication model must contain 67 public records; found ${archive.entries.length}.`);
expect(archive.hiddenEntries.length === 28, `Publication model must contain 28 Hidden Archive teasers; found ${archive.hiddenEntries.length}.`);
expect(archive.mapEntries.length + archive.hiddenMapEntries.length === 30, "Publication model must resolve all 30 canonical map references.");
expect(archive.curatorRoute.length === 8, "Publication model must preserve all eight Curator Route steps.");

for (const path of archivePaths) {
  const html = htmlByPath.get(path);
  const route = `/${path.replace(/index\.html$/u, "")}`;
  const canonical = `${siteOrigin}${route}`;
  expect(
    html.includes(`<link rel="canonical" href="${canonical}">`),
    `${path} must declare canonical ${canonical}.`,
  );
  expect(
    html.includes('<meta name="robots" content="index, follow">'),
    `${path} must allow indexing in the published release.`,
  );
  expect(!html.includes("Proposal preview"), `${path} must not expose Preview labels.`);
  expect(!html.includes("Preview only"), `${path} must not expose Preview-only labels.`);
  expect(!html.includes("Not canonical publication"), `${path} must not deny its approved projection.`);
}

const homeHtml = htmlByPath.get("index.html") ?? "";
const archiveHtml = htmlByPath.get("archive/index.html") ?? "";
const mapHtml = htmlByPath.get("archive/map/index.html") ?? "";
const hiddenHtml = htmlByPath.get("archive/hidden/index.html") ?? "";

failures.push(...verifyEmittedArchiveProjectionV2({ htmlByPath, archive }));

expect(
  homeHtml.includes("Enter Archive") && homeHtml.includes('href="/archive/"'),
  "Published landing page must open the Archive.",
);
expect(
  archiveHtml.includes("67 public records are indexed in the Archive"),
  "Published Archive entrance must report all 67 public records.",
);
expect(
  archiveHtml.includes('href="/archive/hidden/"') &&
    archiveHtml.includes("Enter with spoiler warning"),
  "Published Archive entrance must retain the warned Hidden Archives doorway.",
);
expect(
  (mapHtml.match(/class="map-link-overlay"/gu) ?? []).length === 1 &&
    (mapHtml.match(/data-map-marker=/gu) ?? []).length === 30 &&
    !mapHtml.includes("map-hotspot"),
  "Published map must retain one semantic link per 30 direct region-and-label targets.",
);
expect(
  hiddenHtml.includes("Spoiler and sensitive-material warning") &&
    hiddenHtml.includes("Hidden and mysterious figures") &&
    hiddenHtml.includes("Concealed and sensitive organizations"),
  "Published Hidden Archives must retain its explicit warning and separated indexes.",
);
expect(
  (hiddenHtml.match(/<details(?:\s|>)/gu) ?? []).length === 28,
  "Published Hidden Archives must emit all 28 teaser drawers.",
);
expect(
  !/<details\b[^>]*\bopen(?:\s|=|>)/iu.test(hiddenHtml),
  "Published Hidden Archive drawers must remain closed by default.",
);

for (const asset of approvedArchiveAssetFilesV2) {
  expect(
    await stat(join(root, "images", "archive", asset))
      .then((entry) => entry.isFile())
      .catch(() => false),
    `Published Archive asset must exist: ${asset}.`,
  );
}

failures.push(
  ...(await verifyArchiveAssetInventoryV2({
    archiveAssetRoot: join(root, "images", "archive"),
  })),
);
failures.push(
  ...(await findInternalPublicationLeaksV2({
    outputRoot: root,
    canonicalSourcePaths: sources.map((source) => source.relativePath),
  })),
);

const emittedHtml = [...htmlByPath.values()].join("\n");
for (const privateField of [
  "projectionHash",
  "approvedBy",
  "approvedOn",
  "schema_version",
  "public_projection",
  "disclosure",
]) {
  expect(
    !emittedHtml.includes(privateField),
    `Published HTML must not expose internal publication field ${privateField}.`,
  );
}

const hrefPattern = /\shref="([^"]+)"/gu;
for (const [sourcePath, html] of htmlByPath) {
  for (const [, href] of html.matchAll(hrefPattern)) {
    const url = new URL(
      href,
      `${siteOrigin}/${sourcePath.replace(/index\.html$/u, "")}`,
    );
    if (url.origin !== siteOrigin) continue;
    if (/\.[a-z0-9]+$/iu.test(url.pathname)) continue;

    const targetPath =
      url.pathname === "/"
        ? "index.html"
        : `${url.pathname.replace(/^\//u, "").replace(/\/$/u, "")}/index.html`;
    const targetHtml = htmlByPath.get(targetPath);
    expect(Boolean(targetHtml), `${sourcePath} links to missing route ${url.pathname}.`);
    if (targetHtml && url.hash) {
      const fragment = decodeURIComponent(url.hash.slice(1));
      expect(
        targetHtml.includes(`id="${fragment}"`),
        `${sourcePath} links to missing fragment ${url.pathname}${url.hash}.`,
      );
    }
  }
}

if (failures.length > 0) {
  console.error(`Archive publication verification failed (${failures.length}):`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(
  "Archive publication verification passed: 210 Schema v1 records, 95 hash-approved projections, 72 pages, 67 public records, 30 canonical map links, 28 closed Hidden Archive teasers, exact emitted projection, approved assets, and valid internal links.",
);
