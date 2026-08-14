# Change Log — Editorial QA & Orchestration

## 0.1.0 — 2026-08-14

Status: draft for editorial-owner review.

- Bound `01_SPECIFICATION.md` to `MWM-EQA-SPEC` v0.1.0-draft; source hash is recorded in `package_manifest.json`.
- Added 33 machine-readable orchestration rules for envelope/preconditions, authority, dependency graphs, route safety, family boundaries, comparison, confidence, human gates, receipts, regression, security, exceptions, and release.
- Added 14 explicit MWM decision hooks for stages, precedence, ownership, routes, confidentiality, thresholds, independent review, formats, blocking, proof/status, fixity, regression, reports, and appeals.
- Added schemas for invocation envelopes, dependency nodes, route decisions, family results, typed findings, comparisons, confidence, receipts, provenance events, release packages, ledgers, outputs, and cross-family contracts.
- Added a 50-fixture synthetic evaluation set (`MWM-EQA-EVAL-2026-08`) with named critical cases, rule crosswalk, adversarial/negative controls, integration cases, and deterministic scorer.
- Added regression intake and production-failure capture for authority override, stale dependencies, unsafe routes, boundary drift, evidence/confidence failures, critical-score masking, receipt gaps, and release-control failures.

## Change policy

Any specification, family interface, rule, exception, dependency, model/tool route, parser, format, release-policy, production-failure, or appeal change requires impact assessment, fixture regression, failure review, approval, and a first-production-run receipt. Material history is append-only.

## 2026-08-14 packaging update

- Added `01_SPECIFICATION.docx` as a source-preserving Word version of the governing specification. The Markdown specification remains the design authority; no editorial rule or open MWM decision was changed.
