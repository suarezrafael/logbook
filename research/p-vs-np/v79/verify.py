#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MIGRATED = (
    ROOT / "v54" / "verify.py", ROOT / "v55" / "verify.py",
    ROOT / "v56" / "verify.py", ROOT / "v56" / "verify_independent.py",
    ROOT / "v57" / "verify.py", ROOT / "v57" / "verify_independent.py",
    ROOT / "v58" / "verify.py", ROOT / "v58" / "verify_independent.py",
    ROOT / "v58" / "verify_exact.py", ROOT / "v59" / "verify.py",
    ROOT / "v59" / "verify_independent.py",
)
WRITE_FLAGS = ("w", "a", "x", "+")
BASE_FOCUSED = ("V53", "V54", "V55", "V56", "V57", "V58", "V59", "V78", "V79")


def version_number(value: str) -> int:
    assert value.startswith("V") and value[1:].isdigit()
    return int(value[1:])


def string_argument(node: ast.Call, positional_index: int, keyword: str) -> str | None:
    value: ast.expr | None = None
    if len(node.args) > positional_index:
        value = node.args[positional_index]
    else:
        value = next((item.value for item in node.keywords if item.arg == keyword), None)
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    return None


def writing_calls(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in {"write_text", "write_bytes", "dump"}:
                findings.append(node.func.attr)
            elif node.func.attr == "open":
                mode = string_argument(node, 0, "mode")
                if mode is not None and any(flag in mode for flag in WRITE_FLAGS):
                    findings.append(f"Path.open:{mode}")
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            mode = string_argument(node, 1, "mode")
            if mode is not None and any(flag in mode for flag in WRITE_FLAGS):
                findings.append(f"open:{mode}")
    return findings


def main() -> None:
    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    promoted = version_number(status["promoted_version"])
    candidate = status.get("candidate_version")
    assert promoted >= 79
    if candidate is not None:
        assert version_number(candidate) == promoted + 1
        assert status["highest_directory"] == candidate
        assert status["promotion_state"] == "candidate"
    else:
        assert status["highest_directory"] == status["promoted_version"]
        assert status["promotion_state"] == "promoted"
    assert status["infrastructure_frozen"] is True

    baseline = []
    for line in (HERE / "EXPECTED_MUTATIONS.tsv").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        kind, path = line.split("\t")
        baseline.append((kind, path))
    assert len(baseline) == 9
    assert Counter(kind for kind, _ in baseline) == Counter({"modified": 9})
    assert not any(
        any(f"v{version}/" in path for version in (54, 55, 56, 57, 58, 59))
        for _, path in baseline
    )

    assert all(path.is_file() for path in MIGRATED)
    for path in MIGRATED:
        assert writing_calls(path) == []

    workflow = (ROOT.parent.parent / ".github" / "workflows" / "p-vs-np-verify.yml").read_text(encoding="utf-8")
    assert "branches:\n      - main" in workflow
    assert "github.event.pull_request.draft == false" in workflow
    assert "types: [opened, synchronize, reopened, ready_for_review]" in workflow
    assert "  compatibility:\n" in workflow
    assert "run_verification_in_sandbox.sh --compat" in workflow
    assert "  schedule:\n" in workflow
    full_job = workflow.split("  full:\n", 1)[1].split("  latex:\n", 1)[0]
    assert "github.event_name == 'schedule'" in full_job
    assert "github.event_name == 'push'" not in full_job

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    focused_match = re.search(r"FOCUSED_VERSIONS=\(([^)]*)\)", runner)
    assert focused_match
    focused = tuple(focused_match.group(1).split())
    assert focused[: len(BASE_FOCUSED)] == BASE_FOCUSED
    if candidate is not None:
        assert candidate in focused
    entries = re.findall(r'"(V\d+)\|([^|]+)\|([^|]+)\|([^|]+)\|', runner)
    quick = [entry for entry in entries if entry[0] in focused and entry[3] == "quick"]
    full = [entry for entry in entries if entry[3] in {"quick", "full"}]
    assert len(quick) >= 18
    assert len(full) >= 63
    assert '--compat) MODE="compat"' in runner

    sandbox = (ROOT / "run_verification_in_sandbox.sh").read_text(encoding="utf-8")
    assert '--compat) MODE="compat"' in sandbox
    assert 'expected = load_full_baseline(baseline_path) if mode in {"compat", "full"} else set()' in sandbox

    verification_policy = status["verification_policy"]
    assert verification_policy["quick_expected_mutations"] == 0
    assert verification_policy["compatibility_expected_mutations"] == 9
    assert verification_policy["full_expected_mutations"] == 9

    print(
        "V79 primary verification passed: immutable evidence, focused quick CI, "
        "historical compatibility, and scheduled exact replays remain installed "
        "after later mathematical candidates."
    )


if __name__ == "__main__":
    main()
