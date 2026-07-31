# GitHub Actions runtime maintenance audit

**Audit date:** 2026-07-30  
**Scope:** workflow runtime maintenance only; this is separate from mathematical validation.

## Observation

The V63 GitHub-hosted jobs ran on Actions Runner `2.336.0`. The logs warned that `actions/checkout@v4` targets Node.js 20 and was being forced to Node.js 24. This warning did not cause a scientific verifier failure, but leaving it unresolved would create avoidable workflow maintenance risk.

## Primary-source check

The official `actions/checkout` repository and Marketplace entry identify `v6.0.2` as the current release. The official README states:

- checkout v5 moved to the Node.js 24 runtime and requires runner `2.327.1` or later;
- checkout v6 stores persisted credentials under `$RUNNER_TEMP`;
- authenticated Git commands from Docker container actions require runner `2.329.0` or later.

Sources checked:

- https://github.com/actions/checkout
- https://github.com/actions/checkout/blob/main/README.md
- https://github.com/actions/checkout/blob/main/CHANGELOG.md
- https://github.com/marketplace/actions/checkout

## Compatibility decision

This repository uses GitHub-hosted Ubuntu runners, observed at `2.336.0`, and the verification workflow does not invoke Docker container actions. Therefore the workflow is upgraded from `actions/checkout@v4` to `actions/checkout@v6`.

## Separation from scientific evidence

The action upgrade changes repository checkout plumbing only. Quick and full verification remain the scientific merge gates. A successful action setup does not validate a theorem, and a runtime warning is not a mathematical counterexample.
