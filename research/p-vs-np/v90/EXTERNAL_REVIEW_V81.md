# External review packet — V81 deficiency conservation and balanced width tradeoff

## Purpose

This packet isolates two elementary structural statements from Laboratory V81 for independent checking. It makes no novelty claim and does not ask the reviewer to assess the wider P-versus-NP program.

## Setting

Let `H=(X,M)` be a finite hypergraph, where `M` is the set of hyperedges (“gates”) and `X=N(M)` is the set of active vertices. Define the global excess

```text
sigma = |M|-|X|.
```

For `S subseteq M`, write

```text
N(S)      = union of the hyperedges in S,
delta(S)  = |S|-|N(S)|,
lambda(S) = |N(S) intersect N(M\S)|.
```

No sign restriction is placed on `delta(S)`.

## Claim A — exact conservation identity

For every `S subseteq M`,

```text
delta(S)+delta(M\S)=sigma-lambda(S).
```

### Proof supplied

By inclusion-exclusion,

```text
|N(S)|+|N(M\S)|=|X|+lambda(S).
```

Subtracting this from

```text
|S|+|M\S|=|M|
```

gives the identity.

## Claim B — balanced width/deficiency consequence

Suppose a branch decomposition of the hyperedge set is supplied, represented by an unrooted subcubic tree whose leaves are bijective with `M`. Let its width under `lambda` be at most `w`.

Then one can find, by scanning tree edges, a side `S` satisfying

```text
ceil(|M|/3) <= |S| <= floor(2|M|/3)
```

and

```text
delta(S) >= ceil((sigma-w)/2).
```

Here one may choose whichever side of the balanced cut has larger deficiency.

### Proof supplied

Every leaf-labelled subcubic tree has an edge with both leaf sides between one third and two thirds of all leaves. For its cut,

```text
lambda(S)<=w.
```

Claim A gives

```text
delta(S)+delta(M\S)>=sigma-w.
```

At least one of the two integer deficiencies is at least the ceiling of half the right-hand side.

## Scope and nonclaims

- The identity is rank-independent.
- The balanced-edge lemma is purely a tree statement.
- The result assumes a branch decomposition is supplied; it is not a decomposition algorithm.
- It does not imply a deterministic avoidance algorithm or a circuit lower bound.
- The factor `1/2` is tight if only one balanced cut and the conservation identity are used; the repository includes a rank-one equality example.

## Questions for the reviewer

1. Is Claim A stated with the correct active-vertex convention `X=N(M)`?
2. Does the balanced-edge lemma cover all unrooted subcubic trees, including degree-two vertices if they are retained?
3. Are the ceiling/floor and integer-rounding statements in Claim B correct for all small `|M|>=2`?
4. Is this identity or the quantitative consequence standard under a known name in hypergraph branchwidth or connectivity-function literature?
5. Is there a stronger known consequence that replaces the factor `1/2` under rank-three, simplicity, or linearity assumptions?

## Repository evidence

The V81 primary and independent verifiers exhaustively checked 22,528 subset-cut states on the committed finite controls. This is validation evidence, not a substitute for proof or external review.
