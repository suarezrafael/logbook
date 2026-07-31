# Structural analysis of the V67 `c=36` witness

V68 reconstructs the branch signatures and support-position incidence of the preserved V67 witness.

## Exact observations

- complete consistent signatures: `36`;
- frozen gate bits: indices `7` and `8`, both fixed to zero;
- independent branch-factor bits: indices `3` and `5`;
- deleting either independent bit leaves exactly `18` residual signatures, and each residual occurs with both bit values;
- branch-set factorization: `2 x 18`;
- variables never used in the pinned first support position: `3`, `4`, and `9`.

The last item uses the V68 big-endian local convention in which mask `0x07` pins the first support coordinate.

## Interpretation

The sampled `c=36` witness is not itself the final scalable family. Its useful signal is that branch multiplicity survives where variables escape the repeatedly pinned position and where one branch coordinate separates as a direct factor.

The spine construction distills this into one globally pinned variable and disjoint fresh pairs. It replaces the sampled `2 x 18` factorization with an exact product of `k-1` binary factors.

## Boundary

This analysis explains a mechanism in one finite witness. The exponential theorem comes from the separately defined spine family and its proof, not from extrapolating the sampled maximum.
