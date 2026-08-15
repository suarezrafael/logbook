# Laboratory V101 — functional-anchor DAG compression

V101 strengthens the V100 safe-relaxation idea without composing two-input
functions into neighboring local gates.

## Functional anchor

For a local output `g_e` and target bit `b`, call a fiber **functional in head
`v`** if no two points of the fiber agree on all other support variables while
disagreeing on `v`. Equivalently, the fiber is contained in the graph

```text
x_v = h(other local inputs)
```

of a partial Boolean function. Extend undefined rows of `h` arbitrarily to make
it total and forget the rest of the original fiber. This is a safe relaxation.

V101 selects such output/target/head triples with:

- distinct head variables; and
- an acyclic dependency graph from the tail variables to the head.

If `s` anchors are selected, exactly `s` input variables are heads and the
remaining

```text
mu = n-s
```

variables are roots. Every root assignment extends uniquely through the DAG to
one relaxed full assignment. The relaxed domain therefore has exactly
`2^mu` points.

After deleting the `s` selected output coordinates, the circuit still has

```text
m-s > n-s = mu
```

unselected output coordinates. Enumerating the relaxed functional domain and
choosing a missing remaining output word yields a deterministic

```text
O(2^mu poly(N))
```

avoider. The selected target bits and the V100 peel records then lift the word
to the original circuit.

Thus `mu=O(log N)` is a polynomial regime, with no locality-four composition,
exact child comparison, or oracle.

## Exact ternary classification

Among the 218 essential ternary truth tables, exactly **186** have a functional
anchor. Only **32** do not. The two anchor-free NPN orbits are

```text
0x17    8 tables   signed MAJ_3,
0x1b   24 tables   mux/bijunctive selector orbit.
```

The classification has a symbolic explanation. Every unbalanced ternary
predicate has a fiber of size at most three; a set of at most three cube
vertices cannot contain an edge in all three coordinate directions, so it is
functional in some coordinate. For a balanced four-point fiber, functional
projection makes it the graph of a total two-input Boolean function. Essential
balanced functional predicates are therefore either affine graphs or, when the
two-input function is non-affine, NPN-equivalent to the graph of AND, which is
the `0x1e` orbit.

After V100, the residual hard orbits were

```text
0x16, 0x17, 0x1b, 0x1e, 0x69.
```

V101 adds functional anchors for `0x16`, `0x1e`, and `0x69`; the exact local
functional-anchor-free frontier is therefore `0x17/0x1b`.

## Strict balanced-nonaffine family

For every `N>=5`, put canonical `0x1e` gates on all cyclic triples

```text
(i,i+1,i+2) mod N
```

and add one `MAJ_3` output. Canonical `0x1e` is balanced, non-affine, essential,
and can be written as

```text
f(x0,x1,x2) = x2 XOR (x0 OR x1).
```

For target zero it gives the total functional anchor

```text
x_{i+2}=x_i OR x_{i+1}.
```

V101 greedily selects the first `N-2` cyclic outputs, giving the acyclic
recurrence

```text
x2=h(x0,x1), x3=h(x1,x2), ..., x_{N-1}=h(x_{N-3},x_{N-2}).
```

Only roots `x0,x1` remain, so the relaxed domain has four assignments. The last
two cyclic outputs plus the extra majority output give three remaining output
bits, hence a missing word exists.

The support component is connected and every input has degree at least three,
so V97 has `lambda=N`. V100 performs zero peels because `0x1e` and `0x17` are
among its residual hard orbits. V101 therefore gives a strict polynomial
extension on a genuinely balanced non-affine family.

## Frontier after V101

The local hard frontier has collapsed from ten essential ternary NPN orbits to
two:

- signed majority `0x17`, where V99 already showed the simple signed loose-X
  certificate is surjective in nonzero switching classes;
- mux/bijunctive `0x1b`, whose two fixed-output fibers are 2-CNF implication
  gadgets but whose target word still has to be constructed.

The next version should attack one of these two classes or combine functional
DAG compression with affine-cycle equations when the dependency graph is cyclic.

## Nonclaims

V101 does not solve arbitrary low-`mu` versus high-`mu` transitions, does not put
all `NC0_3-Avoid` in P, does not improve the Huang--Li--Zhong unrestricted
worst-case exponent, does not establish novelty or peer review, and does not
resolve P versus NP.
