#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from deficiency_conservation import build_results

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def version_number(value: str) -> int:
    assert value.startswith("V") and value[1:].isdigit()
    return int(value[1:])


def main() -> None:
    committed = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert build_results() == committed

    theorem = (HERE / "DEFICIENCY_CONSERVATION_AND_MIN_UNION.md").read_text(encoding="utf-8")
    literature = (HERE / "LOSSLESS_EXPANDER_AUDIT.md").read_text(encoding="utf-8")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    core = (HERE / "V82_CORE_CONTEXT.md").read_text(encoding="utf-8")
    tex = (HERE / "V81_DEFICIENCY_CONSERVATION_THEOREM.tex").read_text(encoding="utf-8")

    for phrase in (
        "deficiency conservation",
        "width-deficiency tradeoff",
        "Minimum `p`-Union",
        "Lagrangian scan",
        "unsupported",
    ):
        assert phrase.lower() in theorem.lower()
    assert "degree exactly three" in literature
    assert "does not prove a polynomial-time algorithm or NP-hardness" in readme
    assert "unsupported points" in core
    assert "Deficiency conservation" in tex
    assert "Width--deficiency tradeoff" in tex

    status = json.loads((ROOT / "LAB_STATUS.json").read_text(encoding="utf-8"))
    promoted = status["promoted_version"]
    candidate = status.get("candidate_version")
    assert version_number(promoted) >= 81
    if candidate is None:
        assert status["highest_directory"] == promoted
        assert status["promotion_state"] == "promoted"
        assert status["next_laboratory_version"] == f"V{version_number(promoted) + 1}"
    else:
        assert version_number(candidate) == version_number(promoted) + 1
        assert status["highest_directory"] == candidate
        assert status["promotion_state"] == "candidate"
        assert status["next_laboratory_version"] == candidate
    assert status["infrastructure_frozen"] is True
    assert status["scientific_status"]["p_vs_np_route_active"] is False

    runner = (ROOT / "verify_all.sh").read_text(encoding="utf-8")
    assert "V81|primary|v81/verify.py|quick|" in runner
    assert "V81|independent|v81/verify_independent.py|quick|" in runner
    assert "V81" in runner.split("FOCUSED_VERSIONS=(", 1)[1].split(")", 1)[0]
    manifest = (ROOT / "LATEX_MODULES.tsv").read_text(encoding="utf-8")
    assert "v81\tv81/V81_DEFICIENCY_CONSERVATION_THEOREM.tex" in manifest

    total = sum(row["conservation_checks"] for row in committed["v80_census"].values())
    assert total == 22528
    for row in committed["v80_census"].values():
        assert row["minimum_neighborhood_witness_is_lagrangian_supported"] is False
        assert row["lagrangian_supported_deficient_cardinalities"] == [row["m"]]
    half = committed["structured_controls"]["rank_one_half_tight"]
    assert [0, 2, 2] in half["balanced_low_width_census"]["distinct_conservation_triples"]

    print(
        "V81 primary verification passed: conservation, balanced width-deficiency, "
        "Minimum p-Union curves, and unsupported Lagrangian Hall points remain preserved."
    )


if __name__ == "__main__":
    main()
