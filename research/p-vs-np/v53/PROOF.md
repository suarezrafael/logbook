# Detailed proof — V53

## 1. Proof of the union-free transfer

For an edge subfamily `A subseteq E`, write

```text
Y_A = product_{e in A} Y_e.
```

After substituting the circuit outputs,

```text
Phi_H(Y_A)
 = product_{e in A} product_{v in e} X_v.
```

On the Boolean cube, multilinearization uses `X_v^r = X_v` for every positive integer `r`. Hence

```text
Phi_H(Y_A) = product_{v in union(A)} X_v = X_{union(A)}.
```

Suppose `H` is t-union-free. For all distinct `A,B` with sizes at most `t`,

```text
union(A) != union(B).
```

Thus `Phi_H(Y_A)` and `Phi_H(Y_B)` are distinct multilinear input monomials. Distinct multilinear monomials are linearly independent as functions on the Boolean cube over every field.

Therefore the images of all output monomials of degree at most `t` are linearly independent. No nonzero polynomial of output degree at most `t` can map to zero. Hence no such polynomial vanishes on the complete image of `C_H`, proving

```text
sd_F(Range(C_H)) > t.
```

## 2. Proof of the incidence-girth criterion

Assume `H` is not t-union-free. There are distinct subfamilies `A,B`, each of size at most `t`, with equal unions.

Remove common edges:

```text
A' = A \ B,
B' = B \ A.
```

Both are nonempty, disjoint, and still have the same vertex union.

Consider the incidence subgraph induced by the hyperedges in `A' union B'` and all vertices in their common union.

- Every left incidence vertex, representing a 3-edge, has degree three.
- Every right incidence vertex lies in at least one edge of `A'` and at least one edge of `B'`, because the two unions are equal. Its degree is therefore at least two.

Every finite graph of minimum degree at least two contains a cycle. The cycle is bipartite and uses at most

```text
|A'| + |B'| <= 2t
```

left vertices. Its length is therefore at most `4t`.

Consequently, incidence girth greater than `4t` rules out every collision and forces t-union-freeness.

## 3. Stretch-one construction

Take a simple cubic graph `G_N` on `N` vertices with girth `g_N = Omega(log N)`. Randomized polynomial-time constructions of such regular high-girth graphs are known.

Form its bipartite double cover `B_N`. It has:

```text
N left vertices,
N right vertices,
degree three on both sides,
girth at least g_N.
```

Take three disjoint copies of `B_N`. Add one new left vertex `e_*` and connect it to one right vertex in each of the three copies.

The resulting bipartite graph has:

```text
left side:  3N + 1,
right side: 3N.
```

Every left vertex has degree exactly three, so it is the incidence graph of a 3-uniform hypergraph `H_N` with

```text
|E(H_N)| = 3N+1,
|V(H_N)| = 3N.
```

No new cycle can use `e_*`: after entering one connected component through `e_*`, a simple path cannot reach a different component without returning through `e_*`. Therefore the incidence girth remains at least `g_N`.

Choose

```text
t_N = floor((g_N-1)/4).
```

By Theorems 1 and 2,

```text
sd_F(Range(C_{H_N})) > t_N = Omega(log N) = Omega(log n).
```

## 4. Output flips

Let `T_a(y)=y XOR a`. Over any field, on Boolean coordinates this is the invertible affine substitution

```text
Y_i -> Y_i                 if a_i=0,
Y_i -> 1-Y_i               if a_i=1.
```

It preserves total degree and maps the vanishing ideal of `S` bijectively to the vanishing ideal of `T_a(S)`. Hence the minimum degree is preserved.

## 5. What the proof does not establish

1. It does not show `NC⁰₃-Avoid` is hard.
2. It does not contradict the polynomial algorithm for monotone `NC⁰₃-Avoid`.
3. It does not produce a circuit lower bound.
4. It does not show that every algebraic certificate is hard; it excludes only globally vanishing identities of degree `o(log n)` for this family.
5. The high-girth construction is randomized-constructible here. A clean deterministic explicit construction with fully quantified constants remains a V54 task.
