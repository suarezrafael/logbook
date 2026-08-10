# Laboratory V94 — fixed-language child-count comparison

## Classification

V94 is a **barrier laboratory with a tractable control branch**. It replaces the
closed V93 global-affine-certificate search with the actual V92 primitive

```text
Delta(C,p,j)=N(p0)-N(p1).
```

The laboratory obtains a theorem-level barrier for arbitrary prefixes and a
polynomial exact comparator for affine circuits, while preserving the required
separation from canonical prefixes.

## Main theorem

There is an explicit fixed language `Gamma_V94` with nine gate types of maximum
arity three such that deciding

```text
N_C(p0) <= N_C(p1)
```

for an arbitrary supplied prefix `p` is PP-complete even for

```text
NC0_3 circuits with m=n+1.
```

The hardness reduction is exact up to one common power-of-two factor. It
compiles a pair of 3-CNF counting instances using:

```text
DEF(z,l2,l3):  z = l2 OR l3,
COND(s,c,l1,z): inactive off selector branch c, clause-enforcing on branch c,
PROJ(s):        the compared next output.
```

One auxiliary is uniquely determined per source clause. Optional free dummies
make the final stretch exactly one without changing the comparison.

## Why this does not prove canonical hardness

The reduction fixes every `DEF` output to `1`. But a `DEF` truth table has four
ones and four zeros, so when one is ordered first the two empty-prefix child
counts tie. V92's rule chooses `0` on a tie.

Therefore the explicit PP-hard prefix diverges from the canonical prefix at the
first bit. V94 records this as a mandatory separation theorem, not as a defect
to hide.

What remains open is whether canonical prefixes possess enough structure to
avoid this arbitrary-prefix barrier, or whether a different hardness compiler
can be made canonical.

## Positive control — affine circuits

When every local gate is affine, every prefix is a linear system over `GF(2)`.
Gaussian elimination gives both child counts exactly. An incremental row basis
makes the canonical rule especially simple:

- independent next row -> equal children -> choose `0`;
- dependent next row -> one bit forced -> choose the opposite, empty child;
- after the fiber is empty -> append zeros.

Hence affine `NC0_3-Avoid[n,n+1]` has a deterministic polynomial-time canonical
avoider. This is a control result consistent with the classical affine #CSP
tractability theorem; no novelty is claimed.

## Finite implementation audit

```text
arbitrary-prefix compiler:
  4,096 ordered signed-clause pairs
  0 exact-count mismatches
  0 stretch-one mismatches

affine comparator:
  65,536 affine 3-input / 4-output circuits
  262,144 child decisions
  0 brute-force count mismatches
  0 incremental-output mismatches
  0 canonical outputs in the range
```

These are regression gates only. The proof is in `THEOREMS.md`.

## Scientific consequence

V94 explains why replacing Huang-Li-Zhong's traversed-space evaluation with a
polynomial **all-prefix exact counter/comparator** is too strong a target: for a
fixed ternary local language, that primitive already captures PP on arbitrary
prefixes.

This does not rule out a faster avoidance algorithm. It narrows the next useful
question to one of two routes:

1. exploit the special structure of V92-generated canonical prefixes; or
2. construct an avoided output without solving exact child comparison on every
   step.

## Files

- `child_count_comparison.py` — exact compiler, affine comparator, deterministic audits;
- `THEOREMS.md` — PP-completeness reduction, canonical separation, affine theorem;
- `LITERATURE_BOUNDARY.md` — source calibration and non-implications;
- `RESULTS.json` — immutable finite regression snapshot;
- `IMPLICATION.json` — implication-ratio declaration;
- `verify.py`, `verify_independent.py` — primary and independent checks;
- `V95_CORE_CONTEXT.md` — next theorem-native target.

## Nonclaims

V94 does not prove that canonical-prefix comparison is PP-hard, that range
avoidance is PP-hard, that exact comparison is necessary for avoidance, that
P differs from PP, that P differs from NP, or that the V94 theorem is novel or
peer reviewed. It does not improve the current all-instance `NC0_3-Avoid`
runtime baseline.
