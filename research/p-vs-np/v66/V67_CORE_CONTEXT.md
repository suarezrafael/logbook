# Frozen context for Laboratory V67

## Stable facts

1. V66 reproduces all 243 affine-cell partition systems of the V57 gadget.
2. Every V57 partition system has exactly one consistent complete branch; optimal adaptive pruning uses 8 or 9 leaves.
3. The complete three-variable NPN-expanded domain has 392 gate variants and at most four consistent branches after four gates.
4. The canonical `n=3`, `m=4` census covers 40,920 systems with maximum `L_aff=11` and `G_aff=17`.
5. The `n=4` result is a 50,000-sample deterministic stress test, not a theorem.
6. No asymptotic polynomial branching bound, unrestricted `NC0_3-Avoid` algorithm, lower bound, or P-versus-NP implication is established.
7. Earliest external follow-up date is 2026-08-24.

## Required V67 behavior

1. Search for scalable lower-bound or upper-bound families for affine-cell branching rather than extrapolating finite counts.
2. Test direct sums, overlap chains, parity mixtures and support-expansion constructions separately.
3. Preserve the smallest family that forces growth in consistent branches, `L_aff`, or `G_aff`.
4. Compare tree and DAG complexity; do not treat them as interchangeable.
5. Formalize any proof-complexity simulation before using established lower bounds.
6. Keep the direct P-versus-NP route inactive absent a complete reduction.
7. Merge only after quick and full CI pass.
