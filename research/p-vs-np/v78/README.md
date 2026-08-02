# Laboratory V78 — reproducibility firewall

V78 blocks further theorem promotion until cumulative verification is demonstrably read-only on a clean checkout.

## Priority-zero deliverables

- store CI transcripts outside the repository checkout;
- run a blocking clean-tree assertion after quick and full verification;
- replace the hand-maintained LaTeX workflow command list with a validated manifest;
- derive runner coverage from `STATE.md` and the filesystem rather than the stale ledger;
- inventory and repair every verifier or generator that modifies versioned artifacts;
- reconcile `LEDGER.json` through the promoted laboratory;
- preserve historical retractions independently of regenerators;
- canonicalize committed JSON and remove wall-clock measurements from scientific snapshots.

## Current phase

Quick and full cumulative verification now execute from an exact `git archive` inside a disposable sandbox. Legacy regenerators may modify only that sandbox; every modified, created, or deleted path is still printed as a mutation inventory. The source checkout remains protected by the blocking clean-tree gate.

This isolation fixes the CI boundary without treating generated files as harmless or adding an allowlist. The inventory remains technical debt: V78 is not complete until the historical verifiers are individually converted to compare immutable committed evidence without rewriting it.

## Nonclaims

V78 is infrastructure and audit work. It establishes no avoidance result, no circuit lower bound, and no progress claim toward resolving P versus NP.
