import assert from "node:assert/strict";
import test from "node:test";

import { validatePublicationManifest } from "./lib/publication-boundary.mjs";

test("rejects undeclared manifest-level fields", async () => {
  await assert.rejects(
    validatePublicationManifest(
      { schemaVersion: 1, entries: [], privateNotes: "Never publish this." },
      { repositoryRoot: "/tmp/aetherhaven-manifest-shape-fixture" },
    ),
    /unrecognized manifest field: privateNotes/,
  );
});
