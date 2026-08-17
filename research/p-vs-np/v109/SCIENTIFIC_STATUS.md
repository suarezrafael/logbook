# V109 scientific status

## Established inside the candidate package

- Gate-disjoint opposite-phase directed MUX cycles give a constructive fixed-output contradiction.
- A gate-capacitated max-flow search detects such double cycles in polynomial time.
- In a strongly connected branch graph, the same network yields an exact alternative: flow two gives the missing-output certificate; flow one gives a single output gate dominating both return cones.
- Exact-stretch Hall-minimal family with strongly connected branch graph that V109 solves.
- The same family has no V108 SCC-separated certificate under **any** ignored-output set.
- Exact V102 backdoor on that family: `beta = 1 + 2 ceil(k/2) = Theta(n)`.

## Still open

- Turning the one-gate bottleneck alternative into a polynomial missing-output construction.
- Polynomial-time avoidance for every essential MUX/bijunctive `0x1b` circuit.
- Unrestricted `NC0_3-Avoid`.
- Any new general circuit lower bound.
- P versus NP.

## Validation status

Primary and independent verifiers are included.  No novelty, priority, or external peer-review claim is made.  Current primary range-avoidance literature still describes the low-stretch `NC0_3` frontier as difficult and does not, in the targeted searches, expose a matching MUX gate-flow theorem.  Search absence is not novelty evidence.
