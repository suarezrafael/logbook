# P versus NP Laboratory V55

## Affine-fiber block redundancy for ternary Range Avoidance

**Scientific status:** internally proved and independently verified research
package. Not peer reviewed. Novelty is not established. This work does not
solve general `NC0_3-Avoid`, prove an unrestricted circuit lower bound, or
resolve P versus NP.

## Main result

The essential ternary NPN class with canonical mask `0x18` has an active fiber
formed by two antipodal assignments. Every output gate is equivalent to a
block of two affine parity equations.

All lifted equation rows lie in an `n`-dimensional augmented subspace. Hence,
when `m>n`, one complete gate block is implied by the others. Requesting the
implying gates to be active and the implied gate to be inactive constructs a
missing output in deterministic polynomial time.

This gives a stretch-one algorithm for a genuinely ternary, nonmonotone NPN
class beyond the singleton-fiber orbit treated in V54.

## General theorem

For any circuit in which every output has a nonempty affine fiber, block
redundancy gives deterministic Range Avoidance when

```text
m>n+1.
```

The theorem allows arbitrary mixtures of affine-fiber ternary NPN classes.

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

## Reproduce

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

- `THEOREM.md` — theorem statements and scope;
- `PROOF.md` — detailed proofs;
- `NPN_CLASSIFICATION.md` — all 14 classes and algorithmic routes;
- `AFFINE_FIBER_METHOD.md` — executable algorithm specification;
- `CLASSIFICATION.json` — machine-readable catalogue;
- `CERTIFICATES.json` — serialized finite certificates;
- `v55_core.py` — primary implementation;
- `verify.py` and `verify_independent.py` — independent audits;
- `V56_CORE_CONTEXT.md` — next research program.
