# Laboratory V78 — reproducibility firewall

V78 establishes a clean-checkout boundary for cumulative verification before further theorem expansion.

## Completed deliverables

- CI transcripts are stored outside the repository checkout;
- quick, full, and LaTeX jobs end with blocking clean-tree assertions;
- quick and full verification run from an exact `git archive` in a disposable sandbox;
- the sandbox reports every modified, created, or deleted path instead of hiding mutations;
- the hand-maintained LaTeX command list is replaced by a validated manifest;
- runner coverage is derived from `STATE.md` and the filesystem rather than the stale ledger;
- the V53 retraction record is validated without rewriting its committed snapshots;
- the complete legacy mutation baseline is recorded in `MUTATION_INVENTORY.md`.

## Scope boundary

V78 solves the containment and observability problem: cumulative verification can execute all historical checks while the protected checkout remains unchanged, and legacy writes remain visible as an explicit inventory.

Converting all historical generators into immutable-evidence comparators is a separate migration with a larger change surface. That remediation is assigned to V79 rather than being hidden inside the firewall release.

## V79 handoff

V79 must reduce the recorded mutation inventory to zero, remove wall-clock data from scientific snapshots, classify generated diagnostics versus committed evidence, and reconcile `STATE.md`, `LEDGER.json`, and publication indexes through the promoted laboratory.

## Nonclaims

V78 is infrastructure and audit work. It establishes no avoidance result, no circuit lower bound, and no progress claim toward resolving P versus NP.
