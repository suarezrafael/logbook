#!/usr/bin/env python3
"""Validate runner coverage against the explicit operational status file."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POLICY_VERSION = 63
STATUS_PATH = ROOT / "LAB_STATUS.json"
EXPECTED_FOCUSED = ("V53", "V54", "V55", "V56", "V57", "V58", "V59", "V78", "V79")


def version_number(name: str) -> int:
    match = re.fullmatch(r"[vV](\d+)", name)
    if not match:
        raise ValueError(name)
    return int(match.group(1))


def focused_versions(runner: str) -> tuple[str, ...]:
    match = re.search(r"FOCUSED_VERSIONS=\(([^)]*)\)", runner)
    assert match, "verify_all.sh does not declare FOCUSED_VERSIONS"
    return tuple(match.group(1).split())


def main() -> None:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    declared_highest = status["highest_directory"]

    if candidate is None:
        assert declared_highest == promoted
        active_versions = (promoted,)
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert declared_highest == candidate
        active_versions = (promoted, candidate)

    assert status["promotion_state"] == "promoted"
    assert status["metadata_policy"]["authority"] == "LAB_STATUS.json"
    assert status["infrastructure_freeze_after_candidate"] is True
    assert status["infrastructure_frozen"] is True
    assert status["next_laboratory_version"] == f"V{version_number(promoted) + 1}"
    assert status["next_laboratory_focus"] == "mathematical research"

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    entries = re.findall(r'"(V\d+)\|([^|]+)\|([^|]+)\|([^|]+)\|', runner)
    keys = [(version, kind) for version, kind, _path, _tier in entries]
    assert len(keys) == len(set(keys)), "duplicate version/kind entries in runner"

    registered = {(version, kind, path) for version, kind, path, _tier in entries}
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

    for version in active_versions:
        directory = f"v{version_number(version)}"
        assert (version, "primary", f"{directory}/verify.py") in registered
        assert (version, "independent", f"{directory}/verify_independent.py") in registered

    highest_directory = max(
        version_number(path.name) for path in ROOT.glob("v[0-9]*") if path.is_dir()
    )
    assert highest_directory == version_number(declared_highest), (
        f"LAB_STATUS.json declares highest {declared_highest}, "
        f"but the highest laboratory directory is V{highest_directory}"
    )

    focused = focused_versions(runner)
    assert focused == EXPECTED_FOCUSED
    quick_entries = [
        entry for entry in entries if entry[0] in focused and entry[3] == "quick"
    ]
    full_entries = [entry for entry in entries if entry[3] in {"quick", "full"}]
    assert len(quick_entries) == 18
    assert len(full_entries) == 63

    candidate_label = candidate or "none"
    print(
        f"Runner coverage passed: promoted={promoted}; candidate={candidate_label}; "
        f"quick={len(quick_entries)} checks; full={len(full_entries)} checks."
    )


if __name__ == "__main__":
    main()
