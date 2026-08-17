# V106 — adaptive pair repair for signed-majority range avoidance

V106 extends V105 by allowing a bounded number of signed-majority gates to use
one of their two noncanonical pair clauses before the V105 odd-handcuff detector
is run.

## Main parameter

`σ(C)` is the minimum number of gates whose canonical pair must be changed so
that the selected signed pair graph contains a V105-detectable barbell or
figure-eight with two odd transport cycles.

Enumerating all repair sets of size at most `k` gives

```text
O((2m)^k poly(N))
```

time.  Hence constant `σ` is a deterministic polynomial-time regime.

## Strict family

`strict_one_repair_family(q)` has

```text
n = 5 + 2q,
m = n + 1.
```

The canonical selected graph has a theta core with cycle transport signature
`(0,1,1)`, so V105 rejects it.  Exactly one one-gate repair works: gate 4 changes
from canonical pair `(1,3)` to pair `(3,4)`, producing a figure-eight whose two
cycles are odd.  Thus

```text
σ = 1.
```

For this family the V102 strong-affine-backdoor size is exactly

```text
β = q+4 = (n+3)/2,
```

while signed-majority's V101/V103/V104 obstructions keep

```text
μ = n,
ν = n,
η_AF = n.
```

The family is switching-unbalanced.  It is also minimally positive-surplus: the
full set has `m=n+1`, while deleting any one output leaves a support-system
perfect matching.  Therefore every proper output subset satisfies Hall.

## Hall ↔ frame-matroid bridge

Every majority gate supplies three candidate pair edges whose transport labels
XOR to one.  The candidate triangle is therefore unbalanced.  For any subfamily
`F`, every connected component of the union of **all** its candidate pairs is
unbalanced, so its signed-frame rank equals `|N(F)|`.

Rado's matroid transversal criterion consequently reduces to the ordinary Hall
inequalities on output supports.  This identifies the high-value next question:
minimal positive surplus lies exactly one edge beyond the frame-independent
transversal threshold.  Can that forced colorful dependence always be converted
into an odd handcuff, or can balanced cycles remain unavoidable?

## Verification

`verify.py` is the primary implementation verifier.  It checks complete original
ranges for the small strict-family instances, exact one-repair uniqueness,
`β=(n+3)/2`, proper-surplus controls, and single-deletion Hall matchings.

`verify_independent.py` does not import the V106 algorithm.  It reconstructs the
family and target independently, checks the contradiction through a separate
2-SAT SCC implementation, brute-forces small original ranges, verifies the
canonical theta signature, and audits the frame-rank/neighborhood identity on
all subfamilies of the first instances.

## Scientific boundary

V106 is a parameterized extension, not an all-signed-majority theorem.  It does
not show `σ=O(1)` (or even sublinear) for arbitrary circuits.  It does not solve
unrestricted `NC0_3-Avoid`, improve the general published worst-case exponent,
establish a new circuit lower bound, or resolve P versus NP.
