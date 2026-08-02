#!/usr/bin/env python3
"""Fail when a promoted-era laboratory verifier is omitted from verify_all.sh."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POLICY_VERSION = 63


def version_number(name: str) -> int:
    match = re.fullmatch(r"v(\d+)", name)
    if not match:
        raise ValueError(name)
    return int(match.group(1))


def current_version_from_state() -> str:
    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    match = re.search(r"\*\*Current laboratory:\*\* V(\d+)(?: candidate)?", state)
    assert match, "STATE.md does not declare the current laboratory"
    return f"V{int(match.group(1))}"


def main() -> None:
    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    entries = re.findall(r'"(V\d+)\|([^|]+)\|([^|]+)\|', runner)
    keys = [(version, kind) for version, kind, _ in entries]
    assert len(keys) == len(set(keys)), "duplicate version/kind entries in runner"

    registered = {(version, kind, path) for version, kind, path in entries}
    required: list[tuple[str, str, str]] = []
    for directory in sorted(
        ROOT.glob("v[0-9]*"), key=lambda path: version_number(path.name)
    ):
        number = version_number(directory.name)
        if number < POLICY_VERSION:
            continue
        version = f"V{number}"
        if (directory / "verify.py").is_file():
            required.append((version, "primary", f"{directory.name}/verify.py"))
        if (directory / "verify_independent.py").is_file():
            required.append(
                (version, "independent", f"{directory.name}/verify_independent.py")
            )

    missing = [item for item in required if item not in registered]
    assert not missing, f"promoted-era verifier omitted from runner: {missing}"

    current = current_version_from_state()
    number = int(current[1:])
    directory = f"v{number}"
    assert (current, "primary", f"{directory}/verify.py") in registered
    assert (current, "independent", f"{directory}/verify_independent.py") in registered

    highest_directory = max(
        version_number(path.name) for path in ROOT.glob("v[0-9]*") if path.is_dir()
    )
    assert number <= highest_directory, (
        f"STATE.md declares {current}, but the highest laboratory directory is V{highest_directory}"
    )

    print(
        f"Runner coverage passed: {len(required)} promoted-era verifier entries; "
        f"current={current}; highest-directory=V{highest_directory}."
    )


if __name__ == "__main__":
    main()
