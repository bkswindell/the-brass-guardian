import { cp, mkdir, rm } from "node:fs/promises";
import { dirname } from "node:path";

export const syncPreviewAssets = async ({
  enabled,
  sourceRoot,
  publicRoot,
}) => {
  await rm(publicRoot, { recursive: true, force: true });
  if (!enabled) return;

  await mkdir(dirname(publicRoot), { recursive: true });
  await cp(sourceRoot, publicRoot, {
    recursive: true,
    errorOnExist: true,
    force: false,
  });
};
