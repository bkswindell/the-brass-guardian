# Aetherhaven Schema Change Proposal

**Proposal status:** PROPOSED  
**Current schema version:**  
**Proposed schema version:**  
**Requested by:**  
**Date:**  

> Use this template for any material change to `docs/standards/AETHERHAVEN_CONTENT_SCHEMA.md` after the schema is locked. Do not implement an accepted schema change until the author has explicitly approved it.

## 1. Problem

What cannot be represented safely, accurately, or maintainably with the current schema?

## 2. Why the Existing Model Is Insufficient

Identify the exact existing fields, record types, relationships, or ownership boundaries that fail to meet the requirement.

Explain why a local website adapter, presentation configuration, derived field, or one-off transformation is not sufficient.

## 3. Proposed Change

Describe the proposed schema modification precisely.

Include:

- fields added, removed, renamed, or reinterpreted;
- record types or subtypes affected;
- enum changes;
- relationship changes;
- asset or chronology changes;
- validation behavior;
- default behavior, if any.

## 4. Ownership Classification

For each new or changed property, classify its owner:

- Canon content
- Publication approval
- Derived data
- Website/presentation configuration

Explain why the property belongs there.

## 5. Alternatives Considered

List reasonable alternatives, especially options that avoid changing the schema.

For each alternative, explain why it was rejected.

## 6. Semantic Version Impact

Proposed classification:

- [ ] PATCH — documentation/clarification only
- [ ] MINOR — backward-compatible additive change
- [ ] MAJOR — breaking structural or semantic change

Explain the classification.

## 7. Record Types Affected

- [ ] Character
- [ ] Location
- [ ] Organization
- [ ] Artifact
- [ ] Vessel
- [ ] Historical event
- [ ] Story draft
- [ ] Story arc
- [ ] Placeholder profile
- [ ] Other:

## 8. Estimated Migration Scope

Estimated files affected:

Known directories affected:

Any records requiring manual review:

Any records that can be migrated deterministically:

## 9. Website Impact

Identify affected:

- Astro content ingestion;
- route generation;
- Archive catalog/search;
- Hidden Archives;
- Map Room;
- Curator's Route;
- related-record rendering;
- SEO/sharing metadata;
- asset pipeline;
- build verification;
- tests;
- other consumers.

## 10. Publication / Spoiler Impact

Does this change affect:

- public-safe projections;
- teaser/restricted classifications;
- author approval behavior;
- publication fingerprints/hashes;
- fail-closed production behavior;
- creator-only data isolation?

Describe the risk and mitigation.

## 11. Validation Changes

List validators, schemas, CI checks, or tests that must change.

## 12. Migration Plan

Provide the exact sequence:

1. update the governing schema;
2. update validators;
3. update templates;
4. migrate affected metadata;
5. flag substantive canon questions;
6. update website ingestion/adapters;
7. run repository-wide validation;
8. verify publication isolation;
9. audit representative records;
10. document completion.

## 13. Rollback Plan

How can the repository return to the previous schema version if the migration fails or produces unexpected semantic changes?

## 14. Risks

Include risks of:

- information loss;
- accidental canon reinterpretation;
- publication leakage;
- broken cross-links;
- duplicate identities;
- stale derived indexes;
- mixed schema versions;
- website regression.

## 15. Author Decision

**Status:** PROPOSED

- [ ] APPROVED
- [ ] REJECTED
- [ ] REVISE AND RESUBMIT

**Author approval date:**  
**Approved scope / conditions:**  

Do not mark this proposal APPROVED unless the author explicitly approves the change.