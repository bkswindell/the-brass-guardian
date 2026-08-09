import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

import { isArchivePreviewEnabled } from "../src/lib/archive-preview.mjs";
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

await syncPreviewAssets({ enabled, sourceRoot, publicRoot });

let exitCode = 1;
try {
  exitCode = await new Promise((resolve, reject) => {
    const child = spawn(
      process.execPath,
      [astroCli, "build", ...process.argv.slice(2)],
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
} finally {
  await syncPreviewAssets({ enabled: false, sourceRoot, publicRoot });
}

process.exitCode = exitCode;
