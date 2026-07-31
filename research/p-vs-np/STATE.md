# Cumulative scientific state

**Current laboratory:** V65  
**Updated:** 2026-07-30  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent

## Current scientific position

The central narrative remains V56 affine-positive, V57 bijunctive-negative and V58 orientation-depth localization. V65 gives V56 a standalone LaTeX proof module and a normative specification, then validates the dichotomy exhaustively for every multiset of `n+1` nonempty affine subsets in dimensions `n=1,2,3`. Larger generated equation-block systems exercise the constructive certificates.

The project is deliberately searching for lower-bound bridges, but it has no valid direct implication to P versus NP. The known literature shows consequences for explicit constructions, rigid matrices, restricted circuit lower bounds and exponential-time classes. The repository still lacks unrestricted `NC0_3-Avoid`, an NP circuit lower bound and a complete reduction to a P-versus-NP separation.

## V65 exact finite scope

- `n=1`: 6 affine families;
- `n=2`: 286 affine families;
- `n=3`: 316,251 affine families;
- total: 316,543 complete multiset checks;
- every family is either inconsistent or contains a redundant complete block;
- empty fibers are handled immediately;
- no novelty or priority is inferred from finite verification.

## Lower-bound route gates

1. Replace the affine theorem by a certificate covering all six non-affine essential ternary classes.
2. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
3. Establish a complete reduction to a lower bound strong enough to bear on NP versus polynomial-size circuits.
4. Only then evaluate a logical P-versus-NP consequence.

## External requests

The two original Gmail subjects were checked once during V65. No incoming replies were found and no follow-up was sent. Silence is not evidence of novelty, correctness or approval.

## Historical corrections

**V22 reproducibility correction:** the original `full_certificate_cases.json` is absent. V22 remains a proof candidate without repository-reproduced finite evidence, and its cumulative row remains a justified skip. V26 remains a justified missing-script skip. The incomplete `n=9` search remains falsification/regression only.

## Repository entry points

- `v65/V56_AFFINE_FIBER_THEOREM.tex` — formal theorem and proof;
- `v65/V56_AFFINE_FIBER_SPEC.json` — normative specification;
- `v65/P_VS_NP_ROUTE_AUDIT.md` — bridge analysis;
- `v65/V66_CORE_CONTEXT.md` — next technical experiment.
