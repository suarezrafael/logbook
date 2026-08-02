# Degree-three transversal girth is NP-complete

## 1. Problem

A bipartite graph `B=(M,X;E)` presents a transversal matroid on ground set `M`:
`I subseteq M` is independent exactly when a matching saturates `I` into `X`.
The girth is the minimum circuit cardinality.

The restricted decision problem is:

```text
D3-TRANSVERSAL-GIRTH
Input: B=(M,X;E), max_{e in M}|N(e)| <= 3, and L.
Question: is girth(T(B)) <= L?
```

A dependent set of size at most `L` is an NP certificate, because dependence is
checked by one maximum-matching computation and every dependent set contains a
circuit no larger than itself. Thus the problem is in NP.

## 2. Path-selector series expansion

Let `B=(M,X;E)` be any finite presentation. Fix an ordering

```text
N_B(e) = (x_{e,1},...,x_{e,d_e})
```

for every nonloop element `e`.

Replace `e` by left elements

```text
C_e = {e_1,...,e_{d_e}}
```

and introduce private right vertices

```text
P_e = {p_{e,1},...,p_{e,d_e-1}}.
```

Set

```text
N(e_i) = {x_{e,i}}
         union ({p_{e,i-1}} if i>1)
         union ({p_{e,i}} if i<d_e).
```

The endpoint copies have degree two and the internal copies degree three. A
source loop is retained as one degree-zero loop.

### Lemma 2.1 — private matching

Every proper subset of `C_e` is matchable into `P_e`.

**Proof.** Choose a missing index `j`. Match `e_i` to `p_{e,i}` for `i<j`, and
match `e_i` to `p_{e,i-1}` for `i>j`. This saturates `C_e-{e_j}` using all
private vertices. Restricting the matching handles every smaller subset. ∎

### Lemma 2.2 — complete-chain equivalence

For every `A subseteq M`, let `C(A)=union_{e in A} C_e`. Then

```text
A is matchable in B  iff  C(A) is matchable in B'.
```

**Forward direction.** Given a source matching that sends `e` to `x_{e,j}`,
match `e_j` to that external vertex. Match the remaining copies of `C_e` to
`P_e` by the construction of Lemma 2.1.

**Reverse direction.** A complete chain `C_e` has `d_e` left elements but only
`d_e-1` private right vertices. Any matching saturating `C(A)` must therefore
match at least one member of each chain to an external vertex in `N_B(e)`.
Choose one such external edge per chain. The chosen external vertices are
distinct because they came from a matching, so they give a source matching of
`A`. ∎

### Theorem 2.3 — exact circuit correspondence

The circuits of `B'` are exactly

```text
{ C(A) : A is a circuit of B }.
```

**Proof.** Let `Q` be a circuit of `B'`. If `Q` intersects a chain `C_e` in a
nonempty proper subset `R`, then `R` is privately matchable. If `Q-R` were
matchable, combining the two disjoint matchings would match `Q`; hence `Q-R` is
dependent only if `Q` is. Since `Q` is dependent, `Q-R` must be dependent,
contradicting circuit minimality. Therefore every circuit is a union of whole
chains.

By Lemma 2.2, a union of whole chains is dependent exactly when its source set
is dependent. Minimality is preserved in both directions: removing a whole
chain corresponds to removing a source element, while any subset that cuts a
chain can match that partial chain privately and match its remaining complete
chains from the corresponding proper source subset. ∎

### Corollary 2.4 — weighted and uniform girth

The expanded girth is the minimum source-circuit weight for weights
`w(e)=d_e`. If all source elements have degree `D`, then

```text
girth(T(B')) = D * girth(T(B)).
```

The construction has polynomial size and maximum left degree three.

## 3. The Clique presentation

The reduction starts from the Clique template in Colbourn and Elmallah,
“Reliable assignments of processors to tasks and factoring on matroids,”
*Discrete Mathematics* 114 (1993), 115–129,
DOI `10.1016/0012-365X(93)90360-6`, Theorem 2.1.

### Source arithmetic audit

The available author-hosted final-version manuscript displays

```text
ell = binom(k,2)-k-1 = binom(k-1,2).
```

