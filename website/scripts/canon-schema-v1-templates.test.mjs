import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const templateCases = [
  ["Character_Profile_Template.md", "character"],
  ["Location_Profile_Template.md", "location"],
  ["Organization_Profile_Template.md", "organization"],
  ["Artifact_Profile_Template.md", "artifact"],
  ["Historical_Event_Profile_Template.md", "historical_event"],
  ["Story_Profile_Template.md", "story"],
  ["Story_Arc_Profile_Template.md", "story_arc"],
  ["Vessel_Profile_Template.md", "vessel"],
];

for (const [filename, recordType] of templateCases) {
  test(`${filename} declares the locked Version 1 universal contract`, async () => {
    const url = new URL(`../../templates/${filename}`, import.meta.url);
    const source = await readFile(url, "utf8");

    assert.match(source, /^---\n/u);
    assert.match(source, /\nschema_version: 1\n/u);
    assert.match(source, new RegExp(`\\nrecord_type: ${recordType}\\n`, "u"));
    assert.match(source, /\nslug: [a-z0-9-]+\n/u);
    assert.match(source, /\naliases: \[\]\n/u);
    assert.match(source, /\ncanon:\n\s+status: proposed\n\s+scope: \[\]\n/u);
    assert.match(source, /\ndevelopment:\n\s+status: concept\n/u);
    assert.match(source, /\ndisclosure:\n\s+level: creator-only\n/u);
    assert.match(source, /\nrelationships: \[\]\n/u);
    assert.match(source, /\nassets: \[\]\n/u);
    assert.match(source, /\nprovenance:\n\s+sources: \[\]\n/u);
    assert.match(source, /Passes the Version 1 executable validator/u);

    assert.doesNotMatch(source, /(?:character|location|organization|artifact|historical_event|story_arc|story_draft)_id:/u);
    assert.doesNotMatch(source, /\ncanon_status:/u);
    assert.doesNotMatch(source, /\ncanonical_scope:/u);
    assert.doesNotMatch(source, /\ncanonical_images:/u);
  });
}

test("all eight locked canonical record types have a reusable template", () => {
  assert.deepEqual(
    templateCases.map(([, type]) => type).sort(),
    [
      "artifact",
      "character",
      "historical_event",
      "location",
      "organization",
      "story",
      "story_arc",
      "vessel",
    ],
  );
});