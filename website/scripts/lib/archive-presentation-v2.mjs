const rootFields = new Set([
  "schemaVersion",
  "approval",
  "mapEntries",
  "curatorRoute",
]);
const approvalFields = new Set(["approvedBy", "approvedOn"]);
const mapEntryFields = new Set([
  "id",
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
const canonicalIdPattern = /^AH-[A-Z0-9]+(?:-[A-Z0-9]+)*$/u;
const isoDatePattern = /^\d{4}-\d{2}-\d{2}$/u;
const archiveRoomHrefPattern = /^\/archive\/(?:[a-z0-9]+(?:-[a-z0-9]+)*\/)*$/u;

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const assertObject = (value, label) => {
  assert(
    value && typeof value === "object" && !Array.isArray(value),
    `${label} must be an object.`,
  );
};

const assertKnownFields = (value, fields, label) => {
  assertObject(value, label);
  const unknown = Object.keys(value).find((field) => !fields.has(field));
  assert(!unknown, `unrecognized ${label} field: ${unknown}`);
};

const assertNonEmptyString = (value, label) => {
  assert(typeof value === "string" && value.trim().length > 0, `${label} must be a non-empty string.`);
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
  assert(
    Number.isFinite(value) && value >= minimum && value <= maximum,
    `${label} is outside the approved map geometry range.`,
  );
};

const validateMapEntry = (entry) => {
  assertKnownFields(entry, mapEntryFields, "map entry");
  assert(
    typeof entry.id === "string" && canonicalIdPattern.test(entry.id),
    `map entry has invalid canonical id: ${entry.id}`,
  );
  assertKnownFields(entry.mapRegion, mapRegionFields, "map region");
  assertFiniteRange(entry.mapRegion.cx, 0, 1539, "map geometry cx");
  assertFiniteRange(entry.mapRegion.cy, 0, 1152, "map geometry cy");
  assertFiniteRange(entry.mapRegion.r, Number.EPSILON, 1539, "map geometry radius");

  assertKnownFields(entry.mapLabel, mapLabelFields, "map label");
  assertFiniteRange(entry.mapLabel.x, 0, 1539, "map geometry label x");
  assertFiniteRange(entry.mapLabel.y, 0, 1152, "map geometry label y");
  assertFiniteRange(entry.mapLabel.width, Number.EPSILON, 1539, "map geometry label width");
  assertFiniteRange(entry.mapLabel.height, Number.EPSILON, 1152, "map geometry label height");
  assert(
    entry.mapLabel.x + entry.mapLabel.width <= 1539 &&
      entry.mapLabel.y + entry.mapLabel.height <= 1152,
    `map geometry label for ${entry.id} exceeds the map bounds.`,
  );

  if (entry.mapPosition !== undefined) {
    assertKnownFields(entry.mapPosition, mapPositionFields, "map position");
    assertFiniteRange(entry.mapPosition.x, 0, 100, "map position x");
    assertFiniteRange(entry.mapPosition.y, 0, 100, "map position y");
  }
};

const validateRouteStep = (step) => {
  const fields = step?.kind === "room" ? roomRouteFields : recordRouteFields;
  assertKnownFields(step, fields, "Curator Route step");
  assertNonEmptyString(step.id, "Curator Route step id");
  assertNonEmptyString(step.kind, "Curator Route step kind");
  assertNonEmptyString(step.label, "Curator Route label");
  assertNonEmptyString(step.note, "Curator Route note");

  if (step.kind === "record") {
    assert(
      canonicalIdPattern.test(step.id),
      `Curator Route record has invalid canonical id: ${step.id}`,
    );
    return;
  }

  assert(step.kind === "room" && step.id === "map-room", "Curator Route room step must be map-room.");
  assertNonEmptyString(step.title, "Curator Route room title");
  assert(
    typeof step.href === "string" && archiveRoomHrefPattern.test(step.href),
    "Curator Route room href must be a canonical Archive path.",
  );
};

export const validateArchivePresentationV2 = (presentation) => {
  assertKnownFields(presentation, rootFields, "archive presentation");
  assert(presentation.schemaVersion === 2, "archive presentation schemaVersion must be 2.");
  assertKnownFields(presentation.approval, approvalFields, "presentation approval");
  assert(
    presentation.approval.approvedBy === "author" &&
      isIsoDate(presentation.approval.approvedOn),
    "archive presentation requires a dated author approval.",
  );
  assert(Array.isArray(presentation.mapEntries), "archive presentation mapEntries must be an array.");
  assert(presentation.mapEntries.length === 30, "archive presentation requires exactly 30 map entries.");
  assert(Array.isArray(presentation.curatorRoute), "archive presentation curatorRoute must be an array.");
  assert(presentation.curatorRoute.length === 8, "archive presentation requires exactly eight Curator Route annotations.");

  const ids = new Set();
  for (const entry of presentation.mapEntries) {
    validateMapEntry(entry);
    assert(!ids.has(entry.id), `duplicate map entry id: ${entry.id}`);
    ids.add(entry.id);
  }

  const routeIds = new Set();
  for (const step of presentation.curatorRoute) {
    validateRouteStep(step);
    assert(!routeIds.has(step.id), `duplicate Curator Route step id: ${step.id}`);
    routeIds.add(step.id);
  }

  return presentation;
};
