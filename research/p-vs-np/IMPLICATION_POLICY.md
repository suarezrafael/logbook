# Implication-ratio policy

Starting with V90, every laboratory must state its implication ratio before it is treated as scientific progress.

## Required declaration

Each `vNN/IMPLICATION.json` must contain:

- `target_problem`: a named open problem or recognized frontier question;
- `conditional_implication`: the exact statement of the form “if result X is proved, then consequence Y follows”;
- `bridge_lemmas`: every nontrivial implication needed between X and Y;
- `current_gap`: the first unproved bridge;
- `classification`: one of `frontier_progress`, `barrier`, `infrastructure`, `audit`, `closure`, or `barrier_and_closure`;
- `stop_rule`: the condition under which the front is abandoned;
- `external_validation_target`: a paper, theorem, seminar, or expert review against which the result can be checked.

A laboratory with no credible implication to a recognized frontier is not counted as frontier progress. It may still be valuable as infrastructure, a barrier result, a reproducibility improvement, or a disciplined closure. The compound value `barrier_and_closure` is reserved for a laboratory that both records a route-level barrier and fires the stop rule for that front.

## Evidence levels

1. **Direct implication.** The new theorem itself resolves or improves a named open problem.
2. **Closed chain.** The new theorem plus already proved, cited lemmas yields the frontier consequence.
3. **Conditional chain.** The new theorem advances a chain but one or more bridge lemmas remain open.
4. **Internal-only.** The result improves the laboratory’s own model without a known external consequence.
5. **Infrastructure/barrier/closure.** The work improves reliability, rules out a route, or prevents further drift.

Only levels 1 and 2 are counted as completed frontier progress. Level 3 is counted as trajectory progress only when the remaining bridge is explicit and recognized in the literature.

## Natural-proofs checkpoint

Before opening another polynomially checkable certificate program, the laboratory must answer all three Razborov–Rudich questions for the induced property of Boolean functions:

- Is the property constructive in the relevant truth-table model?
- Is it large?
- Is it useful against the target circuit class?

A polynomial-time certificate on circuit presentations is not automatically a natural property. Representation independence, largeness, and usefulness must be established. Nevertheless, certificate searches that deliberately seek broad, efficiently recognizable random obstructions must record a natural-proofs risk assessment before receiving more budget.

Primary reference: A. Razborov and S. Rudich, “Natural Proofs,” JCSS 55(1), 1997; ECCC TR94-010.

## Algorithmic-method checkpoint

A proposed SAT or #SAT speedup must instantiate a precise transfer theorem, including:

- the circuit class and its closure properties;
- the allowed circuit size;
- the exact running-time saving;
- whether SAT, #SAT, CAPP, or another analysis problem is required;
- the resulting lower-bound class.

“Faster than brute force” is not a sufficient implication statement. For example, the Vyas–Williams #SAT transfer gives concrete polynomial-factor and subexponential-saving benchmarks for typical circuit classes.

Primary references: R. Williams, “Non-uniform ACC Circuit Lower Bounds,” JACM 61(1), 2014; N. Vyas and R. Williams, “Lower Bounds Against Sparse Symmetric Functions of ACC Circuits,” STACS 2020 / ToCS 2023.

## Governance

- Candidate status requires a valid implication declaration.
- Promotion notes must distinguish frontier progress from internal, barrier, or infrastructure progress.
- A front whose stop rule fires is closed even if it has produced correct intermediate lemmas.
- Reopening a closed front requires a new implication chain, not merely a new computational experiment.
