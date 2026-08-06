#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

PROGRAM_ROOT = Path(__file__).resolve().parent.parent


def verify_external_validation() -> bool:
    gate = json.loads(
        (PROGRAM_ROOT / "EXTERNAL_VALIDATION_GATE.json").read_text(encoding="utf-8")
    )
    assert gate["blocks"] == "V93 execution"
    assert gate["outreach_sequence"] == [
        "public_narrow_technical_question",
        "preprint_readiness_and_optional_submission",
        "brazilian_academic_contact",
        "targeted_author_email_tied_to_specific_theorem",
    ]
    assert gate["preprint_policy"]["upload_required_for_v93_release"] is False
    assert gate["preprint_policy"]["upload_must_not_be_used_only_to_satisfy_gate"]

    required = gate["required_submissions"]
    assert [item["laboratory"] for item in required] == ["V81", "V87"]
    for item in required:
        assert item["submission_status"] in {"not_submitted", "submitted"}
        assert item["review_status"] in {
            "awaiting_submission",
            "awaiting_response",
            "response_received",
        }
        assert item["qualifying_evidence"]
        if item["submission_status"] == "submitted":
            assert item["submitted_at"]
            assert item["recipient_description"]
            assert item["evidence_reference"]
            assert item["review_status"] in {"awaiting_response", "response_received"}
        else:
            assert item["submitted_at"] is None
            assert item["recipient_description"] is None
            assert item["evidence_reference"] is None
            assert item["review_status"] == "awaiting_submission"

    all_submitted = all(item["submission_status"] == "submitted" for item in required)
    assert gate["status"] == ("released" if all_submitted else "blocking")

    outreach = (PROGRAM_ROOT / "EXTERNAL_OUTREACH_SEQUENCE.md").read_text(encoding="utf-8")
    assert "public technical question" in outreach
    assert "targeted author email" in outreach
    assert "Tone firewall" in outreach

    public_draft = (PROGRAM_ROOT / "v90" / "CSTHEORY_V81_DRAFT.md").read_text(encoding="utf-8")
    assert "I am not claiming novelty" in public_draft
    assert "delta(S) + delta(M\\S) = sigma - lambda(S)" in public_draft

    preprint = (PROGRAM_ROOT / "v90" / "ARXIV_PREPRINT_READINESS.md").read_text(encoding="utf-8")
    assert "Do not upload" in preprint
    assert "authorship and contributor roles" in preprint

    email = (PROGRAM_ROOT / "v90" / "TARGETED_FOLLOWUP_EMAIL.md").read_text(encoding="utf-8")
    assert "Theorem X" in email
    assert "stable preprint or public-note link" in email
    assert "no request to review the entire project" in email
    assert "no mention of solving P versus NP" in email

    cadence = gate["v93_cadence"]
    assert cadence["planning_unit"] == "week"
    assert cadence["minimum_initial_horizon_weeks"] >= 2
    assert cadence["same_day_promotion_from_finite_evidence"] is False
    assert cadence["open_after_milestone_one_is_valid"]
    assert [item["name"].split()[0] for item in cadence["milestones"]] == ["M0", "M1", "M2"]
    return all_submitted


if __name__ == "__main__":
    print(f"external validation gate verified; all_submitted={verify_external_validation()}")
