#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
VERIFY = (REPO / ".github/workflows/p-vs-np-verify.yml").read_text(encoding="utf-8")
CLEANUP = (REPO / ".github/workflows/cleanup-merged-research-branches.yml").read_text(encoding="utf-8")
RUNNER = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
SANDBOX = (ROOT / "run_verification_in_sandbox.sh").read_text(encoding="utf-8")
STATUS = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))


def between(text: str, first: str, second: str | None = None) -> str:
    assert first in text
    tail = text.split(first, 1)[1]
    return tail if second is None else tail.split(second, 1)[0]


def main() -> None:
    assert "  schedule:\n" in VERIFY
    assert "cron: '17 06 * * 1'" in VERIFY
    assert "  changes:\n" in VERIFY
    assert "  compatibility:\n" in VERIFY
    assert "run_verification_in_sandbox.sh --compat" in VERIFY

    full = between(VERIFY, "  full:\n", "  latex:\n")
    assert "github.event_name == 'schedule'" in full
    assert "github.event_name == 'workflow_dispatch'" in full
    assert "needs.changes.outputs.full_replay == 'true'" in full
    assert "github.event_name == 'push'" not in full

    latex = between(VERIFY, "  latex:\n")
    assert "needs.changes.outputs.latex == 'true'" in latex

    assert "--compat) MODE=\"compat\"" in RUNNER
    assert "exact replay requires --full" in RUNNER
    assert "check_ci_contract.py" in RUNNER
    assert '--compat) MODE="compat"' in SANDBOX
    assert 'mode in {"compat", "full"}' in SANDBOX

    policy = STATUS["ci_policy"]
    assert policy["draft_pull_request"] == ["quick", "latex_when_relevant"]
    assert policy["ready_pull_request"] == ["quick", "compatibility", "latex_when_relevant", "full_when_ci_sensitive"]
    assert policy["main_push"] == ["quick", "latex_when_relevant"]
    assert policy["scheduled"] == ["full"]
    assert policy["manual_dispatch"] == ["quick", "full", "latex"]

    verification = STATUS["verification_policy"]
    assert verification["quick_expected_mutations"] == 0
    assert verification["compatibility_expected_mutations"] == 9
    assert verification["full_expected_mutations"] == 9

    assert "pull_request:\n    types: [closed]" in CLEANUP
    assert "github.event.pull_request.merged == true" in CLEANUP
    assert "startsWith(github.event.pull_request.head.ref, 'agent/')" in CLEANUP
    assert "github.event.pull_request.head.repo.full_name == github.repository" in CLEANUP
    assert "branches=(" not in CLEANUP

    print("CI contract passed: safe promotion gates, scheduled exact replays, conditional LaTeX, dynamic cleanup.")


if __name__ == "__main__":
    main()
