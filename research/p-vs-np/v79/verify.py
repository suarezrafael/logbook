#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
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

    assert len(baseline) == 9
    assert Counter(kind for kind, _ in baseline) == Counter({"modified": 9})
    assert not any(
        any(f"v{version}/" in path for version in (54, 55, 56, 57, 58, 59))
        for _, path in baseline
    )

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
        ROOT / "v57" / "verify.py",
        ROOT / "v57" / "verify_independent.py",
        ROOT / "v58" / "verify.py",
        ROOT / "v58" / "verify_independent.py",
        ROOT / "v59" / "verify.py",
        ROOT / "v59" / "verify_independent.py",
    ]
    for path in verifier_paths:
        source = path.read_text(encoding="utf-8")
        assert ".write_text(" not in source, path
        assert "elapsed_seconds" not in source, path
        assert "time.perf_counter" not in source, path

    for path in verifier_paths[1:]:
        assert "RESULTS.json" in path.read_text(encoding="utf-8"), path

    print(
        "V79 primary verification passed: V54-V59 are read-only, the legacy "
        "mutation baseline is reduced to nine modified paths, and regressions are blocking."
    )


if __name__ == "__main__":
    main()