That equality is false: `binom(k-1,2)=binom(k,2)-k+1`. The surrounding proof
also alternates between consequences of the two incompatible values. V83 does
not rely on the displayed equality. It chooses the only reservoir size that
makes a `k`-clique have Hall deficiency one,

```text
r = binom(k,2)-k-1,
```

and proves the complete threshold statement below directly from Hall's
condition. Thus the bounded-degree theorem depends on a self-contained
corrected reduction, not on the inconsistent arithmetic line.

For a Clique instance `(G,k)` with `k>=4`, set

```text
q = binom(k,2),
r = q-k-1,
D = r+2 = q-k+1.
```

Create one left element for every edge of `G`. The right side consists of the
vertices of `G` and a reservoir `Z` of `r` new vertices. The element
corresponding to edge `uv` is adjacent to `u`, `v`, and every member of `Z`.
Every left element therefore has the same degree `D`.

### Lemma 3.1 — no circuit below q

Every edge set `F` with `|F|<q` is matchable.

**Proof.** It suffices to verify Hall's condition for every `H subseteq F`. Let
`t=|H|` and let `v` be the number of graph vertices incident with `H`. For
nonempty `H`,

```text
|N(H)| = r+v.
```

We show `t-v<=r`.

- If `v>=k`, then `t-v <= (q-1)-k = r`.
- If `v<=k-1`, simplicity gives `t<=binom(v,2)`, hence

  ```text
  t-v <= binom(v,2)-v <= binom(k-1,2)-(k-1) <= r.
  ```

The final inequality differs by `k-3`, which is nonnegative for `k>=4`.
Therefore every subset satisfies Hall's condition. ∎

### Lemma 3.2 — threshold circuits are cliques

An edge set `F` of cardinality `q` is a circuit exactly when it is the edge set
of a `k`-clique.

**Proof.** If `F` is a `k`-clique, then

```text
|N(F)| = r+k = q-1,
```

so it is dependent; Lemma 3.1 makes every proper subset independent.

Conversely, if `F` is not a `k`-clique, it cannot consist of `q` distinct edges
on at most `k` vertices. Thus it is incident with at least `k+1` vertices and
`|N(F)|>=r+k+1=q`. Every proper subset satisfies Hall by Lemma 3.1, so `F`
itself is matchable. ∎

Thus `G` has a `k`-clique exactly when the source transversal matroid has girth
at most `q`.

## 4. Degree-three hardness

Apply the path-selector expansion to every source edge element. The source is
left-regular of degree `D`, so Corollary 2.4 gives

```text
girth(T(B')) = D * girth(T(B)).
```

Therefore

```text
G has a k-clique  iff  girth(T(B')) <= qD.
```

The expanded presentation has maximum left degree three and polynomial size:
`D=O(k^2)`, and each source element creates `D` left elements and `D-1` private
right vertices. The threshold `qD` is polynomially bounded.

### Theorem 4.1

`D3-TRANSVERSAL-GIRTH` is NP-complete.

By V82's identity

```text
h*(B) = girth(T(B))-1,
```

the exact minimum Hall-neighborhood objective is NP-hard even when every left
support has cardinality at most three.

## 5. Why the gadget avoids the usual failure

A naive binary selector tree can create short local Hall deficiencies. The
path-selector construction does not merely preserve intended witnesses below a
chosen threshold. Lemma 2.1 removes every partial chain from every minimal
dependent set, and Theorem 2.3 classifies all expanded circuits exactly. This
provides the reverse direction and the no-shortcut guarantee required by the
V82 stopping rule.

## 6. Literature and novelty boundary

The unrestricted hardness theorem has a primary source, but V83 records and repairs
an arithmetic inconsistency in the available source proof. The corrected Clique
threshold and the bounded-degree step are proved in this laboratory and exhaustively audited on finite instances.
The literature search used for V82 and V83 did not locate this exact
left-degree-three statement or this exact presentation gadget. That absence is
not a novelty proof. External matroid-complexity review is required before any
novelty claim.

## 7. Nonclaims

NP-completeness of this auxiliary optimization problem does not imply
`P!=NP`, does not imply Boolean circuit lower bounds, and does not make the
direct P-versus-NP route active.
