# Is this deficiency/connectivity conservation identity standard for hypergraph branch decompositions?

Let `H=(X,M)` be a finite hypergraph, where `M` is the set of hyperedges and `X=N(M)` is the set of vertices contained in at least one hyperedge. Define the global excess

```text
sigma = |M|-|X|.
```

For `S subseteq M`, let

```text
N(S)      = union of the hyperedges in S,
delta(S)  = |S|-|N(S)|,
lambda(S) = |N(S) intersect N(M\S)|.
```

There is no assumption that `delta(S)` is nonnegative.

By inclusion-exclusion,

```text
|N(S)|+|N(M\S)| = |X|+lambda(S),
```

and therefore

```text
delta(S)+delta(M\S) = sigma-lambda(S).        (1)
```

This gives the following immediate consequence. Suppose a branch decomposition of the hyperedge set is supplied, represented by an unrooted subcubic tree whose leaves are bijective with `M`, and suppose every displayed cut has `lambda`-value at most `w`. A standard balanced-edge argument gives an edge whose two leaf sides both have size between `|M|/3` and `2|M|/3`. For that cut, equation (1) implies that one side `S` satisfies

```text
ceil(|M|/3) <= |S| <= floor(2|M|/3)
```

and

```text
delta(S) >= ceil((sigma-w)/2).
```

My questions are:

1. Is identity (1) standard under a known name in hypergraph, matroid, connectivity-function, or branchwidth literature?
2. Is the balanced deficiency consequence already recorded in this form, or does it follow from a more general theorem about symmetric submodular connectivity functions?
3. Are there convention issues for retained degree-two vertices in the decomposition tree or for very small `|M|` that require changing the ceiling/floor statement?
4. Under rank-three, simplicity, or linearity assumptions, is there a known strengthening of the factor `1/2`?

I am mainly looking for a reference, a convention correction, or a counterexample to the quantitative statement. I am not claiming novelty.
