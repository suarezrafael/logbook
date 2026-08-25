# V118 frozen core context — signed-MUX realizability after the two-chain W[1] barrier

## Inherited facts

V116 proves polynomial `Delta<=1` decision when every non-common stage has feedback-gate number at most one.

V117 closes the generic feedback-interface compression route: even when DAG residual requests form exactly two chains, the gate-resource problem is W[1]-hard parameterized by the supplied chain-break/feedback interface size. The reduction uses Slivkins' two-parallel-demand DAG EDP hardness.

## Critical gap

V117 is not yet a signed-MUX hardness theorem. Its hard residual instances are abstract gate-resource graphs with prescribed feedback-chain usage. A valid signed-MUX stage must additionally satisfy:

- each output is an essential ternary MUX with one selector and two data inputs;
- the hard routes arise from the V113 dominator decomposition of one fixed opposite-phase first pair;
- target requirements agree on every shared gate used by an accepting witness;
- the V113 optimum face must be handled correctly rather than bypassing the hard structure;
- the global circuit must retain positive stretch `m>n` (preferably exact `m=n+1`).

## Track A — lift the V117 barrier into MUX

Encode every source DAG edge by a branch-zero MUX whose other branch enters a dead trap. Encode the feedback connectors as MUX gates. Determine whether the prescribed chain traversal can be forced by topology and target phases without introducing a short compatible bypass.

Promotion target: W[1]-hardness parameterized by a supplied or minimum feedback-gate set for the actual fixed-pair signed-MUX `Delta<=1` problem.

## Track B — find the realizability obstruction

If the lift fails, isolate the exact signed-MUX invariant that prevents arbitrary two-chain gate-linkage instances. Candidate invariants:

- selector reuse and branch pairing;
- phase consistency at feedback interfaces;
- unavoidable common gate dominators;
- existence of shortcut/bypass returns;
- a bounded form of demand interaction induced by one MUX output per resource.

A polynomial recognition/compression theorem for that invariant is promotable.

## Track C — minimum feedback parameter

V117 parameterizes the supplied feedback interface. Strengthen to the minimum feedback-gate number only if the reduction proves a parameter bound for the minimum set or forces the supplied set to be minimum. Do not silently identify the two notions.

## Promotion rule

V118 is promotable with at least one of:

- a correct W[1]-hardness transfer to the signed-MUX feedback parameter;
- a rigorous MUX-realizability obstruction invalidating the V117 hard family plus an algorithmic consequence;
- an FPT theorem exploiting a signed-MUX invariant absent from generic gate-linkage;
- another structural result that decisively narrows the remaining feedback-parameter frontier.

Larger fixed-tau experiments alone are not promotable.

## Global boundary

No V117/V118 barrier by itself resolves unrestricted `NC0_3-Avoid`, circuit lower bounds, or P versus NP.
