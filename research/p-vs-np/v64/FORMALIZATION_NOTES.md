# Formalization notes

## Normative layers

1. `V57_BLOCK_IRREDUNDANCY_SPEC.json` is the machine-readable source of variables, clauses, blocks, masks and witnesses.
2. `V57_BLOCK_IRREDUNDANCY_THEOREM.tex` is the typeset theorem/proof module.
3. `verify.py` derives all finite claims from the JSON specification.
4. `verify_independent.py` reimplements clause evaluation and orbit generation independently.

## What is formally checked

- exact six-clause collapse;
- unique model `0000`;
- five complete-block deletion witnesses;
- six clause-deletion witnesses;
- truth-table masks `0x51, 0x45, 0x51, 0x45, 0x15`;
- NPN orbit size 48 and membership in the orbit of `0x07`;
- direct-sum parameter identity `m=n+1`;
- consistency between JSON, LaTeX, ledger and cumulative runner.

## Boundary

The exhaustive check proves the stated four-variable finite gadget. The direct-sum preservation is elementary and explicitly stated. The package does not establish minimality outside the previously searched universe, novelty, a general `NC0_3-Avoid` algorithm, or a circuit lower bound.
