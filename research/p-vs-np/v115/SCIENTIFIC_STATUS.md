# V115 scientific status

## Promotable claim candidate

V115 proves a polynomial-time fixed-pair decision theorem for excess overlap at most one under the structural hypothesis that every non-common V113 dominator stage is acyclic.

The proof has three independent components:

1. the V113 theorem that minimum overlap equals the number of common gate dominators;
2. the V115 DAG prefix/suffix separation lemma for the unique extra shared gate;
3. a finite-state extension of the V113 phase DP with one excess-overlap budget bit.

## Why this is a material advance

V113 handles only the exact minimum-overlap face (`Delta=0`). V114 shows that arbitrary one-extra-gate completion in a general directed return graph is NP-complete, so an unrestricted guessed-waypoint continuation is not available.

V115 identifies a structural frontier where positive excess overlap is nevertheless tractable. The strict family has exact positive stretch `m=n+1`, is rejected on the full V113 optimum face, and requires exactly one additional shared gate.

## Verification status to preserve

The primary implementation must be cross-checked against direct route enumeration on small all-DAG-stage instances. The independent verifier must not import the V115 algorithm and must reconstruct the strict family and semantic target checks separately.

The committed finite corpus is falsification evidence, not the proof. Larger local exploratory corpora may be mentioned only as development evidence and must not replace the structural argument.

## Literature calibration

Tholey's 2012 DAG two-disjoint-paths result is prior art at the graph level. Fortune--Hopcroft--Wyllie's 1980 directed linkage hardness result is the relevant general-directed boundary. V115 claims neither result as new.

The signed-MUX dominator-stage transfer and exact-stretch separation family have not received specialist external review. Novelty is unconfirmed.

## Current global status

The result remains conditional on the all-DAG-stage structural hypothesis. No argument shows that arbitrary signed-MUX instances satisfy that hypothesis. Cyclic stages remain the next obstruction.

This laboratory does not resolve unrestricted signed-MUX `0x1b`, unrestricted `NC0_3-Avoid`, general circuit lower bounds, or P versus NP.
