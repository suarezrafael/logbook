#!/usr/bin/env python3
"""Validate the deterministic LaTeX build manifest."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "LATEX_MODULES.tsv"


def load_manifest() -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line_number, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 2 or not all(part.strip() for part in parts):
            raise AssertionError(f"invalid LaTeX manifest line {line_number}: {raw!r}")
        output_key, relative_path = (part.strip() for part in parts)
        entries.append((output_key, relative_path))
    return entries


def main() -> None:
    entries = load_manifest()
    assert entries, "LaTeX manifest is empty"

    output_keys = [output_key for output_key, _ in entries]
    paths = [relative_path for _, relative_path in entries]
    assert len(output_keys) == len(set(output_keys)), "duplicate LaTeX output key"
    assert len(paths) == len(set(paths)), "duplicate LaTeX module path"

    listed = {ROOT / relative_path for relative_path in paths}
    missing = sorted(str(path.relative_to(ROOT)) for path in listed if not path.is_file())
    assert not missing, f"LaTeX manifest references missing files: {missing}"

    discovered = set(ROOT.glob("v[0-9]*/V*_THEOREM.tex"))
    manuscript = ROOT / "v71" / "MANUSCRIPT.tex"
    if manuscript.is_file():
        discovered.add(manuscript)

    omitted = sorted(str(path.relative_to(ROOT)) for path in discovered - listed)
    stale = sorted(str(path.relative_to(ROOT)) for path in listed - discovered)
    assert not omitted, f"formal LaTeX modules omitted from manifest: {omitted}"
    assert not stale, f"manifest entries are not formal modules: {stale}"

    print(f"LaTeX manifest passed: {len(entries)} formal modules.")


if __name__ == "__main__":
    main()
