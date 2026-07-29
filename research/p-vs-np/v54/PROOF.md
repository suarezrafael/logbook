# Detailed proofs — V54

## Nonempty 2-core

Start with a finite hypergraph `H=(V,E)` satisfying `|E|-|V|>0`. Repeatedly delete an isolated vertex, or delete a degree-one vertex together with its unique incident edge. The first operation increases the excess by one; the second preserves it. The process cannot end with the empty hypergraph, whose excess is zero. Thus a nonempty 2-core remains.

## Forcing polynomial

Choose a core edge `e`. For each `v in e`, core degree at least two gives an edge `f_v != e` containing `v`. Let `F_e` be the distinct witnesses.

If all witness outputs are one, every variable in every witness is one, including every vertex of `e`. Hence `Y_e=1`. Therefore

```text
Q_e=(1-Y_e) product_{f in F_e}Y_f
```

vanishes on the range. The target with witness coordinates one and `Y_e=0` makes `Q_e=1` and is absent. Since at most one witness is chosen per vertex, `deg Q_e<=k+1`.

## Exactness for UF2 and UF3

The valid V53 transfer says that distinct unions of all edge subfamilies through size `t` imply no identity of degree at most `t` over any field. UF2 is 2-union-free and has a degree-three forcing separator. UF3 is 3-union-free and has a degree-four forcing separator. Their separating degrees are therefore exactly three and four.

## Why the V53 girth proof failed

The original proof removed common edges from equal-union families and assumed both residual families were nonempty. This fails for nested collisions.

For

```text
e={0,1,2}, f0={0,3,4}, f1={1,5,6}, f2={2,7,8},
```

the incidence graph is a tree, yet

```text
union({f0,f1,f2})=union({e,f0,f1,f2}).
```

Thus even infinite incidence girth does not imply 4-union-freeness.

## Signed singleton-fiber gates

For a ternary gate with a singleton fiber, choose `Z_i=Y_i` or `Z_i=1-Y_i` so that `Z_i=1` on exactly one local assignment. Then `Z_i(C(x))` is a conjunction of three signed literals. Treat signed literals as vertices and repeat the 2-core argument. Because each `Z_i` is affine in `Y_i`, the separator degree remains at most four.

## Complexity

Incidence construction and 2-core peeling are linear in the representation size. The target and separator use at most `k+1` output coordinates. No enumeration of the input cube or image is required.
