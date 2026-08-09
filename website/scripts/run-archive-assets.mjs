import { access } from "node:fs/promises";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const websiteRoot = fileURLToPath(new URL("../", import.meta.url));
const script = fileURLToPath(
  new URL("generate-archive-assets.py", import.meta.url),
);
const candidates = [
  new URL("../.venv/bin/python", import.meta.url),
  new URL("../.venv/Scripts/python.exe", import.meta.url),
];

let python;
for (const candidate of candidates) {
  const path = fileURLToPath(candidate);
  try {
    await access(path);
    python = path;
    break;
  } catch {
    // Check the next platform-specific virtual-environment path.
  }
}

if (!python) {
  console.error(
    "Archive asset generation requires website/.venv with dependencies from scripts/requirements-generator.txt.",
  );
  process.exit(1);
}

const exitCode = await new Promise((resolve, reject) => {
  const child = spawn(python, [script, ...process.argv.slice(2)], {
    cwd: websiteRoot,
    stdio: "inherit",
  });
  child.once("error", reject);
  child.once("exit", (code, signal) => {
    if (signal) {
      reject(new Error(`Archive asset generator terminated by ${signal}.`));
      return;
    }
    resolve(code ?? 1);
  });
});

process.exitCode = exitCode;
