# V93 literature boundary

## Checked baseline

Huang, Li, and Zhong, *Range Avoidance and Remote Point: New Algorithms and Hardness*, ITCS 2026, Theorem 1.14, gives for `NC0_k-Avoid[n,n+1]` a family of algorithms with runtime

```text
O(n * 2^((k-2)n/(k-1))).
```

For `k=3` this is `O(n * 2^(n/2))`. V93 uses this only as the runtime baseline for the target row; V93 does not improve it.

## Repository boundary

V85 proves that on C4-free ternary supports every constant output-parity syndrome reduces to an affine subsystem dependency. V87 proves existence of linear-support-branchwidth ternary families, but its width obstruction is existential and not an output-producing certificate. V92 fixes the canonical halving semantics and makes the remaining first bridge the implementation of the exact child comparison on high-width instances.

V93's theorem is internal to the explicitly defined certificate model `AS(C)=(supports,Sigma(C))`. No claim is made that the no-go formulation or proof is novel in the literature. External prior-art validation is still required before presenting it as a new theorem.

## Nonclaims

The certificate collision is not a hardness theorem for exact counting, PP, Compare-#P, canonical Range Avoidance, or `NC0_3-Avoid` itself. It only proves insufficiency of the stated certificate as a total comparison/output oracle.
