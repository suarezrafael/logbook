from __future__ import annotations

import json
from pathlib import Path


EXPECTED_MISSING = {"001", "010", "100", "111"}
EXPECTED_ALLOWED = {"000", "011", "101", "110"}


def main() -> None:
    results = json.loads(
        Path(__file__).with_name("RESULTS.json").read_text(encoding="utf-8")
    )

    catalogue = results["catalogue"]
    experiments = results["experiments"]
    status = results["scientific_status"]

    assert results["version"] == "V27"
    assert catalogue["hard_functions"] == 1280
    assert catalogue["distinct_nonconstant_vectors"] == 640
    assert catalogue["complement_pairs"] == 640
    assert catalogue["noncomplement_affine_triples"] == 5120
    assert catalogue["smallest_relation_size"] == 3
    assert set(catalogue["missing_outputs"]) == EXPECTED_MISSING
    assert set(catalogue["allowed_outputs"]) == EXPECTED_ALLOWED
    assert experiments["benchmark_cases"] == 96
    assert experiments["failures"] == 0
    assert experiments["independent_verification"] is True
    assert status["peer_reviewed"] is False
    assert status["novelty_confirmed"] is False
    assert status["p_vs_np_resolved"] is False

    print("V27 index checks passed.")


if __name__ == "__main__":
    main()
