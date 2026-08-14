#!/usr/bin/env python3
"""Deterministic scorer for the synthetic MWM EQA evaluation set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"
RULES = ROOT / "02_RULES" / "ruleset.json"
CATALOG = EVALS / "fixture_catalog.json"
CROSSWALK = EVALS / "rule_fixture_crosswalk.json"
CONTROLS = EVALS / "adversarial_negative_controls.json"
INTEGRATIONS = EVALS / "integration_cases.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fixture_map() -> dict[str, dict[str, Any]]:
    return {item["fixture_id"]: item for item in load(CATALOG)["fixtures"]}


def validate_suite() -> dict[str, Any]:
    catalog = load(CATALOG)
    ruleset = load(RULES)
    crosswalk = load(CROSSWALK)
    controls = load(CONTROLS)
    integrations = load(INTEGRATIONS)
    fixtures = catalog["fixtures"]
    ids = [item["fixture_id"] for item in fixtures]
    errors: list[str] = []
    if catalog.get("fixture_count") != len(fixtures) or len(ids) != len(set(ids)):
        errors.append("fixture count or uniqueness mismatch")
    if not all(item.get("synthetic") is True for item in fixtures):
        errors.append("all fixtures must be synthetic")
    observed: dict[str, int] = {}
    rule_ids = {rule["rule_id"] for rule in ruleset["rules"]}
    for item in fixtures:
        observed[item["kind"]] = observed.get(item["kind"], 0) + 1
        gold = item.get("gold", {})
        for key in ("fixture_id", "kind", "title", "synthetic", "input", "gold"):
            if key not in item:
                errors.append(f"{item.get('fixture_id', '<unknown>')} missing {key}")
        for key in ("expected_status", "expected_rule_ids", "expected_interventions", "must_not_emit_rule_ids"):
            if key not in gold:
                errors.append(f"{item.get('fixture_id', '<unknown>')} missing gold.{key}")
        for rule_id in gold.get("expected_rule_ids", []) + gold.get("must_not_emit_rule_ids", []):
            if rule_id not in rule_ids:
                errors.append(f"{item.get('fixture_id')} references unknown rule {rule_id}")
    if observed != catalog.get("fixture_kind_counts"):
        errors.append(f"fixture counts differ: {observed}")
    if len(ruleset["rules"]) != 33 or len(rule_ids) != 33:
        errors.append("expected 33 unique rules")
    if len(load(ROOT / "02_RULES" / "decision_hooks.json").get("hooks", [])) != 14:
        errors.append("expected 14 decision hooks")
    rows = crosswalk.get("rows", [])
    if len(rows) != len(rule_ids) or {row.get("rule_id") for row in rows} != rule_ids:
        errors.append("crosswalk must have one row per rule")
    fixture_ids = set(ids)
    for row in rows:
        for key in ("positive", "negative", "adversarial", "integration"):
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
            errors.append(f"missing named critical fixture {named}")
    return {"evaluation_set_id":catalog.get("evaluation_set_id"),"fixture_count":len(fixtures),"fixture_counts":observed,"rule_count":len(rule_ids),"decision_hook_count":len(load(ROOT / "02_RULES" / "decision_hooks.json").get("hooks", [])),"crosswalk_rows":len(rows),"errors":errors,"pass":not errors}


def values(value: Any) -> list[str]:
    return list(value or [])


def score_fixture(fixture: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    gold = fixture["gold"]
    mismatches: list[str] = []
    if candidate.get("status") != gold["expected_status"]:
        mismatches.append("status")
    for field, gold_field in (("rule_ids","expected_rule_ids"),("interventions","expected_interventions"),("states","expected_states"),("hooks","expected_hooks"),("routes","expected_routes")):
        if gold_field in gold and set(values(candidate.get(field))) != set(values(gold[gold_field])):
            mismatches.append(field)
    if set(values(candidate.get("rule_ids"))).intersection(set(values(gold.get("must_not_emit_rule_ids")))):
        mismatches.append("forbidden_rule_ids")
    return {"fixture_id":fixture["fixture_id"],"mismatches":mismatches,"pass":not mismatches}


def gold_candidate(fixture: dict[str, Any]) -> dict[str, Any]:
    gold = fixture["gold"]
    return {"status":gold["expected_status"],"rule_ids":gold["expected_rule_ids"],"interventions":gold["expected_interventions"],"states":gold.get("expected_states",[]),"hooks":gold.get("expected_hooks",[]),"routes":gold.get("expected_routes",[])}


def self_test() -> dict[str, Any]:
    fixtures = fixture_map()
    details = [score_fixture(item, gold_candidate(item)) for item in fixtures.values()]
    zero_ids = [item["fixture_id"] for item in fixtures.values() if item["kind"] in {"adversarial","negative_control"}]
    zero_passed = sum(next(result for result in details if result["fixture_id"] == fixture_id)["pass"] for fixture_id in zero_ids)
    passed = sum(result["pass"] for result in details)
    return {"fixture_count":len(details),"passed_count":passed,"scored_count":len(details),"accuracy":passed/len(details) if details else 0.0,"pass":passed == len(details),"zero_tolerance":{"passed":zero_passed,"total":len(zero_ids)},"details":details}


def score_file(path: Path) -> dict[str, Any]:
    data = load(path)
    candidates = data.get("candidates", data)
    fixtures = fixture_map()
    details = []
    for fixture_id, candidate in candidates.items():
        if fixture_id not in fixtures:
            details.append({"fixture_id":fixture_id,"mismatches":["unknown_fixture"],"pass":False})
        else:
            details.append(score_fixture(fixtures[fixture_id], candidate))
    passed = sum(result["pass"] for result in details)
    return {"fixture_count":len(details),"passed_count":passed,"accuracy":passed/len(details) if details else 0.0,"pass":passed == len(details),"details":details}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-suite", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--score", type=Path)
    args = parser.parse_args()
    output: dict[str, Any] = {}
    if args.validate_suite:
        output["suite_validation"] = validate_suite()
    if args.self_test:
        output["self_test"] = self_test()
    if args.score:
        output["candidate_score"] = score_file(args.score)
    if not output:
        output = {"suite_validation":validate_suite(),"self_test":self_test()}
    print(json.dumps(output, indent=2, sort_keys=True))
    if any(not value.get("pass", False) for value in output.values() if isinstance(value, dict) and "pass" in value):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
