# Laboratory V63 — clean-CI promotion and reviewer appendices

## Goal

Promote the V62 manuscript package from locally validated draft material to a clean-CI, reviewer-facing and routinely mergeable research record.

## Outputs

- `CI_PROMOTION_RECORD.md` — exact quick/full CI evidence and V60 repair history.
- `REVIEWER_PACKET.md` — concise external-review entry point.
- `APPENDIX_A_AFFINE_FIBERS.md` — V56 assumptions, algorithm and certificates.
- `APPENDIX_B_BIJUNCTIVE_BLOCKS.md` — V57 clauses and explicit witnesses.
- `APPENDIX_C_ORIENTATION_DEPTH.md` — V58 parameter and algorithm.
- `EXTERNAL_RESPONSE_CHECK.md` — dated no-reply check without inference.
- `PROMOTION_POLICY.md` — one lab, one PR, CI, squash merge to main.
- `CHANGELOG_FROM_V62.md` — exact editorial and governance delta.
- `RESULTS.json` — machine-readable laboratory result.
- `verify.py`, `verify_independent.py` — primary and independent checks.
- `V64_CORE_CONTEXT.md` — next-session contract.

## Scientific result

V63 does not add a stronger theorem. It strengthens reviewability and reproducibility:

- V57 block and clause witnesses are explicit;
- V56/V57/V58 assumptions and nonclaims are isolated;
- cumulative quick and full CI are now recorded as passed;
- external silence remains pending rather than interpreted;
- promotion to `main` becomes routine and version-scoped.

## Verification

```bash
python verify.py
python verify_independent.py
```

The cumulative runner includes both V63 verifiers.
