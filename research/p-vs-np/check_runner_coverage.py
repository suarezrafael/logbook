#!/usr/bin/env python3
"""Validate runner coverage against the explicit operational status file."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POLICY_VERSION = 63
IMPLICATION_POLICY_VERSION = 90
STATUS_PATH = ROOT / "LAB_STATUS.json"
EXPECTED_FOCUSED = (
    "V53", "V54", "V55", "V56", "V57", "V58", "V59", "V78", "V79", "V80", "V81", "V82", "V83", "V84", "V85", "V86", "V87", "V88", "V89", "V90", "V91", "V92", "V93", "V94", "V95", "V96", "V97", "V98", "V99", "V100", "V101", "V102", "V103", "V104", "V105", "V106", "V107", "V108", "V109"
)


def version_number(name: str) -> int:
    match = re.fullmatch(r"[vV](\d+)", name)
    if not match:
        raise ValueError(name)
    return int(match.group(1))


def focused_versions(runner: str) -> tuple[str, ...]:
    match = re.search(r"FOCUSED_VERSIONS=\(([^)]*)\)", runner)
    assert match, "verify_all.sh does not declare FOCUSED_VERSIONS"
    return tuple(match.group(1).split())


def verify_implication_declaration(directory: Path, version: str) -> None:
    path = directory / "IMPLICATION.json"
    assert path.is_file(), f"{version} lacks mandatory IMPLICATION.json"
    declaration = json.loads(path.read_text(encoding="utf-8"))
    assert declaration["laboratory"] == version
    assert declaration["classification"] in {
        "frontier_progress",
        "barrier",
        "infrastructure",
        "audit",
        "closure",
        "barrier_and_closure",
    }
    assert declaration["target_problem"]
    assert declaration["conditional_implication"]
    assert declaration["current_gap"]
    assert declaration["stop_rule"]
    assert declaration["external_validation_target"]
    assert isinstance(declaration["bridge_lemmas"], list)


def main() -> None:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    declared_highest = status["highest_directory"]

    if candidate is None:
        assert declared_highest == promoted
        assert status["promotion_state"] == "promoted"
        assert status["next_laboratory_version"] == f"V{version_number(promoted) + 1}"
        active_versions = (promoted,)
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert declared_highest == candidate
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == candidate
        active_versions = (promoted, candidate)

    assert status["metadata_policy"]["authority"] == "LAB_STATUS.json"
    assert status["infrastructure_freeze_after_candidate"] is True
    assert status["infrastructure_frozen"] is True
    if version_number(declared_highest) >= IMPLICATION_POLICY_VERSION:
        assert (ROOT / "IMPLICATION_POLICY.md").is_file()
        assert "IMPLICATION_POLICY.md" in status["metadata_policy"]

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    entries = re.findall(r'"(V\d+)\|([^|]+)\|([^|]+)\|([^|]+)\|', runner)
    keys = [(version, kind) for version, kind, _path, _tier in entries]
    assert len(keys) == len(set(keys)), "duplicate version/kind entries in runner"

    registered = {(version, kind, path) for version, kind, path, _tier in entries}
    required: list[tuple[str, str, str]] = []
    for directory in sorted(ROOT.glob("v[0-9]*"), key=lambda path: version_number(path.name)):
        number = version_number(directory.name)
        if number >= IMPLICATION_POLICY_VERSION:
            verify_implication_declaration(directory, f"V{number}")
        if number < POLICY_VERSION:
            continue
        version = f"V{number}"
        if (directory / "verify.py").is_file():
            required.append((version, "primary", f"{directory.name}/verify.py"))
        if (directory / "verify_independent.py").is_file():
            required.append((version, "independent", f"{directory.name}/verify_independent.py"))

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
    quick_entries = [entry for entry in entries if entry[0] in focused and entry[3] == "quick"]
    expected_pairs = {(version, kind) for version in focused for kind in ("primary", "independent")}
    assert {(version, kind) for version, kind, _path, _tier in quick_entries} == expected_pairs
    full_entries = [entry for entry in entries if entry[3] in {"quick", "full"}]

    candidate_label = candidate or "none"
    print(
        f"Runner coverage passed: promoted={promoted}; candidate={candidate_label}; "
        f"quick={len(quick_entries)} checks; full={len(full_entries)} checks."
    )


if __name__ == "__main__":
    main()
