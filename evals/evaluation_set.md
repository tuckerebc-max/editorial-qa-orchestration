# MWM-EQA-EVAL-2026-08

This synthetic evaluation set tests the Editorial QA & Orchestration specification at v0.1.0. It contains 50 fixtures: 8 clean, 16 single-error, 14 adversarial, 6 negative controls, and 6 integration cases.

The named critical cases include EQA-11 (high-risk numeric disagreement), EQA-17 (unregressed route change), EQA-19 (open critical proof query), EQA-25 (model override attempt), EQA-27 (aggregate score masking a critical block), EQA-36 (post-publication boundary), EQA-43 (format-limited coverage), EQA-46 (stale dependency output), and EQA-50 (full release receipt).

Acceptance requirements:

- Required-envelope and dependency preconditions are detected without false clearance.
- Authority conflicts, route denials, high-risk disagreement, and human gates remain explicit.
- Family boundaries and typed outputs are preserved.
- Disagreement evidence and source reports survive comparison.
- Confidence includes an evidence basis and does not compensate for missing evidence.
- Critical blocks override aggregate scores.
- Material decisions have append-only provenance, fixity, supersession, and receipts.
- Accessibility coverage is format- and scope-specific.
- Post-publication matters remain separate cases.
- Material spec/interface/rule/route/format/failure changes trigger regression.
- A release package cannot be created without acceptable family statuses, fixity, residual-risk disposition, named authority, and receipt.
