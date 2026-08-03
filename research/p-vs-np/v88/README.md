# Laboratory V88 — repeated-table `Eval_H` collision geometry

V88 attacks the constructive support-only list problem isolated by V85 and
preserved by V87. Its organizing principle is to exploit the repeated local
truth-table coordinates of `Eval_H`, rather than treating the map as an
arbitrary locality-eleven circuit.

## 1. Collision normal form

A `k`-row target list is coverable exactly when one can assign each input
variable a normalized pattern in `{0,1}^{k-1}` such that every pair of target
rows that differs at output `i` is separated by at least one variable of the
support `S_i`.

This gives an exact local CSP with alphabet `2^(k-1)` and arity at most three.
The only obstruction created by repeated truth-table coordinates is a collision
of equal local addresses carrying incompatible target bits.

## 2. Two and three rows

- Every two-row target list is coverable by an explicit union-of-supports
  witness.
- Three-row coverability is exactly a labeled three-color hypergraph problem.
  A nonconstant target column labels its support by its unique equal row pair;
  a valid coloring may make that support monochromatic only in the labeled
  color.
- A bad-cylinder intersection argument proves that every three-row target list
  with at most fourteen active simple ternary outputs is coverable. Thus the
  first possible three-row obstruction needs at least fifteen active outputs.
- At the target stretch `m=n+ceil(n^(2/3))`, this rules out three-row
  obstructions for `5 <= n <= 9`.

## 3. Property B and the constructor lower bound

If the support hypergraph has Property B, any proper two-coloring can be
embedded into the three active row-pair colors. Every support is then
nonmonochromatic, independently of its target label. Therefore every target
matrix with at most three rows is coverable.

Achlioptas and Moore prove that a random 3-uniform hypergraph at any fixed edge
density below

```text
(7/2) ln 2 - 1 = 1.426015...
```

is two-colorable with high probability. The V87 model has density

```text
(n+ceil(n^(2/3)))/n -> 1.
```

Coupling it to the denser fixed-ratio model at `5n/4` shows that the V87 random
support family has Property B with high probability.

Intersecting this event with the V86/V87 Hall, simplicity, syndrome, and
linear-width events gives one target-stretch family that simultaneously has:

1. linear-scale local Hall expansion;
2. no nonzero constant syndrome under `NOR3`;
3. support branchwidth `Omega(n)`;
4. Property B.

Hence every list of at most three targets remains coverable on that resistant
family. This proves the precise constructor-model lower bound

```text
universal support-only Eval_H list size >= 4.
```

This satisfies the V88 stop condition requesting a rigorous lower bound in a
specified constructor model. It remains far below the existential
`O(n^(1/3))` counting upper bound.

## 4. Executable evidence

The committed independent audits include:

- `7,264` exact collision-normal-form instances;
- `1,710` labeled pairs of distinct ternary supports;
- all `2,187` labelings of the Fano support control;
- five exact first/second-moment contradiction scales;
- the three V80 controls, with `4`, `20`, and `30` proper two-colorings;
- eight deterministic V87 samples, with `42`, `10`, `36`, `56`, `36`, `60`,
  `70`, and `128` proper two-colorings.

The larger coloring censuses use exact integer bitsets. The primary and
independent verifiers do not import one another's theorem kernels.

## Files

- `COLLISION_NORMAL_FORM.md` — exact repeated-table normal form;
- `THREE_ROW_BARRIER.md` — fourteen-output theorem;
- `PROPERTY_B_BOUNDARY.md` — asymptotic Property-B composition and constructor
  lower bound;
- `collision_normal_form.py` — collision CSP and exact small census;
- `three_row_barrier.py` — bad-cylinder formulas and Fano audit;
- `property_b_boundary.py` — density calibration and finite Property-B census;
- `RESULTS.json` and `PROPERTY_B_RESULTS.json` — committed evidence;
- `verify.py` and `verify_independent.py` — independent verification paths;
- `LITERATURE_BOUNDARY.md` — primary-source and novelty boundary;
- `VALIDATION.md` — execution record;
- `V89_CORE_CONTEXT.md` — reserved continuation priorities.

## Current frontier

The direct continuation is no longer a three-row search on the V87 family.
The next focused targets are:

1. construct an explicit four-row missing output;
2. derive a four-row analogue of the collision-label geometry;
3. seek deterministic non-Property-B support families preserving the Hall,
   syndrome, and width barriers;
4. raise the lower bound for restricted linear, cyclic, or low-degree
   constructors.

## Candidate status

V88 remains a candidate until integrated quick and compatibility verification
complete. Repository promotion means internal verification only; it would not
establish external novelty or peer review.

## Nonclaims

V88 does not construct the `O(n^(1/3))` list, produce a four-row obstruction,
solve unrestricted `NC0_3-Avoid`, derandomize the V87 family, construct rigid
matrices, prove a new unrestricted circuit lower bound, confirm novelty, pass
peer review, or resolve `P` versus `NP`.
