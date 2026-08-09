import { spawn } from "node:child_process";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { isArchivePreviewEnabled } from "../src/lib/archive-preview.mjs";
import { readOutputDirectory } from "./lib/build-output.mjs";
import { pruneProductionArchiveArtifacts } from "./lib/prune-production-archive.mjs";
import { syncPreviewAssets } from "./lib/preview-assets.mjs";

const websiteRoot = fileURLToPath(new URL("../", import.meta.url));
const sourceRoot = fileURLToPath(
  new URL("../content/preview/assets/archive/", import.meta.url),
);
const publicRoot = fileURLToPath(
  new URL("../public/images/archive/", import.meta.url),
);
const astroCli = fileURLToPath(
  new URL("../node_modules/astro/bin/astro.mjs", import.meta.url),
);
const enabled = isArchivePreviewEnabled(process.env);
const buildArgs = process.argv.slice(2);
const outputDirectory = await readOutputDirectory({ args: buildArgs, websiteRoot });
const outputArchiveRoot = join(outputDirectory, "images/archive");

await syncPreviewAssets({ enabled: false, sourceRoot, publicRoot });
await syncPreviewAssets({
  enabled: false,
  sourceRoot,
  publicRoot: outputArchiveRoot,
});

let exitCode = 1;
try {
  exitCode = await new Promise((resolve, reject) => {
    const child = spawn(
      process.execPath,
      [astroCli, "build", ...buildArgs],
      {
        cwd: websiteRoot,
        env: process.env,
        stdio: "inherit",
      },
    );
    child.once("error", reject);
    child.once("exit", (code, signal) => {
      if (signal) {
        reject(new Error(`Astro build terminated by ${signal}.`));
        return;
      }
      resolve(code ?? 1);
    });
  });

  if (exitCode === 0) {
    if (enabled) {
      await syncPreviewAssets({
        enabled: true,
        sourceRoot,
        publicRoot: outputArchiveRoot,
      });
    } else {
      await pruneProductionArchiveArtifacts({ outputRoot: outputDirectory });
    }
  }
} finally {
  await syncPreviewAssets({ enabled: false, sourceRoot, publicRoot });
}

process.exitCode = exitCode;
