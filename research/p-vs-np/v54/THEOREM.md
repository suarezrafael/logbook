# V54 — Quartic separators from forcing cores

## Definitions

Let `F` be a field and `S subseteq {0,1}^m`. For `y notin S`, define

```text
sepdeg_F(S,y) = min deg(Q),
```

where `Q` ranges over nonzero multilinear polynomials satisfying `Q(s)=0` for every `s in S` and `Q(y) != 0`.

For a `k`-uniform hypergraph `H=(V,E)`, define

```text
C_H(x)_e = product_{v in e} x_v.
```

## Theorem 1 — positive excess forces a nonempty 2-core

If `|E|>|V|`, then the support hypergraph has a nonempty 2-core. Repeatedly deleting isolated vertices or degree-one vertices with their unique incident edge never decreases `|E|-|V|`, so the process cannot end empty.

## Theorem 2 — forcing-core separator

Let `e` be an edge in the 2-core. For every `v in e`, choose another core edge `f_v != e` containing `v`, and let `F_e` be the set of distinct witnesses. Then

```text
Q_e(Y) = (1-Y_e) product_{f in F_e} Y_f
```

vanishes on `Range(C_H)` over every field, has degree at most `k+1`, and rejects the explicit target with `y_e=0`, `y_f=1` for witnesses, and all other coordinates zero.

Therefore

```text
min_{y notin Range(C_H)} sepdeg_F(Range(C_H),y) <= k+1.
```

## Corollary — pure AND3

Every pure `AND3` circuit with `m>n` has an explicit missing target with separating degree at most four over every field.

The preserved examples are exact:

```text
UF2: sepdeg = 3,
UF3: sepdeg = 4
```

over `GF(2)`, `GF(3)`, and `GF(5)`.

## Ceiling on the V53 union-free transfer

No `k`-uniform hypergraph with positive excess can be `(k+1)`-union-free in the V53 sense, because

```text
union(F_e) = union(F_e union {e}).
```

For `k=3`, positive stretch rules out 4-union-freeness.

## Signed singleton-fiber extension

Suppose every ternary gate belongs to the NPN orbit of `AND3`, so one output value has a unique local assignment. Orient each output as `Z_i=Y_i` or `Z_i=1-Y_i` so that `Z_i` is a conjunction of three signed input literals.

Build the signed-support hypergraph on used literal nodes `(x_v=0)` and `(x_v=1)`. If the number of gates exceeds the number `L` of used signed literals, a 2-core yields

```text
(1-Z_e) product_f Z_f = 0
```

with degree at most four and an explicit missing target.

Consequences:

- coherent input polarities: `L<=n`, so `m>n` suffices;
- arbitrary polarities: `L<=2n`, so `m>2n` suffices.

## Scientific boundary

The V53 union-free substitution theorem remains valid. The V53 girth implication and the derived `Omega(log n)` family are retracted. V54 does not solve general `NC0_3-Avoid`.
