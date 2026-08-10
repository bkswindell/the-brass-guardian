import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import manifest from "../content/public/manifest.json" with { type: "json" };
import presentation from "../content/public/archive-presentation.json" with { type: "json" };
import release from "../content/public/archive-release.json" with { type: "json" };
import { getArchivePublication } from "../src/lib/archive-publication.mjs";
import {
  approvedArchiveAssetFiles,
  buildExactApprovedProjection,
  findInternalPublicationLeaks,
  verifyArchiveAssetInventory,
  verifyEmittedApprovedProjection,
  verifyExactApprovedProjection,
} from "./lib/archive-publication-verifier.mjs";

const withTemporaryRoot = async (run) => {
  const root = await mkdtemp(join(tmpdir(), "tbg-publication-verifier-"));
  try {
    await run(root);
  } finally {
    await rm(root, { recursive: true, force: true });
  }
};

const escapeHtmlText = (value) => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;");

const escapeHtmlAttribute = (value) => escapeHtmlText(value).replaceAll('"', "&quot;");

const buildArtifactFixture = () => {
  const expected = buildExactApprovedProjection({ manifest, presentation, release });
  const htmlByPath = new Map();

  for (const entry of expected.entries) {
    const values = [
      entry.publicTitle,
      entry.publicSummary,
      entry.entityType,
      entry.spoilerClassification,
      entry.publicAccessLabel,
      ...(entry.tags ?? []),
    ].filter(Boolean).map((value) => `<span>${escapeHtmlText(value)}</span>`).join("");
    const image = entry.image
      ? `<img src="${escapeHtmlAttribute(entry.image.src)}" alt="${escapeHtmlAttribute(entry.image.alt)}">`
      : "";
    const related = (entry.relatedEntryIds ?? []).map((relatedId) => {
      const record = expected.entries.find((candidate) => candidate.id === relatedId);
      return record
        ? `<a href="/archive/${record.entityType}/${record.slug}/">${escapeHtmlText(record.publicTitle)}</a>`
        : "";
    }).join("");
    htmlByPath.set(
      `archive/${entry.entityType}/${entry.slug}/index.html`,
      `<article>${values}${image}${related}</article>`,
    );
  }

  htmlByPath.set(
    "archive/hidden/index.html",
    expected.hiddenEntries.map((entry) => {
      const id = entry.mapMarker ? `map-${entry.mapMarker}` : entry.slug;
      return `<details id="${id}"><strong>${escapeHtmlText(entry.publicTitle)}</strong><em>${escapeHtmlText(entry.publicAccessLabel ?? entry.spoilerClassification)}</em><p>${escapeHtmlText(entry.publicSummary)}</p></details>`;
    }).join(""),
  );
  htmlByPath.set(
    "archive/map/index.html",
    [...expected.mapEntries, ...expected.hiddenMapEntries].map((entry) => {
      const href = entry.tags.includes("hidden-archive")
        ? `/archive/hidden/#map-${entry.mapMarker}`
        : `/archive/${entry.entityType}/${entry.slug}/`;
      return `<a href="${href}" data-map-marker="${entry.mapMarker}"><title>${escapeHtmlText(entry.publicTitle)}</title><circle cx="${entry.mapRegion.cx}" cy="${entry.mapRegion.cy}" r="${entry.mapRegion.r}"></circle><rect x="${entry.mapLabel.x}" y="${entry.mapLabel.y}" width="${entry.mapLabel.width}" height="${entry.mapLabel.height}"></rect></a>`;
    }).join(""),
  );
  htmlByPath.set(
    "archive/index.html",
    `<ol class="route-list">${expected.curatorRoute.map((step) =>
      `<li><a href="${step.href}"><small>${escapeHtmlText(step.label)}</small><strong>${escapeHtmlText(step.title)}</strong><span>${escapeHtmlText(step.note)}</span></a></li>`
    ).join("")}</ol>`,
  );

  return { expected, htmlByPath };
};

