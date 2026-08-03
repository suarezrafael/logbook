# V88 validation record

## Initial collision packet

The initial candidate was executed in a clean temporary directory with Python
3 and bytecode side effects disabled by the repository runner policy.

```text
python3 verify.py
python3 verify_independent.py
```

The two paths agreed on all `7,264` collision instances. Initial elapsed times
were approximately `1.60s` for the primary path and `1.11s` for the independent
path.

## Three-row barrier extension

The optimized bitset implementation independently recomputed:

- `1,710` labeled distinct-support intersections;
- every one of the `2,187` Fano labelings;
- the five fourteen-output moment certificates.

The standalone barrier kernel completed locally in approximately `2.95s`; the
independent combined verifier completed in approximately `3.83s` before the
Property-B extension.

## Property-B extension

The Property-B kernel completed locally in approximately `3.05s`. It checked
all three V80 controls and eight deterministic V87 samples and reproduced the
committed proper-coloring counts.

The extended independent verifier was also executed locally after adding the
Property-B checks. It completed in approximately `3.62s` and reported:

```text
V88 independent verification passed: collision geometry, bad-cylinder moments,
Fano labelings, 11 Property-B controls, and the universal three-row constructor
lower bound.
```

The asymptotic density calculation is source-backed rather than established by
finite execution: the verifier checks the exact constant
`(7/2)ln(2)-1`, the strict comparison with `5/4`, and the target-density
coupling arithmetic.

## Repository gates

GitHub Actions is authoritative for the integrated quick gate and conditional
documentation checks. Before promotion, the candidate must pass the ready-PR
compatibility gate and any full replay triggered by CI-sensitive changes.

No external novelty, peer-review status, or promotion is implied by the local
execution record.
