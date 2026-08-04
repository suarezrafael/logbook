# Retroactive implication audit: V80–V90

This audit applies the implication-ratio policy retrospectively. It does not retract correct mathematical results. It changes how they are counted.

| Laboratory | Main product | External implication status | Classification |
|---|---|---|---|
| V80 | finite Hall/branchwidth controls and target-stretch setup | no closed external consequence | infrastructure/internal |
| V81 | conservation and balanced width-deficiency relations | potentially useful structural lemma; external consequence not yet reviewed | conditional/internal |
| V82 | Hall minima and transversal-girth equivalence | connects to established optimization/complexity questions, but no new lower bound follows alone | trajectory-support |
| V83 | exact selector correspondence and degree-three hardness | correct complexity classification; no closed implication to a frontier lower bound | internal/complexity audit |
| V84 | FP^NP extraction and Hall-expander promise reduction | explicit conditional chain through Range Avoidance and rigidity-style lower-bound programs | conditional frontier chain |
| V85 | predicate/syndrome and remote-point machinery | explicit conditional chain through Range Avoidance/remote-point constructions | conditional frontier chain |
| V86 | defeat of Hall plus constant-syndrome certificates | rules out two broad internal mechanisms; natural-proofs risk becomes visible | barrier |
| V87 | probabilistic family defeating Hall, syndrome, and bounded width | no direct external lower bound; strong negative evidence against the certificate ladder | barrier/internal |
| V88 | exact Eval_H collision geometry and four-row lower bound | no known external consequence beyond the laboratory constructor model | internal |
| V89 | eight-row addressing condition, overlap geometry, and peeling obstructions | conditional bridge only; no global theorem and no external lower bound | conditional/internal |
| V90 | finite entropy ball plus barrier/closure decision | the local theorem is internal; the governance result prevents further drift | barrier/closure |

## Consequences

1. V84 and V85 remain the strongest trajectory-aligned laboratories because they have an explicit conditional chain into Range Avoidance and lower-bound work.
2. V86 and V87 are not failed positive laboratories. They are barrier laboratories showing that the certificate ladder does not scale by simply adding another broad, efficiently recognizable obstruction.
3. V88–V90 produced correct mathematics but did not close an implication to a recognized frontier. They are not counted as completed frontier progress.
4. V81 and the rank-three transfer used in V87 should be isolated into short statements suitable for external checking. Their value must be decided by independent review rather than internal accumulation.

## Reopening rule

The `Eval_H` front may be reopened only with a new external implication chain. Improving a finite census, a local radius, or an internal constructor constant is insufficient by itself.
