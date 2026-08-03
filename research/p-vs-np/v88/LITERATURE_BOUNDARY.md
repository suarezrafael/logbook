# V88 literature boundary

## Internal scope

The collision normal form, the universal two-row constructor, and the exact
three-row labeled-hypergraph reduction are proved directly in the V88 theorem
packet and verified by exhaustive finite audits. This initial candidate does
not depend on an external asymptotic theorem.

## Adjacent areas requiring a separate source audit

Future constructive work may touch:

- separating hash families and perfect hash families;
- small-bias and splitters;
- labeled hypergraph coloring and property-B variants;
- deterministic CSP unsatisfiability constructions;
- remote-point algorithms for structured local maps.

No theorem from those areas is imported by the current packet. Before a later
V88 commit uses one, the exact statement, parameter scale, uniformity, and
constructivity assumptions must be checked against a primary source.

## Novelty discipline

The normal form is an exact reformulation of repeated truth-table consistency.
It is useful to the laboratory but is not claimed to be new in coding,
constraint-satisfaction, or hypergraph language. The finite census establishes
implementation agreement, not asymptotic novelty.

No claim is made about `P` versus `NP`, circuit lower bounds, proof complexity,
or explicit rigid matrices.
