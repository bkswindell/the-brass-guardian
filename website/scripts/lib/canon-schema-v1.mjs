const recordTypes = new Set([
  "character",
  "location",
  "organization",
  "artifact",
  "vessel",
  "historical_event",
  "story",
  "story_arc",
]);

const disclosureLevels = new Set([
  "public",
  "teaser",
  "story-sensitive",
  "creator-only",
]);
const canonStatuses = new Set(["canonical", "proposed", "superseded"]);
const developmentStatuses = new Set([
  "complete",
  "working",
  "placeholder",
  "concept",
]);
const temporalRelevance = new Set([
  "none",
  "low",
  "moderate",
  "high",
  "very-high",
  "critical",
  "unresolved",
]);
const cartographyCategories = new Set(["numbered", "restricted", "unlisted"]);
const chronologyStatuses = new Set([
  "exact",
  "approximate",
  "range",
  "relative",
  "disputed",
  "unknown",
  "anomalous",
]);
const chronologyCertainty = new Set([
  "confirmed",
  "probable",
  "disputed",
  "unknown",
]);
const archiveSections = new Set(["catalog", "hidden"]);
const publicClassifications = new Set(["public", "teaser"]);

const kebabCase = /^[a-z0-9]+(?:-[a-z0-9]+)*$/u;
const canonicalId = /^[A-Z0-9]+(?:-[A-Z0-9]+)*$/u;
const isoDate = /^\d{4}-\d{2}-\d{2}$/u;

const topLevelFields = new Set([
  "schema_version",
  "id",
  "record_type",
  "name",
  "slug",
  "aliases",
  "last_updated",
  "canon",
  "development",
  "disclosure",
  "subtype",
  "descriptor",
  "provenance",
  "relationships",
  "assets",
  "cartography",
  "chronology",
  "public_projection",
  "character",
  "location",
  "organization",
  "artifact",
  "historical_event",
  "story",
  "vessel",
  "production",
]);

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const assertObject = (value, label) => {
  assert(value && typeof value === "object" && !Array.isArray(value), `${label} must be an object.`);
};

const assertKnownFields = (object, allowed, label) => {
  assertObject(object, label);
  const unknown = Object.keys(object).find((key) => !allowed.has(key));
  assert(!unknown, `${label} contains unknown field: ${unknown}`);
};

const assertNonEmptyString = (value, label) => {
  assert(typeof value === "string" && value.trim().length > 0, `${label} must be a non-empty string.`);
};

const assertStringArray = (value, label, { allowEmpty = true } = {}) => {
  assert(Array.isArray(value), `${label} must be an array.`);
  if (!allowEmpty) assert(value.length > 0, `${label} must not be empty.`);
  value.forEach((entry, index) => assertNonEmptyString(entry, `${label}[${index}]`));
};

const assertUniqueStrings = (value, label) => {
  assertStringArray(value, label);
  assert(new Set(value).size === value.length, `${label} must contain unique values.`);
};

const isValidIsoDate = (value) => {
  if (typeof value !== "string" || !isoDate.test(value)) return false;
  const [year, month, day] = value.split("-").map(Number);
  const date = new Date(Date.UTC(year, month - 1, day));
  return (
    date.getUTCFullYear() === year &&
    date.getUTCMonth() === month - 1 &&
    date.getUTCDate() === day
  );
};

const assertKebab = (value, label) => {
  assertNonEmptyString(value, label);
  assert(kebabCase.test(value), `${label} must be lowercase kebab-case.`);
};

const assertCanonicalId = (value, label) => {
  assertNonEmptyString(value, label);
  assert(canonicalId.test(value), `${label} must use the canonical uppercase/hyphen ID form.`);
};

const validateCanon = (value, id) => {
  const fields = new Set(["status", "scope"]);
  assertKnownFields(value, fields, `${id}.canon`);
  assert(canonStatuses.has(value.status), `${id}.canon.status is invalid.`);
  assertStringArray(value.scope, `${id}.canon.scope`);
  value.scope.forEach((entry, index) => assertKebab(entry, `${id}.canon.scope[${index}]`));
  if (value.status !== "proposed") {
    assert(value.scope.length > 0, `${id}.canon.scope must not be empty for active or superseded canon.`);
  }
};

