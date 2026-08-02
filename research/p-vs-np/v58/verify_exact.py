#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "exact_single_flip_search.cpp"
COMMITTED_CSV = ROOT / "EXACT_SEARCH_RESULTS.csv"
COMMITTED_SUMMARY = ROOT / "EXACT_SEARCH_SUMMARY.json"


def main() -> None:
    expected_summary = json.loads(COMMITTED_SUMMARY.read_text(encoding="utf-8"))
    threads = int(expected_summary["threads"])

    with tempfile.TemporaryDirectory(prefix="v58-exact-") as temp_dir:
        binary = Path(temp_dir) / "exact_single_flip_search"
        compile_command = [
            "g++",
            "-O3",
            "-std=c++17",
            "-fopenmp",
            str(SOURCE),
            "-o",
            str(binary),
        ]
        try:
            subprocess.run(
                compile_command,
                check=True,
                capture_output=True,
                text=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            raise SystemExit(f"cannot compile exact verifier: {exc}") from exc

        run = subprocess.run(
            [str(binary), "3", "8", "500000000", str(threads)],
            check=True,
            capture_output=True,
            text=True,
            timeout=240,
        )

    actual_csv = run.stdout.strip() + "\n"
    expected_csv = COMMITTED_CSV.read_text(encoding="utf-8").strip() + "\n"
    assert actual_csv == expected_csv

    rows = list(csv.DictReader(actual_csv.splitlines()))
    assert len(rows) == 12
    assert all(
        row["found_counterexample"] == "0" and row["complete"] == "1"
        for row in rows
    )

    actual_summary = {
        "n_min": 3,
        "n_max": 8,
        "canonical_types": [1, 3],
        "cases": len(rows),
        "counterexamples": 0,
        "all_complete": True,
        "total_nodes": sum(int(row["nodes"]) for row in rows),
        "threads": threads,
    }
    assert actual_summary == expected_summary

    print("V58 exact verifier passed:")
    print("  complete symmetry-reduced search for n=3..8;")
    print("  both normalized first-block types checked;")
    print(f"  {actual_summary['total_nodes']} DFS nodes; zero one-flip counterexamples;")
    print("  committed exact evidence matches without writing repository artifacts.")


if __name__ == "__main__":
    main()
