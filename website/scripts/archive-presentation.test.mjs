import assert from "node:assert/strict";
import test from "node:test";

import { validateArchivePresentation } from "./lib/archive-presentation.mjs";

const markers = [
  ...Array.from({ length: 24 }, (_, index) => String(index + 1)),
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
];

const recordIds = markers.map((marker) => `location-map-${marker.toLowerCase()}`);
const routeRecordIds = recordIds.slice(0, 7);
const publicationManifest = {
  schemaVersion: 1,
  entries: recordIds.map((id, index) => ({
    id,
    slug: `map-${markers[index].toLowerCase()}`,
    entityType: "location",
    publicTitle: `Map ${markers[index]}`,
    tags: index >= 24 ? ["hidden-archive"] : [],
  })),
};

const makePresentation = () => ({
  schemaVersion: 1,
  approval: {
    approvedBy: "author",
    approvedOn: "2026-08-10",
  },
  mapEntries: markers.map((mapMarker, index) => ({
    id: recordIds[index],
    mapMarker,
    ...(index === 0 ? { mapPosition: { x: 50, y: 50 } } : {}),
    mapRegion: { cx: 100 + index, cy: 100 + index, r: 20 },
    mapLabel: { x: 50 + index, y: 50 + index, width: 40, height: 20 },
  })),
  curatorRoute: [
    ...routeRecordIds.map((id, index) => ({
      id,
      kind: "record",
      label: `Route label ${index + 1}`,
      note: `Route annotation ${index + 1}.`,
    })),
    {
      id: "map-room",
      kind: "room",
      title: "The Map Room",
      href: "/archive/map/",
      label: "Cartographic table",
      note: "Set the records beside their numbered places.",
    },
  ],
});

test("accepts the exact approved map and Curator Route presentation contract", () => {
  const presentation = makePresentation();
  assert.equal(
    validateArchivePresentation(presentation, publicationManifest),
    presentation,
  );
});

test("rejects unknown presentation fields at every level", () => {
  const mutations = [
    (value) => {
      value.privateNotes = "never public";
    },
    (value) => {
      value.approval.internalComment = "never public";
    },
    (value) => {
      value.mapEntries[0].sourcePath = "proposal/catalog.mjs";
    },
    (value) => {
      value.mapEntries[0].mapRegion.privateRadius = 9;
    },
    (value) => {
      value.mapEntries[0].mapLabel.privateLabel = true;
    },
    (value) => {
      value.mapEntries[0].mapPosition.privateOffset = 1;
    },
    (value) => {
      value.curatorRoute[0].proposalStatus = "approved";
    },
  ];

  for (const mutate of mutations) {
    const presentation = makePresentation();
    mutate(presentation);
    assert.throws(
      () => validateArchivePresentation(presentation, publicationManifest),
      /unrecognized .* field/,
    );
  }
});

test("rejects malformed types and impossible dates", () => {
  const mutations = [
    (value) => {
      value.mapEntries = {};
    },
    (value) => {
      value.curatorRoute = {};
    },
    (value) => {
      value.approval.approvedOn = "2026-02-30";
    },
    (value) => {
      value.mapEntries[0].mapMarker = 1;
    },
    (value) => {
      value.mapEntries[0].mapRegion.cx = "100";
    },
    (value) => {
      value.curatorRoute[0].note = "";
    },
  ];

  for (const mutate of mutations) {
    const presentation = makePresentation();
    mutate(presentation);
    assert.throws(() =>
      validateArchivePresentation(presentation, publicationManifest),
    );
  }

  for (const href of [
    "/archive/../creator-only/",
    "/archive/%2e%2e/creator-only/",
    "/archive/map/?mode=internal",
    "/archive/map/#internal",
    "/archive//map/",
    "https://example.com/archive/map/",
  ]) {
    const presentation = makePresentation();
    presentation.curatorRoute.find((step) => step.kind === "room").href = href;
    assert.throws(
      () => validateArchivePresentation(presentation, publicationManifest),
      /href/u,
    );
  }
});

test("rejects out-of-map geometry and percentage ranges", () => {
  const mutations = [
    (value) => {
      value.mapEntries[0].mapRegion.cx = 1540;
    },
    (value) => {
      value.mapEntries[0].mapRegion.r = 0;
    },
    (value) => {
      value.mapEntries[0].mapLabel.x = -1;
    },
    (value) => {
      value.mapEntries[0].mapLabel.width = 2000;
    },
    (value) => {
      value.mapEntries[0].mapPosition.x = 101;
    },
  ];

  for (const mutate of mutations) {
    const presentation = makePresentation();
    mutate(presentation);
    assert.throws(
      () => validateArchivePresentation(presentation, publicationManifest),
      /map (geometry|position)/,
    );
  }
});

test("rejects duplicate markers, IDs, route steps, and missing references", () => {
  const mutations = [
    (value) => {
      value.mapEntries[1].mapMarker = value.mapEntries[0].mapMarker;
    },
    (value) => {
      value.mapEntries[1].id = value.mapEntries[0].id;
    },
    (value) => {
      value.curatorRoute[1].id = value.curatorRoute[0].id;
    },
    (value) => {
      value.mapEntries[0].id = "location-not-approved";
    },
    (value) => {
      value.curatorRoute[0].id = "location-not-approved";
    },
  ];

  for (const mutate of mutations) {
    const presentation = makePresentation();
    mutate(presentation);
    assert.throws(
      () => validateArchivePresentation(presentation, publicationManifest),
      /(duplicate|not present in the approved publication manifest)/,
    );
  }
});

test("requires exactly the approved marker set and eight route annotations", () => {
  const missingMap = makePresentation();
  missingMap.mapEntries.pop();
  assert.throws(
    () => validateArchivePresentation(missingMap, publicationManifest),
    /exactly 30 map entries/,
  );

  const missingRoute = makePresentation();
  missingRoute.curatorRoute.pop();
  assert.throws(
    () => validateArchivePresentation(missingRoute, publicationManifest),
    /exactly eight Curator Route annotations/,
  );
});