const validateDevelopment = (value, id) => {
  const fields = new Set(["status", "temporal_relevance"]);
  assertKnownFields(value, fields, `${id}.development`);
  assert(developmentStatuses.has(value.status), `${id}.development.status is invalid.`);
  if (value.temporal_relevance !== undefined) {
    assert(temporalRelevance.has(value.temporal_relevance), `${id}.development.temporal_relevance is invalid.`);
  }
};

const validateDisclosure = (value, id) => {
  const fields = new Set(["level"]);
  assertKnownFields(value, fields, `${id}.disclosure`);
  assert(disclosureLevels.has(value.level), `${id}.disclosure.level is invalid.`);
};

const validateProvenance = (value, id) => {
  const fields = new Set(["sources"]);
  assertKnownFields(value, fields, `${id}.provenance`);
  assert(Array.isArray(value.sources), `${id}.provenance.sources must be an array.`);
  value.sources.forEach((source, index) => {
    const sourceFields = new Set(["kind", "ref", "note"]);
    assertKnownFields(source, sourceFields, `${id}.provenance.sources[${index}]`);
    assertKebab(source.kind, `${id}.provenance.sources[${index}].kind`);
    assertNonEmptyString(source.ref, `${id}.provenance.sources[${index}].ref`);
    if (source.note !== undefined) assertNonEmptyString(source.note, `${id}.provenance.sources[${index}].note`);
  });
};

const validateRelationships = (value, id) => {
  assert(Array.isArray(value), `${id}.relationships must be an array.`);
  const pairs = new Set();
  value.forEach((relationship, index) => {
    const fields = new Set(["target", "type", "visibility", "note"]);
    assertKnownFields(relationship, fields, `${id}.relationships[${index}]`);
    assertCanonicalId(relationship.target, `${id}.relationships[${index}].target`);
    assertKebab(relationship.type, `${id}.relationships[${index}].type`);
    assert(disclosureLevels.has(relationship.visibility), `${id}.relationships[${index}].visibility is invalid.`);
    if (relationship.note !== undefined) assertNonEmptyString(relationship.note, `${id}.relationships[${index}].note`);
    const pair = `${relationship.target}|${relationship.type}`;
    assert(!pairs.has(pair), `${id}.relationships contains duplicate target/type pair: ${pair}`);
    pairs.add(pair);
  });
};

const validateAssets = (value, id) => {
  assert(Array.isArray(value), `${id}.assets must be an array.`);
  const ids = new Set();
  value.forEach((asset, index) => {
    const fields = new Set(["id", "path", "role", "visibility", "alt", "caption", "placement"]);
    assertKnownFields(asset, fields, `${id}.assets[${index}]`);
    assertKebab(asset.id, `${id}.assets[${index}].id`);
    assert(!ids.has(asset.id), `${id}.assets contains duplicate asset id: ${asset.id}`);
    ids.add(asset.id);
    assertNonEmptyString(asset.path, `${id}.assets[${index}].path`);
    assert(!asset.path.startsWith("/") && !asset.path.includes("\\") && !asset.path.split("/").includes(".."), `${id}.assets[${index}].path must be repository-relative and traversal-safe.`);
    assert(!asset.path.split("/").includes("unused"), `${id}.assets[${index}].path must not reference unused/.`);
    assertKebab(asset.role, `${id}.assets[${index}].role`);
    assert(disclosureLevels.has(asset.visibility), `${id}.assets[${index}].visibility is invalid.`);
    assertNonEmptyString(asset.alt, `${id}.assets[${index}].alt`);
    if (asset.caption !== undefined) assertNonEmptyString(asset.caption, `${id}.assets[${index}].caption`);
    if (asset.placement !== undefined) assertNonEmptyString(asset.placement, `${id}.assets[${index}].placement`);
  });
};

