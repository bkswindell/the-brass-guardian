import { readFile, readdir } from "node:fs/promises";
import { join, relative, sep } from "node:path";

export const approvedArchiveAssetFilesV2 = Object.freeze([
  "aetherhaven-archive-threshold-1024.webp",
  "aetherhaven-archive-threshold-768.webp",
  "clockwork-gardens-at-night-480.webp",
  "clockwork-gardens-at-night-767.webp",
  "map-of-aetherhaven-1152.webp",
  "map-of-aetherhaven-1539.webp",
  "map-of-aetherhaven-768.webp",
  "wayfinder-above-clouds-1024.webp",
  "wayfinder-above-clouds-640.webp",
]);

const binaryExtensions = new Set([
  ".avif",
  ".gif",
  ".ico",
  ".jpeg",
  ".jpg",
  ".otf",
  ".png",
  ".ttf",
  ".webp",
  ".woff",
  ".woff2",
]);

const extensionOf = (path) => {
  const match = /\.[^.\/]+$/u.exec(path);
  return match?.[0]?.toLowerCase() ?? "";
};

const walkFiles = async (root, current = root) => {
  const entries = await readdir(current, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const path = join(current, entry.name);
    if (entry.isDirectory()) files.push(...(await walkFiles(root, path)));
    else if (entry.isFile()) files.push(path);
  }
  return files;
};

const escapeHtmlText = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;");

const escapeHtmlAttribute = (value) =>
  escapeHtmlText(value).replaceAll('"', "&quot;");

const escapeRegex = (value) =>
  String(value).replace(/[.*+?^${}()|[\]\\]/gu, "\\$&");

const findOwnedElement = ({ html, tag, attributes }) => {
  const lookaheads = attributes
    .map(
      ([name, value]) =>
        `(?=[^>]*[\\t\\n\\f\\r ]${escapeRegex(name)}="${escapeRegex(
          escapeHtmlAttribute(value),
        )}")`,
    )
    .join("");
  return (
    new RegExp(
      `<${tag}\\b${lookaheads}[^>]*>[\\s\\S]*?<\\/${tag}>`,
      "u",
    ).exec(html)?.[0] ?? ""
  );
};

const entryHref = (entry) => `/archive/${entry.entityType}/${entry.slug}/`;
const recordArtifactPath = (entry) =>
  `archive/${entry.entityType}/${entry.slug}/index.html`;
const hiddenDrawerId = (entry) =>
  entry.mapMarker ? `map-${entry.mapMarker}` : entry.slug;
const mapEntryHref = (entry) =>
  entry.archiveSection === "hidden"
    ? `/archive/hidden/#map-${entry.mapMarker}`
    : entryHref(entry);

