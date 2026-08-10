import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

import archiveRelease from "../content/public/archive-release.json" with { type: "json" };
import { isArchiveEnabledForBuild } from "./lib/archive-release.mjs";
import { readOutputDirectory } from "./lib/build-output.mjs";
import { pruneProductionArchiveArtifacts } from "./lib/prune-production-archive.mjs";

const websiteRoot = fileURLToPath(new URL("../", import.meta.url));
const astroCli = fileURLToPath(
  new URL("../node_modules/astro/bin/astro.mjs", import.meta.url),
);
const enabled = isArchiveEnabledForBuild(archiveRelease, process.env);
const buildArgs = process.argv.slice(2);
const outputDirectory = await readOutputDirectory({ args: buildArgs, websiteRoot });

let exitCode = 1;
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

if (exitCode === 0 && !enabled) {
  await pruneProductionArchiveArtifacts({ outputRoot: outputDirectory });
}

process.exitCode = exitCode;