test("exact projection verification rejects altered record and presentation values", async () => {
  const archive = structuredClone(
    await getArchivePublication({ VERCEL_ENV: "production" }),
  );
  archive.entries[0].publicSummary = "A raw proposal replacement.";
  archive.mapEntries[0].mapRegion.cx += 1;
  archive.curatorRoute[0].note = "A changed Curator Route annotation.";

  const failures = verifyExactApprovedProjection({
    archive,
    manifest,
    presentation,
    release,
  });

  assert.ok(failures.some((failure) => failure.includes("record projection")));
  assert.ok(failures.some((failure) => failure.includes("map presentation")));
  assert.ok(failures.some((failure) => failure.includes("Curator Route")));
});

test("publication leak scan checks every emitted non-binary artifact", async () => {
  await withTemporaryRoot(async (outputRoot) => {
    const extensions = [
      "html",
      "css",
      "js",
      "mjs",
      "json",
      "txt",
      "xml",
      "svg",
      "webmanifest",
      "map",
    ];
    for (const extension of extensions) {
      await writeFile(
        join(outputRoot, `artifact.${extension}`),
        `<internal>${manifest.entries[0].sourcePaths[0]}</internal>`,
      );
    }
    await writeFile(join(outputRoot, "extensionless"), "Proposal preview.");
    await writeFile(join(outputRoot, "clean.svg"), "<svg>public safe</svg>");
    await writeFile(
      join(outputRoot, "approved-binary.webp"),
      manifest.entries[0].sourcePaths[0],
    );

    const failures = await findInternalPublicationLeaks({
      outputRoot,
      manifest,
    });

    for (const path of [
      ...extensions.map((extension) => `artifact.${extension}`),
      "extensionless",
    ]) {
      assert.ok(failures.some((failure) => failure.includes(path)), path);
    }
    assert.ok(!failures.some((failure) => failure.includes("clean.svg")));
    assert.ok(!failures.some((failure) => failure.includes("approved-binary.webp")));
  });
});

test("emitted projection verification rejects reassociated record, map, and route values", () => {
  const { expected, htmlByPath } = buildArtifactFixture();
  assert.deepEqual(
    verifyEmittedApprovedProjection({ htmlByPath, manifest, presentation, release }),
    [],
  );

  const firstRecord = expected.entries[0];
  const recordPath = `archive/${firstRecord.entityType}/${firstRecord.slug}/index.html`;
  htmlByPath.set(
    recordPath,
    htmlByPath.get(recordPath).replace(
      escapeHtmlText(firstRecord.publicSummary),
      "unapproved replacement projection",
    ),
  );

  const mapHtml = htmlByPath.get("archive/map/index.html");
  htmlByPath.set(
    "archive/map/index.html",
    mapHtml
      .replace('data-map-marker="1"', 'data-map-marker="temporary"')
      .replace('data-map-marker="2"', 'data-map-marker="1"')
      .replace('data-map-marker="temporary"', 'data-map-marker="2"'),
  );

  const [firstStep, secondStep] = expected.curatorRoute;
  const routeHtml = htmlByPath.get("archive/index.html");
  htmlByPath.set(
    "archive/index.html",
    routeHtml
      .replace(escapeHtmlText(firstStep.note), "temporary-route-note")
      .replace(escapeHtmlText(secondStep.note), escapeHtmlText(firstStep.note))
      .replace("temporary-route-note", escapeHtmlText(secondStep.note)),
  );

  const failures = verifyEmittedApprovedProjection({
    htmlByPath,
    manifest,
    presentation,
    release,
  });
  assert.ok(failures.some((failure) => failure.includes("record artifact")));
  assert.ok(failures.some((failure) => failure.includes("map anchor")));
  assert.ok(failures.some((failure) => failure.includes("Curator Route step")));
});

