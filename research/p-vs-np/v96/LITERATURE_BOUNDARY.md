# V96 literature boundary

## 1. Huang--Li--Zhong, ITCS 2026

Huang, Li, and Zhong, *Range Avoidance and Remote Point: New Algorithms and
Hardness*, ITCS 2026, give an all-instance local algorithm for
`NC0_k-Avoid[n,n+1]` with running time

```text
O(n * 2^(((k-2)/(k-1))*n)).
```

For `k=3` this is

```text
O(n * 2^(n/2)).
```

V96 does not improve this running time.  Its universal-list upper bounds are
nonuniform existence theorems, not algorithms.

## 2. Guruswami--Lyu--Wang, APPROX/RANDOM 2022

Guruswami, Lyu, and Wang, *Range Avoidance for Low-Depth Circuits and
Applications*, construct explicit polynomial hitting sets for suitable
low-depth/local circuit regimes.  Their `NC0_k` instantiation requires

```text
m >= 2^(4k+1) n^(k-1) + n.
```

At `k=3` this becomes

```text
m >= 8192 n^2 + n,
```

which is far above exact minimal stretch `m=n+1`.

Therefore V96 must not cite the published hitting-set theorem as a constructive
solution at stretch one.  The V96 counting theorem applies at `n+1`, but loses
uniform explicitness; the published theorem has uniform explicitness, but in a
much larger-stretch regime.  That distinction is the central calibration.

## 3. Gajulapalli--Golovnev--Nagargoje--Saraogi, APPROX/RANDOM 2023

Gajulapalli, Golovnev, Nagargoje, and Saraogi, *Range Avoidance, Remote Point,
and Hardness Magnification*, prove a lower-bound transfer from an `FP^NP`
algorithm for an `NC0_3-Avoid` regime with output length

```text
m = n + n^(2/3)
```

to explicit rigidity/circuit-lower-bound consequences.

V96 uses this only as a **calibration of the missing uniformization bridge**.
If a stretch-one support-conditioned universal list were constructible in
`FP^NP`, NP range-membership queries would yield a stretch-one `FP^NP` avoider;
output truncation would then solve the larger-stretch regime as well.  V96 does
not obtain such a constructor and therefore does not claim the published
consequence has been triggered.

## 4. Boundary with V88/V90

Earlier laboratory stages found support-only existential counting lists in a
different restricted constructor model.  V96 does not relabel those results as
a constructive solution.  Its new contribution is a direct all-circuit
stretch-one counting theorem plus an explicit monotone-OR lower bound and a
uniformization transfer theorem.

## 5. Novelty discipline

The probabilistic-method union bound and the block-OR shattering construction
are elementary enough that V96 makes no novelty claim.  External prior-art
search is still required before treating either formulation as new.  The
laboratory result is useful internally because it sharply separates list
**cardinality**, list **uniform construction**, and final **absence testing**.
