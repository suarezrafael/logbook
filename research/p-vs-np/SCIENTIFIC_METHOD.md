# Scientific Method and Evidence Protocol

## Claim classes

Every claim in the laboratory must be assigned one of the following classes:

1. **Published reproduction** - the claim is attributed to a primary source and the implementation is a reproduction.
2. **Finite exhaustive theorem** - the universe is explicitly finite and the search is complete.
3. **Proof candidate** - a complete human-readable argument is provided, but external review is pending.
4. **Formal theorem** - a proof assistant or independently checkable formal certificate verifies the claim.
5. **Conjecture** - no proof is claimed; a counterexample search must be specified.
6. **Empirical observation** - the statement is limited to the tested distribution.
7. **Counterexample** - a concrete input falsifies a prior hypothesis.

## Promotion gates

A result may be promoted to the next level only after the relevant gates pass.

### Finite computer-assisted result

- complete generator argument;
- independent verifier;
- preserved certificate and hashes;
- boundary conditions stated;
- no asymptotic extrapolation from benchmark fits.

### Proof candidate

- theorem statement with all assumptions;
- proof decomposed into lemmas;
- dependency on external theorems clearly identified;
- implementation separated from the proof;
- adversarial examples and failed alternatives preserved;
- prior-art search documented.

### Externally validated result

At least one of:

- written review by an expert in the relevant subfield;
- acceptance by a specialist archive or conference screening process;
- formal proof artifact checked by a standard proof assistant.

Silence, GitHub stars, benchmark success, and automated language-model agreement do not count as mathematical validation.

## Reproducibility requirements

Each laboratory version should contain:

```text
README / research note
precise theorem or hypothesis
source code
independent verifier
machine-readable results
manifest with SHA-256 hashes
evidence ledger
hypothesis ledger
limitations
next-version context
```

## Retraction and correction policy

If a flaw is found:

1. keep the original version available;
2. mark the affected claim as withdrawn or corrected;
3. document the smallest failing example;
4. publish a replacement version rather than silently rewriting history;
5. update all summaries and citation metadata.

## P versus NP language policy

The project must not claim progress on P versus NP merely because it:

- improves a heuristic;
- solves finite instances;
- proves a restricted-model theorem already known in the literature;
- finds a faster implementation;
- gives a lower bound for a very restricted class.

A direct P versus NP claim would require a complete proof accepted under extraordinary mathematical scrutiny. No current laboratory result meets that threshold.
