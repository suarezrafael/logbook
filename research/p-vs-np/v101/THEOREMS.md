# Laboratory V101 — functional-anchor DAG compression

## 1. Functional fibers

Let

```text
C : {0,1}^n -> {0,1}^m,  m>n,
```

be the residual explicit circuit after V100.

### Definition 1.1

For output `e`, target `b`, and one input `v` in its essential support, call the
fiber `g_e^{-1}(b)` **functional in head `v`** if the projection onto all other
support variables is injective with respect to `v`: whenever two fiber points
agree off `v`, they also agree on `v`.

Then the fiber is contained in the graph of a partial Boolean function

```text
x_v = h_e,b,v(tail variables).
```

Extend undefined tail assignments by a fixed convention (zero) to obtain a
total function `h`.

## 2. Safe functional relaxation

### Lemma 2.1

If `g_e=b` has a functional head `v`, replace the selected fiber by the total
graph relation

```text
x_v=h(tails)
```

and delete output coordinate `e`. Any missing word for the unselected outputs
over the relaxed graph domain lifts, by inserting `b`, to a missing word for the
original circuit.

**Proof.** Every original input realizing `g_e=b` lies in the selected fiber and
therefore satisfies the graph relation. The graph extension can add inputs but
cannot remove an original realization. Hence absence from the relaxed domain is
stronger. QED.

## 3. Acyclic distinct-head systems

Choose selected outputs so that:

```text
1. no input variable is the head of two selected anchors;
2. directing every tail variable toward the head gives a DAG.
```

Let `s` be the number of selected anchors and let `mu=n-s` be the number of
variables that are not heads.

### Lemma 3.1 — root parametrization

Every assignment to the `mu` non-head variables extends uniquely to a full
assignment satisfying all relaxed functional graph relations.

**Proof.** Topologically order the dependency DAG. Root/non-head variables are
assigned first. Each selected head appears once and its tail variables precede
it, so its total function determines the head uniquely. QED.

Thus the relaxed domain has exactly `2^mu` assignments.

### Theorem 3.2 — functional-anchor avoider

A deterministic greedy algorithm that selects functional anchors while
preserving distinct heads and acyclicity gives a missing output in

```text
O(2^mu poly(N)),
```

where `mu` is the number of roots left by that fixed greedy policy after V100.

**Proof.** Delete the `s=n-mu` selected output coordinates. By stretch,

```text
m-s > n-s = mu.
```

Enumerate all `2^mu` root assignments, extend them by Lemma 3.1, and record the
unselected output words. A map from at most `2^mu` relaxed assignments to a cube
with more than `mu` output bits cannot be surjective. Choose a missing remaining
word, insert all selected target bits, apply Lemma 2.1 for every anchor, and
reverse the V100 reductions. QED.

### Corollary 3.3

If `mu=O(log N)`, combined V100/V101 range avoidance is deterministic polynomial
time.

## 4. Exact ternary functional-anchor boundary

### Lemma 4.1 — every unbalanced ternary predicate has a functional fiber

A nonconstant unbalanced ternary predicate has a fiber of size at most three.
Such a set of at most three vertices of the Boolean cube is functional in some
coordinate.

**Proof.** Failure of functionality in coordinate `j` means the set contains a
cube edge parallel to direction `j`. If a set of at most three vertices failed
in all three directions, those vertices would contain edges in all three cube
directions. Three vertices can form at most a length-two path in the bipartite
cube graph, not a triangle with three distinct edge directions. Hence some
coordinate has no parallel fiber edge, so projection off that coordinate is
injective. QED.

### Lemma 4.2 — balanced functional predicates

Let an essential balanced ternary predicate have a functional four-point fiber
with head `z`. Then that fiber is the graph of a total two-input Boolean
function

```text
z=h(x,y).
```

If `h` is affine, the ternary predicate is affine. If `h` is non-affine,
essentiality forces `h` to depend on both inputs, and every essential non-affine
two-input Boolean function is NPN-equivalent to `AND`. Hence the ternary
predicate is NPN-equivalent to the graph-of-AND orbit `0x1e`.

QED.

### Theorem 4.3 — exact 186/32 split

Exactly 186 of the 218 essential ternary truth tables have a functional anchor.
The only functional-anchor-free NPN orbits are

```text
0x17  (8 tables),
0x1b (24 tables).
```

**Proof.** All unbalanced essential predicates are covered by Lemma 4.1.
Balanced affine essential predicates are parity/complement and are functional in
every coordinate. Lemma 4.2 adds exactly the balanced non-affine graph-of-AND
orbit `0x1e` of size 24. The fixed ternary NPN classification then leaves only
the majority orbit `0x17` and mux/bijunctive orbit `0x1b`, totaling 32. QED.

### Corollary 4.4 — post-V100 frontier

After V100's five-orbit literal peeling, the residual local classes were

```text
0x16,0x17,0x1b,0x1e,0x69.
```

Among these, `0x16`, `0x1e`, and `0x69` have functional anchors. The exact local
class with no V101 functional anchor is therefore `0x17/0x1b`.

## 5. Strict cyclic `0x1e` family

Let `H_N` have `N` inputs, `N` cyclic `0x1e` outputs on

```text
(i,i+1,i+2) mod N,
```

and one additional majority output.

### Lemma 5.1

For every `N>=5`, `H_N` is connected, exact-stretch, essential ternary, and
every input has incidence degree at least three. Consequently V97 performs no
leaf/unary/constant reduction and

```text
lambda(H_N)=N.
```

V100 performs zero peels because both `0x1e` and signed majority are V100 hard
orbits. QED.

### Lemma 5.2

Canonical `0x1e` satisfies

```text
f(x0,x1,x2)=x2 XOR (x0 OR x1).
```

Thus target zero on cyclic output `i` gives the total functional relation

```text
x_{i+2}=x_i OR x_{i+1}.
```

Selecting outputs `i=0,...,N-3` gives distinct heads
`x_2,...,x_{N-1}` and an acyclic dependency DAG rooted at `x_0,x_1`.
QED.

### Theorem 5.3 — strict balanced-nonaffine separation

For every `N>=5`, V101 solves `H_N` by enumerating exactly four relaxed root
assignments, while V97 has `lambda=N` and V100 performs zero peels.

**Proof.** Lemma 5.2 gives `s=N-2` selected anchors and `mu=2` roots. Three
output coordinates remain: the last two cyclic outputs and the added majority
output. Since three output bits exceed two root bits, Theorem 3.2 constructs a
missing word. QED.

This family is balanced and non-affine, so the extension is qualitatively beyond
V100's literal-graph local eliminations.

## 6. Boundary

V101 leaves two ternary NPN orbits with no functional anchor: signed majority
`0x17` and mux/bijunctive `0x1b`. High-root functional systems also remain
exponential. No unrestricted polynomial-time algorithm or P-versus-NP claim is
made.
