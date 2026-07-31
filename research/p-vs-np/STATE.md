# Cumulative scientific state

**Current laboratory:** V64  
**Updated:** 2026-07-30  
**Program name:** `NC0_k-Avoid Laboratory`  
**P-versus-NP route active:** no  
**External review:** requested, replies pending  
**External contact:** sent  
**Promotion model:** one laboratory per PR, CI, then merge to `main`

## One-paragraph state

The main narrative remains V56 affine-positive versus V57 bijunctive-negative, followed by V58 orientation-depth localization. V64 makes the V57 finite obstruction formally reviewable through a standalone LaTeX theorem/proof and a normative JSON specification. Primary and independent implementations exhaust all 16 assignments, verify five complete-block witnesses, six clause witnesses, the unique model `0000`, and membership of all five gate masks in the 48-element NPN orbit of `0x07`. The workflow runtime is separately maintained by upgrading `actions/checkout` from v4 to v6.

## V64 formal module

The five blocks are

```text
B1 = not x0 and (not x1 or x2)
B2 = not x0 and (x1 or not x2)
B3 = not x0 and (not x1 or x3)
B4 = not x0 and (x1 or not x3)
B5 = not x0 and (not x2 or not x3)
```

Their conjunction has unique model `0000`. Block witnesses are `0101, 0010, 0110, 0001, 0111`; after collapsing the duplicated unit clause, clause witnesses are `1000` followed by the same five assignments. The exact finite construction is verified; general 2-CNF irredundancy remains prior art and no novelty claim is made.

## Workflow runtime audit

The V63 jobs used runner `2.336.0` and emitted a Node.js 20 deprecation warning for `actions/checkout@v4`. Official checkout documentation identifies v6.0.2 as current, v5 as Node.js 24 with minimum runner 2.327.1, and v6 Docker-container credential use as requiring runner 2.329.0. This workflow uses GitHub-hosted runners and no Docker container action, so it is upgraded to `actions/checkout@v6`. This maintenance decision is separate from scientific validation.

## External requests

The two exact Gmail subjects were checked once during V64. Both returned zero incoming messages. No follow-up was sent because the requests were sent earlier the same date. Silence is not evidence of novelty, correctness or priority.

## Historical reproducibility corrections

**V22 reproducibility correction:** `full_certificate_cases.json` was never committed. The theorem remains a proof candidate, the finite certificate evidence is not repository-reproduced, and the cumulative runner records a justified `SKIP`. V26 remains a justified missing-script skip.

The incomplete `n=9` search remains falsification/regression only and supplies no theorem.

## Current nonclaims

The project does not establish general deterministic `NC0_3-Avoid`, universally bounded orientation depth, unrestricted circuit lower bounds, novelty of general 2-CNF irredundancy, completion of `n=9`, or `P != NP`.

## Repository entry points

- `v62/INTEGRATED_MANUSCRIPT.md` — integrated manuscript.
- `v64/V57_BLOCK_IRREDUNDANCY_THEOREM.tex` — formal theorem/proof.
- `v64/V57_BLOCK_IRREDUNDANCY_SPEC.json` — normative finite specification.
- `v64/ACTION_RUNTIME_AUDIT.md` — workflow maintenance audit.
- `v64/V65_CORE_CONTEXT.md` — next laboratory context.
