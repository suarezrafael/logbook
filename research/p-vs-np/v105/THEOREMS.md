# V105 theorem ledger — signed-majority implication dumbbells

## Definition 1 — signed-majority pair transport

Let

```text
g_e = MAJ(x_u XOR p_u, x_v XOR p_v, x_w XOR p_w).
```

For a target bit `t`, the condition `g_e=t` says that at most one local literal
disagrees with `t`. On the pair `(u,v)`, if

```text
a = 1 XOR t XOR p_u,
```

then the pair clause implies

```text
x_u=a -> x_v=a XOR delta_e,
delta_e = 1 XOR p_u XOR p_v.
```

The same binary clause also gives the contraposition

```text
x_v=not(a XOR delta_e) -> x_u=not a.
```

Conversely, for either desired source value `a`, choosing

```text
t = 1 XOR p_u XOR a
```

realizes this implication.

## Definition 2 — odd-triangle dumbbell

For every signed-majority output, take the first two support variables as one
canonical pair edge and label that edge by `delta_e`.

An **odd triangle** is a three-edge triangle whose edge labels XOR to one.
An **odd-triangle dumbbell** consists of two vertex-disjoint odd triangles and a
path joining one vertex of the first to one vertex of the second, using no
triangle edge and no triangle vertex internally.

## Theorem 1 — path transport

For any oriented canonical-pair path

```text
v_0,e_1,v_1,...,e_k,v_k
```

and either starting value `a`, output targets on the path edges can be chosen in
linear time so that the resulting 2-CNF implication graph contains

```text
x_(v_0)=a -> x_(v_k)=a XOR delta(e_1) XOR ... XOR delta(e_k).
```

It simultaneously contains the contrapositive implication in the reverse
direction.

### Proof

At each edge, use Definition 1 with the currently propagated source value. The
new endpoint value is exactly the source value XOR the edge transport label.
Induction along the path gives the claimed endpoint. Every local implication is
a genuine clause of the exact majority target condition, so their composition
is valid. Contraposition is already present edge by edge in the 2-SAT implication
graph.

## Theorem 2 — odd triangle forces one polarity

On an odd triangle, targets can be chosen so that

```text
x_v=a -> x_v=not a
```

for either selected base value `a`.

### Proof

Apply Theorem 1 around the triangle. Odd transport means the accumulated XOR is
one.

## Theorem 3 — odd-triangle dumbbell avoider

If the canonical pair graph contains an odd-triangle dumbbell, a full output
outside the circuit range is constructible in deterministic polynomial time.

### Proof

Let the left triangle be based at `u`, the right at `v`, and let `P` connect
`u` to `v`.

Choose targets on the left triangle to obtain

```text
u:a -> u:not a.
```

Apply path transport starting from `u:not a`; write the endpoint as `v:b`. Thus

```text
u:not a -> v:b.
```

The same path clauses provide the contraposition

```text
v:not b -> u:a.
```

Choose right-triangle targets to obtain

```text
v:b -> v:not b.
```

The triangle edges and path edges are disjoint, so these target choices do not
conflict. The implication graph therefore contains the directed cycle

```text
u:a -> u:not a -> v:b -> v:not b -> u:a.
```

Both literals of variable `u` lie in one strongly connected component. By the
standard 2-SAT criterion, the selected exact target constraints are
inconsistent. Completing every unused output coordinate arbitrarily therefore
gives a word outside the original range.

Odd triangles can be enumerated from the canonical pair multigraph and candidate
triangle pairs connected by BFS, so detection and construction are polynomial.

## Theorem 4 — strict exact-stretch family

For every `r>=2`, there is a signed-majority circuit with

```text
n=r+6,
m=n+1,
```

whose canonical pair graph is two triangles joined by a path with `r` internal
vertices. Every canonical pair edge has transport label one. Therefore both
triangles are odd and Theorem 3 applies.

One left-triangle gate negates only its third literal. The other gates are
positive majority. Because the other two left-triangle gates use the same three
variables positively, the incidence switching equations force those three input
switches equal and simultaneously force the negated-third variable opposite,
which is impossible. Hence the positive-surplus component is not
switching-balanced.

## Theorem 5 — separation from preceding structural parameters

On the strict family:

1. **V96 surplus.** No proper output subset has positive surplus. The canonical
   pair graph is a graph-theoretic dumbbell with `m=n+1`; deleting any edge
   reduces every connected component to cyclomatic rank at most one, so every
   proper edge subset has at most as many edges as pair vertices. Circuit support
   size is at least pair-vertex count.
2. **V97 peeling.** The support hypergraph is connected, every gate is essential
   ternary, and every input has incidence degree at least two, so `lambda=n`.
3. **V98 switching.** The literal-sign conflict in Theorem 4 makes the component
   switching-unbalanced.
4. **V101 functional anchors.** Signed majority has no exact functional target
   fiber, so `mu=n`.
5. **V102 strong affine backdoor.** Every majority support must be hit in at
   least two variables. The path contains linearly many disjoint support triples,
   giving `beta=Omega(n)`; the full input set gives `beta=O(n)`. Thus
   `beta=Theta(n)`. Finite exact checks match `floor(2n/3)`.
6. **V103 affine hull.** Both target fibers of signed majority have full affine
   hull, so `nu=n`.
7. **V104 affine-first hybrid.** With zero affine rank and zero functional heads,
   `eta_AF=n`.

Thus V105 gives a polynomial-time regime on an infinite exact-stretch family
where the preceding V97/V101/V102/V103/V104 structural exponents remain linear,
and where the V98 switching reduction does not apply.

## Boundary

The theorem requires the detected odd-triangle dumbbell in the canonical pair
graph. It does not solve arbitrary signed-majority circuits. No unrestricted
`NC0_3-Avoid` algorithm, worst-case exponent improvement, circuit lower bound,
novelty claim, peer review, or P-versus-NP resolution is asserted.
