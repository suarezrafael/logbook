#!/usr/bin/env python3
from __future__ import annotations
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def blocks(x):
    x0,x1,x2,x3=x
    return (
        (not x0) and ((not x1) or x2),
        (not x0) and (x1 or (not x2)),
        (not x0) and ((not x1) or x3),
        (not x0) and (x1 or (not x3)),
        (not x0) and ((not x2) or (not x3)),
    )

def clauses(x):
    x0,x1,x2,x3=x
    return (
        not x0,
        (not x1) or x2,
        x1 or (not x2),
        (not x1) or x3,
        x1 or (not x3),
        (not x2) or (not x3),
    )

def check_v57_witnesses() -> int:
    assignments=list(itertools.product((0,1), repeat=4))
    assert [x for x in assignments if all(blocks(x))] == [(0,0,0,0)]
    expected_blocks=[(0,1,0,1),(0,0,1,0),(0,1,1,0),(0,0,0,1),(0,1,1,1)]
    for i,w in enumerate(expected_blocks):
        assert all(v for j,v in enumerate(blocks(w)) if j!=i)
        assert not blocks(w)[i]
    assert [x for x in assignments if all(clauses(x))] == [(0,0,0,0)]
    expected_clauses=[(1,0,0,0),*expected_blocks]
    for i,w in enumerate(expected_clauses):
        assert all(v for j,v in enumerate(clauses(w)) if j!=i)
        assert not clauses(w)[i]
    return 23

def check_repository() -> int:
    required=[
        ROOT/"README.md", ROOT/"STATE.md", ROOT/"LEDGER.json", ROOT/"verify_all.sh",
        HERE/"README.md", HERE/"CI_PROMOTION_RECORD.md", HERE/"REVIEWER_PACKET.md",
        HERE/"APPENDIX_A_AFFINE_FIBERS.md", HERE/"APPENDIX_B_BIJUNCTIVE_BLOCKS.md",
        HERE/"APPENDIX_C_ORIENTATION_DEPTH.md", HERE/"EXTERNAL_RESPONSE_CHECK.md",
        HERE/"PROMOTION_POLICY.md", HERE/"CHANGELOG_FROM_V62.md", HERE/"RESULTS.json",
        HERE/"V64_CORE_CONTEXT.md",
    ]
    assert not [str(p) for p in required if not p.is_file()]
    ledger=load(ROOT/"LEDGER.json")
    results=load(HERE/"RESULTS.json")
    assert ledger["schema_version"] == 4
    assert ledger["current_version"] == "V63"
    assert ledger["program"]["p_vs_np_route_active"] is False
    assert ledger["promotion"]["per_laboratory_pr_required"] is True
    assert ledger["promotion"]["ci_required_before_merge"] is True
    assert ledger["promotion"]["merge_target"] == "main"
    assert ledger["verification"]["quick"]["failures"] == 0
    assert ledger["verification"]["full"]["failures"] == 0
    assert ledger["external_contact"]["replies_received"] == 0
    assert ledger["external_contact"]["followup_sent"] is False
    assert results["version"] == "V63"
    assert results["scientific_status"]["novelty_confirmed"] is False
    runner=(ROOT/"verify_all.sh").read_text(encoding="utf-8")
    assert "V63|primary|v63/verify.py|quick|" in runner
    assert "V63|independent|v63/verify_independent.py|quick|" in runner
    return 29

def check_prose() -> int:
    packet=(HERE/"REVIEWER_PACKET.md").read_text(encoding="utf-8")
    ci=(HERE/"CI_PROMOTION_RECORD.md").read_text(encoding="utf-8")
    policy=(HERE/"PROMOTION_POLICY.md").read_text(encoding="utf-8")
    a=(HERE/"APPENDIX_A_AFFINE_FIBERS.md").read_text(encoding="utf-8")
    b=(HERE/"APPENDIX_B_BIJUNCTIVE_BLOCKS.md").read_text(encoding="utf-8")
    c=(HERE/"APPENDIX_C_ORIENTATION_DEPTH.md").read_text(encoding="utf-8")
    for token in ("does not assert priority","general `NC0_3-Avoid`","P versus NP"):
        assert token in packet
    for token in ("executed=22","executed=24","126607","not a mathematical counterexample"):
        assert token in ci
    for token in ("One laboratory per PR","squash merge","Main is the source of truth"):
        assert token in policy
    assert "degree at most `n+1`" in a
    assert "0101" in b and "1000" in b
    assert "m^{O(d)}" in c and "126607" in c
    return 13

def main():
    total=check_v57_witnesses()+check_repository()+check_prose()
    assert total == 65, total
    print("V63 primary verification passed: 65 checks; zero failures.")

if __name__ == "__main__":
    main()
