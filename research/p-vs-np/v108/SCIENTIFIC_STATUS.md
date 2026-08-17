# V108 scientific status

## Established inside the candidate package

- Exact fixed-target 2-CNF representation for signed essential ternary MUX gates.
- Directed-cycle literal-forcing construction using one selected branch per output.
- Polynomial-time SCC-separated two-cycle bridge detector and missing-output constructor.
- XP hierarchy `O(m^k poly(N))` parameterized by the number of ignored outputs needed to expose the certificate.
- Infinite exact-stretch family with `kappa_SCC=0`.
- Hall-minimality of that family.
- For cycle length divisible by three, exact V102 backdoor `beta=2n/3` on the same family.

## Still open

- Polynomial-time avoidance for every essential MUX/bijunctive `0x1b` circuit.
- A polynomial selector for the residual one-cyclic-SCC regime.
- FPT dependence on `kappa_SCC`.
- Unrestricted `NC0_3-Avoid`.
- Any new general circuit lower bound.
- P versus NP.

## Validation status

The package has primary and independent verifiers, but no external specialist review or novelty confirmation.  Search of the current primary range-avoidance literature did not locate a MUX/bijunctive exact-stretch theorem; search absence is not evidence of novelty.
