#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

MIGRATED = (
    ROOT / "v54" / "verify.py",
    ROOT / "v55" / "verify.py",
    ROOT / "v56" / "verify.py",
    ROOT / "v56" / "verify_independent.py",
    ROOT / "v57" / "verify.py",
    ROOT / "v57" / "verify_independent.py",
    ROOT / "v58" / "verify.py",
    ROOT / "v58" / "verify_independent.py",
    ROOT / "v58" / "verify_exact.py",
    ROOT / "v59" / "verify.py",
    ROOT / "v59" / "verify_independent.py",
)


def writing_calls(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute) and node.func.attr in {
            "write_text",
            "write_bytes",
            "dump",
        }:
            findings.append(node.func.attr)
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            for arg in node.args[1:2]:
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if any(mode in arg.value for mode in ("w", "a", "x", "+")):
                        findings.append(f"open:{arg.value}")
    return findings


def main() -> None:
    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    assert status["promoted_version"] == "V78"
    assert status["candidate_version"] == "V79"
    assert status["infrastructure_freeze_after_candidate"] is True
    assert status["next_laboratory_focus"] == "mathematical research"

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
        assert writing_calls(path) == [], (path, writing_calls(path))

    workflow = (ROOT.parent.parent / ".github" / "workflows" / "p-vs-np-verify.yml").read_text(
        encoding="utf-8"
    )
    assert "branches:\n      - main" in workflow
    assert "github.event.pull_request.draft == false" in workflow
    assert "types: [opened, synchronize, reopened, ready_for_review]" in workflow

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert runner.count("|quick|") <= 20
    assert runner.count("|full|") > runner.count("|quick|")

    sandbox = (ROOT / "run_verification_in_sandbox.sh").read_text(encoding="utf-8")
    assert 'expected = load_full_baseline(baseline_path) if mode == "full" else set()' in sandbox

    print(
        "V79 primary verification passed: V54-V59 including the V58 exact verifier "
        "are read-only; draft CI is focused; full historical verification remains "
        "a promotion gate; operational metadata is explicit."
    )


if __name__ == "__main__":
    main()
