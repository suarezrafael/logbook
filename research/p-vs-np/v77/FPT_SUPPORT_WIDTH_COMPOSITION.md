# FPT composition for NC0_3-Avoid parameterized by support branchwidth

## 1. Support connectivity function

For a circuit with output-gate set `M`, define

```text
lambda_C(S)
  = |union_{i in S} supp(i) intersect union_{i notin S} supp(i)|.
```

Equivalently, each input variable contributes one exactly when it occurs in a
gate on both sides of the gate partition.

For every circuit, `lambda_C` is:

- normalized: `lambda_C(empty)=0`;
- symmetric: `lambda_C(S)=lambda_C(M\S)`;
- integer valued and nonnegative;
- submodular.

The last property follows because `lambda_C` is the sum, over input variables,
of the cut indicator of the set of gates containing that variable. Each such
indicator is a symmetric submodular function. Thus `lambda_C` is a
**connectivity function** in the sense used by branchwidth algorithms.

For fan-in at most three, one oracle query can be evaluated by scanning the
supports in `O(m)` time, or faster with precomputed incidence bitsets. Write
this oracle cost as `gamma`.

## 2. Prior-art decomposition discovery

For `m>1`, Korhonen and Oum prove that, given an integer `k` and oracle access
to a connectivity function on a ground set of size `m`, one can find a branch
decomposition of width at most `k`, or determine that none exists, in

```text
2^{O(k)} gamma m^6 log m + 2^{O(k^2)} gamma m
```

time. The abstract also states the valid simplified upper bound

```text
2^{O(k^2)} gamma m^6 log m.
```

Apply their theorem to `lambda_C`. If

```text
k = branchwidth(lambda_C),
```

the algorithm supplies a width-`k` gate branch decomposition. When `k` is not
known in advance, run the decision/construction algorithm for increasing
values of `k`; the total is dominated by the successful parameter value.

Fomin and Korhonen's earlier factor-two FPT framework gives an approximate
alternative, but it is not needed for the exact composition below.

## 3. Composition with V77, V75, and V74

If `m<=1`, then `m>n` leaves only a constant-size instance and direct output
enumeration finds an avoided word. Assume `m>1`. Starting from the decomposition
produced by Korhonen--Oum:

1. V77's restricted topology-tree transfer produces a rooted binary gate tree
   with width at most `2k`, height `O(log m)`, and external path length
   `O(m log m)`.
2. V75 compiles the V74 weighted residual recurrence on that tree into a
   monotone arithmetic DAG.
3. V74's exact prefix-count identity chooses a zero-preimage branch at each
   output coordinate. When `m>n`, the final word is outside the circuit range.

Therefore `NC0_3-Avoid`, parameterized by support connectivity branchwidth
`k`, has running time

```text
2^{O(k)} gamma m^6 log m
  + 2^{O(k^2)} gamma m
  + O(m log m A(2k)^2 poly(n,m)).
```

A simpler but weaker display is

```text
2^{O(k^2)} gamma m^6 log m
  + O(m log m A(2k)^2 poly(n,m)).
```

Since `gamma=O(m)` for explicit fan-in-three supports and `A(2k)` depends only
on `k`, this is fixed-parameter tractable in `k`.

## 4. Theorem

**Theorem (support-branchwidth FPT avoidance).** Let `C:{0,1}^n -> {0,1}^m`
be an explicitly represented fan-in-at-most-three Boolean circuit with `m>n`,
and let `k` be the branchwidth of `lambda_C`. There is an algorithm that
constructs `y notin range(C)` in

```text
2^{O(k)} gamma m^6 log m
  + 2^{O(k^2)} gamma m
  + O(m log m A(2k)^2 poly(n,m))
```

time, where `gamma` is the time for one `lambda_C` oracle evaluation. In the
explicit support representation, `gamma=O(m)`.

The proof is a black-box composition of the Korhonen--Oum decomposition theorem
with the internally proved V77 transfer and the internally verified V75/V74
symbolic-prefix machinery, with direct enumeration for the trivial `m<=1`
case.

## 5. Exact oracle audit

The committed audit enumerates every nonempty simple support family over three
variables. There are `127` families. Across them it checks:

```text
2,186 subset values,
78,124 ordered submodularity pairs,
zero normalization violations,
zero symmetry violations,
zero submodularity violations.
```

The independent verifier reconstructs the same census without importing the
oracle module. These finite checks validate the implementation; the proof of
submodularity is the per-variable cut-indicator argument.

## 6. Scope and nonclaims

This result removes the **supplied-decomposition assumption** from the
parameterized chain. It does not remove dependence on support branchwidth,
does not show that arbitrary `NC0_3` circuits have bounded branchwidth, and
does not yield a standard-model lower bound.

V77 does not implement the Korhonen--Oum algorithm; it invokes their published
theorem as a prior-art black box. The composition is not claimed peer reviewed
or novel. It does not solve unrestricted `NC0_3-Avoid` and does not resolve P
versus NP.

## References

- Tuukka Korhonen and Sang-il Oum, *Branch-width of connectivity functions is
  fixed-parameter tractable*, arXiv:2601.04756, 2026.
- Fedor V. Fomin and Tuukka Korhonen, *Fast FPT-Approximation of Branchwidth*,
  STOC 2022, DOI `10.1145/3519935.3519996`.
