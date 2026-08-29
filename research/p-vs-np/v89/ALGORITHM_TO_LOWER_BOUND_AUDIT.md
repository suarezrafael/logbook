# V91 algorithm-to-lower-bound audit

This is the primary-front worksheet. It freezes the theorem before adapting the
engine.

## 1. Primary theorem candidates

### Candidate A — SAT algorithms imply lower bounds

Source family: Ryan Williams, *Improving Exhaustive Search Implies
Superpolynomial Lower Bounds* and the subsequent algorithms-versus-circuits
framework.

Default theorem schema to verify from the primary source:

```text
For every constant k, a sufficiently uniform SAT algorithm for n-input,
n^k-size circuits from a suitable class C, running within the required
2^n/n^k-type time bound, implies that NEXP has no polynomial-size C-circuits.
```

For unrestricted Boolean circuits, the target consequence is

```text
NEXP not subseteq P/poly.
```

This file intentionally does not replace the theorem's exact hypotheses with
`2^n/n^{omega(1)}`. The final audit must copy:

- the quantifiers over `k`;
- the exact input circuit size;
- deterministic versus randomized requirements;
- the closure properties required of `C`;
- the runtime including input-reading cost;
- the precise lower-bound class and uniformity conclusion.

Primary anchor:

- https://doi.org/10.1137/10080703X
- https://people.csail.mit.edu/rrw/improved-algs-lbs2.pdf

### Candidate B — #SAT extends the lower-bound class

Source family: Vyas and Williams, *Lower Bounds Against Sparse Symmetric
Functions of ACC Circuits: Expanding the Reach of #SAT Algorithms*.

The abstract-level schema is:

```text
For all k, #SAT for n^k-size C-circuits in 2^n/n^k time
  -> NEXP has no polynomial-size f o C circuits
```

for the paper's typical classes `C` and sparse symmetric top functions `f`.

The final audit must copy the exact definition of a typical class, closure
conditions, and reduction overhead.

Primary anchors:

- https://arxiv.org/abs/2001.07788
- https://doi.org/10.4230/LIPIcs.STACS.2020.59

## 2. Existing engine normalization

### V75 exact counting object

V75 represents

```text
P_C(u_1,v_1,...,u_m,v_m)
  = sum_{x in {0,1}^n} product_i z_{i,C_i(x)}.
```

Selecting one literal from every pair extracts the number of assignments with a
specified output vector. Thus it is already an exact counting engine for a
multi-output local circuit under a supplied structural decomposition.

### V77 complete runtime

For support-connectivity branchwidth `b`, the current high-level runtime is

```text
T(n,m,b)
  = 2^{O(b^2)} gamma m^6 log m
    + O(m log m A(2b)^2 poly(n,m)),
```

with `gamma=O(m)` for explicit rank-three supports and

```text
A(q) <= (q+1) 2^{floor(q^2/4)+q}.
```

Therefore the total state dependence is `2^{O(b^2)}`. This gives:

- polynomial time for `b=O(sqrt(log m))`;
- subexponential dependence on the variable count if a whole target class has
  `b=o(sqrt(n))`, after exact constants and polynomial factors are accounted
  for;
- no worst-case saving for classes containing linear-branchwidth instances,
  including the V87 resistant support family.

### Missing conversion

The engine counts assignments to a prescribed vector of local outputs. To call
this `#C-SAT`, V91 must define a standard class `C` and prove one of:

```text
one-output C-circuit
  -> rank-three multi-output local circuit plus a prescribed output vector,
```

or

```text
C-CSP / conjunction of local gates
  -> coefficient or evaluation of P_C.
```

The translation must preserve the number of variables closely enough that the
runtime saving remains theorem-qualified.

## 3. Candidate-class matrix

| Candidate | Engine compatibility | Required new theorem | Williams-fit risk | Novelty risk | Initial status |
|---|---:|---|---:|---:|---|
| rank-three CSP with supplied branch decomposition | very high | formal #SAT encoding | high: supplied-structure promise may fail closure | very high | calibration only |
| rank-three CSP parameterized by support branchwidth | very high | exact runtime with bit complexity | high: parameter-bounded class may not be a typical circuit class | high | calibration only |
| sparse circuits | low to medium | sparsity-to-small-separator theorem | high: sparse expanders have linear width | medium | no-go unless new separator |
| bounded-fan-in constant-depth circuits | medium | restriction/decomposition reducing the hard core | medium to high | high | open audit |
| bounded-width branching programs | low until translated | model-preserving width translation | high: different width notion | high | terminology quarantine |
| sparse symmetric function over a compatible local base class | high if #SAT base class is established | verify Vyas--Williams hypotheses | medium | medium | first serious target |

## 4. Quantitative worksheet

Complete one table per candidate class.

| Field | Value |
|---|---|
| class `C` | |
| number of variables before reduction | |
| number of variables after reduction | |
| circuit size before reduction | |
| circuit size after reduction | |
| support branchwidth guarantee for every instance | |
| decomposition-discovery time | |
| arithmetic-DAG construction time | |
| exact-count evaluation time | |
| bit length of intermediate counts | |
| complete runtime `T(n)` | |
| saving `2^n/T(n)` | |
| theorem-required saving | |
| closure properties | |
| closure proof | |
| implied lower bound | |

The row is `go` only if every field is filled from a proof or a cited theorem.

## 5. Immediate no-go tests

### 5.1 Sparsity alone

A linear number of local constraints can form an expander-like incidence graph
with linear treewidth or branchwidth. Therefore gate sparsity alone cannot feed
the V77 runtime into a nontrivial worst-case bound.

### 5.2 Width optimization against V87

V87 supplies linear support branchwidth in the resistant model. Improving
`2^{O(b^2)}` constants or extending the polynomial regime from
`sqrt(log n)` to `log n` does not solve that family and does not create a
Williams-qualified algorithm for a class containing it.

### 5.3 A promise class without closure

A class defined only by `support branchwidth <= g(n)` may not be closed under
negation, conjunction, composition, projections, or the transformations used by
the transference theorem. A fast algorithm for such a promise class does not
inherit the lower-bound consequence automatically.

### 5.4 Input-reading floor

The target `2^n/n^k` bound cannot be claimed for circuits whose encoding length
already exceeds the proposed runtime. Circuit size and representation costs
must be included.

## 6. First implementation-free tasks

Before writing a new solver:

1. transcribe the exact Williams theorem and all quantifiers;
2. transcribe the exact Vyas--Williams `#SAT` theorem;
3. define the closest standard `#SAT` problem already computed by V75;
4. compare that problem with known CSP/treewidth counting algorithms;
5. test closure of the parameter-bounded class;
6. derive the exact exponent from `A(2b)` rather than use `O(b^2)`;
7. decide whether any candidate crosses the theorem threshold.

## 7. Go/no-go rule

### Go

Open an algorithm laboratory only if there is a standard class `C` for which:

- the existing engine or one explicit extension solves `C-SAT` or `#C-SAT`;
- every instance has a proved structural guarantee;
- the complete runtime crosses the frozen theorem threshold;
- the class satisfies the required closure hypotheses;
- the result is not already subsumed by a stronger known algorithm.

### No-go

Close the front for the current engine if all candidate classes fail because of
linear width, closure, representation overhead, or prior art. Preserve the
negative audit as a barrier result and move the main budget to the
meta-complexity reduction ledger.

## 8. Nonclaims

The existing FPT algorithm is not yet a Williams-qualified SAT algorithm. A
subexponential algorithm on a narrow promise class does not automatically imply
a circuit lower bound. The words `sparse`, `bounded depth`, and `bounded width`
do not establish structural compatibility by themselves.
