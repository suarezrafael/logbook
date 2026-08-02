# Laboratory V80 — high-width Hall/branchwidth dichotomy audit

V80 returns the laboratory to mathematics and audits the missing high-width side of the V77 support-branchwidth program.

The guiding question is not presented as a route to solving P versus NP. The V65 route audit remains authoritative: no direct route is active. The lower-bound-relevant target is the documented `FP^NP` regime for `NC0_3-Avoid` at

```text
m = n + ceil(n^(2/3)).
```

## Main correction

For every circuit with `m>n`, a Hall-deficient output set exists trivially: the full gate set uses at most `n` variables. This proves that an avoided projection exists, but counting alone does **not** construct one deterministically in `FP^NP`.

- If the witness neighborhood has `O(log n)` variables, direct enumeration is polynomial and constructs a missing projection.
- For an arbitrary deficient witness of deficiency `d`, uniform sampling plus an NP range-membership query succeeds with probability at least `1-2^{-d}` per trial. This gives a zero-error expected-polynomial randomized NP-oracle procedure, which is already available globally by taking all outputs.
- The deterministic `FP^NP` bridge therefore requires a derandomization or a polynomial-size canonical candidate list; Hall counting by itself does not close Gate B of V65.

## Structural theorem

For gate set `M`, active variable set `X`, and `N(S)` the variables used by gates in `S`, V80 proves

```text
lambda_C(S) = |N(S)| + |N(M\S)| - |X|.
```

Thus, whenever both sides of a cut are Hall-nondeficient,

```text
lambda_C(S) >= |M| - |X|.
```

Consequently, if every balanced gate set Hall-expands, support branchwidth is at least the stretch. In the target regime, a fully balanced-Hall-expanding obstruction has branchwidth at least `n^(2/3)` and lies far outside the polynomially relevant low-width regime of V77.

## Barrier to the naive Hall arm

A probabilistic construction proves that, for all sufficiently large `n`, rank-at-most-three support families exist at the target stretch with no Hall-deficient gate set of size at most

```text
n / (16 e^2).
```

Therefore high-width analysis cannot rely on a universal logarithmic-size Hall witness. The refined high-width arm must instead produce one of:

1. a small-neighborhood Hall certificate;
2. an affine, sunflower, or overlap structure yielding a polynomial candidate list;
3. an explicit Hall-expanding obstruction for the all-orders lower-bound program.

## Exact finite audit

Three deterministic rank-three examples at the target stretch are checked exactly. Their minimum Hall-deficient set sizes are `7`, `8`, and `9`, while their exact support branchwidths are `5`, `5`, and `6`. These are obstruction candidates and implementation controls, not asymptotic lower bounds.

## Files

- `HIGH_WIDTH_DICHOTOMY_AUDIT.md` — theorem proofs, algorithmic boundary, and refined win-win;
- `V80_HALL_BRANCHWIDTH_DICHOTOMY_THEOREM.tex` — standalone formal module;
- `hall_branchwidth.py` — exact Hall, matching, cut, and branchwidth auditor;
- `RESULTS.json` — immutable exact finite evidence;
- `verify.py` and `verify_independent.py` — primary and independent read-only checks;
- `V81_CORE_CONTEXT.md` — deterministic candidate-list target and bounded-arithmetic second front.

## Literature boundary

The lower-bound motivation is the `NC0_3-Avoid` bridge of Gajulapalli, Golovnev, Nagargoje, and Saraogi, ECCC TR23-021. The broader algorithm/lower-bound interface is documented by Huang, Li, and Zhong, ECCC TR25-049. The cryptographic and proof-complexity warning is documented by Ren, Wang, and Zhong, ECCC TR25-191.

## Nonclaims

V80 does not give a deterministic `FP^NP` algorithm for unrestricted `NC0_3-Avoid`, does not prove that high branchwidth always yields an affine or sunflower certificate, does not establish an all-orders lower bound, does not formalize the argument in `APC^1`, does not claim novelty or peer review, and does not resolve P versus NP.
