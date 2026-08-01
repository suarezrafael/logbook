# V72 prior-art scope

## Graph linearwidth

Dimitrios M. Thilikos introduced and studied graph linear-width using the same edge-order vertex-boundary function used here:

- D. M. Thilikos, *Algorithms and obstructions for linear-width and related search parameters*, Discrete Applied Mathematics 105 (2000), 239–271.
- DOI: `10.1016/S0166-218X(00)00175-X`.

The paper gives structural and algorithmic results for small graph linearwidth. V72 does not claim to introduce graph linearwidth.

## Computational complexity and exact algorithms

Yasuaki Kobayashi and Yu Nakahata record that computing graph linearwidth is NP-hard and give an exact `O*(2^n)` graph algorithm:

- Y. Kobayashi and Y. Nakahata, *A Note on Exponential-Time Algorithms for Linearwidth*, arXiv:`2010.02388`.

V72 contributes a repository-specific exact `O*(2^m)` labelled-hyperedge DP and the explicit private-vertex transfer showing NP-completeness for simple three-uniform support hypergraphs. The reduction is elementary once graph NP-hardness is used; novelty is not claimed without review.

## Pathwidth and vertex separation

The equality between pathwidth and vertex separation is classical:

- N. G. Kinnersley, *The vertex separation number of a graph equals its path-width*, Information Processing Letters 42(6) (1992), 345–350.
- DOI: `10.1016/0020-0190(92)90234-M`.

V71 used this correspondence to derive constructible gate orders. V72 implements the exact vertex-separation DP only as an audit and benchmark tool.

## Linearwidth versus pathwidth

Kobayashi and Nakahata discuss the corrected relation that graph linearwidth and pathwidth differ by at most one, with a small exceptional graph. V72 uses this only to transfer the known unbounded pathwidth of perfect binary trees to unbounded graph linearwidth; the finite implementation also verifies the relevant inequalities on its preserved instances.

## Branch decompositions and affine residuals

Branchwidth and tree-decomposition dynamic programming are classical frameworks. V72's claim is deliberately narrower: for this repository's affine-cell residual semantics, child residual sets can be conjoined and projected exactly over a supplied binary gate decomposition. No novelty claim is made for generic tree-decomposition dynamic programming, and no equivalence to a standard branching-program or proof-complexity model is asserted.

## Current literature status

The prior-art audit supports the terminology and the hardness source. It does not establish novelty of the hypergraph formulation, the exact padding statement, or the affine branch-residual composition theorem. External review remains pending, and no public DOI or submission status is claimed.