test("emitted ownership requires exact attribute names", () => {
  const assertMutationFails = (mutate, expectedId) => {
    const fixture = buildArtifactFixture();
    mutate(fixture);
    const failures = verifyEmittedApprovedProjection({
      htmlByPath: fixture.htmlByPath,
      manifest,
      presentation,
      release,
    });
    assert.ok(
      failures.some((failure) => failure.includes(expectedId)),
      expectedId,
    );
  };

  const fixture = buildArtifactFixture();
  const firstMapEntry = fixture.expected.mapEntries[0];
  const firstStep = fixture.expected.curatorRoute[0];
  const firstHidden = fixture.expected.hiddenEntries[0];
  const mapHref = `/archive/${firstMapEntry.entityType}/${firstMapEntry.slug}/`;
  const drawerId = firstHidden.mapMarker
    ? `map-${firstHidden.mapMarker}`
    : firstHidden.slug;

  assertMutationFails(({ htmlByPath }) => {
    htmlByPath.set(
      "archive/map/index.html",
      htmlByPath.get("archive/map/index.html").replace(
        ` href="${mapHref}"`,
        ` data-href="${mapHref}"`,
      ),
    );
  }, firstMapEntry.id);
  assertMutationFails(({ htmlByPath }) => {
    htmlByPath.set(
      "archive/map/index.html",
      htmlByPath.get("archive/map/index.html").replace(
        ` data-map-marker="${firstMapEntry.mapMarker}"`,
        ` x-data-map-marker="${firstMapEntry.mapMarker}"`,
      ),
    );
  }, firstMapEntry.id);
  assertMutationFails(({ htmlByPath }) => {
    htmlByPath.set(
      "archive/index.html",
      htmlByPath.get("archive/index.html").replace(
        ` href="${firstStep.href}"`,
        ` data-href="${firstStep.href}"`,
      ),
    );
  }, firstStep.id);
  assertMutationFails(({ htmlByPath }) => {
    htmlByPath.set(
      "archive/hidden/index.html",
      htmlByPath.get("archive/hidden/index.html").replace(
        ` id="${drawerId}"`,
        ` data-id="${drawerId}"`,
      ),
    );
  }, firstHidden.id);

  for (const [path, exactAttribute, prefixedAttribute, expectedId] of [
    ["archive/map/index.html", `href="${mapHref}"`, `data-\u00a0href="${mapHref}"`, firstMapEntry.id],
    [
      "archive/map/index.html",
      `data-map-marker="${firstMapEntry.mapMarker}"`,
      `x-\u00a0data-map-marker="${firstMapEntry.mapMarker}"`,
      firstMapEntry.id,
    ],
    ["archive/hidden/index.html", `id="${drawerId}"`, `data-\u00a0id="${drawerId}"`, firstHidden.id],
  ]) {
    assertMutationFails(({ htmlByPath }) => {
      htmlByPath.set(
        path,
        htmlByPath.get(path).replace(` ${exactAttribute}`, ` ${prefixedAttribute}`),
      );
    }, expectedId);
  }
});

test("emitted projection rejects Hidden Archive drawer reassociation", () => {
  const { expected, htmlByPath } = buildArtifactFixture();
  const [firstHidden, secondHidden] = expected.hiddenEntries;
  htmlByPath.set(
    "archive/hidden/index.html",
    htmlByPath.get("archive/hidden/index.html")
      .replace(escapeHtmlText(firstHidden.publicSummary), "temporary-hidden-summary")
      .replace(
        escapeHtmlText(secondHidden.publicSummary),
        escapeHtmlText(firstHidden.publicSummary),
      )
      .replace(
        "temporary-hidden-summary",
        escapeHtmlText(secondHidden.publicSummary),
      ),
  );

  const failures = verifyEmittedApprovedProjection({
    htmlByPath,
    manifest,
    presentation,
    release,
  });
  assert.ok(failures.some((failure) => failure.includes(firstHidden.id)));
  assert.ok(failures.some((failure) => failure.includes(secondHidden.id)));
});

test("Archive image inventory rejects any file beyond the nine approved files", async () => {
  await withTemporaryRoot(async (archiveAssetRoot) => {
    await mkdir(archiveAssetRoot, { recursive: true });
    await Promise.all(
      [...approvedArchiveAssetFiles, "unapproved-extra.webp"].map((file) =>
        writeFile(join(archiveAssetRoot, file), "fixture"),
      ),
    );

    const failures = await verifyArchiveAssetInventory({ archiveAssetRoot });

    assert.deepEqual(failures, [
      "Archive image inventory contains unapproved file: unapproved-extra.webp.",
    ]);
  });
});
