#!/usr/bin/env python3
from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

TARGETS = (
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
    assert all(path.is_file() for path in TARGETS)
    for path in TARGETS:
        assert writing_calls(path) == [], (path, writing_calls(path))

    baseline_lines = [
        line
        for line in (HERE / "EXPECTED_MUTATIONS.tsv").read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#")
    ]
    assert len(baseline_lines) == len(set(baseline_lines)) == 9
    parsed = [tuple(line.split("\t")) for line in baseline_lines]
    assert all(len(entry) == 2 for entry in parsed)
    assert Counter(kind for kind, _ in parsed) == Counter({"modified": 9})
    assert not any(
        any(f"v{version}/" in path for version in (54, 55, 56, 57, 58, 59))
        for _, path in parsed
    )

    print(
        "V79 independent verification passed: AST audit finds no file-writing calls "
        "in the migrated V54-V59 verifiers and the nine-path baseline is unique."
    )


if __name__ == "__main__":
    main()
