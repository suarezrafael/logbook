# Laboratory V103 — affine-hull rank compression

## Status

Candidate theorem package. Internally proved, adversarially audited, and checked
by primary and independent verifiers. Not peer reviewed. Novelty and priority
are not established. V103 does not solve unrestricted `NC0_3-Avoid`, does not
improve the Huang--Li--Zhong all-instance worst-case exponent, and does not
resolve P versus NP.

## Main theorem

Let

```text
C : {0,1}^n -> {0,1}^m,  m>n.
```

For each output gate choose a canonical target bit: the minority output value,
with tie broken toward zero. Let `F_i` be that target fiber and replace it by its
affine hull `aff(F_i)` over `GF(2)`. This is a safe relaxation because

```text
F_i subseteq aff(F_i).
```

If a canonical fiber is empty, its target bit is already an avoided coordinate.
If all canonical affine hull equations are inconsistent, the full canonical
target word is absent.

Otherwise let `R(C)` be the coefficient rank of the combined affine-hull system
and define

```text
nu(C) = n - R(C).
```

Greedily retain an output block only when its hull equations increase rank. If
`s` outputs are retained, then `s<=R`. The retained relaxed system has exactly
`2^nu` assignments. After deleting the retained output coordinates, at least

```text
m-s >= m-R > n-R = nu
```

output bits remain. Evaluate those original gates on the `2^nu` relaxed
assignments and choose a residual word not observed. Reinserting the retained
target bits gives an avoided output for the original circuit.

Thus V103 constructs a missing word deterministically in

```text
O(2^nu poly(N)).
```

In particular `nu=O(log N)` is a polynomial-time regime. Unlike V101, cycles
among the local relations are harmless: they are solved simultaneously by
global rank over `GF(2)`.

## Exact ternary consequence

Among the 218 essential ternary truth tables, the canonical target fiber has a
proper affine hull for exactly **162** tables. The remaining **56** are exactly
the balanced non-affine predicates.

The symbolic reason is simple. An unbalanced canonical minority fiber has at
most three cube vertices, so its affine hull has dimension at most two. A
balanced four-point fiber has a proper affine hull exactly when its four points
form an affine plane; then the complementary fiber is the other coset and the
predicate is affine. Therefore a balanced non-affine predicate has full affine
hull on both fibers.

For canonical `0x16` (EXACT-ONE), target one has fiber

```text
{001,010,100}
```

and affine hull

```text
x0 XOR x1 XOR x2 = 1.
```

This local relaxation adds the fourth point `111` but contributes one exact
rank equation.

## Strict separation from V97, V101, and V102

For every `k>=1`, set `n=4k`. Gadget `j` uses variables

```text
a_j,b_j,c_j,d_j.
```

Add canonical `0x16` gates on

```text
(a_j,b_j,c_j)
(a_j,b_j,d_j)
(a_j,c_j,d_j)
```

and, for every `j>=1`, a bridge gate on

```text
(d_(j-1),b_j,c_j).
```

There are `4k-1=n-1` such gates. Add two `0x17` signed-majority outputs, one on
the first gadget and one on the last, so `m=n+1`.

Every `0x16` target-one hull contributes parity `=1`. The three internal
equations imply

```text
a_j=1,
b_j=c_j=d_j=t_j.
```

Every bridge then forces `t_(j-1)=1`. Hence

```text
t_0=...=t_(k-2)=1,
t_(k-1) is free.
```

The affine relaxed system has exactly two points, rank `n-1`, and

```text
nu=1.
```

The same family has exact previous parameters:

```text
V97:  lambda = 4k = n
V101: mu     = k+1
V102: beta   = 3k
V103: nu     = 1
```

For V97, the support is connected and every input has degree at least two, so no
unused/leaf/unary reduction applies. V100 performs zero local graph peels because
`0x16` and `0x17` are residual hard orbits.

For V101, each gadget's three internal triples have at most two distinct maxima
in any topological order, and each bridge contributes at most one new head, so
at most `3k-1` anchors can be selected. This bound is achieved by an explicit
acyclic orientation, leaving exactly `k+1` roots.

For V102, every `0x16` gate requires at least two support variables in a strong
affine backdoor. The three internal triples force at least three selected
variables per gadget. Selecting `b_j,c_j,d_j` for every gadget attains the bound
and also handles all bridges and both majority outputs, so `beta=3k`.

This is a strict infinite-family separation from all three preceding structural
parameters, rather than another local truth-table census.

## Validation

Primary verifier:

- exact census `218 = 162 proper + 56 full`;
- `0x16` hull recomputation;
- 1,080 seeded random circuits cross-checked against complete range enumeration;
- strict family brute-forced through `k=4` and rank-checked through `k=20`;
- V101 `mu=k+1` upper and matching lower construction checked through `k=19`;
- V102 `beta=3k` local and global certificates checked through `k=19`.

Independent verifier:

- recomputes affine-hull codimension without importing the V103 engine;
- rank-checks the strict family through `k=40`;
- directly enumerates the two relaxed solutions through `k=4`;
- audits 360 additional random circuits by a separate exhaustive-domain method.

Both verifiers report zero failures.

## Literature boundary

Affine hulls and Gaussian elimination are elementary linear-algebra tools, and
V56 already used exact affine fibers internally. The V103 move is different:
it safely enlarges an arbitrary chosen fiber to its affine hull and then uses
global block rank to keep at most `R` target coordinates before enumerating the
`n-R` dimensional relaxed domain.

The targeted external search covered ECCC TR22-102, TR23-072, TR23-193,
TR25-034, and TR25-049. These works establish important range-avoidance
algorithms, reductions, and related affine variants, but the search did not
locate this exact affine-hull-rank parameterization. That absence is not evidence
of novelty; no novelty claim is made pending expert prior-art review.

## Next frontier

V103 does not bound `nu(C)` in the worst case. Its local blind spot is exactly
the 56 balanced non-affine essential ternary predicates whose canonical fibers
have full affine hull. The next version should combine V101 functional graphs,
V102 backdoors, and V103 affine-hull rank, or construct an explicit family where
`lambda`, `mu`, `beta`, and `nu` are all linear and isolate a genuinely new
compressible invariant.
