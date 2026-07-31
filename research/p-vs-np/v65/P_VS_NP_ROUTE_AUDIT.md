# P versus NP route audit — V65

## Status

The laboratory is actively investigating lower-bound bridges motivated by P versus NP, but it does **not** currently possess a direct route to a separation. `p_vs_np_research_active` is true; `p_vs_np_route_active` and `p_vs_np_resolved` remain false.

## What the current theorem actually gives

V56 solves Range Avoidance only for circuits having a chosen affine output fiber at every coordinate. V57 shows that the direct complete-block argument already fails for one bijunctive ternary orbit. V58 recovers an algorithm only when orientation depth is bounded. These are structural results inside restricted local circuits.

They do not provide:

- deterministic polynomial-time Range Avoidance for all `NC0_3` circuits;
- an algorithm for general Boolean-circuit Range Avoidance;
- an explicit lower bound against polynomial-size circuits for an NP language;
- `P != NP`.

## Primary-source bridge map

1. **ECCC TR22-048 — Ren, Santhanam and Wang.** Algorithms for restricted Range Avoidance can imply explicit constructions and circuit lower bounds; the consequences depend sharply on the circuit class and stretch.
2. **ECCC TR23-021 — Gajulapalli, Golovnev, Nagargoje and Saraogi.** An `FP^NP` algorithm for `NC0_3-Avoid` at stretch `m=n+n^(2/3)` would imply explicit rigid matrices and super-linear lower bounds for log-depth circuits.
3. **ECCC TR25-049 — Huang, Li and Zhong.** For constant-depth classes containing `AC0`, suitable `FP^NP` Range-Avoidance algorithms are equivalent to exponential lower bounds for `E^NP` against the same class; the report also gives subexponential algorithms for `NC0_k-Avoid` at super-linear stretch.
4. **ECCC TR25-191 — Ren, Wang and Zhong.** Hardness of Range Avoidance is connected to demi-bits and proof-complexity generators under cryptographic assumptions.
5. **ECCC TR26-118 — Ren and Williams.** A recent near-maximum lower bound for an exponential-time class uses the Range-Avoidance-to-lower-bounds framework as one ingredient.

These works confirm that Range Avoidance is a serious lower-bound interface. They do not make the present affine-fiber theorem sufficient for P versus NP.

## Gates for this research route

| Gate | Required advance | Current status |
|---|---|---|
| A | Handle all six essential non-affine ternary NPN classes, or prove a replacement certificate | Open; V57 is a counterexample to naive block redundancy |
| B | Obtain deterministic or `FP^NP` algorithms for unrestricted `NC0_3-Avoid` in a lower-bound-relevant stretch regime | Open |
| C | Connect the achieved regime to a lower bound strong enough to bear on NP versus polynomial-size circuits | No such bridge in this repository |
| D | Convert any circuit lower-bound consequence into a logically valid implication for P versus NP | Open; larger exponential-time-class lower bounds alone do not settle P versus NP |

## V66 research target

The next technical experiment should attack Gate A. Each remaining essential ternary fiber is a disjoint union of two affine pieces. Define a branch-state system that selects one affine piece per active gate, then search for either:

1. a bounded branch-rank certificate that yields avoidance; or
2. a smallest explicit counterexample showing that branch rank can grow beyond every proposed bound.

Counterexamples must be promoted before conjectures. No progress percentage toward P versus NP may be recorded.
