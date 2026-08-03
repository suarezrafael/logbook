# V88 validation record

## Local execution before publication

The initial candidate was executed in a clean temporary directory with Python
3 and bytecode side effects disabled by the repository runner policy.

```text
python3 verify.py
python3 verify_independent.py
```

Observed results:

```text
V88 verification passed: 7,264 exact target instances, collision/direct
equivalence, universal pair constructor, and three-row coloring reduction.

V88 independent verification passed: direct observed-table extension matches
the pattern CSP and the three-color reduction on 7,264 instances.
```

Measured local elapsed time was approximately `1.60s` for the primary path and
`1.11s` for the independent path.

## Pending repository gates

Because V88 is opened as a draft candidate, GitHub Actions remains authoritative
for the integrated quick gate and any conditional documentation checks. Before
promotion, the branch must also pass the required compatibility gate and any
full replay triggered by CI-sensitive changes.

No promotion is implied by the local result.
