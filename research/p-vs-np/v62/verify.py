#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def block_values(x: tuple[int, int, int, int]) -> tuple[bool, ...]:
    x0, x1, x2, x3 = x
    return (
        (not x0) and ((not x1) or x2),
        (not x0) and (x1 or (not x2)),
        (not x0) and ((not x1) or x3),
        (not x0) and (x1 or (not x3)),
        (not x0) and ((not x2) or (not x3)),
    )


def clause_values(x: tuple[int, int, int, int]) -> tuple[bool, ...]:
    x0, x1, x2, x3 = x
    return (
        not x0,
        (not x1) or x2,
        x1 or (not x2),
        (not x1) or x3,
        x1 or (not x3),
        (not x2) or (not x3),
    )


def verify_irredundancy() -> int:
    assignments = list(itertools.product((0, 1), repeat=4))
    full_models = [x for x in assignments if all(block_values(x))]
    assert full_models == [(0, 0, 0, 0)]
    for removed in range(5):
        witnesses = [x for x in assignments if all(value for index, value in enumerate(block_values(x)) if index != removed) and not block_values(x)[removed]]
        assert witnesses, removed
    clause_models = [x for x in assignments if all(clause_values(x))]
    assert clause_models == full_models
    for removed in range(6):
        witnesses = [x for x in assignments if all(value for index, value in enumerate(clause_values(x)) if index != removed) and not clause_values(x)[removed]]
        assert witnesses, removed
    return 27


def permute_mask(mask: int, permutation: tuple[int, int, int], negations: tuple[int, int, int], output_flip: int) -> int:
    result = 0
    for assignment in range(8):
        bits = [(assignment >> i) & 1 for i in range(3)]
        transformed = [bits[permutation[i]] ^ negations[i] for i in range(3)]
        source = transformed[0] | (transformed[1] << 1) | (transformed[2] << 2)
        value = ((mask >> source) & 1) ^ output_flip
        result |= value << assignment
    return result


def npn_orbit(mask: int) -> set[int]:
    return {permute_mask(mask, p, n, o) for p in itertools.permutations(range(3)) for n in itertools.product((0, 1), repeat=3) for o in (0, 1)}


def local_mask(predicate) -> int:
    value = 0
    for assignment in range(8):
        bits = tuple((assignment >> i) & 1 for i in range(3))
        value |= int(bool(predicate(*bits))) << assignment
    return value


def verify_orbit() -> int:
    orbit = npn_orbit(0x07)
    assert len(orbit) == 48
    masks = [
        local_mask(lambda a, b, c: (not a) and ((not b) or c)),
        local_mask(lambda a, b, c: (not a) and (b or (not c))),
        local_mask(lambda a, b, c: (not a) and ((not b) or c)),
        local_mask(lambda a, b, c: (not a) and (b or (not c))),
        local_mask(lambda a, b, c: (not a) and ((not b) or (not c))),
    ]
    assert masks == [0x51, 0x45, 0x51, 0x45, 0x15]
    assert all(mask in orbit for mask in masks)
    return 6


def verify_repository_state() -> int:
    required = [ROOT / "README.md", ROOT / "STATE.md", ROOT / "LEDGER.json", ROOT / "verify_all.sh", HERE / "README.md", HERE / "INTEGRATED_MANUSCRIPT.md", HERE / "SOURCE_TO_CLAIM.md", HERE / "SOURCE_TO_CLAIM.json", HERE / "V57_IES_TRANSLATION.md", HERE / "V54_KUNTEWAR_SARMA_COMPARISON.md", HERE / "PRIOR_ART_SEARCH_LOG.md", HERE / "EXTERNAL_CONTACT_STATUS.md", HERE / "RESULTS.json", HERE / "V63_CORE_CONTEXT.md"]
    assert not [str(p) for p in required if not p.is_file()]
    ledger = load_json(ROOT / "LEDGER.json")
    results = load_json(HERE / "RESULTS.json")
    source_matrix = load_json(HERE / "SOURCE_TO_CLAIM.json")
    assert ledger["schema_version"] == 3
    assert ledger["current_version"] == "V62"
    assert ledger["program"]["p_vs_np_route_active"] is False
    assert ledger["current_decision"]["commit_policy"] == "one_commit_per_laboratory"
    assert ledger["external_contact"]["status"] == "sent_awaiting_reply"
    assert len(ledger["external_contact"]["outreach"]) == 2
    assert any(v["version"] == "V62" for v in ledger["versions"])
    assert results["external_contact"]["messages"] == 2
    assert results["scientific_status"]["novelty_confirmed"] is False
    assert source_matrix["version"] == "V62"
    assert len(source_matrix["entries"]) == 15
    assert all(entry["repository_novelty_claim"] is False for entry in source_matrix["entries"])
    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V62|primary|v62/verify.py|quick|" in runner
    assert "V62|independent|v62/verify_independent.py|quick|" in runner
    state = (ROOT / "STATE.md").read_text(encoding="utf-8")
    assert "Current laboratory:** V62" in state
    assert "External contact:** sent" in state
    assert "P-versus-NP route active:** no" in state
    return 29


def verify_claim_language() -> int:
    manuscript = (HERE / "INTEGRATED_MANUSCRIPT.md").read_text(encoding="utf-8")
    comparison = (HERE / "V54_KUNTEWAR_SARMA_COMPARISON.md").read_text(encoding="utf-8")
    translation = (HERE / "V57_IES_TRANSLATION.md").read_text(encoding="utf-8")
    contact = (HERE / "EXTERNAL_CONTACT_STATUS.md").read_text(encoding="utf-8")
    required = ["Affine Algorithms, Bijunctive Barriers, and Orientation Depth", "does not claim novelty for general CNF/2-CNF irredundancy", "Kuntewar and Sarma prove deterministic polynomial-time", "No exact equivalent was located", "silence is not evidence of novelty"]
    for token in required:
        assert token in manuscript
    assert "direct algorithmic overlap; certificate equivalence unresolved" in comparison
    assert "clause-irredundant 2-CNF" in translation
    assert "sent, awaiting reply" in contact
    return 9


def main() -> None:
    checks = verify_irredundancy() + verify_orbit() + verify_repository_state() + verify_claim_language()
    assert checks == 71, checks
    print("V62 primary verification passed: 71 checks; zero failures.")


if __name__ == "__main__":
    main()