const validateCartography = (value, id) => {
  assert(Array.isArray(value), `${id}.cartography must be an array.`);
  value.forEach((entry, index) => {
    const fields = new Set(["map_id", "category", "reference", "parent_reference"]);
    assertKnownFields(entry, fields, `${id}.cartography[${index}]`);
    assertKebab(entry.map_id, `${id}.cartography[${index}].map_id`);
    assert(cartographyCategories.has(entry.category), `${id}.cartography[${index}].category is invalid.`);
    if (entry.category === "unlisted") {
      assert(entry.reference === undefined, `${id}.cartography[${index}].reference must be omitted for unlisted records.`);
    } else {
      assertNonEmptyString(entry.reference, `${id}.cartography[${index}].reference`);
    }
    if (entry.parent_reference !== undefined) assertNonEmptyString(entry.parent_reference, `${id}.cartography[${index}].parent_reference`);
  });
};

const validateChronology = (value, id) => {
  const fields = new Set(["status", "display", "sort_key", "accounts", "note"]);
  assertKnownFields(value, fields, `${id}.chronology`);
  assert(chronologyStatuses.has(value.status), `${id}.chronology.status is invalid.`);
  assertNonEmptyString(value.display, `${id}.chronology.display`);
  if (value.sort_key !== undefined) assert(Number.isInteger(value.sort_key), `${id}.chronology.sort_key must be an integer.`);
  if (value.note !== undefined) assertNonEmptyString(value.note, `${id}.chronology.note`);
  if (value.accounts !== undefined) {
    assert(Array.isArray(value.accounts), `${id}.chronology.accounts must be an array.`);
    value.accounts.forEach((account, index) => {
      const accountFields = new Set(["label", "value", "certainty", "note"]);
      assertKnownFields(account, accountFields, `${id}.chronology.accounts[${index}]`);
      assertNonEmptyString(account.label, `${id}.chronology.accounts[${index}].label`);
      assertNonEmptyString(account.value, `${id}.chronology.accounts[${index}].value`);
      assert(chronologyCertainty.has(account.certainty), `${id}.chronology.accounts[${index}].certainty is invalid.`);
      if (account.note !== undefined) assertNonEmptyString(account.note, `${id}.chronology.accounts[${index}].note`);
    });
  }
};

const validateCharacter = (value, id) => {
  const fields = new Set(["titles", "age_status", "public_identity", "former_roles", "current_roles"]);
  assertKnownFields(value, fields, `${id}.character`);
  if (value.titles !== undefined) assertStringArray(value.titles, `${id}.character.titles`);
  if (value.age_status !== undefined) assertNonEmptyString(value.age_status, `${id}.character.age_status`);
  if (value.public_identity !== undefined) assertNonEmptyString(value.public_identity, `${id}.character.public_identity`);
  if (value.former_roles !== undefined) assertStringArray(value.former_roles, `${id}.character.former_roles`);
  if (value.current_roles !== undefined) assertStringArray(value.current_roles, `${id}.character.current_roles`);
};

const validateLocation = (value, id) => {
  const fields = new Set(["jurisdiction", "access_status"]);
  assertKnownFields(value, fields, `${id}.location`);
  if (value.jurisdiction !== undefined) assertStringArray(value.jurisdiction, `${id}.location.jurisdiction`);
  if (value.access_status !== undefined) assertStringArray(value.access_status, `${id}.location.access_status`);
};

const validateOrganization = (value, id) => {
  const fields = new Set(["jurisdiction", "access_classes"]);
  assertKnownFields(value, fields, `${id}.organization`);
  if (value.jurisdiction !== undefined) assertStringArray(value.jurisdiction, `${id}.organization.jurisdiction`);
  if (value.access_classes !== undefined) assertStringArray(value.access_classes, `${id}.organization.access_classes`);
};

const validateArtifact = (value, id) => {
  const fields = new Set(["category", "catalog_number"]);
  assertKnownFields(value, fields, `${id}.artifact`);
  if (value.category !== undefined) assertNonEmptyString(value.category, `${id}.artifact.category`);
  if (value.catalog_number !== undefined) assertNonEmptyString(value.catalog_number, `${id}.artifact.catalog_number`);
};