export const verifyEmittedArchiveProjectionV2 = ({ htmlByPath, archive }) => {
  const failures = [];

  for (const entry of archive.entries) {
    const path = recordArtifactPath(entry);
    const html = htmlByPath.get(path) ?? "";
    if (!html) {
      failures.push(`Published record artifact is missing: ${path}.`);
      continue;
    }
    const associatedValues = [
      entry.publicTitle,
      entry.publicSummary,
      entry.entityType,
      entry.spoilerClassification,
      entry.publicAccessLabel,
      ...(entry.tags ?? []),
    ].filter(Boolean);
    for (const value of associatedValues) {
      if (!html.includes(escapeHtmlText(value))) {
        failures.push(
          `Published record artifact ${path} is missing approved value: ${value}`,
        );
      }
    }
    if (entry.image) {
      for (const value of [entry.image.src, entry.image.alt]) {
        if (!html.includes(escapeHtmlAttribute(value))) {
          failures.push(
            `Published record artifact ${path} is missing approved image value: ${value}`,
          );
        }
      }
    }
    for (const relatedId of entry.relatedEntryIds ?? []) {
      const relatedEntry = archive.entries.find(
        (candidate) => candidate.id === relatedId,
      );
      if (
        relatedEntry &&
        (!html.includes(
          `href="${escapeHtmlAttribute(entryHref(relatedEntry))}"`,
        ) ||
          !html.includes(escapeHtmlText(relatedEntry.publicTitle)))
      ) {
        failures.push(
          `Published record artifact ${path} has an incorrect related-record association: ${relatedId}.`,
        );
      }
    }
  }

  const hiddenHtml = htmlByPath.get("archive/hidden/index.html") ?? "";
  for (const entry of archive.hiddenEntries) {
    const drawer = findOwnedElement({
      html: hiddenHtml,
      tag: "details",
      attributes: [["id", hiddenDrawerId(entry)]],
    });
    if (
      !drawer ||
      !drawer.includes(escapeHtmlText(entry.publicTitle)) ||
      !drawer.includes(escapeHtmlText(entry.publicSummary)) ||
      !drawer.includes(
        escapeHtmlText(entry.publicAccessLabel ?? entry.spoilerClassification),
      )
    ) {
      failures.push(
        `Published Hidden Archive drawer has an incorrect association: ${entry.id}.`,
      );
    }
  }

  const mapHtml = htmlByPath.get("archive/map/index.html") ?? "";
  for (const entry of [...archive.mapEntries, ...archive.hiddenMapEntries]) {
    const anchor = findOwnedElement({
      html: mapHtml,
      tag: "a",
      attributes: [
        ["href", mapEntryHref(entry)],
        ["data-map-marker", entry.mapMarker],
      ],
    });
    if (
      !anchor ||
      !anchor.includes(escapeHtmlText(entry.publicTitle)) ||
      !anchor.includes(
        `cx="${entry.mapRegion.cx}" cy="${entry.mapRegion.cy}" r="${entry.mapRegion.r}"`,
      ) ||
      !anchor.includes(
        `x="${entry.mapLabel.x}" y="${entry.mapLabel.y}" width="${entry.mapLabel.width}" height="${entry.mapLabel.height}"`,
      )
    ) {
      failures.push(
        `Published map anchor has an incorrect approved association: ${entry.id}.`,
      );
    }
  }

  const archiveHtml = htmlByPath.get("archive/index.html") ?? "";
  const routeList =
    /<ol\b[^>]*class="route-list"[^>]*>[\s\S]*?<\/ol>/u.exec(
      archiveHtml,
    )?.[0] ?? "";
  for (const step of archive.curatorRoute) {
    const anchor = findOwnedElement({
      html: routeList,
      tag: "a",
      attributes: [["href", step.href]],
    });
    if (
      !anchor ||
      !anchor.includes(escapeHtmlText(step.label)) ||
      !anchor.includes(escapeHtmlText(step.note)) ||
      !anchor.includes(escapeHtmlText(step.title))
    ) {
      failures.push(
        `Published Curator Route step has an incorrect association: ${step.id}.`,
      );
    }
  }

  return failures;
};

export const findInternalPublicationLeaksV2 = async ({
  outputRoot,
  canonicalSourcePaths = [],
}) => {
  const files = (await walkFiles(outputRoot)).filter(
    (path) => !binaryExtensions.has(extensionOf(path)),
  );
  const markers = [
    "sourcePaths",
    "publicationStatus",
    "previewStatus",
    "projectionHash",
    "approvedBy",
    "approvedOn",
    "Proposal preview.",
    "Preview only",
    "Not canonical publication",
    ...canonicalSourcePaths,
  ].filter(Boolean);
  const failures = [];

  for (const path of files) {
    const content = await readFile(path, "utf8");
    for (const marker of markers) {
      if (content.includes(marker)) {
        const displayPath = relative(outputRoot, path).split(sep).join("/");
        failures.push(
          `Internal publication marker found in ${displayPath}: ${marker}`,
        );
      }
    }
  }

  return failures;
};

export const verifyArchiveAssetInventoryV2 = async ({ archiveAssetRoot }) => {
  const entries = await readdir(archiveAssetRoot, { withFileTypes: true }).catch(
    () => [],
  );
  const actualFiles = entries
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name);
  const actualSet = new Set(actualFiles);
  const approvedSet = new Set(approvedArchiveAssetFilesV2);
  const failures = [];

  for (const file of approvedArchiveAssetFilesV2) {
    if (!actualSet.has(file)) {
      failures.push(`Archive image inventory is missing approved file: ${file}.`);
    }
  }
  for (const entry of entries) {
    if (!entry.isFile() || !approvedSet.has(entry.name)) {
      failures.push(`Archive image inventory contains unapproved file: ${entry.name}.`);
    }
  }

  return failures.sort();
};
