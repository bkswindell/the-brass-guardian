import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import { pruneProductionArchiveArtifacts } from "./lib/prune-production-archive.mjs";

const exists = (path) => stat(path).then(() => true).catch(() => false);

const withOutput = async (run) => {
  const outputRoot = await mkdtemp(join(tmpdir(), "tbg-production-prune-"));
  try {
    await run(outputRoot);
  } finally {
    await rm(outputRoot, { recursive: true, force: true });
  }
};

test("removes production Archive routes and unreachable Archive CSS only", async () => {
  await withOutput(async (outputRoot) => {
    await mkdir(join(outputRoot, "archive", "map"), { recursive: true });
    await mkdir(join(outputRoot, "images", "archive"), { recursive: true });
    await mkdir(join(outputRoot, "_astro"), { recursive: true });
    await writeFile(
      join(outputRoot, "archive", "index.html"),
      '<link rel="stylesheet" href="/_astro/archive-entry.css">Archive sealed',
    );
    await writeFile(join(outputRoot, "archive", "map", "index.html"), "Map sealed");
    await writeFile(
      join(outputRoot, "index.html"),
      '<link rel="stylesheet" href="/_astro/site.css"><main>Coming Soon</main>',
    );
    await writeFile(join(outputRoot, "_astro", "site.css"), ".site-shell{display:block}");
    await writeFile(
      join(outputRoot, "_astro", "ArchiveLayout.preview.css"),
      ".archive-shell{min-height:100vh}.archive-interior-scene{position:fixed}",
    );
    await writeFile(
      join(outputRoot, "_astro", "archive-entry.css"),
      ".arrival-desk{display:grid}.curator-card{background:paper}",
    );
    await writeFile(join(outputRoot, "_astro", "unused.css"), ".unused{display:none}");
    await writeFile(join(outputRoot, "images", "archive", "map.webp"), "approved-map");

    await pruneProductionArchiveArtifacts({ outputRoot });

    assert.equal(await exists(join(outputRoot, "archive")), false);
    assert.equal(await exists(join(outputRoot, "images", "archive")), false);
    assert.equal(
      await exists(join(outputRoot, "_astro", "ArchiveLayout.preview.css")),
      false,
    );
    assert.equal(await exists(join(outputRoot, "_astro", "archive-entry.css")), false);
    assert.equal(await exists(join(outputRoot, "_astro", "site.css")), true);
    assert.equal(await exists(join(outputRoot, "_astro", "unused.css")), false);
  });
});

test("fails closed on Preview-only landing CSS reachable from production HTML", async () => {
  await withOutput(async (outputRoot) => {
    await mkdir(join(outputRoot, "_astro"), { recursive: true });
    await writeFile(
      join(outputRoot, "index.html"),
      '<link rel="stylesheet" href="/_astro/site.css"><main>Coming Soon</main>',
    );
    const siteCss = join(outputRoot, "_astro", "site.css");
    await writeFile(
      siteCss,
      ".site-shell{display:block}.archive-invitation{display:grid}",
    );

    await assert.rejects(
      pruneProductionArchiveArtifacts({ outputRoot }),
      /Production output references Archive Preview artifact/,
    );
    assert.equal(await exists(siteCss), true);
  });
});

test("fails closed before deleting an Archive artifact referenced by production HTML", async () => {
  await withOutput(async (outputRoot) => {
    await mkdir(join(outputRoot, "_astro"), { recursive: true });
    await writeFile(
      join(outputRoot, "index.html"),
      '<link rel="stylesheet" href="/_astro/ArchiveLayout.preview.css">',
    );
    const archiveCss = join(outputRoot, "_astro", "ArchiveLayout.preview.css");
    await writeFile(archiveCss, ".archive-shell{min-height:100vh}");

    await assert.rejects(
      pruneProductionArchiveArtifacts({ outputRoot }),
      /Production output references Archive Preview artifact/,
    );
    assert.equal(await exists(archiveCss), true);
  });
});

test("follows transitive production references before pruning Archive JavaScript", async () => {
  await withOutput(async (outputRoot) => {
    await mkdir(join(outputRoot, "_astro"), { recursive: true });
    await writeFile(
      join(outputRoot, "index.html"),
      '<script type="module" src="/_astro/site.js"></script>',
    );
    await writeFile(
      join(outputRoot, "_astro", "site.js"),
      'import "./archive-preview.js";',
    );
    const archiveScript = join(outputRoot, "_astro", "archive-preview.js");
    await writeFile(
      archiveScript,
      'document.documentElement.dataset.archiveShell = "open";',
    );

    await assert.rejects(
      pruneProductionArchiveArtifacts({ outputRoot }),
      /Production output references Archive Preview artifact/,
    );
    assert.match(await readFile(archiveScript, "utf8"), /archiveShell/);
  });
});