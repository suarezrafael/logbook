# Cumulative scientific state

**Current laboratory:** V68  
**Updated:** 2026-07-31  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP research active:** exploratory  
**Direct P-versus-NP route active:** no  
**P versus NP resolved:** no  
**External review:** requested, replies pending  
**External contact:** sent

## Current scientific position

V68 promotes an explicit stretch-one spine family. For `k>=1` it uses one shared spine variable and `k` fresh variable pairs, with `n=2k+1` and `m=2k+2=n+1`. Every gate lies in the NPN orbit of `0x07`, and every branch cell is affine.

The exact branch count is

```text
c=2^(k-1)=2^((n-3)/2).
```

Since distinct complete consistent signatures require distinct complete leaves, complete inconsistency-pruned affine-cell branching trees are exponentially large on this family. This is an asymptotic theorem for the specified tree model, not an inference from sampled maxima.

The same family has an explicit linear DAG under a stronger quotient. After each gate, equations on variables absent from all remaining supports are existentially projected away, and the canonical residual affine system is hashed. The fixed ordered construction has

```text
G_proj=3k+4
```

nonterminal states. `G_proj` is not the historical `G_aff`, and no minimum-DAG or standard proof-system equivalence is claimed.

## V68 exact scope

- masks `0x07`, `0x0b`, and `0x0d`, all in one NPN orbit;
- exact construction for every `k>=1`;
- proof that motif zero is frozen by two anchors;
- proof that each remaining motif contributes exactly two independent signatures;
- tree lower bound `L_aff>=2^(k-1)`;
- explicit projected ordered DAG with `3k+4` nonterminal states;
- brute-force validation for `k=1..5`;
- symbolic/bitset and projected-DAG checks for `k=1..64`;
- independent semantic verifier using explicit relations rather than the primary GF(2) engine;
- structural reconstruction of the V67 `c=36` witness: frozen gates `7,8`, factor `2 x 18`, and variables `3,4,9` absent from the pinned position.

## Consequence for the branching program

The inconsistency-pruned tree route is closed as a general polynomial strategy for this frontier: an explicit stretch-one orbit-`0x07` family forces exponentially many complete leaves.

The projected-DAG question remains open. The spine family is easy after dead-variable projection and therefore does not supply a DAG lower bound. The next binary target is whether every affine-cell stretch-one system admits a polynomial constructible projected residual DAG or whether some explicit family forces superpolynomial `G_proj`.

## Lower-bound route gates

1. Resolve projected-DAG complexity across all six non-affine classes, not only the spine family.
2. Reach unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime.
3. Establish a complete reduction to a lower bound strong enough to bear on NP versus polynomial-size circuits.
4. Only then evaluate a logical P-versus-NP consequence.

## Proof-complexity boundary

The repository has no simulation theorem between `G_proj` and OBDD, FBDD, resolution, Res-Lin, or tree-like parity systems. Tseitin/expander constructions are future experimental candidates only; existing lower bounds cannot be imported without a size-preserving translation.

## External requests

The earliest planned follow-up date remains **2026-08-24**. Silence is not evidence of novelty, correctness, or approval.

## Historical corrections

**V22 reproducibility correction:** the original `full_certificate_cases.json` is absent. V22 remains a proof candidate without repository-reproduced finite evidence. V26 remains a justified missing-script skip. The incomplete `n=9` search remains falsification/regression only.

## Repository entry points

- `v68/SPINE_FAMILY_THEOREM.md` — construction and proof;
- `v68/V68_SPINE_TREE_DAG_THEOREM.tex` — formal module;
- `v68/affine_bitset.py` — incremental RREF and projected hashing;
- `v68/PROJECTED_DAG_MODEL.md` — exact `G_proj` definition;
- `v68/RESULTS.json` — finite and symbolic verification output;
- `v68/V69_CORE_CONTEXT.md` — next laboratory constraints.
