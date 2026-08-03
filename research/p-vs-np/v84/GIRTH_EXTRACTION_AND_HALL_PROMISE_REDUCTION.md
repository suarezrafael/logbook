# Exact FP^NP extraction and the logarithmic Hall-expander promise

## 1. Setup

Let `F:{0,1}^n -> {0,1}^m` be an `NC0_3` map. For each output gate `e`, let
`N(e)` be the set of input variables on which it depends, so `|N(e)|<=3`.
The bipartite support graph `B=(M,X;E)` presents a transversal matroid on the
output set `M`.

Write `g(B)` for the minimum circuit size, with `g(B)=infinity` if the matroid
is free. The NP language used by V84 is

```text
D3-TRANSVERSAL-GIRTH = {(B,L): max_e |N(e)|<=3 and g(B)<=L}.
```

Membership in NP follows because a dependent output set of size at most `L` is
a certificate and dependence is checked by bipartite matching. V83 proves
NP-hardness even under the degree-three promise.

## 2. Exact girth

### Theorem 2.1

The exact value `g(B)` is computable with an NP oracle using

```text
ceil(log2 m)
```

queries when dependence is guaranteed, and at most one additional existence
query otherwise.

### Proof

If dependence is not promised, query `(B,m)`. A no answer means the matroid is
free. Otherwise `1<=g(B)<=m`. Binary-search the least `L` for which the oracle
answers yes. The predicate is monotone in `L`, and thresholds require only
`O(log m)` bits. In the range-avoidance regime `m>n`, the full output set is
dependent because it has at most `n` neighbors, so the existence query is
unnecessary. ∎

## 3. Canonical shortest circuit by deletion

Fix a total order `e_1,...,e_m`. After computing `g=g(B)`, maintain a current
restriction `B_i`. For each `e_i` still present, query whether

```text
g(B_i \ e_i) <= g.
```

Delete `e_i` exactly when the answer is yes.

### Lemma 3.1 — preservation

Every accepted deletion preserves the girth exactly.

### Proof

Deletion cannot create a new circuit, hence cannot lower girth. The yes answer
supplies a circuit of size at most the old girth `g`, so the new girth is also
at most `g`. Therefore it equals `g`. ∎

### Theorem 3.2 — canonical circuit

After at most `m` deletion queries, the remaining output set is a unique
shortest circuit. It is canonical relative to the fixed order.

### Proof

By Lemma 3.1, a shortest circuit of size `g` survives throughout. At the end,
for each remaining element `e`, deleting `e` would raise the girth above `g`.
Thus every shortest circuit in the final restriction contains every remaining
element. Conversely every shortest circuit is a subset of the remaining
ground set. Hence the remaining ground set itself equals the unique shortest
circuit. The sequence of deterministic oracle decisions under the fixed order
makes this circuit canonical. ∎

All restrictions are obtained only by deleting left vertices. Therefore the
maximum left degree never exceeds three.

## 4. Exact Hall witness

### Lemma 4.1 — circuit deficiency

For every transversal circuit `C`,

```text
|N(C)| = |C|-1.
```

### Proof

Dependence gives a Hall-deficient subset `T subseteq C`. Circuit minimality
makes every proper subset independent, so `T=C` and `|N(C)|<|C|`. On the other
hand, for any `e in C`, the set `C-{e}` is matchable and therefore has at least
`|C|-1` neighbors, all contained in `N(C)`. ∎

### Theorem 4.2 — minimum neighborhood

If `C` is a shortest circuit of size `g`, then `N(C)` is a minimum-neighborhood
Hall witness and

```text
h* = |N(C)| = g-1.
```

### Proof

The circuit attains neighborhood size `g-1`. Conversely every Hall-deficient
set contains a circuit `D`; then `N(D) subseteq N(S)` and
`|N(D)|=|D|-1>=g-1`. ∎

This reproves the V82 identity in the exact form needed by the extraction
algorithm.

## 5. Local enumeration and lift

Restrict the circuit to the gates in `C` and variables in `N(C)`. The local
map has domain size

```text
2^|N(C)| = 2^(g-1)
```

and codomain size `2^g`. Enumerating the domain lists at most half of the local
output cube. Choose the lexicographically first missing projection `z_C`.
Define a global output string `z` by placing `z_C` on `C` and zeros elsewhere.
For every global input `x`, the projection `F(x)|_C` belongs to the enumerated
local range and is different from `z_C`; hence `F(x)!=z`.

The deterministic work is `2^(g-1) poly(n+m)`. Therefore, after the oracle
extraction, every instance with `g=O(log(n+m))` is solved in polynomial time.

## 6. Parameterized dichotomy

### Theorem 6.1 — extract, solve, or expose expansion

For every integer threshold `L`, a deterministic polynomial-time machine with
an NP oracle returns exactly one of:

1. an avoided global output, after `2^(g-1) poly(n+m)` local work, when `g<=L`;
2. the original instance together with the promise

   ```text
   |N(S)| >= |S| for every S subseteq M with |S|<=L,
   ```

   when `g>L`.

### Proof

The first branch is Section 5. In the second branch, any set `S` of size at
most `L` is smaller than every circuit and is therefore independent. Hall's
criterion gives `|N(S)|>=|S|`. ∎

This is a Turing preprocessing dichotomy or promise reduction. It is not a
many-one reduction to a solved problem: the large-girth branch remains the
obstruction.

Choosing `L=c log(n+m)` for fixed `c` yields polynomial local enumeration and
reduces the unresolved part to logarithmic Hall expansion. V80's stronger
finite and asymptotic obstruction families, which exclude deficient sets on
larger scales, are contained in this branch; V84 does not prove that every
logarithmic Hall expander has the additional spectral or pseudorandom structure
needed by known range-avoidance algorithms.

## 7. Query and bit complexity

In the guaranteed-dependent range-avoidance regime, the total number of oracle
queries is at most

```text
ceil(log2 m) + m.
```

Without that promise, add one existence query. Each query contains the same
support rows, an active-element bit mask, and an `O(log m)`-bit threshold.
The query construction, matching checks used by the finite audit, neighborhood
extraction, and output lift are polynomial in the explicit circuit description.

## 8. Literature boundary and nonclaims

The target `m=n+n^(2/3)` is lower-bound sensitive: a complete `FP^NP`
algorithm there would imply explicit matrix rigidity and superlinear log-depth
circuit lower bounds. At the upper side, a 2025 deterministic result solves
`NC0_t-Avoid` for `m >= c_t n^((t-1)/2) log n`, giving `m>=c n log n` when
`t=3`. The V84 theorem sits strictly below a complete algorithm: it removes
the short-girth branch and identifies the remaining Hall-expanding promise.

No claim of novelty, matrix rigidity, circuit lower bounds, `NC1` separation,
or `P != NP` is made.
