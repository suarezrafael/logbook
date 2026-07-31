# Clean-CI promotion record — V63

## Promoted baseline

The V62 cumulative package was validated in a clean GitHub Actions checkout after the historical V60 verifier was repaired.

| Field | Value |
|---|---|
| Repository | `suarezrafael/logbook` |
| Pull request | `#1` |
| Corrective commit | `233745d3f6a0613bc1d27fcfe9725ecb4a20d628` |
| Successful workflow run | `30595354956` |
| Workflow | `NC0_k-Avoid verification` |
| Legacy merge commit to `main` | `968ac5d1b1b480484db1f4f22425e680f4204de9` |

## Quick job

```text
executed=22
skipped=4
failures=0
status=success
```

The four skips were:

1. V22 primary — required original `full_certificate_cases.json` is absent;
2. V26 primary — verifier script is not present;
3. V56 index — full tier only;
4. V58 exact — full tier only.

## Full job

```text
executed=24
skipped=2
failures=0
status=success
```

The two skips were:

1. V22 primary — missing original certificate dataset;
2. V26 primary — verifier script is not present.

Additional full-only evidence:

- V56 index verifier passed;
- V58 exact verifier passed after `126607` DFS nodes;
- V60 primary passed `285` checks;
- V62 primary passed `71` checks;
- V62 independent passed `38` checks.

## Earlier failure and repair

Workflow run `30591741077` failed only in `v60/verify.py`. It required the current cumulative state and ledger to keep saying that external contact had not been sent. That condition was historically true for V60 but became false in V62.

The corrective commit changed the verifier so that:

- permanent facts such as inactive P-versus-NP routing and incomplete `n=9` remain checked in current cumulative state;
- historical `not sent` is checked in `v60/EXTERNAL_CONTACT_STATUS.md`;
- the live ledger may evolve to `sent_awaiting_reply`.

This was a verifier-governance defect, not a mathematical counterexample or failed theorem.

## Nonblocking warning

GitHub Actions reports that `actions/checkout@v4` targets the deprecated Node.js 20 runtime and is currently forced onto Node.js 24. The warning did not affect checkout or verification. It is maintenance debt, not a scientific failure.

## Promotion conclusion

The complete historical runner is now clean in GitHub Actions. V22 and V26 remain explicit, justified skips. No skipped row is counted as a pass.
