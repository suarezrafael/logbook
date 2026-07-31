# Computable branching sandwich

## Statement

For every affine-cell branching system in the V66/V67 model,

```text
c <= L_aff <= L_greedy.
```

Here:

- `c` is the number of consistent complete branch signatures;
- `L_aff` is the minimum leaf count over adaptive inconsistency-pruned trees;
- `L_greedy` is the leaf count of the explicit greedy policy implemented in `v67_branch_growth_probe.py`.

## Lower bound

Two different consistent complete signatures disagree on at least one gate choice. A valid branching tree must separate those choices before reaching a complete consistent leaf. Therefore distinct consistent signatures terminate at distinct leaves, giving `c <= L_aff`.

## Upper bound

The greedy policy is one valid adaptive policy. Since `L_aff` minimizes over all valid policies, its leaf count cannot exceed `L_greedy`.

## Why this matters

Exact optimization of `L_aff` is exponential in the number of gates. Counting `c` by enumerating inputs and evaluating one fixed greedy policy are substantially cheaper. The sandwich therefore supports searches at larger `n`:

1. use `c` to detect unavoidable tree growth;
2. use `L_greedy` to test whether a simple policy remains small;
3. run exact `L_aff` only on selected witnesses.

The bounds do not decide whether `c_max(n)` or `L_aff` is polynomial or exponential. They provide a reproducible way to search for either behavior.

## V67 witnesses

```text
n=10, m=11: 16 <= L_aff=25 <= L_greedy=25
n=11, m=12: 36 <= L_aff=61 <= L_greedy=62
```

The selected-policy residual-state counts are `G_aff=47` and `G_aff=108`, respectively. These are not claimed to be minimum DAG sizes.