const validateHistoricalEvent = (value, id) => {
  const fields = new Set(["public_record_status", "restricted_record_status"]);
  assertKnownFields(value, fields, `${id}.historical_event`);
  if (value.public_record_status !== undefined) assertNonEmptyString(value.public_record_status, `${id}.historical_event.public_record_status`);
  if (value.restricted_record_status !== undefined) assertNonEmptyString(value.restricted_record_status, `${id}.historical_event.restricted_record_status`);
};

const validateStory = (value, id) => {
  const fields = new Set(["subtitle", "title_status", "proposed_book", "proposed_placement"]);
  assertKnownFields(value, fields, `${id}.story`);
  for (const field of ["subtitle", "title_status", "proposed_book"]) {
    if (value[field] !== undefined) assertNonEmptyString(value[field], `${id}.story.${field}`);
  }
  if (value.proposed_placement !== undefined) assertStringArray(value.proposed_placement, `${id}.story.proposed_placement`);
};

const validateVessel = (value, id) => {
  const fields = new Set(["class", "status"]);
  assertKnownFields(value, fields, `${id}.vessel`);
  if (value.class !== undefined) assertKebab(value.class, `${id}.vessel.class`);
  if (value.status !== undefined) assertKebab(value.status, `${id}.vessel.status`);
};

const validateProduction = (value, id) => {
  const fields = new Set(["slate_number", "image_status", "visual_transcription_status"]);
  assertKnownFields(value, fields, `${id}.production`);
  if (value.slate_number !== undefined) assert(Number.isInteger(value.slate_number), `${id}.production.slate_number must be an integer.`);
  if (value.image_status !== undefined) assertNonEmptyString(value.image_status, `${id}.production.image_status`);
  if (value.visual_transcription_status !== undefined) assertNonEmptyString(value.visual_transcription_status, `${id}.production.visual_transcription_status`);
};

const validatePublicProjection = (value, record) => {
  const id = record.id;
  const fields = new Set(["title", "summary", "classification", "archive_section", "access_label", "tags", "related", "image"]);
  assertKnownFields(value, fields, `${id}.public_projection`);
  assertNonEmptyString(value.title, `${id}.public_projection.title`);
  assertNonEmptyString(value.summary, `${id}.public_projection.summary`);
  assert(publicClassifications.has(value.classification), `${id}.public_projection.classification is invalid.`);
  assert(archiveSections.has(value.archive_section), `${id}.public_projection.archive_section is invalid.`);
  assertNonEmptyString(value.access_label, `${id}.public_projection.access_label`);
  assert(value.access_label.length <= 40, `${id}.public_projection.access_label must be 40 characters or fewer.`);
  assertUniqueStrings(value.tags, `${id}.public_projection.tags`);
  assertUniqueStrings(value.related, `${id}.public_projection.related`);
  value.related.forEach((target, index) => assertCanonicalId(target, `${id}.public_projection.related[${index}]`));

  const relationships = record.relationships ?? [];
  for (const target of value.related) {
    const safeRelationship = relationships.find(
      (relationship) =>
        relationship.target === target &&
        (relationship.visibility === "public" || relationship.visibility === "teaser"),
    );
    assert(safeRelationship, `${id}.public_projection.related target ${target} is not backed by a public/teaser relationship.`);
  }

  if (value.image !== undefined) {
    const imageFields = new Set(["asset", "alt"]);
    assertKnownFields(value.image, imageFields, `${id}.public_projection.image`);
    assertKebab(value.image.asset, `${id}.public_projection.image.asset`);
    if (value.image.alt !== undefined) assertNonEmptyString(value.image.alt, `${id}.public_projection.image.alt`);
    const asset = (record.assets ?? []).find((candidate) => candidate.id === value.image.asset);
    assert(asset, `${id}.public_projection.image references unknown asset: ${value.image.asset}`);
    assert(asset.visibility === "public" || asset.visibility === "teaser", `${id}.public_projection.image asset is not public/teaser.`);
  }
};

