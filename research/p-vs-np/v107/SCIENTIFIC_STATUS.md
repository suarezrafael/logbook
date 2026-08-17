# V107 scientific status

**Classification:** candidate frontier progress pending repository CI, review, and external mathematical validation.

Candidate result:

> Every explicit `NC0_3` circuit with `m>n` whose outputs are essential ternary
> signed-majority gates admits a deterministic polynomial-time missing-output
> construction.

The proof combines:

- inclusion-minimal positive-surplus extraction;
- V106's Hall/frame-rank identity;
- polynomial matroid intersection for a one-pair-per-gate frame-independent
  transversal after omitting one output;
- a direct V105 handcuff when the omitted gate spans multiple unbalanced
  unicyclic components;
- a path-compression theorem reducing the same-component case to at most six
  virtual paths;
- a computer-assisted exact finite lemma over 164 generated kernel
  descriptions and 16,032 signed/polarity cases;
- explicit lifting of every virtual implication back to exact pair clauses of
  the original majority outputs.

The implementation does not consult a stored witness table.  It runs matroid
intersection on the actual instance, compresses the actual unicyclic component,
enumerates at most 128 phase/target choices on its constant kernel, checks
2-SAT SCC unsatisfiability, and lifts the chosen phases.

Independent verification is intentionally structurally different: it generates
the reduced kernels from Prüfer trees and separately enumerates unreduced simple
unicyclic controls.

Not established:

- unrestricted polynomial-time `NC0_3-Avoid`;
- polynomial-time avoidance for the remaining MUX/bijunctive `0x1b` orbit;
- any new general circuit lower bound;
- P versus NP;
- novelty, priority, or peer review.

If repository CI and review pass, the highest-value next action is external
specialist review of the computer-assisted kernel lemma and the matroid
transversal/lifting argument before presenting the exact-stretch majority result
as novel.
