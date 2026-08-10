const rootFields = new Set([
  "schemaVersion",
  "approval",
  "mapEntries",
  "curatorRoute",
]);
const approvalFields = new Set(["approvedBy", "approvedOn"]);
const mapEntryFields = new Set([
  "id",
  "mapMarker",
  "mapPosition",
  "mapRegion",
  "mapLabel",
]);
const mapRegionFields = new Set(["cx", "cy", "r"]);
const mapLabelFields = new Set(["x", "y", "width", "height"]);
const mapPositionFields = new Set(["x", "y"]);
const recordRouteFields = new Set(["id", "kind", "label", "note"]);
const roomRouteFields = new Set([
  "id",
  "kind",
  "title",
  "href",
  "label",
  "note",
]);
const mapMarkers = [
  ...Array.from({ length: 24 }, (_, index) => String(index + 1)),
  "A",
  "B",
  "C",
  "D",
  "E",
  "F",
];
const markerSet = new Set(mapMarkers);
const isoDatePattern = /^\d{4}-\d{2}-\d{2}$/u;
const archiveRoomHrefPattern = /^\/archive\/(?:[a-z0-9]+(?:-[a-z0-9]+)*\/)*$/u;

const assertObject = (value, label) => {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be an object.`);
  }
};

const assertKnownFields = (value, fields, label) => {
  assertObject(value, label);
  const unknownField = Object.keys(value).find((field) => !fields.has(field));
  if (unknownField) {
    throw new Error(`unrecognized ${label} field: ${unknownField}`);
  }
};

const assertNonEmptyString = (value, label) => {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${label} must be a non-empty string.`);
  }
};

const isIsoDate = (value) => {
  if (typeof value !== "string" || !isoDatePattern.test(value)) return false;
  const [year, month, day] = value.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return (
    date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day
  );
};

const assertFiniteRange = (value, minimum, maximum, label) => {
  if (!Number.isFinite(value) || value < minimum || value > maximum) {
    throw new Error(`${label} is outside the approved map geometry range.`);
  }
};

const validateMapEntry = (entry, approvedById) => {
  assertKnownFields(entry, mapEntryFields, "map entry");
  assertNonEmptyString(entry.id, "map entry id");
  if (!approvedById.has(entry.id)) {
    throw new Error(
      `map entry ${entry.id} is not present in the approved publication manifest.`,
    );
  }
  if (typeof entry.mapMarker !== "string" || !markerSet.has(entry.mapMarker)) {
    throw new Error(`map entry ${entry.id} has an invalid map marker.`);
  }

  const approvedEntry = approvedById.get(entry.id);
  const hidden = approvedEntry.tags?.includes("hidden-archive") ?? false;
  const restrictedMarker = /^[A-F]$/u.test(entry.mapMarker);
  if (hidden !== restrictedMarker) {
    throw new Error(
      `map entry ${entry.id} has a marker that conflicts with its publication class.`,
    );
  }

  assertKnownFields(entry.mapRegion, mapRegionFields, "map region");
  assertFiniteRange(entry.mapRegion.cx, 0, 1539, "map geometry cx");
  assertFiniteRange(entry.mapRegion.cy, 0, 1152, "map geometry cy");
  assertFiniteRange(entry.mapRegion.r, Number.EPSILON, 1539, "map geometry radius");

  assertKnownFields(entry.mapLabel, mapLabelFields, "map label");
  assertFiniteRange(entry.mapLabel.x, 0, 1539, "map geometry label x");
  assertFiniteRange(entry.mapLabel.y, 0, 1152, "map geometry label y");
  assertFiniteRange(
    entry.mapLabel.width,
    Number.EPSILON,
    1539,
    "map geometry label width",
  );
  assertFiniteRange(
    entry.mapLabel.height,
    Number.EPSILON,
    1152,
    "map geometry label height",
  );
  if (
    entry.mapLabel.x + entry.mapLabel.width > 1539 ||
    entry.mapLabel.y + entry.mapLabel.height > 1152
  ) {
    throw new Error(`map geometry label for ${entry.id} exceeds the map bounds.`);
  }

  if (entry.mapPosition !== undefined) {
    assertKnownFields(entry.mapPosition, mapPositionFields, "map position");
    assertFiniteRange(entry.mapPosition.x, 0, 100, "map position x");
    assertFiniteRange(entry.mapPosition.y, 0, 100, "map position y");
  }
};

