# NC0_k-Avoid Laboratory

> Structural research on Range Avoidance and circuit lower-bound interfaces. The project is motivated by P versus NP, but it does **not** claim a direct route or a solution.

## Start here

- [STATE.md](STATE.md) — cumulative scientific state.
- [LEDGER.json](LEDGER.json) — machine-readable claims, reproducibility, outreach and promotion ledger.
- [`v62/INTEGRATED_MANUSCRIPT.md`](v62/INTEGRATED_MANUSCRIPT.md) — integrated manuscript.
- [`v67/`](v67/) — direct-sum proposition and overlap growth witnesses.
- [`v68/`](v68/) — explicit spine family separating branching trees from projected residual DAGs.
- [`verify_all.sh`](verify_all.sh) — cumulative quick/full verifier.

## Current position

Laboratory V68 answers the tree-side question left open by V66–V67.

For every `k>=1`, an explicit stretch-one family in the NPN orbit of `0x07` has

```text
n=2k+1
m=n+1
c=2^(k-1)=2^((n-3)/2)
```

Therefore every complete inconsistency-pruned affine-cell branching tree has exponentially many consistent leaves on this family.

The same family is linear in a stronger projected residual-state model: after existentially removing variables absent from remaining supports, the fixed ordered DAG has exactly

```text
G_proj=3k+4
```

nonterminal states. `G_proj` is distinct from the historical `G_aff`; no equivalence to OBDD, FBDD, resolution, Res-Lin, or another standard proof system is claimed.

V67 remains important: direct sums of V57 components have `c=1`, while overlapping supports produced the finite `c=36` witness whose frozen and factorized structure motivated the spine construction.

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
| V66 | Exact affine-cell census and CI hardening | Merged and CI verified |
| V67 | Direct-sum proposition and overlap growth witnesses | Merged and CI verified |
| V68 | Exponential spine-tree lower bound and linear projected DAG | Current laboratory |

## Reproducibility and promotion

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

Each laboratory follows `main -> branch -> non-draft PR -> quick/full/LaTeX CI -> squash merge to main`. V22 and V26 remain justified skips. The direct P-versus-NP route remains inactive.
