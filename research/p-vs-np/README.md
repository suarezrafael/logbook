# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable claims, reproducibility, outreach and promotion ledger.
- [`v62/INTEGRATED_MANUSCRIPT.md`](v62/INTEGRATED_MANUSCRIPT.md) — integrated manuscript.
- [`v65/`](v65/) — formal V56 theorem and lower-bound route audit.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

Laboratory V65 formalizes the affine consistency-or-redundancy theorem and validates it by two independent methods. All multisets of `n+1` nonempty affine subsets are exhausted for `n<=3`, and larger random equation-block systems exercise both the inconsistent and redundant branches.

The laboratory also records the exact gap between the current local results and P versus NP. Range Avoidance is a genuine interface to circuit lower bounds, but the repository has neither a general `NC0_3-Avoid` algorithm nor a reduction yielding NP circuit lower bounds.

## Contribution chain

| Version | Main contribution | Status |
|---|---|---|
| V16–V27 | Finite classifications and proof candidates | Historical/supplementary |
| V53 | Corrected union-free line and retractions | Partially preserved |
| V54 | Pure-`AND_k` degree separator | Verified; overlap recorded |
| V56 | Affine consistency-or-redundancy | Verified; formally packaged in V65 |
| V57 | Orbit-`0x07` block-irredundancy and direct sums | Verified construction |
| V58 | Orientation depth and parameterized avoidance | Verified; novelty unconfirmed |
| V59–V60 | Geometry, barriers and randomized regime | Verified/context |
| V61–V64 | Reproducibility, manuscript, outreach, CI and formal V57 module | Verified |
| V65 | Formal V56 module and P-versus-NP route audit | Current laboratory |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> non-draft PR -> quick/full CI -> squash merge to main`. V22 and V26 remain justified skips.
