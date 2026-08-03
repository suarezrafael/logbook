# P-versus-NP verification policy

This document describes the executable CI contract enforced by
`check_ci_contract.py`.

## Pull requests

Draft pull requests run the focused `quick` gate. LaTeX is installed and all
formal modules are compiled only when a theorem module, the manifest, the
manifest checker, or the verification workflow changes.

A pull request marked ready for review also runs `compatibility`. This mode
executes every ordinary historical verifier, not merely the focused versions.
Its purpose is to detect old status assumptions and cross-version contract
regressions before promotion.

The exact replay tier also runs on a ready pull request when the change touches
the verification workflow, runner, sandbox/clean-tree machinery, CI contract
checker, or one of the exact replay programs. Thus CI changes validate the
expensive path they modify, while ordinary mathematical laboratories avoid
paying that cost on every promotion.

## Main branch

A push to `main` runs `quick`, plus LaTeX only when relevant files changed. It
does not repeat the exact replay already validated before merge. Promotion-only
changes to `LAB_STATUS.json` therefore receive a focused compatibility check
without reinstalling TeX Live or re-running the historical exact searches.

## Scheduled and manual verification

The complete `full` suite, including V56, V58, and V70 exact replay tiers, runs
weekly on Monday at 06:17 UTC. `workflow_dispatch` runs `quick`, `full`, and
LaTeX and is the explicit recovery/audit path.

## Runner modes

- `verify_all.sh`: focused recent regression gate;
- `verify_all.sh --compat`: every ordinary historical verifier, excluding the
  exact replay tier;
- `verify_all.sh --full`: all historical verifiers and exact replays;
- `verify_all.sh --list`: complete registration inventory.

All modes execute in the sandbox and the workflow separately asserts that the
repository checkout remains clean.

## Branch cleanup

`cleanup-merged-research-branches.yml` reacts to a merged same-repository pull
request whose head starts with `agent/`. It deletes that exact branch and is
idempotent if GitHub has already removed it. No version-specific branch list is
maintained.

## Safety boundary

This optimization does not replace historical compatibility with only recent
checks. It separates ordinary historical verifiers from the small exact replay
tier. Any change to the CI machinery itself still triggers the complete suite
before merge.
