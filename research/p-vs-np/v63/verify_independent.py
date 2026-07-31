#!/usr/bin/env python3
from __future__ import annotations
import json
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def version_number(value):
    m=re.fullmatch(r"V(\d+)", value); assert m, value; return int(m.group(1))

def independent_metadata() -> int:
    ledger=load(ROOT/"LEDGER.json")
    results=load(HERE/"RESULTS.json")
    assert version_number(ledger["current_version"]) >= 63
    assert ledger["promotion"]["policy_effective_version"] == "V63"
    assert ledger["promotion"]["completed_prs_must_be_non_draft"] is True
    assert ledger["promotion"]["preferred_merge_method"] == "squash"
    assert ledger["verification"]["last_clean_ci_run_id"] >= 30595354956
    assert results["ci"]["quick"] == {"executed":22,"skipped":4,"failures":0,"status":"passed"}
    assert results["ci"]["full"] == {"executed":24,"skipped":2,"failures":0,"status":"passed"}
    assert results["external_review"]["replies_found_at_check"] == 0
    assert results["external_review"]["followup_sent"] is False
    assert results["scientific_status"]["p_vs_np_resolved"] is False
    return 10

def independent_documents() -> int:
    files={
      "a":(HERE/"APPENDIX_A_AFFINE_FIBERS.md").read_text(encoding="utf-8"),
      "b":(HERE/"APPENDIX_B_BIJUNCTIVE_BLOCKS.md").read_text(encoding="utf-8"),
      "c":(HERE/"APPENDIX_C_ORIENTATION_DEPTH.md").read_text(encoding="utf-8"),
      "r":(HERE/"REVIEWER_PACKET.md").read_text(encoding="utf-8"),
      "e":(HERE/"EXTERNAL_RESPONSE_CHECK.md").read_text(encoding="utf-8"),
      "p":(HERE/"PROMOTION_POLICY.md").read_text(encoding="utf-8"),
    }
    assert "minimal inconsistent equation subsystem" in files["a"]
    assert "complete gate block" in files["b"]
    assert "Clause-level irredundancy witnesses" in files["b"]
    assert "rho_S(b)" in files["c"]
    assert "Hamming-ball enumeration" in files["c"]
    assert "does not assert priority" in files["r"]
    assert "zero matching incoming messages" in files["e"]
    assert "No reminder or duplicate request" in files["e"]
    assert "non-draft pull request" in files["p"]
    assert "CI is a merge gate" in files["p"]
    forbidden=["we prove p != np","first general nc0_3-avoid algorithm","silence confirms novelty"]
    corpus="\n".join(files.values()).lower()
    assert all(x not in corpus for x in forbidden)
    return 13

def independent_history() -> int:
    ci=(HERE/"CI_PROMOTION_RECORD.md").read_text(encoding="utf-8")
    state=(ROOT/"STATE.md").read_text(encoding="utf-8")
    assert "30591741077" in ci
    assert "30595354956" in ci
    assert "233745d3f6a0613bc1d27fcfe9725ecb4a20d628" in ci
    assert "V22" in state and "justified" in state.lower()
    assert "External contact:** sent" in state
    assert "P-versus-NP route active:** no" in state
    return 6

def main():
    total=independent_metadata()+independent_documents()+independent_history()
    assert total == 29, total
    print("V63 independent verification passed: 29 checks; zero failures.")

if __name__=="__main__":
    main()
