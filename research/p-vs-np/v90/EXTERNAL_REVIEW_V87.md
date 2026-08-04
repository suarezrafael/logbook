# External review packet — V87 rank-three primal-treewidth/branchwidth transfer

## Purpose

This packet isolates one structural lemma used in Laboratory V87. It requests independent checking and literature identification. It makes no novelty claim.

## Definitions

Let `H=(V,E)` be a finite hypergraph of rank at most three.

- The **primal graph** `G=primal(H)` has vertex set `V`, with two vertices adjacent whenever they occur together in one hyperedge.
- For `F subseteq E`, define the support boundary

```text
partial(F)
 = {v in V : v lies in an edge of F and in an edge of E\F}.
```

- A branch decomposition of `H` is an unrooted subcubic tree whose leaves are bijective with `E`; the width of a tree edge is the size of the boundary of the corresponding hyperedge bipartition. Let `bw(H)` be the minimum maximum width.

The claim concerns this hyperedge-boundary branchwidth, not necessarily another convention bearing the same name.

## Claim

For every rank-at-most-three hypergraph `H`,

```text
tw(primal(H))+1
  <= max(3, ceil(3 bw(H)/2)).
```

## Construction supplied

Take a branch decomposition of width `k=bw(H)`.

For each internal tree node `t`, deleting `t` partitions the leaves into three branches with hyperedge sets `E_1,E_2,E_3`. Define a bag

```text
B_t = {v in V : v is incident with hyperedges in at least two of E_1,E_2,E_3}.
```

Add leaf or local bags as needed to cover vertices of a single hyperedge; since rank is at most three, these bags have size at most three.

## Bag-size bound

Let `partial_i` be the boundary of the cut `E_i | (E\E_i)`. Every vertex in `B_t` occurs in at least two of

```text
partial_1, partial_2, partial_3.
```

Therefore

```text
2|B_t| <= |partial_1|+|partial_2|+|partial_3| <= 3k,
```

so

```text
|B_t| <= floor(3k/2).
```

Using the safe integer presentation gives bag size at most

```text
ceil(3k/2),
```

and hence the displayed treewidth inequality after accounting for bags of size at most three.

## Tree-decomposition conditions to check

### Vertex coverage

Every non-isolated primal vertex belongs to at least one hyperedge and is included in a leaf/local bag or in an internal bag where its incident hyperedges first separate.

### Edge coverage

Every primal edge is contained in some hyperedge of rank at most three, so a local bag containing that hyperedge covers the primal edge.

### Running intersection

For a fixed vertex `v`, consider the minimal subtree spanning all leaves corresponding to hyperedges incident with `v`. The internal nodes of this subtree are exactly the nodes where incident hyperedges occupy at least two branches, hence exactly the internal bags containing `v`; adjoining the incident leaf/local bags yields a connected set.

## Consequence used in V87

If a graph formed by selecting one pair inside each ternary support is a subgraph of `primal(H)` and has treewidth `Omega(n)`, then monotonicity of treewidth and the claim imply

```text
bw(H)=Omega(n).
```

The probabilistic random-graph argument supplying the treewidth lower bound is separate from this packet.

## Scope and nonclaims

- The constant `3/2` uses rank at most three.
- The branchwidth notion is the explicit hyperedge support-boundary function above.
- No converse inequality or optimality of the constant is claimed.
- No new graph or circuit lower bound follows from the lemma alone.
- The finite repository audit checked 837 rank-three hypergraphs on five vertices; this is evidence, not the proof.

## Questions for the reviewer

1. Is the bag construction a valid tree decomposition under the stated branchwidth convention?
2. Does the running-intersection argument require any extra bags or subdivisions not stated here?
3. Is `max(3,ceil(3k/2))` the cleanest integer form, or can `max(3,floor(3k/2))` be used?
4. Is this transfer already standard for rank-`r` hypergraphs or connectivity systems, perhaps with a general `r/2` coefficient?
5. Are isolated vertices or repeated hyperedges the only degenerate cases requiring separate conventions?

## Requested review outcome

A useful response is one of:

- proof confirmed under the definitions;
- a specific counterexample or missing condition;
- a citation to a standard theorem subsuming the claim;
- a corrected constant or convention translation.
