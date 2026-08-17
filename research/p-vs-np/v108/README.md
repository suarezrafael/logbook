# Laboratory V108 — MUX SCC-cycle bridge

V108 attacks the remaining essential ternary MUX/bijunctive `0x1b` orbit left open after V107.

The key observation is that fixing a signed MUX output produces two exact 2-CNF clauses.  Each branch therefore acts as a directed implication from a selector literal to a data literal.  A directed cycle can be targeted to force one selector literal.  If an omitted MUX gate carries that forced literal into a different cyclic SCC, a second cycle can be targeted to force the opposite literal on the arrival variable, giving an explicit contradiction.

## Main candidate result

An **SCC-separated bridge certificate** is detectable and usable in polynomial time.  More generally, if at most `k` outputs need to be ignored before such a certificate appears, enumeration gives `O(m^k poly(N))` time.  The parameter is called `kappa_SCC`.

## Strict family

For two disjoint `k`-cycles of canonical MUX gates plus one bridge,

```text
n=2k,
m=n+1,
kappa_SCC=0.
```

The support family is Hall-minimal.  When `3|k`, its V102 strong-affine backdoor is exactly

```text
beta=4k/3=2n/3.
```

Thus the family separates the new SCC certificate from the linear-backdoor regime.

## Verification

`verify.py` checks certificate soundness against complete original ranges on the strict family and signed switchings, audits Hall minimality, computes exact small-instance beta, and runs fresh random soundness checks.

`verify_independent.py` does not import the V108 implementation.  It reconstructs the strict family and an explicit missing target, proves unsatisfiability with an independent 2-SAT SCC solver through large `k`, brute-forces the original image for small instances, independently checks deletion-perfect support matchings, and computes exact beta by cycle-state enumeration.

## Nonclaims

V108 does not solve every MUX/bijunctive circuit.  The residual case in which the useful cycles remain in one cyclic SCC is open.  It does not solve unrestricted `NC0_3-Avoid` or P versus NP, and no novelty or priority claim is made without external validation.
