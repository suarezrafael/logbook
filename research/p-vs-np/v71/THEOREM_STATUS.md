# V54–V71 theorem-status table

| Item | Category | Status | Scope / limitation |
|---|---|---|---|
| V54 pure-`AND_k` degree separator | proved theorem | internally verified | direct monotone overlap exists |
| V56 affine consistency-or-redundancy | proved theorem | internally verified and formally packaged | efficiently represented affine mixtures only |
| V57 five-block orbit-`0x07` irredundancy | proved construction | internally verified | circuit-specific block statement |
| V58 orientation-depth algorithm | proved parameterized algorithm | internally verified | runtime depends on orientation depth |
| V59 internal-boundary inequality | prior-art application | classical | not a new isoperimetric theorem |
| V60 easy-membership Las Vegas sampler | elementary theorem | internally verified | assumes polynomial-time image membership |
| V68 spine complete-tree lower bound | proved theorem | internally verified | does not lower-bound DAGs |
| V68 linear projected DAG for spine | proved construction | internally verified | separates tree from projected DAG only |
| V69 set-layer invariance and subset-lattice optimization | proved theorem/algorithm | internally verified | exact algorithm is exponential in gate count |
| V70 support-frontier residual bound | proved theorem | internally verified | needs a small supplied/found frontier order |
| V70 component factorisation | proved theorem | internally verified | components use the full processed incidence graph |
| V71 `q*` = support-hypergraph linear branch-width | proved correspondence | internally verified | exact vocabulary identification |
| V71 pathwidth sandwich | proved theorem | internally verified | additive rank-dependent equivalence |
| V71 path-decomposition projected-DAG bound | proved constructive corollary | internally verified | parameterized by supplied primal pathwidth |
| V71 tree-decomposition affine DP | proved parameterized DP | internally verified | feasibility DP, not a bound on linear `G*_proj` |
| V66–V70 numerical records | finite experiments | reproducible | no global maximum or asymptotic inference |
| V53 girth-to-union-free implication | retraction | false and preserved | cannot support a lower bound |
| universal polynomial good order | open conjecture | unproved | direct positive route remains open |
| superpolynomial `G*_proj` family | open conjecture | unproved | direct negative route remains open |
| simulation to OBDD/FBDD/resolution/Res-Lin | open interface | unproved | external lower bounds cannot be imported |
| P versus NP | open problem | unresolved | direct route inactive |

## Reviewed prior-art anchors

- Thomas-style graph linear-width is the rank-two specialization of the V71 edge layout.
- Hypergraph branch decompositions use the same vertex-boundary separation function.
- Kinnersley proves vertex separation equals pathwidth.
- Bodlaender–Kloks provide constructive fixed-parameter pathwidth/treewidth algorithms.
- Range-Avoidance references in the cumulative ledger remain the lower-bound interface background.

“Internally verified” means proof text plus repository checks; it does not mean peer reviewed or novelty confirmed.
