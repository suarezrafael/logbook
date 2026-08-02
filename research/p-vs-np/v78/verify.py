#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO_ROOT = ROOT.parent.parent


def main() -> None:
    required = [
        HERE / "README.md",
        HERE / "MUTATION_INVENTORY.md",
        HERE / "verify.py",
        HERE / "verify_independent.py",
        ROOT / "assert_clean_tree.sh",
        ROOT / "run_verification_in_sandbox.sh",
        ROOT / "LATEX_MODULES.tsv",
        ROOT / "check_latex_manifest.py",
    ]
    assert all(path.is_file() for path in required)

    workflow = (REPO_ROOT / ".github" / "workflows" / "p-vs-np-verify.yml").read_text(
        encoding="utf-8"
    )
    for token in (
        "${RUNNER_TEMP}/verify-quick.log",
        "${RUNNER_TEMP}/verify-full.log",
        "run_verification_in_sandbox.sh",
        "Assert quick verification is read-only",
        "Assert full verification is read-only",
        "bash ./assert_clean_tree.sh",
        "LATEX_MODULES.tsv",
        "check_latex_manifest.py",
    ):
        assert token in workflow, token

    sandbox_runner = (ROOT / "run_verification_in_sandbox.sh").read_text(
        encoding="utf-8"
    )
    for token in (
        "git -C \"$REPO_ROOT\" archive --format=tar HEAD",
        "mktemp -d",
        "Sandbox mutation inventory",
        "bash ./verify_all.sh",
    ):
        assert token in sandbox_runner, token

    clean_gate = (ROOT / "assert_clean_tree.sh").read_text(encoding="utf-8")
    for token in (
        "git status --porcelain --untracked-files=all",
        "git diff --stat",
        "exit 1",
    ):
        assert token in clean_gate, token

    coverage = (ROOT / "check_runner_coverage.py").read_text(encoding="utf-8")
    assert "STATE.md" in coverage
    assert "LEDGER.json" not in coverage
    assert "Current laboratory" in coverage

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V78|primary|v78/verify.py|quick|" in runner
    assert "V78|independent|v78/verify_independent.py|quick|" in runner

    manifest = (ROOT / "LATEX_MODULES.tsv").read_text(encoding="utf-8")
    entries = [line for line in manifest.splitlines() if line.strip()]
    assert len(entries) >= 14
    assert all(len(line.split("\t")) == 2 for line in entries)

    inventory = (HERE / "MUTATION_INVENTORY.md").read_text(encoding="utf-8")
    modified = [line for line in inventory.splitlines() if line.startswith("- `v")]
    assert len(modified) == 21
    assert "Modified tracked artifacts (16)" in inventory
    assert "Newly generated artifacts (5)" in inventory
    assert "reduce the sandbox mutation inventory to zero" in inventory

    readme = (HERE / "README.md").read_text(encoding="utf-8").lower()
    assert "v79" in readme
    for forbidden in (
        "p versus np is solved",
        "we prove p != np",
        "new avoidance theorem",
    ):
        assert forbidden not in readme

    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    current = re.search(r"\*\*Current laboratory:\*\* V(\d+)(?: candidate)?", state)
    assert current and int(current.group(1)) >= 77

    print(
        "V78 primary verification passed: clean source-checkout gates, disposable "
        "verification sandbox, explicit 21-path mutation baseline, external CI logs, "
        "validated LaTeX manifest, and ledger-independent runner coverage are installed."
    )


if __name__ == "__main__":
    main()
