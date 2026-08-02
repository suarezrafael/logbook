#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO_ROOT = ROOT.parent.parent


def run(*args: str) -> str:
    completed = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.stdout


def main() -> None:
    manifest_output = run("python3", "check_latex_manifest.py")
    assert "LaTeX manifest passed" in manifest_output

    coverage_output = run("python3", "check_runner_coverage.py")
    assert "Runner coverage passed" in coverage_output

    list_output = run("bash", "verify_all.sh", "--list")
    assert "V78" in list_output
    assert "v78/verify.py" in list_output
    assert "v78/verify_independent.py" in list_output

    workflow = (REPO_ROOT / ".github" / "workflows" / "p-vs-np-verify.yml").read_text(
        encoding="utf-8"
    )
    quick_index = workflow.index("Focused quick verification")
    quick_clean_index = workflow.index("Assert quick verification is read-only")
    full_index = workflow.index("Cumulative full verification")
    full_clean_index = workflow.index("Assert full verification is read-only")
    assert quick_index < quick_clean_index
    assert full_index < full_clean_index
    assert workflow.count("run_verification_in_sandbox.sh") == 2
    assert "path: ${{ runner.temp }}/verify-quick.log" in workflow
    assert "path: ${{ runner.temp }}/verify-full.log" in workflow
    assert workflow.count("run: bash ./assert_clean_tree.sh") == 3
    assert "branches:\n      - main" in workflow
    assert "ready_for_review" in workflow

    sandbox_runner = (ROOT / "run_verification_in_sandbox.sh").read_text(
        encoding="utf-8"
    )
    assert "git -C \"$REPO_ROOT\" archive --format=tar HEAD" in sandbox_runner
    assert "Sandbox mutation inventory" in sandbox_runner
    assert "exit \"$verification_status\"" in sandbox_runner
    assert 'mode == "full" else set()' in sandbox_runner

    clean_gate = (ROOT / "assert_clean_tree.sh").read_text(encoding="utf-8")
    assert clean_gate.startswith("#!/usr/bin/env bash")
    assert "git status --porcelain --untracked-files=all" in clean_gate

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    assert status["promoted_version"] == "V78"
    assert status["candidate_version"] == "V79"

    print(
        "V78 independent verification passed: validators execute, V78 remains "
        "registered, focused/full modes share the disposable archive, and all "
        "executed CI jobs end in source-tree gates."
    )


if __name__ == "__main__":
    main()
