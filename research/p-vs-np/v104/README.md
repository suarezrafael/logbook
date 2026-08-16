# Laboratory V104 — canonical affine-first hybrid compression

## Status

Official V104 candidate theorem package. Internally proved and adversarially
audited; repository promotion gates are pending. Novelty, priority, and peer
review are not established. V103 is promoted and merged on `main`.

## Main result

V104 removes the supplied-certificate caveat. It defines a deterministic,
polynomial-time preprocessing rule:

1. choose every output's canonical target bit (minority value, tie to zero);
2. greedily build a rank-increasing basis of the canonical affine-hull blocks;
3. **protect** every input variable appearing in the retained affine equations;
4. scan the remaining outputs in order and greedily add a canonical functional
   anchor only when its head is unprotected, unused, and preserves acyclicity.

Let `R` be the affine basis rank and `f` the number of functional heads chosen by
this canonical rule. Define

```text
eta_AF(C) = n - R - f.
```

The preprocessing is polynomial. V104 then deterministically constructs a word
outside the range in

```text
O(2^eta_AF(C) poly(N)).
```

Thus `eta_AF=O(log N)` is a fully algorithmic polynomial-time regime; no
structural certificate needs to be supplied by the caller.

## Why affine-first is safe

Every variable occurring in a retained affine equation is protected from
becoming a functional head. Therefore all retained affine equations remain
supported entirely on the eventual functional roots. Their rank is still `R`.

The functional DAG leaves `n-f` roots and every root assignment extends uniquely
through the total functional graph relaxations. The protected affine system
cuts the root cube to exactly

```text
2^(n-f-R) = 2^eta_AF
```

assignments. If `s_A` affine output blocks were retained, then `s_A<=R`, so the
number of unselected outputs satisfies

```text
m - f - s_A >= m - f - R > n - f - R = eta_AF.
```

Evaluating the original residual gates on the relaxed domain and choosing a
missing residual word therefore produces an avoided output.

If the canonical affine-hull system is inconsistent, the complete canonical
target vector gives an immediate missing word; if a canonical fiber is empty,
its target coordinate is immediately absent.

## Strict exact-stretch family

For every `k>=1`, take `n=8k` inputs and `m=n+1` outputs.

The first `4k` variables carry a cyclic `0x1e` graph-of-OR block. The second
`4k` variables carry the V103 `0x16` parity-hull block of rank `4k-1`. Add one
majority output inside the second block and one majority output crossing the
blocks.

The canonical affine-first procedure automatically behaves as desired:

- the affine basis consists of the `4k-1` `0x16` blocks and protects the second
  group of variables;
- the `0x1e` outputs have full canonical affine hull, so they do not consume
  affine rank;
- the functional scan then selects the first `4k-2` `0x1e` graph relations;
- the two majority outputs have no functional anchor.

Hence

```text
R       = 4k-1,
f       = 4k-2,
eta_AF  = 3,
```

so the relaxed domain always has eight assignments and four residual outputs.

On the same connected family:

```text
lambda(V97) = 8k,
mu(V101)     = k+3,
beta(V102)   = Theta(k), with 3k <= beta <= 7k,
nu(V103)     = 4k+1,
eta_AF(V104) = 3.
```

This is a strict asymptotic separation from all four preceding structural
parameters using a parameter that is discovered by the algorithm itself.

## Falsification completed before candidate registration

- strict family checked against the complete original range for `k=1` (`n=8`)
  and `k=2` (`n=16`);
- structural rank/connectivity identities checked through `k=20`;
- 712 random mutations of the four residual outputs checked against the complete
  original range, with zero counterexamples;
- the canonical affine-first algorithm checked on **1,800** random circuits with
  `2<=n<=7`, `m=n+1`, against complete brute-force ranges, with zero
  counterexamples;
- the canonical procedure returned `eta_AF=3` on the strict family for
  `k=1,...,7`;
- primary and independent implementations include an explicit inconsistent-hull
  canonical-witness regression.

The committed primary verifier calls the canonical implementation directly. The
independent verifier reimplements the affine basis, protection rule, functional
scan, rank reduction, and missing-word construction without importing the V104
canonical engine. These are now registered in the official focused runner, and
the standalone theorem module is registered in the LaTeX manifest.

## Next obstruction

The frozen V105 handoff gives a switching-unbalanced cyclic signed-majority
family for which affine hulls and functional anchors are both blind:

```text
lambda = n,
mu = n,
beta = ceil(2n/3),
nu = n,
eta_AF = n.
```

The next useful question is therefore not another ordering heuristic. It is
whether one-hit conditioning of majority can be composed into one globally
missing output, or whether that branch-composition primitive has a rigorous
hardness barrier.

## Literature boundary

Affine hulls, Gaussian elimination, functional dependencies, and greedy
acyclicity checks are standard ingredients. The targeted primary-source search
did not locate this exact affine-first protection rule for Range Avoidance, but
that absence is not evidence of novelty. No novelty claim is made.

## Nonclaims

`eta_AF(C)` can still be linear in the worst case. V104 does not prove
unrestricted `NC0_3-Avoid` is in P, does not improve the unrestricted published
worst-case exponent, does not establish a new circuit lower bound, and does not
resolve P versus NP.
