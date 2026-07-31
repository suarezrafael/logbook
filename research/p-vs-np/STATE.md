# Cumulative scientific state

**Current laboratory:** V67  
**Updated:** 2026-07-31  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent

## Current scientific position

V66 introduced affine-cell branching for the six essential non-affine ternary classes. V67 now distinguishes independent composition from genuine overlap.

For disjoint systems, consistent branch counts multiply. Since every affine-cell partition of the V57 gadget has `c=1`, direct sums of those gadgets retain `c=1`; a grafted tree has an additive leaf upper bound. Thus V57 direct sums are not candidates for amplifying branch complexity.

Overlapping supports behave differently. A deterministic seed-42 probe over 4,000 positive-fiber `0x07` systems with `m=n+1` preserves `c=16` at `n=10` and finds `c=36` at `n=11`. The latter witness satisfies:

```text
36 <= L_aff=61 <= L_greedy=62
G_aff=108
```

This is a finite lower-bound witness for tree leaves, not an asymptotic exponential family. It also does not establish a minimum DAG size.

## V67 exact scope

- direct-sum proposition: `c(A ⊕ B)=c(A)c(B)`;
- tree composition: `L_aff(A ⊕ B) <= L_aff(A)+c(A)(L_aff(B)-1)`;
- V57 direct-sum corollary: `c=1` and additive tree upper bound;
- 18 explicit regular cyclic overlap controls for `4<=n<=12`, all with `c=1`;
- 4,000 seeded random overlapping-support systems;
- preserved `n=10,m=11,c=16` witness at iteration 344;
- strongest sampled `n=11,m=12,c=36` witness at iteration 2360;
- computable sandwich `c <= L_aff <= L_greedy`.

## What remains open

The binary question is whether a scalable family forces superpolynomial or exponential `c`, or whether all systems admit a polynomial branching/DAG bound. Finite sampled maxima do not decide this.

The next laboratory must analyze the `c=36` witness structurally, attempt an explicit recursive amplification, and separately optimize merged residual-state DAGs. Exact `L_aff` should be reserved for selected witnesses; larger searches should use the `c`/greedy sandwich.

## Lower-bound route gates

1. Obtain a scalable certificate, upper bound, or explicit lower-bound family for all six non-affine classes.
2. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
3. Establish a complete reduction to a lower bound strong enough to bear on NP versus polynomial-size circuits.
4. Only then evaluate a logical P-versus-NP consequence.

## External requests

The earliest planned follow-up date remains **2026-08-24**. Silence is not evidence of novelty, correctness, or approval.

## Historical corrections

**V22 reproducibility correction:** the original `full_certificate_cases.json` is absent. V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. The incomplete `n=9` search remains falsification/regression only.

## Repository entry points

- `v67/DIRECT_SUM_PROPOSITION.md` — exact composition theorem;
- `v67/BRANCHING_SANDWICH.md` — scalable lower/upper bounds;
- `v67/OVERLAP_GROWTH_REPORT.md` — experimental scope;
- `v67/WITNESSES.json` — exact `c=16` and `c=36` systems;
- `v67/V68_CORE_CONTEXT.md` — next laboratory constraints.
