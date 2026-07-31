# NC0_k-Avoid Laboratory V67

## Overlap growth, direct-sum elimination, and computable branching bounds

**Scientific status:** internally verified finite experiment plus one elementary structural proposition. The laboratory is not peer reviewed, does not establish novelty, does not prove an asymptotic branching bound, does not solve unrestricted `NC0_3-Avoid`, and does not resolve P versus NP.

## Contributions

1. **Direct-sum proposition.** For affine-cell branching systems on disjoint variables,
   `c(A ⊕ B)=c(A)c(B)`. A tree for `A` followed by a tree for `B` at each consistent leaf gives
   `L_aff(A ⊕ B) <= L_aff(A)+c(A)(L_aff(B)-1)`.
   Consequently direct sums of V57 components, each with `c=1`, retain `c=1` and admit an additive leaf upper bound. This eliminates V57 direct sums as a source of consistent-branch growth, but it does not eliminate direct sums of arbitrary components with `c>1`.

2. **Regular overlap controls.** Two explicit cyclic support patterns with `m=n+1` were checked for every `4<=n<=12`. Both have `c=1` throughout. This is evidence about those patterns only, not a theorem about all overlap chains.

3. **Random overlap growth.** A deterministic seed-42 probe samples 4,000 positive-fiber `0x07` systems with ordered three-variable supports and `m=n+1`.
   It preserves a `c=16` witness at `n=10` and finds a stronger `c=36` witness at `n=11`.

4. **Computable sandwich.** Every experiment records
   `c <= L_aff <= L_greedy`.
   For the preserved witnesses:
   - `n=10`: `16 <= 25 <= 25`, with selected-policy `G_aff=47`;
   - `n=11`: `36 <= 61 <= 62`, with selected-policy `G_aff=108`.

## Reproduce

```bash
python v67_branch_growth_probe.py
python verify.py
python verify_independent.py
```

From the parent directory:

```bash
bash ./verify_all.sh
bash ./verify_all.sh --full
```

## Files

- `v67_branch_growth_probe.py` — seeded search and tree calculations;
- `DIRECT_SUM_PROPOSITION.md` — exact structural statement and proof;
- `BRANCHING_SANDWICH.md` — lower/upper bounds used for scalable searches;
- `OVERLAP_GROWTH_REPORT.md` — experimental scope and witnesses;
- `WITNESSES.json` — exact supports, partitions, signatures, and metrics;
- `RESULTS.json` — generated summary;
- `verify.py` and `verify_independent.py` — primary and independent validation;
- `V68_CORE_CONTEXT.md` — frozen next-laboratory tasks.
