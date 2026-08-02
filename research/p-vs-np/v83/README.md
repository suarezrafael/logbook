# Laboratory V83 — degree-three transversal girth hardness

V83 closes the exact complexity boundary isolated by V82.

The decision problem

```text
D3-TRANSVERSAL-GIRTH
Input: a bipartite presentation G=(M,X;E) with |N(e)| <= 3 for every e in M,
       and an integer L.
Question: does the transversal matroid T(G) contain a circuit of size at most L?
```

is **NP-complete**.

The proof has two components.

1. The Colbourn–Elmallah theorem supplies the Clique-reduction template. The
   author-hosted final-version manuscript contains an arithmetically inconsistent
   displayed identity for the reservoir size. V83 discards that identity and
   rederives the corrected choice `r=binom(k,2)-k-1` from Hall's condition. The
   resulting presentation has uniform left degree

   ```text
   D = binom(k,2) - k + 1.
   ```

   It has no circuit shorter than `q=binom(k,2)`, and its circuits of size `q`
   correspond exactly to the `k`-cliques of the source graph.

2. A path-selector series expansion replaces a left element with ordered
   neighborhood `(x_1,...,x_D)` by a chain of `D` left elements and `D-1`
   private right vertices. Every new left degree is at most three. The circuits
   of the expanded presentation are exactly the unions of whole chains coming
   from circuits of the source presentation.

Because the Colbourn–Elmallah presentation is left-regular, every circuit size
is multiplied by the same factor `D`. Therefore Clique has a `k`-clique if and
only if the degree-three expanded presentation has girth at most `qD`.

## Exact circuit-correspondence theorem

For each source element `e` with ordered neighborhood
`(x_{e,1},...,x_{e,d_e})`, create chain elements
`e_1,...,e_{d_e}` and private right vertices
`p_{e,1},...,p_{e,d_e-1}` with

```text
N'(e_i) = {x_{e,i}} union {p_{e,i-1} if i>1}
                    union {p_{e,i} if i<d_e}.
```

Every proper subset of a chain matches entirely to its private vertices. A
union of complete chains is matchable after expansion exactly when the
corresponding source elements are matchable. Consequently:

```text
circuits(B') = { union_{e in C} chain(e) : C is a circuit of B }.
```

For uniform source degree `D`,

```text
girth(T(B')) = D * girth(T(B)).
```

This is stronger than a gadget test: it rules out every unintended circuit,
not only circuits below the reduction threshold.

## Finite verification

The primary generator and an independent audit check:

- all `512` presentations with three left and three right vertices;
- all `256` presentations with four left and two right vertices;
- exact circuit correspondence on `31,184` expanded nonempty subset states;
- all `64` simple graphs on four vertices for the `k=4` reduction;
- all `1,024` simple graphs on five vertices for the `k=4` reduction;
- direct transformed circuit enumeration for `K4` and `K4` minus one edge;
- `K5` and `K5` minus one edge as a nontrivial chain-length-six control.

For `K4`, the source threshold is `6`, the chain length is `3`, and the
expanded circuit has size `18`. Removing one source edge destroys every source
and expanded circuit in that finite witness.

## Consequences for the laboratory

V82's degree-two/degree-three boundary is now sharp:

```text
left degree <= 2: polynomial via bicircular shortest bicycles;
left degree <= 3: NP-complete.
```

Via the V82 identity `h*=girth-1`, exact minimum Hall-neighborhood computation
is NP-hard already for rank-three supports. This blocks a polynomial exact
optimizer for the first below-diagonal Minimum `p`-Union point unless `P=NP`.
It does not block an `FP^NP` construction, approximation, promised structural
algorithms, or the bounded-width avoidance algorithms proved earlier.

## Files

- `DEGREE_THREE_TRANSVERSAL_GIRTH_HARDNESS.md` — complete proof and boundary audit;
- `V83_DEGREE_THREE_TRANSVERSAL_GIRTH_THEOREM.tex` — standalone formal module;
- `selector_series.py` — exact expansion and finite census generator;
- `RESULTS.json` — immutable evidence snapshot;
- `verify.py` and `verify_independent.py` — primary and independent audits;
- `V84_CORE_CONTEXT.md` — next route after the exact-hardness closure.

## Nonclaims

V83 does not prove `P != NP`, does not establish circuit lower bounds, does not
solve unrestricted `NC0_3-Avoid`, and does not confirm that the path-selector
formulation is new in the literature. The theorem is internally proved and
computationally audited; novelty and peer-review status remain unconfirmed.
