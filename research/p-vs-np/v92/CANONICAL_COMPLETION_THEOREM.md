# Canonical halving completion theorem

## Theorem

Let `C:{0,1}^n->{0,1}^m` with `m>=n+1`. Assume access to an exact prefix-count function

```text
N(p)=|{x in {0,1}^n : C(x) has prefix p}|.
```

The following deterministic procedure returns a word outside `Range(C)`:

1. begin with the empty prefix;
2. query `N(p0)` and `N(p1)`;
3. append zero when `N(p0)<=N(p1)`, and append one otherwise;
4. when the selected count becomes zero, append zero to every remaining coordinate.

The procedure makes at most `2(n+1)` child-count queries before the preimage becomes empty. Its output is uniquely determined by `C` and the fixed output order.

## Proof

For every prefix `p`, the two children partition its preimage, so

```text
N(p0)+N(p1)=N(p).
```

The chosen child has count at most `N(p)/2`. Initially `N(empty)=2^n`. After `t` nonempty choices the count is at most `2^(n-t)`. For `t=n+1`, an integer count strictly below one must be zero. Since `m>=n+1`, the procedure reaches zero before exhausting all output coordinates. Every extension of a zero-preimage prefix has zero preimages, so the zero-filled completion is outside the range.

The fixed coordinate order, zero tie break, and zero suffix make the search function single-valued.

## Adapter corollary

Any exact prefix-count implementation can drive this same output policy.

- The V75 monotone arithmetic DAG supplies exact `N(p)` under a supplied decomposition; V77 supplies the decomposition in the FPT support-width regime.
- Huang–Li–Zhong's connected-preimage-space algorithm supplies the all-instance evaluator with its stated exponential/subexponential runtime.

Therefore the low-width and all-instance branches can be required to return one identical canonical output. This closes the semantic-output bridge isolated in V91.

## Complexity boundary

The theorem is query-relative. It does not make exact prefix counting efficient. The total runtime is the cost of at most `2(n+1)` exact child-count evaluations plus output construction. Consequently every lower-bound implication still depends on the complexity of implementing those queries in the theorem's exact circuit class and size/stretch regime.
