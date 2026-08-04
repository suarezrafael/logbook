# V91 core context — algorithmic-method feasibility audit

## Mission

V91 is not authorized to begin another open-ended combinatorial search. Its sole initial task is to determine whether the existing counting, prefix, branchwidth, and remote-point machinery can instantiate a published algorithm-to-lower-bound theorem for a nontrivial standard circuit class.

## Implication target

V91 must select one exact transfer theorem and fill every parameter. Two admissible families are:

### Track A — SAT/#SAT transfer

For a typical circuit class `C`, the Vyas–Williams benchmark includes:

- #SAT for every `n^k`-size `C` circuit in time `2^n/n^k`, for every fixed `k`, implying an NEXP lower bound against a sparse symmetric function of `C`;
- #SAT for `2^(n^epsilon)`-size `C` circuits in time `2^(n-n^epsilon)` implying a Quasi-NP lower bound against the corresponding stronger class.

Any use of the original Williams method must state the precise closure hypotheses and theorem version rather than citing “a nontrivial SAT algorithm” informally.

### Track B — Missing-String/Range-Avoidance transfer

Vyas–Williams 2024 gives direct generic links from algorithms or restricted uniform circuits for Missing-String to circuit lower bounds. This track is especially relevant because V74–V85 already construct avoided or remote outputs for bounded-width local maps.

V91 must compare Track A and Track B before choosing one. The closer vocabulary of Track B is not itself a proof that the existing FPT algorithm meets the required model.

## Current engine, stated exactly

The inherited results provide:

1. exact preimage counting for a supplied output word when a support branch decomposition is available;
2. a symbolic arithmetic DAG for all output coefficients and prefix counts;
3. logarithmic-height transfer with width at most twice the support branchwidth;
4. FPT discovery/composition for the support connectivity function;
5. remote-point construction in time

```text
2^{O(k^2)} poly(n,m)
  + O(m^2 A(2k)^2 r^2 poly(n,m)),
```

where `k` is support connectivity branchwidth;
6. polynomial time only in the proved regime `k=O(sqrt(log m))`.

These are algorithms for structurally promised local maps. They are not yet SAT/#SAT algorithms for every circuit in a standard nonuniform class.

## Mandatory audit questions

1. **Class definition.** What exact circuit class `C` is recognized in the transfer theorem?
2. **All-instance coverage.** Does the algorithm work on every `C` circuit, or only on a low-width promise subclass?
3. **Circuit size.** Does it handle `n^k` or subexponential size in the theorem’s required range?
4. **Saving.** Is the runtime genuinely `2^n/n^{omega(1)}`, `2^n/n^k` for all `k`, or `2^{n-n^epsilon}` after all decomposition and arithmetic costs?
5. **Closure.** Is `C` closed under the operations required by the transfer proof?
6. **Nontriviality.** Would the resulting lower bound improve what is already known, or is it automatic from a severe structural promise?
7. **Representation.** Can the multi-output local-map problem be encoded into the exact SAT/#SAT or Missing-String input model without losing the saving?
8. **Uniformity and nondeterminism.** Which part of the transfer evades the natural-proofs barrier, and where is nondeterminism or diagonalization used?

## First quantitative obstruction

The present branchwidth method has no uniform saving on unrestricted instances because V87 constructs relevant families with branchwidth `Omega(n)`. Substituting linear `k` into the present `2^{O(k^2)}` decomposition term is far worse than exhaustive search. Therefore the current engine cannot be inserted into a Williams theorem without a new structural reduction or a different circuit class.

This is the starting gap, not a failure to be hidden.

## Candidate deliverables

V91 succeeds only if it produces one of:

- a complete theorem instantiation with a recognized class and a verified runtime saving;
- a rigorous no-go showing that the current width engine cannot meet any selected transfer benchmark;
- a new reduction that converts an unrestricted class to instances whose width/runtime satisfies the benchmark;
- a Missing-String formulation whose algorithmic parameters directly trigger a published lower-bound consequence.

A new finite census, another width certificate, or a speedup only on hand-picked low-width families does not satisfy the implication policy.

## Meta-complexity side audit

In parallel, V91 may translate the Range-Avoidance objects into Missing-String, MCSP, MKTP, or time-bounded Kolmogorov-complexity language. The translation must identify an established reduction or formulate a precise missing bridge. Terminological proximity is not counted as an implication.

## External validation

Before promotion, isolate two short review packets:

- the V81 conservation/width-deficiency statement;
- the rank-three primal-treewidth/branchwidth transfer used in V87.

They should be written so an external complexity or graph-width researcher can check the statement without reading the full laboratory history.

## Stop rule

If V91 cannot identify a nontrivial class plus a published transfer theorem whose quantitative hypotheses are plausibly reachable, the Williams branch is closed as infeasible for the current machinery. The next move is a narrowly scoped Missing-String/meta-complexity problem, not a return to certificate accumulation.

## Primary references

- R. Williams, “Non-uniform ACC Circuit Lower Bounds,” JACM 61(1), 2014.
- N. Vyas and R. Williams, “Lower Bounds Against Sparse Symmetric Functions of ACC Circuits,” STACS 2020 / ToCS 2023.
- N. Vyas and R. Williams, “On Oracles and Algorithmic Methods for Proving Lower Bounds,” ECCC TR24-113.
- S. Hirahara and R. Santhanam, “On the Average-Case Complexity of MCSP and Its Variants,” CCC 2017.
