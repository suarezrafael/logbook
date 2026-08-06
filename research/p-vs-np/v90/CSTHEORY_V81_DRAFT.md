# Draft public question for V81

## Proposed title

Is this deficiency–boundary identity and balanced-cut consequence standard for hypergraph branch decompositions?

## Proposed body

Let `H=(X,M)` be a finite hypergraph, where `M` is the hyperedge set and the active vertex set is

```text
X = N(M).
```

For `S subseteq M`, define

```text
N(S)      = union of the hyperedges in S,
delta(S)  = |S| - |N(S)|,
lambda(S) = |N(S) intersect N(M\S)|,
sigma     = |M| - |X|.
```

No sign restriction is imposed on `delta(S)`.

A direct inclusion–exclusion calculation gives

```text
delta(S) + delta(M\S) = sigma - lambda(S).        (1)
```

Indeed,

```text
|N(S)| + |N(M\S)| = |X| + lambda(S),
```

and subtracting this equality from

```text
|S| + |M\S| = |M|
```

gives (1).

Now suppose a branch decomposition of the hyperedge set is supplied as an unrooted subcubic tree with leaves bijective with `M`, and every displayed cut has boundary at most `w` under `lambda`.

Using the standard balanced-edge property of a leaf-labelled subcubic tree, choose a tree edge whose two leaf sides have sizes between one third and two thirds of `|M|`. For the corresponding side `S`, equation (1) gives

```text
delta(S) + delta(M\S) >= sigma - w.
```

Therefore one of the two balanced sides satisfies

```text
delta(S) >= ceil((sigma-w)/2).
```

My questions are:

1. Is identity (1) standard under a particular name in the literature on hypergraph connectivity functions, branch decompositions, or matroid-style width parameters?
2. Is the balanced consequence above already a known lemma in this form?
3. Are there convention issues when degree-two vertices are retained in the decomposition tree, or for very small `|M|`?
4. Under rank three, simplicity, or linearity of the hypergraph, is a stronger coefficient than `1/2` known?

I am mainly looking for a reference, a standard reformulation, or a correction to the statement. I am not claiming novelty.

## Suggested tags to verify before posting

- `graph-theory`
- `combinatorics`
- a branchwidth, treewidth, hypergraph, or width-parameter tag already present on the site

## Posting checklist

- search the site for `branch decomposition hypergraph boundary deficiency`;
- replace ASCII notation with rendered LaTeX;
- verify that the chosen tags already exist;
- include no link to the wider laboratory in the opening post;
- record the final permalink and posting date in `EXTERNAL_VALIDATION_GATE.json`.
