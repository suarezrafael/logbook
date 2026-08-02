#!/usr/bin/env python3
from __future__ import annotations

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
    quick_index = workflow.index("Quick verification")
    quick_clean_index = workflow.index("Assert quick verification is read-only")
    full_index = workflow.index("Full verification")
    full_clean_index = workflow.index("Assert full verification is read-only")
    assert quick_index < quick_clean_index
    assert full_index < full_clean_index
    assert "path: ${{ runner.temp }}/verify-quick.log" in workflow
    assert "path: ${{ runner.temp }}/verify-full.log" in workflow

    clean_gate = ROOT / "assert_clean_tree.sh"
    assert clean_gate.stat().st_mode & 0o111, "clean-tree script must be executable"

    print(
        "V78 independent verification passed: manifest and runner validators execute, "
        "V78 is registered, and both CI verification jobs end in clean-tree gates."
    )


if __name__ == "__main__":
    main()
