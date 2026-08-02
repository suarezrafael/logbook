#!/usr/bin/env python3
from __future__ import annotations

import ast
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

TARGETS = (
    ROOT / "v54" / "verify.py",
    ROOT / "v55" / "verify.py",
    ROOT / "v56" / "verify.py",
    ROOT / "v56" / "verify_independent.py",
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
    assert len(baseline_lines) == len(set(baseline_lines)) == 15
    assert not any("\t" not in line for line in baseline_lines)
    assert not any("v54/" in line or "v55/" in line or "v56/" in line for line in baseline_lines)

    print(
        "V79 independent verification passed: AST audit finds no file-writing calls "
        "in the migrated V54-V56 verifiers and the reduced baseline is unique."
    )


if __name__ == "__main__":
    main()
