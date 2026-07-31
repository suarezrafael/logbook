#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path

HERE=Path(__file__).resolve().parent

def main():
    expected={}
    for line in (HERE/"SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest,name=line.split("  ",1)
        expected[name]=digest
    failures=[]
    for name,digest in expected.items():
        path=HERE/name
        if not path.is_file():
            failures.append(f"missing:{name}")
            continue
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=digest:
            failures.append(f"hash:{name}")
    assert not failures, failures
    print(f"V63 manifest verification passed: {len(expected)} files; zero failures.")

if __name__=="__main__":
    main()
