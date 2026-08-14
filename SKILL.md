---
name: editorial-qa-orchestration
description: Coordinate the bounded MWM editorial Skill families through a versioned dependency graph and state machine. Use for intake/stage classification, authority and rule resolution, dependency planning, model and tool routing, independent-review comparison, confidence and residual-risk aggregation, human escalation and decision receipts, evaluation/regression, provenance, and release orchestration. Do not use to replace family-specific judgments, invent policy, override human authority, adjudicate misconduct/authorship/legal/ethical status, silently rewrite content, or release without a retained authorization receipt.
---

# Editorial QA & Orchestration

Use this family as the control layer for the bounded editorial Skill packages. The orchestrator supplies context, dependencies, routing, comparison, escalation, provenance, evaluation, and release controls; RCI, SGI, TE, CE, SEI, CPR, and PPR retain their domain judgments. Use a versioned dependency graph plus state machine, never a flat checklist or mega-prompt.

## Executable workflow

1. Create an immutable invocation envelope with run/chapter/stage/purpose, input artifact IDs and fixity, authority/rule versions, risk/sensitivity profile, requested outputs, human owner, confidentiality route, and orchestrator version.
2. Classify stage and purpose. A filename or user request may suggest a provisional stage, but release or post-publication stages require owner confirmation when ambiguity matters.
3. Resolve authority, rule, exception, effective-date, and supersession context. If precedence or scope is materially conflicted, return `awaiting_human`; never use model preference, source order, or majority vote to settle policy.
4. Build the dependency graph. Each node has Skill/spec/rule versions, preconditions, input IDs, expected output schema, failure states, consumers, and eligibility. Do not reuse a stale family result from a changed baseline, rule, source bundle, route, model, or specification.
5. Check confidentiality and route approval. Choose deterministic validators/parsers for identity, schemas, counts, links, hashes, and structured presence; specialist routes for bounded family work; independent review for high-risk/disagreement-sensitive cases; and human routes for authority, substantive, integrity, rights, privacy, status, and critical release decisions.
6. Run eligible family Skills in parallel only when dependencies permit and the expected interaction is preserved. Do not use parallelism to conceal conflict. Preserve each family boundary, schema, status, owner, and coverage statement.
7. Normalize typed outputs and compare independent findings using stable issue keys (family, location, observed object, issue class). Classify agreement, partial agreement, distinct issues, one-sided signals, and contradiction. Preserve both source reports and disagreement evidence.
8. Aggregate confidence and residual risk from evidence completeness/directness, source access, agreement, rule clarity, input quality, consequence, reversibility, route stability, and known failure patterns. Confidence never substitutes for authority or missing evidence; high-risk low-confidence issues escalate.
9. Create a bounded human decision packet containing question, options, excerpt/asset, rule, competing findings, evidence, risk, proposed action, deadline, and authorization effect. Append the owner response to an immutable decision receipt; do not erase the original evidence.
10. Rerun affected downstream nodes after material changes. Record append-only provenance/fixity events for inputs, activities, agents, rules, tools, model routes, outputs, decisions, supersession, and residual risk.
11. Run evaluation/regression when a spec, family interface, rule, exception, model/tool route, parser, format, release policy, production failure, or appeal changes. A passing aggregate score never overrides a critical fixture failure.
12. Reconcile family statuses, open items, proof state, output-format coverage, accessibility scope, provenance/fixity, and human authorization. Return `ready`, `ready_with_tracked_items`, `hold`, `blocked`, `post_publication_case`, or an awaiting state. No release package exists without a retained receipt and named authority.

## Skill routing

- `EQA-01`: intake, stage, purpose, input inventory, missing inputs, risk, owner, confirmation.
- `EQA-02`: authority/rule/exception resolution with conflicts and effective versions.
- `EQA-03`: dependency graph, preconditions, gates, stale-output detection, deferred nodes.
- `EQA-04`: deterministic/specialist/independent/human route approval and confidentiality.
- `EQA-05`: independent comparison by stable issue key; preserve disagreement.
- `EQA-06`: categorical confidence, evidence completeness, uncertainty reason, residual risk.
- `EQA-07`: human escalation, bounded decision packet, append-only receipt.
- `EQA-08`: evaluation, regression, drift, coverage, and critical-fixture override.
- `EQA-09`: append-only editorial decision log, provenance, fixity, status history, supersession.
- `EQA-10`: release checklist, hold, post-publication case, release package, authorization.

## Default graph

`EQA-01 -> EQA-02 + EQA-06 -> EQA-03 -> EQA-04 -> (RCI, SGI, TE, CE, SEI) -> CPR -> PPR -> EQA-05 + EQA-07 -> EQA-08 + EQA-09 -> EQA-10`. Serialization may be stricter by chapter type only through a versioned dependency decision. CPR and PPR are not substitutes for the family reports they consume.

## Status and gates

Run states are `intake`, `planned`, `running`, `awaiting_human`, `awaiting_input`, `awaiting_reproof`, `ready_with_tracked_items`, `hold`, `released`, `post_publication_case`, and `blocked`. A signal is not a finding; an approved variation is not an error; a status issue is not copyediting. Critical blocks cannot be averaged away. `ready_with_tracked_items` requires an allowed residual-risk policy, owner, due action, and receipt.

## Safety boundaries

Do not invent MWM precedence, requirements, owners, metadata, evidence, confidence, route approval, or release authority. Do not let a model/tool/aggregate score override an explicit rule or human decision. Do not convert signals into misconduct, authorship, legal, ethical, privacy, or status findings. Do not silently overwrite baselines, decision records, or released artifacts. Do not generalize accessibility or file-integrity checks beyond tested format/scope. Minimize protected excerpts, block unapproved processing, and treat route denial or suspected disclosure as human escalation.

Invocation: $editorial-qa-orchestration