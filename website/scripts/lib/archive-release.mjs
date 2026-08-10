const allowedFields = new Set([
  "schemaVersion",
  "status",
  "approvedBy",
  "approvedOn",
  "includeHiddenArchives",
]);

const isoDatePattern = /^\d{4}-\d{2}-\d{2}$/;

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

export const validateArchiveRelease = (release) => {
  if (release?.schemaVersion !== 1) {
    throw new Error("archive release schemaVersion must be 1.");
  }

  const unknownField = Object.keys(release).find(
    (field) => !allowedFields.has(field),
  );
  if (unknownField) {
    throw new Error(`unrecognized archive release field: ${unknownField}`);
  }
  if (!["sealed", "published"].includes(release.status)) {
    throw new Error("archive release status must be sealed or published.");
  }
  if (release.approvedBy !== "author" || !isIsoDate(release.approvedOn)) {
    throw new Error("archive release requires a dated author approval.");
  }
  if (typeof release.includeHiddenArchives !== "boolean") {
    throw new Error("archive release includeHiddenArchives must be boolean.");
  }

  return release;
};