const validateRouteStep = (step, approvedById) => {
  const fields = step?.kind === "room" ? roomRouteFields : recordRouteFields;
  assertKnownFields(step, fields, "Curator Route step");
  assertNonEmptyString(step.id, "Curator Route step id");
  assertNonEmptyString(step.kind, "Curator Route step kind");
  assertNonEmptyString(step.label, "Curator Route label");
  assertNonEmptyString(step.note, "Curator Route note");

  if (step.kind === "record") {
    const approvedEntry = approvedById.get(step.id);
    if (!approvedEntry) {
      throw new Error(
        `Curator Route step ${step.id} is not present in the approved publication manifest.`,
      );
    }
    if (approvedEntry.tags?.includes("hidden-archive")) {
      throw new Error(`Curator Route step ${step.id} cannot reference a hidden record.`);
    }
    return;
  }

  if (step.kind !== "room" || step.id !== "map-room") {
    throw new Error(`Curator Route room step must be map-room.`);
  }
  assertNonEmptyString(step.title, "Curator Route room title");
  if (typeof step.href !== "string" || !archiveRoomHrefPattern.test(step.href)) {
    throw new Error(`Curator Route room href must be a canonical Archive path.`);
  }
};

export const validateArchivePresentation = (presentation, publicationManifest) => {
  assertKnownFields(presentation, rootFields, "archive presentation");
  if (presentation.schemaVersion !== 1) {
    throw new Error("archive presentation schemaVersion must be 1.");
  }

  assertKnownFields(presentation.approval, approvalFields, "presentation approval");
  if (
    presentation.approval.approvedBy !== "author" ||
    !isIsoDate(presentation.approval.approvedOn)
  ) {
    throw new Error("archive presentation requires a dated author approval.");
  }
  if (!Array.isArray(publicationManifest?.entries)) {
    throw new Error("approved publication manifest entries must be an array.");
  }
  if (!Array.isArray(presentation.mapEntries)) {
    throw new Error("archive presentation mapEntries must be an array.");
  }
  if (presentation.mapEntries.length !== 30) {
    throw new Error("archive presentation requires exactly 30 map entries.");
  }
  if (!Array.isArray(presentation.curatorRoute)) {
    throw new Error("archive presentation curatorRoute must be an array.");
  }
  if (presentation.curatorRoute.length !== 8) {
    throw new Error(
      "archive presentation requires exactly eight Curator Route annotations.",
    );
  }

  const approvedById = new Map(
    publicationManifest.entries.map((entry) => [entry.id, entry]),
  );
  const mapIds = new Set();
  const seenMarkers = new Set();
  for (const entry of presentation.mapEntries) {
    validateMapEntry(entry, approvedById);
    if (mapIds.has(entry.id)) throw new Error(`duplicate map entry id: ${entry.id}`);
    if (seenMarkers.has(entry.mapMarker)) {
      throw new Error(`duplicate map marker: ${entry.mapMarker}`);
    }
    mapIds.add(entry.id);
    seenMarkers.add(entry.mapMarker);
  }
  for (const marker of mapMarkers) {
    if (!seenMarkers.has(marker)) {
      throw new Error(`archive presentation is missing approved map marker ${marker}.`);
    }
  }

  const routeIds = new Set();
  for (const step of presentation.curatorRoute) {
    validateRouteStep(step, approvedById);
    if (routeIds.has(step.id)) {
      throw new Error(`duplicate Curator Route step id: ${step.id}`);
    }
    routeIds.add(step.id);
  }

  return presentation;
};
