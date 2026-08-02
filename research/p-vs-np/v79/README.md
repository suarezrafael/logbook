# Laboratory V79 — immutable evidence migration

V79 closes the infrastructure phase needed to restore a stable mathematical workflow.

## Promoted scope

- V54–V59 primary and independent verifiers recompute evidence without rewriting committed snapshots.
- The V58 exact C++ search compiles in a temporary directory and compares stdout with committed evidence.
- Draft pull requests run a focused quick gate plus LaTeX; the cumulative full suite runs only when the PR is ready, on `main`, or by manual dispatch.
- Branch pushes no longer duplicate pull-request workflows.
- Quick mode requires zero sandbox mutations.
- Full mode retains a strict nine-path historical mutation baseline for V65–V72.
- `LAB_STATUS.json` is the operational source of truth and records V79 as promoted.
- `STATE.md` and `LEDGER.json` remain conservative scientific/historical records, not CI authorities.

## Deliberate stopping point

The remaining nine legacy snapshot writers are contained by the V78 sandbox and checked by the full V79 baseline. Converting them is useful maintenance but is not required before resuming mathematical research.

The infrastructure phase is frozen. Future maintenance must be triggered by a demonstrated blocker, not by aesthetic cleanup.

## Next direction — V80

V80 returns to the mathematical frontier after V77:

- factor-two versus width-preserving balancing;
- stronger control of support connectivity branchwidth;
- or a new lower-bound interface that can move beyond parameterized avoidance.

## Scientific scope

V79 changes reproducibility and CI organization only. It proves no new avoidance theorem, circuit lower bound, or P-versus-NP result.
