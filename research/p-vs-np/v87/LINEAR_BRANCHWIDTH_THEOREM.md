# V87 theorem packet — linear branchwidth and the three-certificate intersection

## Theorem 1 — direct McDiarmid does not pay for all balanced cuts

Fix a gate subset `S`. Resampling one ternary support can remove at most three
shared variables and introduce at most three new shared variables. Hence
`lambda_H(S)` has bounded-difference constant at most six per gate.

McDiarmid gives

```text
Pr[lambda_H(S) <= E lambda_H(S) - t]
 <= exp(-2t^2/(36m)).
```

Even using the optimistic and generally unavailable deviation `t=n`, at
`m/n -> 1` the exponential rate is at most `1/18`.

By Stirling,

```text
binom(m, floor(m/3))
 = exp((H(1/3)+o(1))m),
H(1/3)=0.636514... .
```

Since `1/18 < H(1/3)`, a direct union bound based on this inequality cannot
prove a uniform positive lower bound over all balanced gate cuts.

This is a limitation of the proposed proof method, not evidence that linear
branchwidth is false.

## Lemma 2 — uniform pair shadow

Let `E` be uniform over the 3-subsets of `[n]`. Conditional on `E`, choose a
uniform pair `P subset E`.

For a fixed pair `{u,v}`, exactly `n-2` triples contain it. Therefore

```text
Pr[P={u,v}]
 = (n-2) / binom(n,3) * 1/3
 = 1 / binom(n,2).
```

Independent support and pair choices give independent uniform graph edges.

## Lemma 3 — branchwidth-to-primal-treewidth transfer

Let `H=(V,E)` be a hypergraph of rank at most three and support branchwidth
`k`. Let `P(H)` be its primal graph: two variables are adjacent when they
occur together in a hyperedge.

Then

```text
tw(P(H)) + 1 <= max(3, ceil(3k/2)).
```

### Proof

Take a branch decomposition tree `T` of `H` of width `k`.

For every leaf corresponding to hyperedge `e`, create the bag `e`, of size at
most three.

For an internal node `t`, deleting `t` partitions the hyperedges into
`E_1,E_2,E_3`. Define `B_t` to contain every variable incident with
hyperedges in at least two of these three parts.

Let `partial(E_i)` be the boundary of the branch cut separating `E_i` from
the other two parts. Each boundary has size at most `k`. Every variable in
`B_t` belongs to at least two of the three boundaries. Hence

```text
2|B_t|
 <= |partial(E_1)|+|partial(E_2)|+|partial(E_3)|
 <= 3k.
```

Thus `|B_t| <= 3k/2`.

Every primal edge is covered by its hyperedge leaf bag. For a fixed variable
`v`, the nodes whose bags contain `v` are exactly the minimal subtree
spanning the leaves of the hyperedges containing `v`; this set is connected.
The bags form a tree decomposition of `P(H)` with the asserted width. `QED`

## Theorem 4 — linear branchwidth in the V86 random support model

Let

```text
m=n+ceil(n^(2/3))
```

and choose `m` ternary supports independently and uniformly.

Then there is a constant `gamma>0` such that, asymptotically almost surely,

```text
bw(H) >= gamma n.
```

### Proof

For the first `q=floor(3n/4)` supports, apply Lemma 2 and form the selected
pair shadow `G`.

The number of repeated selected pairs is tight: its expectation is bounded by

```text
binom(q,2)/binom(n,2)=O(1).
```

After deleting repetitions, the selected set is a uniform random graph with

```text
(3/4+o(1))n
```

edges. This is a supercritical sparse random graph. Lee, Lee, and Oum prove
that sparse random graphs with average degree above one have treewidth linear
in `n`. The standard monotone coupling between `G(n,p)` and the uniform
random-graph process transfers their result to this edge-count model.

Thus `tw(G)=Omega(n)` asymptotically almost surely. Since `G` is a subgraph of
`P(H)`, treewidth monotonicity and Lemma 3 give `bw(H)=Omega(n)`. `QED`

No numerical value such as `0.49` is claimed for `gamma`.

## Corollary 5 — one family defeats all three current certificates

For all sufficiently large `n`, there exists a simple 3-uniform support
family at the target stretch satisfying simultaneously:

1. no Hall-deficient gate set of size at most `n/(16e^2)`;
2. support branchwidth `Omega(n)`;
3. after assigning `NOR3`, no nonzero constant output-parity syndrome.

### Proof

V86 bounds the probability of failure of property 1 by `8/49`.

The probability of a repeated support is at most

```text
binom(m,2)/binom(n,3)=o(1).
```

Theorem 4 says that failure of property 2 has probability `o(1)`. The union
of the three bad events has probability below one for all sufficiently large
`n`. Choose a support family outside that union and apply the V86 `NOR3`
unique-cubic-pivot theorem. `QED`

## Proposition 6 — fixed-cut expectation

For a fixed set of `s` gates, let `a=1-3/n`. A variable fails to occur on the
left with probability `a^s`, fails to occur on the right with probability
`a^(m-s)`, and is unused by all gates with probability `a^m`. Therefore

```text
E lambda_H(S)=n(1-a^s-a^(m-s)+a^m).
```

When `s/m -> 1/3` and `m/n -> 1`, this converges to

```text
(1-e^(-1))(1-e^(-2))=0.546572... .
```

The term `e^(-3)` is required because the V80 identity subtracts the active
variable set `N(M)`, not the whole ambient set `[n]`.

## Boundary of the result

The theorem is probabilistic and existential. It does not produce an
explicit support family or an efficient certificate that a given large
sample has linear branchwidth.

It proves that the three known mechanisms can fail simultaneously. It does
not prove that every instance in the Hall-expander promise branch has linear
branchwidth.
