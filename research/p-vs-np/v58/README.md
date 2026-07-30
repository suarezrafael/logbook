# P versus NP Laboratory V58

## Adaptive orientation depth for bijunctive Range Avoidance

**Scientific status:** internally proved, adversarially audited and independently verified. Not peer reviewed. Novelty is not established. This package does not solve general `NC0_3-Avoid`, prove unrestricted circuit lower bounds, or resolve P versus NP.

## Main result

For a circuit image `S` and a baseline output `b in S`, define the orientation depth as the Hamming distance from `b` to the internal vertex boundary of `S`.

For bijunctive output fibers:

```text
orientation depth d
        -> enumerate orientations within distance d
        -> test 2-SAT consistency and block entailment
        -> construct an absent output
```

The running time is `m^{O(d)} poly(n+m)`.

A one-flip failure is exactly the condition that the radius-two Hamming ball around the baseline is contained in the image.

## Exact 0x07 audit

A complete symmetry-reduced search found no one-flip counterexample for:

```text
3 <= n <= 8
m = n + 1
```

The search is reproduced by `verify_exact.py` and `exact_single_flip_search.cpp`.

The exact status of `n=9` is open in this package.

## V57 reclassification

The 12 finite irredundant families from V57:

- form one variable-isomorphism class;
- all have orientation depth one;
- all 60 single flips create three or four redundant blocks.

The V57 direct-sum family also has depth one for every size.

## Reproduce

```bash
python verify.py
python verify_independent.py
python verify_exact.py
```

Expected summaries are committed in:

- `VALIDATION_PRIMARY.txt`;
- `VALIDATION_INDEPENDENT.txt`;
- `VALIDATION_EXACT.txt`.

## Output-quality files

- `SCIENTIFIC_STATUS.md`;
- `THEOREM.md` and `PROOF.md`;
- `ORIENTATION_DEPTH.md`;
- `SINGLE_FLIP_AUDIT.md`;
- `LAY_SUMMARY.md`;
- `PROMOTION_INDEX.md`;
- `PROGRESS_INDEX.md`;
- `DISTANCIA_ATE_P_VS_NP.md`;
- `FIELD_SURVEY.md`;
- `EXTERNAL_CONTACT_STATUS.md`;
- `V59_CORE_CONTEXT.md`.
