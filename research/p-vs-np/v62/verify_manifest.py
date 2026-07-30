#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "SHA256SUMS.txt"


def main() -> None:
    entries = []
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, relative = line.split("  ", 1)
        path = HERE / relative
        assert path.is_file(), relative
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == digest, (relative, digest, actual)
        entries.append(relative)
    assert len(entries) == len(set(entries))
    print(f"V62 manifest verification passed: {len(entries)} files; zero failures.")


if __name__ == "__main__":
    main()
