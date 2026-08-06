# Huang–Li–Zhong runtime calibration

## Source

Primary source: Huang, Li, Zhong, *Range Avoidance and Remote Point: New Algorithms and Hardness*, ECCC TR25-049, revision 5.

## Algorithm 4

For `NC0_k-Avoid[n,m]`, `m>=n+1`, Algorithm 4 repeatedly fixes an output bit so that the current preimage space shrinks by at least one half. After at most `n+1` fixed bits, the preimage is empty.

V92 specializes the unspecified choices into a canonical policy:

- output coordinates are considered in increasing index order;
- the smaller exact child count is selected;
- ties select zero;
- the suffix after emptiness is all zero.

This specialization remains an instance of Algorithm 4.

## Connected-component representation

After `t` output bits are fixed, their support-overlap graph splits into `s` components. Each component has a preimage subspace `T_i` over a disjoint set of input variables. The number of valid assignments on the used variables is exactly

```text
product_i |T_i|.
```

The traversed decision-space weight is

```text
w(T(t)) = 2^(k-s) product_i |T_i|.
```

Claim 6.8 bounds it by

```text
w(T(t)) <= 2^((k-2)t+k).
```

`canonical_halving.py` checks the component product and this inequality on the committed finite families.

## Runtime

Combining the traversed-space bound with the halving bound `|Preimage(p)|<=2^(n-t)` gives per-step search space

```text
min(2^((k-2)t+k), 2^(n-t))
  <= 2^(k+(k-2)n/(k-1)).
```

The resulting runtime is

```text
O(n * 2^((k-2)n/(k-1))).
```

Examples:

```text
k=2: O(n)
k=3: O(n * 2^(n/2))
k=4: O(n * 2^(2n/3))
```

## Worst-case barrier

Theorem 6.11 shows exponential worst-case behavior for the greedy strategy on `NC0_k-Avoid[n,O(n)]`. The hard pattern is an expanding, locally tree-like support graph with essentially one major preimage component and too few cycles to compress it additively.

This is an algorithm-specific barrier, not an unconditional lower bound for Range Avoidance. The paper explicitly notes that an unconditional exponential lower bound for every algorithm in constant stretch would imply `P!=NP`.

## V92 consequence

The all-instance branch now has the same canonical output semantics as the low-width branch. What remains missing is not correctness or single-valuedness; it is a faster representation or comparison oracle for the two child preimage counts on high-width instances.
