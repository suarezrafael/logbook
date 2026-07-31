# Cumulative scientific state

**Current laboratory:** V66  
**Updated:** 2026-07-31  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent

## Current scientific position

The central narrative remains V56 affine-positive, V57 union-level bijunctive obstruction, and V58 orientation-depth localization. V66 descends below each non-affine fiber into two disjoint affine cells and measures the adaptive branching needed before every leaf has either an inconsistency certificate or a consistent affine V56 certificate.

This does not extend V56 to unrestricted `NC0_3-Avoid`. It supplies exact finite branch-complexity data and preserves the gap to lower-bound-relevant Range Avoidance regimes.

## V66 exact and sampled scope

- six essential non-affine ternary NPN classes: `0x07`, `0x16`, `0x17`, `0x19`, `0x1b`, `0x1e`;
- V57 reproduction: 243 partition systems, one consistent complete branch each, optimal leaf range 8–9;
- complete `n=3` domain: 168 non-affine fibers and 392 affine-cell gate variants;
- exact four-gate signature states: 919 states, at most four consistent complete branches;
- canonical `n=3`, `m=4`: 40,920 systems, maximum `L_aff=11`, maximum selected-policy `G_aff=17`;
- deterministic `n=4`, `m=5` stress: 50,000 samples with seed `660066`, observed maximum five consistent branches, `L_aff=14`, `G_aff=23`.

The `n=4` search is not exhaustive. No asymptotic polynomial branching theorem and no counterexample to polynomial branching are claimed.

## Branch parameters

- `L_aff`: leaves in the lexicographically optimal inconsistency-pruned adaptive tree;
- `D_aff`: maximum depth of that tree;
- `G_aff`: distinct residual `(feasible inputs, remaining gates)` states reached by that selected policy.

These are repository-local finite parameters. No equivalence to resolution width, OBDD size, Res-Lin, or tree-like parity resolution is claimed.

## Lower-bound route gates

1. Find a scalable certificate or branching bound for all six non-affine classes.
2. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
3. Establish a complete reduction to a lower bound strong enough to bear on NP versus polynomial-size circuits.
4. Only then evaluate a logical P-versus-NP consequence.

## External requests

No additional reminder is sent in V66. The earliest planned follow-up date is **2026-08-24**. On or after that date, both original subjects must be checked once before any follow-up. Silence is not evidence of novelty, correctness or approval.

## Validation infrastructure

Promoted-era laboratories with verifiers must be present in the cumulative runner. Quick and full transcripts are retained as GitHub Actions artifacts. Standalone V64 and V65 LaTeX modules compile in a separate CI job. These checks support reproducibility but do not add mathematical evidence.

## Historical corrections

**V22 reproducibility correction:** the original `full_certificate_cases.json` is absent. V22 remains a proof candidate without repository-reproduced finite evidence, and its cumulative row remains a justified skip. V26 remains a justified missing-script skip. The incomplete `n=9` search remains falsification/regression only.

## Repository entry points

- `v66/AFFINE_CELL_BRANCHING_SPEC.json` — normative finite expectations;
- `v66/RESULTS.json` — generated exact and sampled results;
- `v66/N3_EXACT_SEARCH.md` — complete three-variable scope;
- `v66/N4_STRESS_SEARCH.md` — deterministic non-exhaustive stress search;
- `v66/V67_CORE_CONTEXT.md` — next laboratory constraints.
