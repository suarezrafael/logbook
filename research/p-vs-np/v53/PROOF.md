# V53 proof status — corrected by V54

## Valid proof retained

For an edge subfamily `A`, write

```text
Y_A = product_{e in A} Y_e.
```

After substituting the pure `AND3` outputs and multilinearizing on the Boolean cube,

```text
Y_A(C_H(X)) = product_{v in union(A)} X_v.
```

Therefore, if all edge subfamilies of size at most `t` have distinct unions, their output monomials map to distinct input monomials. Distinct multilinear monomials are linearly independent as functions on the Boolean cube over every field. This proves the V53 union-free transfer.

## Invalid proof retracted

The original incidence-girth argument removed common edges from equal-union families `A` and `B` and asserted that both residual families were nonempty. This is false when `A subset B`.

A counterexample is

```text
e  = {0,1,2}
f0 = {0,3,4}
f1 = {1,5,6}
f2 = {2,7,8}.
```

The incidence graph is a tree, but

```text
union({f0,f1,f2}) = union({e,f0,f1,f2}).
```

Thus incidence girth does not control the nested collision needed for full union-freeness.

## Correct replacement

V54 proves that every positive-excess `k`-uniform hypergraph has a nonempty 2-core. Choosing one core edge and one other core edge through each of its vertices gives a relation

```text
(1-Y_e) product_f Y_f = 0
```

of degree at most `k+1` and an explicit missing target. For `AND3`, the degree is at most four.

The detailed corrected proof is in `research/p-vs-np/v54/PROOF.md`.
