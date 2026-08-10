import { readFile, readdir, rm } from "node:fs/promises";
import { basename, extname, join, relative, sep } from "node:path";

const textExtensions = new Set([".css", ".html", ".js", ".json", ".mjs", ".txt"]);
export const archivePreviewMarkers = [
  "aetherhaven-archive-threshold",
  "/images/archive/",
  "archive-atmosphere",
  "archive-backdrop",
  "archive-card-open",
  "archive-invitation",
  "invitation-kicker",
  "invitation-state",
  "invitation-waiting",
  "invitation-released",
  "archive-interior-scene",
  "archive-room-floor",
  "archive-shell-open",
  "archiveShell",
  "arrival-desk",
  "curator-card",
  "route-list",
  "record-card",
  "catalog-controls",
  "map-record-detail",
  "record-sheet",
];

const listFiles = async (root) => {
  const files = [];

  const visit = async (directory) => {
    const entries = await readdir(directory, { withFileTypes: true });
    for (const entry of entries) {
      const path = join(directory, entry.name);
      if (entry.isDirectory()) {
        await visit(path);
      } else if (entry.isFile()) {
        files.push(path);
      }
    }
  };

  await visit(root);
  return files;
};

const toOutputPath = (outputRoot, path) =>
  relative(outputRoot, path).split(sep).join("/");

const referencesFile = (source, target) => {
  if (source.path === target.path || !source.content) return false;

  return (
    source.content.includes(`/${target.outputPath}`) ||
    source.content.includes(`./${target.name}`) ||
    source.content.includes(target.name)
  );
};

const isPreviewSensitive = (file) =>
  /^ArchiveLayout\..+\.(?:css|js)$/u.test(file.name) ||
  archivePreviewMarkers.some((marker) => file.content?.includes(marker));

export const pruneProductionArchiveArtifacts = async ({ outputRoot }) => {
  const paths = await listFiles(outputRoot);
  const files = [];

  for (const path of paths) {
    const isText = textExtensions.has(extname(path));
    files.push({
      path,
      outputPath: toOutputPath(outputRoot, path),
      name: basename(path),
      content: isText ? await readFile(path, "utf8") : undefined,
    });
  }

  const retainedHtml = files.filter(
    (file) =>
      extname(file.path) === ".html" &&
      !file.outputPath.startsWith("archive/"),
  );
  if (retainedHtml.length === 0) {
    throw new Error("Production output contains no retained HTML entry points.");
  }

  const reachable = new Set(retainedHtml.map((file) => file.path));
  const queue = [...retainedHtml];

  while (queue.length > 0) {
    const source = queue.shift();
    for (const target of files) {
      if (reachable.has(target.path) || !referencesFile(source, target)) continue;
      reachable.add(target.path);
      queue.push(target);
    }
  }

  const referencedArtifacts = files.filter(
    (file) => reachable.has(file.path) && isPreviewSensitive(file),
  );

  if (referencedArtifacts.length > 0) {
    const emittedPaths = referencedArtifacts
      .map((file) => file.outputPath)
      .sort()
      .join(", ");
    throw new Error(
      `Production output references Archive Preview artifact(s): ${emittedPaths}`,
    );
  }

  await rm(join(outputRoot, "archive"), { recursive: true, force: true });
  await rm(join(outputRoot, "images", "archive"), {
    recursive: true,
    force: true,
  });

  const unreachableBuildArtifacts = files.filter(
    (file) =>
      file.outputPath.startsWith("_astro/") && !reachable.has(file.path),
  );
  await Promise.all(
    unreachableBuildArtifacts.map((file) => rm(file.path, { force: true })),
  );
};
