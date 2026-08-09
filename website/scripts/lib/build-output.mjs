import { stat } from "node:fs/promises";
import { isAbsolute, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const readOption = (args, name) => {
  const equalsArgument = args.find((argument) => argument.startsWith(`${name}=`));
  if (equalsArgument) return equalsArgument.slice(name.length + 1);

  const argumentIndex = args.indexOf(name);
  if (argumentIndex >= 0 && args[argumentIndex + 1]) {
    return args[argumentIndex + 1];
  }

  return undefined;
};

const existingConfigPath = async (args, websiteRoot) => {
  const configuredPath = readOption(args, "--config");
  if (configuredPath) return resolve(websiteRoot, configuredPath);

  for (const filename of [
    "astro.config.mjs",
    "astro.config.js",
    "astro.config.mts",
    "astro.config.ts",
  ]) {
    const path = resolve(websiteRoot, filename);
    const exists = await stat(path)
      .then((entry) => entry.isFile())
      .catch(() => false);
    if (exists) return path;
  }

  return undefined;
};

const resolveConfigValue = (value, root) => {
  if (value instanceof URL) return fileURLToPath(value);
  if (isAbsolute(value)) return value;
  return resolve(root, value);
};

export const readOutputDirectory = async ({ args, websiteRoot }) => {
  const cliOutDir = readOption(args, "--outDir");
  if (cliOutDir) return resolve(websiteRoot, cliOutDir);

  const configPath = await existingConfigPath(args, websiteRoot);
  if (!configPath) return resolve(websiteRoot, "dist");

  const configModule = await import(pathToFileURL(configPath).href);
  const config = await configModule.default;
  const configRoot = config?.root
    ? resolveConfigValue(config.root, websiteRoot)
    : websiteRoot;

  return config?.outDir
    ? resolveConfigValue(config.outDir, configRoot)
    : resolve(configRoot, "dist");
};
