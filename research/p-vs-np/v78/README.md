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

The first V78 commit installs the firewall and intentionally lets CI expose remaining dirty generators. Subsequent commits must remove every reported mutation. No unexplained allowlist is permitted.

## Nonclaims

V78 is infrastructure and audit work. It establishes no avoidance result, no circuit lower bound, and no progress claim toward resolving P versus NP.
