# V53 theorem — union-free supports force high syndrome degree

## Definitions

Let `F` be a field and let `S subseteq {0,1}^m`. Define

```text
sd_F(S) = min deg(Q),
```

where the minimum is over nonzero multilinear polynomials `Q in F[Y_1,...,Y_m]` that vanish on every point of `S`.

A hypergraph `H=(V,E)` is **t-union-free** when any two distinct edge subfamilies `A,B subseteq E` with `|A|,|B| <= t` satisfy

```text
union(A) != union(B).
```

For a 3-uniform hypergraph `H`, define the local Boolean circuit

```text
C_H : {0,1}^V -> {0,1}^E,
C_H(x)_e = AND_{v in e} x_v.
```

Each output has fan-in exactly three.

## Theorem 1 — union-free transfer

If `H` is t-union-free, then over every field `F`,

```text
sd_F(Range(C_H)) > t.
```

Equivalently, the substitution homomorphism

```text
Phi_H : F[Y_e : e in E]_{multilinear, degree<=t}
        -> F[X_v : v in V]_{multilinear}
Phi_H(Y_e) = product_{v in e} X_v
```

is injective.

## Theorem 2 — incidence girth criterion

If the incidence graph of `H` has girth strictly greater than `4t`, then `H` is t-union-free.

Therefore,

```text
incidence_girth(H) > 4t
    => sd_F(Range(C_H)) > t
```

for every field `F`.

## Theorem 3 — stretch-one NC⁰₃ family with growing degree

There is a randomized polynomial-time constructible infinite family of 3-uniform hypergraphs `H_N` with

```text
|E(H_N)| = |V(H_N)| + 1
```

and incidence girth `Omega(log |V(H_N)|)`.

Consequently, the `AND₃` circuits `C_{H_N}` have stretch one and satisfy

```text
sd_F(Range(C_{H_N})) = Omega(log n)
```

simultaneously over every field.

The construction starts from cubic graphs of logarithmic girth, takes bipartite double covers, uses three disjoint copies, and adds one new left incidence vertex connected once into each copy.

## Theorem 4 — output complements preserve the parameter

For any fixed `a in {0,1}^m`, let

```text
S+a = {y XOR a : y in S}.
```

Then

```text
sd_F(S+a) = sd_F(S).
```

The coordinate substitution `Y_i -> Y_i + a_i` is an invertible degree-preserving affine automorphism of the Boolean coordinate ring.

## Scientific interpretation

The result proves that **constant-degree vanishing identities cannot be a universal solution method even for stretch-one `NC⁰₃` circuits**.

It does not prove that these circuits are hard to avoid. The constructed circuits use monotone `AND₃` gates, and monotone `NC⁰₃-Avoid` is already solvable in polynomial time by a different combinatorial method.

The likely reusable contribution is the transfer:

```text
union-free hypergraph / incidence girth
              -> injective low-degree substitution
              -> lower bound on syndrome degree.
```

Union-free hypergraphs and evaluation-code ideas are established subjects. Priority for this exact Range-Avoidance formulation is not claimed.
