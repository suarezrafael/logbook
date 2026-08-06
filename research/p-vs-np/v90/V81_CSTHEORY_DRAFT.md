# Draft public question for Theoretical Computer Science Stack Exchange

## Proposed title

Is this hypergraph deficiency-conservation identity and balanced branch-decomposition consequence standard?

## Proposed body

Let `H=(X,M)` be a finite hypergraph, where `M` is the set of hyperedges and

```text
X = N(M) = union_{e in M} e
```

is the set of active vertices. Define

```text
sigma = |M|-|X|.
```

For `S subseteq M`, write

```text
N(S)      = union_{e in S} e,
delta(S)  = |S|-|N(S)|,
lambda(S) = |N(S) intersect N(M\S)|.
```

No sign condition is imposed on `delta(S)`.

By inclusion-exclusion,

```text
|N(S)|+|N(M\S)| = |X|+lambda(S),
```

and hence

```text
delta(S)+delta(M\S)=sigma-lambda(S).        (1)
```

Now suppose a branch decomposition of the hyperedge set is given by an unrooted subcubic tree whose leaves are bijective with `M`. Let the width of the decomposition under the cut function `lambda` be at most `w`.

Using the standard balanced-edge property of a leaf-labelled subcubic tree, choose a cut with

```text
ceil(|M|/3) <= |S| <= floor(2|M|/3).
```

For this cut, `lambda(S)<=w`. Equation (1) then gives

```text
delta(S)+delta(M\S) >= sigma-w.
```

Choosing the side with larger deficiency yields a balanced side `T` satisfying

```text
ceil(|M|/3) <= |T| <= floor(2|M|/3)
```

and

```text
delta(T) >= ceil((sigma-w)/2).              (2)
```

I am not claiming that either statement is new. I am trying to identify the correct terminology and prior literature.

My questions are:

1. Is identity (1) standard under a known name in hypergraph, matroid, connectivity-function, or branchwidth literature?
2. Is consequence (2) already recorded in this form, possibly as an immediate corollary of a standard connectivity result?
3. Are there stronger known bounds for rank-three, simple, or linear hypergraphs?
4. Is any convention or small-case qualification missing, particularly if degree-two vertices are retained in the decomposition tree?

A reference, corrected formulation, or counterexample would be especially useful.

## Posting notes

- Do not mention P versus NP or the wider laboratory program.
- Prefer tags related to hypergraphs, graph-decompositions, treewidth/branchwidth, and combinatorics, subject to the site's available tag vocabulary.
- Remove this posting-notes section before publication.
- Record the final public permalink in `EXTERNAL_VALIDATION_GATE.json`; the draft itself is not submission evidence.
