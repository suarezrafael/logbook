# P versus NP Laboratory V55

> **Strengthened by V56.** The V55 block-subspace theorem and all finite classifications remain valid. V56 improves the general mixed affine-fiber threshold from `m>n+1` to the minimum positive stretch `m>n` by first separating the inconsistent case and then translating a common solution to remove the augmented constant coordinate. Use `research/p-vs-np/v56` for the strongest current statement.

## Affine-fiber block redundancy for ternary Range Avoidance

**Scientific status:** internally proved and independently verified research package. Not peer reviewed. Novelty is not established. This work does not solve general `NC0_3-Avoid`, prove an unrestricted circuit lower bound, or resolve P versus NP.

## Preserved V55 results

The essential ternary NPN class with canonical mask `0x18` has an active fiber formed by two antipodal assignments. Every output gate is equivalent to a block of two affine parity equations. V55 proved a stretch-one algorithm for this genuinely ternary, nonmonotone class.

V55 also proved the general augmented-space statement:

```text
If every output has a nonempty affine fiber, m>n+1 suffices.
```

That statement is correct but no longer optimal. V56 proves `m>n` for arbitrary mixtures by a consistency-or-redundancy dichotomy.

## Classification

All 256 ternary truth tables were partitioned into 14 NPN classes.

Essential affine classes:

```text
0x01, 0x06, 0x18, 0x69.
```

Essential non-affine frontier:

```text
0x07, 0x16, 0x17, 0x19, 0x1b, 0x1e.
```

## Reproduce V55

```bash
python verify.py
python verify_independent.py
```

Expected summary:

```text
V55 primary verification passed:
  14/14 ternary NPN classes classified;
  4096 exhaustive antipodal-pair stretch-one circuits;
  360 random antipodal-pair stretch-one circuits;
  280 mixed affine-fiber n+2 circuits;
  160 distance-two-pair n+2 circuits;
  250 parity3 stretch-one circuits;
  550 abstract block-subspace regressions; zero failures.

V55 independent verification passed:
  14 ternary NPN classes rebuilt;
  4096 antipodal-pair circuits rechecked exhaustively;
  19 serialized certificates reconstructed;
  140 fresh random stretch-one circuits; zero failures.
```

## Files

- `THEOREM.md` — V55 theorem statements and the V56 strengthening notice;
- `PROOF.md` — detailed V55 proofs;
- `NPN_CLASSIFICATION.md` — all 14 classes and algorithmic routes;
- `AFFINE_FIBER_METHOD.md` — V55 augmented-space algorithm;
- `CLASSIFICATION.json` — machine-readable catalogue;
- `CERTIFICATES.json` — serialized finite certificates;
- `v55_core.py` — primary implementation;
- `verify.py` and `verify_independent.py` — independent audits;
- `V56_CORE_CONTEXT.md` — historical context, now annotated with the V56 outcome.
