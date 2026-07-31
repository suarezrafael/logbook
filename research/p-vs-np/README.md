# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable claims, reproducibility, outreach and promotion ledger.
- [`v62/INTEGRATED_MANUSCRIPT.md`](v62/INTEGRATED_MANUSCRIPT.md) — integrated manuscript.
- [`v66/`](v66/) — affine-cell branching experiment on the non-affine ternary frontier.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

Laboratory V66 models each non-affine ternary fiber as a disjoint union of two affine cells and measures inconsistency-pruned adaptive branching. It reproduces all 243 affine-cell partition systems of the V57 gadget, performs an exact NPN-expanded three-variable signature-state census, exhausts 40,920 canonical four-gate systems, and records a deterministic 50,000-sample four-variable stress test.

The exact `n=3` experiments show strong finite pruning: at most four consistent complete branches in the full state census, maximum `L_aff=11`, and maximum selected-policy `G_aff=17` in the canonical tree census. These are finite results, not an asymptotic polynomial branching theorem.

V66 also closes three validation gaps: promoted-era verifiers cannot be omitted silently from the runner; quick/full transcripts are uploaded as workflow artifacts; and the standalone V64/V65 LaTeX modules are compiled in CI.

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
| V61–V65 | Reproducibility, manuscript, outreach, CI and formal modules | Verified |
| V66 | Affine-cell branching census and CI coverage hardening | Current laboratory |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> non-draft PR -> quick/full CI -> squash merge to main`. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
