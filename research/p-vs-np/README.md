# NC0_k-Avoid Laboratory

> Structural and algorithmic research on range avoidance for local Boolean circuits. This is **not** an active route to resolving P versus NP.

## Start here

- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable claims, reproducibility, outreach and promotion ledger.
- [`v62/INTEGRATED_MANUSCRIPT.md`](v62/INTEGRATED_MANUSCRIPT.md) — integrated manuscript.
- [`v64/`](v64/) — formal V57 theorem/specification and workflow audit.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

Laboratory V64 converts the V57 bijunctive obstruction into a standalone LaTeX theorem/proof module and a normative JSON specification. Two verifiers independently exhaust all 16 assignments, verify complete block and clause irredundancy, regenerate the 48-element NPN orbit of `0x07`, and check the five local gate masks.

Separately, the GitHub Actions workflow moves from `actions/checkout@v4` to `actions/checkout@v6` after an official-source compatibility audit. Runtime maintenance remains distinct from mathematical validation.

External review requests remain pending. No response, silence or negative search is evidence of novelty.

## Contribution chain

| Version | Main contribution | Status |
|---|---|---|
| V16–V27 | Finite classifications and proof candidates | Historical/supplementary |
| V53 | Corrected union-free line and retractions | Partially preserved |
| V54 | Pure-`AND_k` degree separator | Verified; overlap recorded |
| V56 | Affine consistency-or-redundancy | Verified; novelty unconfirmed |
| V57 | Orbit-`0x07` block-irredundancy and direct sums | Verified construction |
| V58 | Orientation depth and parameterized avoidance | Verified; novelty unconfirmed |
| V59–V60 | Geometry, barriers and randomized regime | Verified/context |
| V61–V63 | Reproducibility, manuscript, outreach and CI promotion | Verified |
| V64 | Formal V57 module and checkout v6 maintenance | Current laboratory |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> non-draft PR -> quick/full CI -> squash merge to main`. V22 remains a justified skip because its original serialized certificate dataset is absent.
