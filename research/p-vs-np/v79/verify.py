#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    required = [
        HERE / "README.md",
        HERE / "EXPECTED_MUTATIONS.tsv",
        HERE / "verify.py",
        HERE / "verify_independent.py",
        ROOT / "run_verification_in_sandbox.sh",
    ]
    assert all(path.is_file() for path in required)

    baseline = []
    for line in (HERE / "EXPECTED_MUTATIONS.tsv").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        kind, path = line.split("\t")
        baseline.append((kind, path))

    assert len(baseline) == 15
    assert all(kind == "modified" for kind, _ in baseline)
    forbidden = {
        "research/p-vs-np/v54/VERIFY_RESULTS.json",
        "research/p-vs-np/v55/RESULTS.json",
        "research/p-vs-np/v55/CLASSIFICATION.json",
        "research/p-vs-np/v56/REPO_VALIDATION_RESULTS.json",
        "research/p-vs-np/v56/REPO_INDEPENDENT_RESULTS.json",
    }
    assert forbidden.isdisjoint(path for _, path in baseline)

    sandbox = (ROOT / "run_verification_in_sandbox.sh").read_text(encoding="utf-8")
    for token in (
        "v79/EXPECTED_MUTATIONS.tsv",
        "Mutation baseline mismatch",
        "unexpected mutations",
        "expected mutations not observed",
    ):
        assert token in sandbox, token

    verifier_paths = [
        ROOT / "v54" / "verify.py",
        ROOT / "v55" / "verify.py",
        ROOT / "v56" / "verify.py",
        ROOT / "v56" / "verify_independent.py",
    ]
    for path in verifier_paths:
        source = path.read_text(encoding="utf-8")
        assert ".write_text(" not in source, path
        assert "elapsed_seconds" not in source, path
        assert "time.perf_counter" not in source, path

    v55_source = verifier_paths[1].read_text(encoding="utf-8")
    v56_source = verifier_paths[2].read_text(encoding="utf-8")
    assert "RESULTS.json" in v55_source
    assert "RESULTS.json" in v56_source

    print(
        "V79 primary verification passed: V54-V56 are read-only, the legacy "
        "mutation baseline is reduced to 15 modified paths, and regressions are blocking."
    )


if __name__ == "__main__":
    main()
