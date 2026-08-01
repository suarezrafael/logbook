# V73 CI scope

The laboratory is complete only after the pull-request workflow passes all three jobs on the same final head SHA:

- `quick` — cumulative primary and independent verifiers;
- `full` — cumulative extended verification;
- `latex` — all formal modules including V73.

The pull request remains unmerged while any job is queued, running, cancelled, or failed. Any correction requires a new complete CI cycle on the corrected head SHA. Promotion uses a squash merge to `main` with the validated head SHA as an explicit guard.
