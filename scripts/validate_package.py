#!/usr/bin/env python3
"""Structural and policy validator for the MWM EQA package."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SPEC_SHA256 = "DA00567892A41E8ABB4EF441A43D696F89A3754FF88A19C8856D8EF6703A54C0"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []
    spec = ROOT / "01_SPECIFICATION.md"
    if not spec.exists():
        errors.append("missing 01_SPECIFICATION.md")
    else:
        digest = hashlib.sha256(spec.read_bytes()).hexdigest().upper()
        if digest != SPEC_SHA256:
            errors.append(f"specification hash mismatch: {digest}")
    skill = ROOT / "SKILL.md"
    if not skill.exists():
        errors.append("missing SKILL.md")
    else:
        text = skill.read_text(encoding="ascii")
        if len(text.splitlines()) > 500:
            errors.append("SKILL.md exceeds 500 lines")
        if not re.search(r"^name:\s*editorial-qa-orchestration\s*$", text, re.MULTILINE):
            errors.append("SKILL.md frontmatter name missing")
        if not re.search(r"^description:\s*\S+", text, re.MULTILINE):
            errors.append("SKILL.md frontmatter description missing")
        if any(token in text for token in ("TODO", "TBD", "FIXME")):
            errors.append("SKILL.md contains unfinished marker")
        if "$editorial-qa-orchestration" not in text:
            warnings.append("SKILL.md invocation token not explicit")
    agent = ROOT / "agents" / "openai.yaml"
    if not agent.exists():
        errors.append("missing agents/openai.yaml")
    else:
        agent_text = agent.read_text(encoding="ascii")
        for marker in ("display_name:", "short_description:", "default_prompt:"):
            if marker not in agent_text:
                errors.append(f"agents/openai.yaml missing {marker}")
    required = [
        "01_SPECIFICATION.md","SKILL.md","agents/openai.yaml","package_manifest.json",
        "02_RULES/ruleset.json","02_RULES/decision_hooks.json","02_RULES/authority_registry.json","02_RULES/status_vocabulary.json","02_RULES/protected_inputs.json",
        "evals/fixture_contract.schema.json","evals/fixture_catalog.json","evals/rule_fixture_crosswalk.json","evals/adversarial_negative_controls.json","evals/integration_cases.json","evals/evaluation_set.md","evals/scorer.py","scripts/validate_package.py",
        "CHANGELOG_REGRESSION/CHANGELOG.md","CHANGELOG_REGRESSION/regression-intake.schema.json","CHANGELOG_REGRESSION/regression-intake.template.json","CHANGELOG_REGRESSION/production-failure.schema.json","CHANGELOG_REGRESSION/production-failure.template.json","CHANGELOG_REGRESSION/regression_policy.json"
    ]
    schema_names = ["invocation-envelope.schema.json","dependency-node.schema.json","route-decision.schema.json","family-result.schema.json","finding.schema.json","comparison.schema.json","confidence.schema.json","decision-receipt.schema.json","provenance-event.schema.json","release-package.schema.json","ledger.schema.json","output.schema.json","cross-family-contracts.json"]
    example_names = ["invocation-envelope.json","dependency-node.json","route-decision.json","family-result.json","finding.json","comparison.json","confidence.json","decision-receipt.json","provenance-event.json","release-package.json","ledger.json","output.json"]
    required.extend(f"schemas/{name}" for name in schema_names)
    required.extend(f"schemas/examples/{name}" for name in example_names)
    for relative in required:
        if not (ROOT / relative).exists():
            errors.append(f"missing {relative}")
    json_files = list(ROOT.rglob("*.json"))
    loaded: dict[str, Any] = {}
    for path in json_files:
        try:
            loaded[str(path.relative_to(ROOT)).replace("\\", "/")] = read_json(path)
        except Exception as exc:
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")
    ruleset = loaded.get("02_RULES/ruleset.json", {})
    hooks = loaded.get("02_RULES/decision_hooks.json", {})
    catalog = loaded.get("evals/fixture_catalog.json", {})
    crosswalk = loaded.get("evals/rule_fixture_crosswalk.json", {})
    controls = loaded.get("evals/adversarial_negative_controls.json", {})
    integrations = loaded.get("evals/integration_cases.json", {})
    rules = ruleset.get("rules", [])
    rule_ids = {rule.get("rule_id") for rule in rules}
    if ruleset.get("ruleset_id") != "MWM-EQA-RULES" or len(rules) != 33 or len(rule_ids) != 33:
        errors.append("expected MWM-EQA-RULES with 33 unique rules")
    if len(hooks.get("hooks", [])) != 14:
        errors.append("expected 14 decision hooks")
    fixtures = catalog.get("fixtures", [])
    fixture_ids = {item.get("fixture_id") for item in fixtures}
    if catalog.get("fixture_count") != 50 or len(fixtures) != 50 or len(fixture_ids) != 50:
        errors.append("expected 50 unique fixtures")
    counts: dict[str, int] = {}
    for item in fixtures:
        counts[item.get("kind")] = counts.get(item.get("kind"), 0) + 1
        if item.get("synthetic") is not True:
            errors.append(f"fixture {item.get('fixture_id')} is not synthetic")
        gold = item.get("gold", {})
        for key in ("expected_status","expected_rule_ids","expected_interventions","must_not_emit_rule_ids"):
            if key not in gold:
                errors.append(f"{item.get('fixture_id')} missing gold.{key}")
        for rule_id in gold.get("expected_rule_ids", []) + gold.get("must_not_emit_rule_ids", []):
            if rule_id not in rule_ids:
                errors.append(f"{item.get('fixture_id')} references unknown rule {rule_id}")
    if counts != {"clean":8,"single_error":16,"adversarial":14,"negative_control":6,"integration":6}:
        errors.append(f"fixture counts differ: {counts}")
    rows = crosswalk.get("rows", [])
    if len(rows) != 33 or {row.get("rule_id") for row in rows} != rule_ids:
        errors.append("crosswalk must have one row for every rule")
    for row in rows:
        for key in ("positive","negative","adversarial","integration"):
            if row.get(key) not in fixture_ids:
                errors.append(f"crosswalk {row.get('rule_id')} references unknown {key}")
    if set(controls.get("adversarial_ids", [])) != {i["fixture_id"] for i in fixtures if i["kind"] == "adversarial"}:
        errors.append("adversarial control coverage mismatch")
    if set(controls.get("negative_ids", [])) != {i["fixture_id"] for i in fixtures if i["kind"] == "negative_control"}:
        errors.append("negative control coverage mismatch")
    if {i["case_id"] for i in integrations.get("cases", [])} != {i["fixture_id"] for i in fixtures if i["kind"] == "integration"}:
        errors.append("integration coverage mismatch")
    for named in ("EQA-11","EQA-17","EQA-19","EQA-25","EQA-27","EQA-36","EQA-43","EQA-46","EQA-50"):
        if named not in fixture_ids:
            errors.append(f"missing named fixture {named}")
    for path in ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            warnings.append(f"generated cache present: {path.relative_to(ROOT)}")
    print(json.dumps({"package":"editorial-qa-orchestration","specification_sha256":SPEC_SHA256,"rule_count":len(rules),"decision_hook_count":len(hooks.get("hooks", [])),"fixture_count":len(fixtures),"crosswalk_rows":len(rows),"json_file_count":len(json_files),"errors":errors,"warnings":warnings,"pass":not errors}, indent=2, sort_keys=True))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
