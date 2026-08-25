# V119 literature and claim boundary

## Inherited boundary

V117 established a parameterized barrier only for the **generic graph-resource residual problem**: supplied-feedback two-chain linkage in a DAG inherits W[1]-hardness from the two-parallel-demand restriction of directed edge-disjoint paths.  That result is not a signed-MUX hardness theorem.

V118 then identified a signed-MUX-specific tractable exception: one exact clone bank per non-common dominator stage admits loop erasure and a polynomial budget-one algorithm even when the raw feedback-gate number is unbounded.

## V119 contribution relative to the laboratory chain

V119 weakens the V118 structural promise from exact signed-MUX cloning to a bounded **branch-image bank**.  Gates inside the bank may have different selectors, data polarities, and output flips.  The normalization argument uses only repeated arrival at the same destination variable inside a private route segment.

The direct consequence proved in this laboratory is an `N^{O(d)}` algorithm for fixed branch-image size `d`; the special case `d=2` is polynomial and strictly contains the V118 family exhibited here.

## Literature calibration

No targeted external source has been identified that exactly states the V119 signed-MUX destination-loop-erasure theorem or its `4d+4` residual-request formulation.  Related routing, module-compression, bounded-interface, and representative-set techniques may contain analogous ideas.

Therefore V119 must **not** claim literature novelty.  A specialist novelty search/review remains an explicit external-validation obligation.

## Hardness boundary

The V117 W[1]-hardness result cannot simply be transferred to V119: V119 imposes a strong signed-MUX promise that all cyclic gates removed from one stage have branch destinations contained in a bounded set `D`.  Whether the V117 hard instances can be encoded while keeping `d` constant is open.

Conversely, the V119 XP algorithm does not imply FPT in `d`; its enumeration degree depends on `d`.

## Safe claims

The repository may state:

- destination loop erasure bounds one private segment to at most `|D|` bank traversals;
- one extra shared gate yields at most `4d+4` residual DAG requests;
- fixed `d` therefore gives deterministic `N^{O(d)}` decision;
- `d=2` is in P under the stated V113-stage promise;
- the strict family separates V119 from the exact-clone promise used in V118.

## Claims explicitly not supported

V119 does not establish:

- FPT parameterized by `d`;
- NP-hardness or W[1]-hardness for constant/small `d`;
- polynomial time for unbounded branch-image size;
- unrestricted signed-MUX `Delta=1` tractability;
- all `0x1b` signed-MUX avoidance;
- unrestricted `NC0_3-Avoid`;
- P versus NP;
- peer-reviewed or externally confirmed novelty.