const typeExtensionFields = {
  character: "character",
  location: "location",
  organization: "organization",
  artifact: "artifact",
  historical_event: "historical_event",
  story: "story",
  vessel: "vessel",
  story_arc: null,
};

export const validateCanonRecord = (record) => {
  assertObject(record, "record");
  const unknown = Object.keys(record).find((key) => !topLevelFields.has(key));
  assert(!unknown, `record contains unknown top-level field: ${unknown}`);

  assert(record.schema_version === 1, `schema_version must be 1.`);
  assertCanonicalId(record.id, "id");
  assert(recordTypes.has(record.record_type), `${record.id}.record_type is invalid.`);
  assertNonEmptyString(record.name, `${record.id}.name`);
  assertKebab(record.slug, `${record.id}.slug`);
  assertStringArray(record.aliases, `${record.id}.aliases`);
  assert(isValidIsoDate(record.last_updated), `${record.id}.last_updated must be a valid YYYY-MM-DD date.`);
  validateCanon(record.canon, record.id);
  validateDevelopment(record.development, record.id);
  validateDisclosure(record.disclosure, record.id);

  if (record.subtype !== undefined) assertKebab(record.subtype, `${record.id}.subtype`);
  if (record.descriptor !== undefined) assertNonEmptyString(record.descriptor, `${record.id}.descriptor`);
  if (record.provenance !== undefined) validateProvenance(record.provenance, record.id);
  if (record.relationships !== undefined) validateRelationships(record.relationships, record.id);
  if (record.assets !== undefined) validateAssets(record.assets, record.id);
  if (record.cartography !== undefined) validateCartography(record.cartography, record.id);
  if (record.chronology !== undefined) validateChronology(record.chronology, record.id);
  if (record.production !== undefined) validateProduction(record.production, record.id);

  const validators = {
    character: validateCharacter,
    location: validateLocation,
    organization: validateOrganization,
    artifact: validateArtifact,
    historical_event: validateHistoricalEvent,
    story: validateStory,
    vessel: validateVessel,
  };
  const expectedExtension = typeExtensionFields[record.record_type];
  for (const field of ["character", "location", "organization", "artifact", "historical_event", "story", "vessel"]) {
    if (record[field] !== undefined) {
      assert(field === expectedExtension, `${record.id}.${field} is not valid for record_type ${record.record_type}.`);
      validators[field](record[field], record.id);
    }
  }

  if (record.public_projection !== undefined) validatePublicProjection(record.public_projection, record);
  return record;
};

export const validateCanonRecords = (records) => {
  assert(Array.isArray(records), "records must be an array.");
  const byId = new Map();
  const bySlug = new Map();

  for (const record of records) {
    validateCanonRecord(record);
    assert(!byId.has(record.id), `duplicate canonical id: ${record.id}`);
    assert(!bySlug.has(record.slug), `duplicate canonical slug: ${record.slug}`);
    byId.set(record.id, record);
    bySlug.set(record.slug, record);
  }

  const mapReferences = new Set();
  for (const record of records) {
    for (const relationship of record.relationships ?? []) {
      assert(byId.has(relationship.target), `${record.id} relationship target does not exist: ${relationship.target}`);
    }
    for (const target of record.public_projection?.related ?? []) {
      assert(byId.has(target), `${record.id} public related target does not exist: ${target}`);
    }
    for (const entry of record.cartography ?? []) {
      if (entry.map_id === "aetherhaven-city" && entry.category !== "unlisted") {
        const key = `${entry.map_id}|${entry.reference}`;
        assert(!mapReferences.has(key), `duplicate map reference: ${key}`);
        mapReferences.add(key);
      }
    }
  }

  return records;
};

export const schemaV1Constants = Object.freeze({
  recordTypes: [...recordTypes],
  disclosureLevels: [...disclosureLevels],
  canonStatuses: [...canonStatuses],
  developmentStatuses: [...developmentStatuses],
  chronologyStatuses: [...chronologyStatuses],
});