# V78 legacy mutation inventory

The cumulative verifier passes mathematically, but legacy scripts still regenerate evidence inside the disposable verification sandbox. V78 records this debt without allowing it to modify the protected source checkout.

## Modified tracked artifacts (16)

- `v55/RESULTS.json`
- `v57/INDEPENDENT_RESULTS.json`
- `v57/RESULTS.json`
- `v58/INDEPENDENT_RESULTS.json`
- `v58/RESULTS.json`
- `v59/INDEPENDENT_RESULTS.json`
- `v59/RESULTS.json`
- `v65/RESULTS.json`
- `v66/RESULTS.json`
- `v67/RESULTS.json`
- `v67/WITNESSES.json`
- `v68/RESULTS.json`
- `v69/RESULTS.json`
- `v70/RESULTS.json`
- `v71/RESULTS.json`
- `v72/RESULTS.json`

## Newly generated artifacts (5)

- `v54/VERIFY_RESULTS.json`
- `v55/CLASSIFICATION.json`
- `v56/REPO_INDEPENDENT_RESULTS.json`
- `v56/REPO_VALIDATION_RESULTS.json`
- `v57/CERTIFICATES.json`

## Classification

The mutations include formatting-only JSON rewrites, wall-clock fields, regenerated expanded witnesses, and outputs that are not part of the committed evidence contract. They are not silently ignored: `run_verification_in_sandbox.sh` prints every modified, created, or deleted path after each cumulative run.

## Laboratory boundary

V78 completes the clean-checkout firewall, deterministic LaTeX manifest, ledger-independent runner coverage, immutable V53 retraction validation, and an explicit mutation inventory.

V79 owns the remediation phase:

1. define a canonical immutable-evidence contract;
2. convert each listed verifier from writer to comparator;
3. remove wall-clock values from scientific snapshots;
4. decide whether each newly generated file is committed evidence or disposable diagnostics;
5. reduce the sandbox mutation inventory to zero;
6. reconcile `STATE.md`, `LEDGER.json`, and publication indexes through the promoted version.

No mathematical theorem or P-versus-NP progress claim follows from this infrastructure work.
