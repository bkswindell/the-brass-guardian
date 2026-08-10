const rootFields = new Set(["schemaVersion", "entries"]);
const entryFields = new Set([
  "id",
  "projectionHash",
  "approvedBy",
  "approvedOn",
  "publicationDate",
]);

const canonicalIdPattern = /^AH-[A-Z0-9]+(?:-[A-Z0-9]+)*$/u;
const projectionHashPattern = /^sha256:[a-f0-9]{64}$/u;
const isoDatePattern = /^\d{4}-\d{2}-\d{2}$/u;

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const assertObject = (value, label) => {
  assert(
    value && typeof value === "object" && !Array.isArray(value),
    `${label} must be an object.`,
  );
};

const assertKnownFields = (value, allowed, label) => {
  assertObject(value, label);
  const unknown = Object.keys(value).find((field) => !allowed.has(field));
  assert(!unknown, `${label} contains an unrecognized field: ${unknown}`);
};

const isIsoDate = (value) => {
  if (typeof value !== "string" || !isoDatePattern.test(value)) return false;
  const [year, month, day] = value.split("-").map(Number);
  const candidate = new Date(Date.UTC(year, month - 1, day));
  return (
    candidate.getUTCFullYear() === year &&
    candidate.getUTCMonth() === month - 1 &&
    candidate.getUTCDate() === day
  );
};

export const validatePublicationLedgerV2 = (ledger) => {
  assertKnownFields(ledger, rootFields, "publication ledger");
  assert(ledger.schemaVersion === 2, "publication ledger schemaVersion must be 2.");
  assert(Array.isArray(ledger.entries), "publication ledger entries must be an array.");

  const ids = new Set();
  for (const entry of ledger.entries) {
    assertKnownFields(entry, entryFields, "publication ledger entry");
    assert(
      typeof entry.id === "string" && canonicalIdPattern.test(entry.id),
      `invalid canonical publication id: ${entry.id}`,
    );
    assert(!ids.has(entry.id), `duplicate publication ledger id: ${entry.id}`);
    ids.add(entry.id);
    assert(
      typeof entry.projectionHash === "string" &&
        projectionHashPattern.test(entry.projectionHash),
      `${entry.id}: invalid projectionHash.`,
    );
    assert(entry.approvedBy === "author", `${entry.id}: approvedBy must be author.`);
    assert(isIsoDate(entry.approvedOn), `${entry.id}: approvedOn must be YYYY-MM-DD.`);
    assert(
      isIsoDate(entry.publicationDate),
      `${entry.id}: publicationDate must be YYYY-MM-DD.`,
    );
  }

  return ledger;
};

export const publicationApprovalMap = (ledger) =>
  new Map(validatePublicationLedgerV2(ledger).entries.map((entry) => [entry.id, entry]));
