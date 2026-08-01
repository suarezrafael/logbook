# V76 core context — balanced decomposition transfer

## Starting theorem chain

V74 gives exact arbitrary-fiber preimage counting and constructive avoidance in

```text
O(m^2 A(b)^2 poly(n,m))
```

on a supplied width-`b` gate branch decomposition.

V75 compiles the same recurrence into one monotone arithmetic DAG of size

```text
S = O(m A(b)^2)
```

and performs a complete incremental prefix search in

```text
O(A(b)^2 (m + EPL(T)) poly(n,m)),
```

where `EPL(T)=sum_i depth_T(i)`. A logarithmic-height supplied tree gives `O(m log m A(b)^2 poly(n,m))`, while a caterpillar can retain quadratic work.

## Primary V76 question

Prove or refute a constructive transfer of the following form:

```text
input:  a support hypergraph of rank at most three and a width-b branch decomposition,
output: a gate branch decomposition of height O(log m) and width f(b),
```

for the smallest defensible function `f`.

Candidate targets, in decreasing strength:

1. `f(b)=O(b)` by a direct balancing theorem for vertex-boundary connectivity;
2. `f(b)=O(b log m)` via a recursively controlled cut-union argument;
3. a transfer through a graph tree decomposition with explicit parameter conversion;
4. a negative family showing unavoidable width/depth tradeoff.

## New literature input

Korhonen and Oum (arXiv:2601.04756, 2026) give an FPT algorithm for finding width-`k` branch decompositions of oracle connectivity functions. The support-boundary function is symmetric and submodular, so decomposition discovery is no longer an untouched parameterized obstacle. The remaining issue for V75 is depth or external path length.

Bodlaender's log-depth tree-decomposition transformation increases graph treewidth `k` to at most `3k+2`. V76 should determine whether rank-three gate supports can be assigned to bags and converted into a logarithmic-depth gate branch tree with a rigorously bounded support frontier.

## Required proof discipline

- Distinguish branchwidth, linear branch-width, primal treewidth, and decomposition height.
- Prove every parameter conversion; do not infer it from finite examples.
- Treat the 2026 FPT construction as external prior art, not a laboratory theorem.
- Keep arithmetic DAG size, dynamic reevaluations, and affine-operation cost separate.
- Preserve the direct P-versus-NP route as inactive unless an unrestricted lower-bound-relevant consequence is actually proved.

## Required experiments

- exact width/depth Pareto frontiers for all small rank-three support hypergraphs;
- balanced transformations of caterpillar and binary-tree decompositions;
- adversarial searches maximizing width inflation under forced logarithmic height;
- independent boundary computation from raw incidence sets;
- regression on V74 OR paths and V72 private-vertex trees;
- proof-guided checks of any proposed separator or centroid recursion.

## Promotion gates

Quick, full, and LaTeX CI must pass on one final SHA. A final-diff Copilot review must complete with no unresolved actionable finding. No merge while the PR remains draft.
