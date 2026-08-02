# Laboratory V81 — deficiency conservation and Minimum p-Union census

V81 follows the high-width audit of V80 without claiming a route to P versus NP.
Its first contribution is an exact conservation theorem that links support
connectivity width to Hall deficiency on every cut. Its second contribution is
a complexity audit of the proposed `MIN-NEIGHBORHOOD-HALL` subproblem.

## Conservation theorem

For gate set `M`, active variables `X`, stretch `sigma=|M|-|X|`, neighborhood
`N(S)`, deficiency `delta(S)=|S|-|N(S)|`, and support connectivity
`lambda_C(S)`, V81 proves

```text
delta(S) + delta(M\S) = sigma - lambda_C(S).
```

Every subcubic leaf decomposition has an edge with both sides between one third
and two thirds of the gates. Therefore a supplied width-`w` decomposition
constructively exposes a balanced side with

```text
deficiency >= ceil((sigma-w)/2).
```

This strengthens the interpretation of the V77 low-width regime: a narrow
decomposition is not only algorithmic input for avoidance; when `w<sigma`, it
also contains a quantitatively Hall-deficient balanced cut.

## Minimum-neighborhood Hall boundary

Let

```text
U(p) = min_{|S|=p} |N(S)|.
```

Then the minimum possible neighborhood of a Hall-deficient set is exactly

```text
min { U(p) : U(p) < p }.
```

Thus the problem is a diagonal-crossing version of Minimum `p`-Union / small-set
bipartite vertex expansion.

For fixed rational `lambda`, minimizing

```text
|N(S)| - lambda |S|
```

is submodular minimization and, for coverage functions, a minimum-closure cut.
However, this Lagrangian scan exposes only supported points of the curve
`(p,U(p))`. On all three V80 obstruction candidates, the minimum-neighborhood
Hall witness is unsupported; the only Lagrangian-supported deficient point is
the full gate set. Therefore the proposed parametric scan does not by itself
solve `MIN-NEIGHBORHOOD-HALL`.

## Exact census

The primary and independent verifiers recompute:

- the conservation identity on every subset of the three V80 families;
- exact branchwidth;
- the complete Minimum `p`-Union curve;
- all Lagrangian-supported cardinalities;
- balanced low-width cut/deficiency profiles;
- two rank-one controls, including a cut where the factor `1/2` is tight from
  conservation alone.

## Literature audit

Explicit constant-degree lossless expanders are known, but the constructions
located in the V81 search require sufficiently large degree depending on the
loss parameters, polynomial degree in the highly unbalanced setting, or only
spectral degree-three expansion. None directly supplies the exact left-degree
three, near-balanced, lossless family required as a ready-made V81 obstruction.

## Files

- `DEFICIENCY_CONSERVATION_AND_MIN_UNION.md` — proofs and complexity boundary;
- `LOSSLESS_EXPANDER_AUDIT.md` — directed literature audit;
- `V81_DEFICIENCY_CONSERVATION_THEOREM.tex` — standalone formal module;
- `deficiency_conservation.py` — exact census generator;
- `RESULTS.json` — immutable finite evidence;
- `verify.py` and `verify_independent.py` — read-only audits;
- `V82_CORE_CONTEXT.md` — next mathematical target.

## Nonclaims

V81 does not prove a polynomial-time algorithm or NP-hardness for
`MIN-NEIGHBORHOOD-HALL`, does not produce an explicit degree-three lossless
expander family at the target parameters, does not construct the deterministic
`FP^NP` candidate list required by V65, does not prove an all-orders lower
bound, does not formalize V56 in `APC^1`, and does not resolve P versus NP.
