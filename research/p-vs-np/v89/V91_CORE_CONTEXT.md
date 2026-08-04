# V91 core context — trajectory reorientation laboratory

V91 is reserved and must not begin until V90 has either met its existing
material-advance condition or closed the `Eval_H` constructor front under the
V90 stop rule.

V91 is not a laboratory whose success criterion is a new isolated theorem. It
is a reorientation laboratory whose success criterion is to place every active
front inside an explicit, source-checked implication chain to a recognized open
problem, or to close that front.

## 1. Mandatory trajectory gate

Before code, a search, or a finite census is permitted, every proposed result
must answer two questions in writing.

### 1.1 Implication question

State all of the following:

1. the exact proposed theorem;
2. the recognized open problem or frontier statement it would advance;
3. the complete implication chain, with every external lemma named and cited;
4. all parameter losses through the chain;
5. the first unproved arrow;
6. the quantitative threshold that must be crossed;
7. a falsifier and a stop rule.

The admissible classifications are:

- `infrastructure`: improves verification, representation, or reproducibility;
- `barrier`: proves that a family of strategies cannot reach a target;
- `bridge`: proves a reduction or parameter-preserving transfer to a recognized
  frontier;
- `frontier progress`: crosses a quantitative threshold in an already verified
  implication chain.

Infrastructure and barriers are legitimate outputs, but they are not counted as
movement toward a lower bound unless they change a bridge or frontier
parameter.

### 1.2 Barrier question

Every proposed theorem must include a three-part barrier audit.

#### Relativization

Does the argument continue to work relative to every oracle? A fully
relativizing argument cannot by itself resolve a separation for which opposite
oracle worlds are known. This is a diagnostic, not a blanket rejection rule:
restricted lower bounds and useful structural results may relativize.

#### Natural proofs

Define the candidate property on the truth-table universe relevant to the
claimed circuit lower bound, and audit all three Razborov--Rudich conditions:

1. `constructivity` in the required truth-table complexity measure;
2. `largeness` under the uniform distribution on truth tables;
3. `usefulness` against the precise circuit class and size bound.

No certificate is called a natural property merely because it is efficiently
checkable on a succinct circuit description or frequently observed in a random
support model. All three conditions must be proved in the correct universe.
Under the standard pseudorandom-function hardness assumptions, a constructive,
large, useful property cannot establish the corresponding strong general
circuit lower bound.

#### Algebrization

Does the argument survive oracle access together with a low-degree extension of
the oracle? If so, record the relevant algebrization limitation. As with
relativization, this is a scope warning rather than an automatic veto on every
restricted result.

A proposal failing to specify the property universe, target class, oracle
model, or low-degree extension receives status `barrier audit incomplete` and
cannot open an implementation branch.

## 2. Closure of the certificate-accumulation route

V85--V89 accumulated Hall, syndrome, width, coloring, and collision
certificates. The current record does not prove that these predicates are
natural properties in the formal Razborov--Rudich sense:

- they are predicates on structured support or circuit descriptions, not yet
  properties on the full truth-table universe;
- constructivity in the required representation has not been formalized;
- largeness of a useful property has not been proved;
- usefulness against a strong general circuit class has not been established.

Therefore V91 must not claim that Razborov--Rudich literally explains every
negative experiment.

The route is nevertheless closed for operational reasons already proved inside
the laboratory:

1. V86 constructs a simple rank-three family defeating the local Hall and
   constant-syndrome mechanisms simultaneously;
2. V87 proves that the same random support model has linear support
   branchwidth, closing width optimization against that resistant family;
3. V88--V89 move to support-only target lists and constant-row addressing, but
   the surviving goals remain far below the constructive
   `O(n^(1/3))` threshold and do not currently cross an external lower-bound
   bridge;
4. V90 already contains a fixed stop rule for the remaining `Eval_H` budget.

After V90, no new polynomially checkable certificate family may be opened
unless its proposal supplies one of the following escape clauses:

- a formally non-large useful property;
- a nonconstructive or higher-complexity recognition mechanism with a precise
  role in a lower-bound proof;
- a reduction to a recognized complete problem with preserved parameters;
- a direct contradiction to a named barrier hypothesis;
- a quantitatively stronger consequence than the closed certificate route.

The detailed classification is maintained in
`NATURALNESS_AND_BARRIER_AUDIT.md`.

## 3. Primary front — algorithms to circuit lower bounds

The primary V91 front is the Williams algorithm-to-lower-bound program.

### 3.1 Frozen theorem schema

V91 must select one primary-source theorem and copy its exact quantifiers before
algorithm design begins. The default schema to audit is:

```text
For every constant k, if SAT for n-input, n^k-size circuits from a suitable
class C can be solved within the theorem's required 2^n / n^k-type bound,
then NEXP does not have polynomial-size C-circuits.
```

For general Boolean circuits this specializes to a route toward

```text
NEXP not subseteq P/poly.
```

The slogan `2^n / n^{omega(1)}` is admissible only after proving that the same
uniform algorithm covers every required polynomial circuit size, that input
reading and reductions fit inside the saving, and that the closure hypotheses
on `C` are satisfied.

For the counting route, V91 must separately audit the stronger `#SAT`
transference theorems, including the schema in which `#SAT` for `n^k`-size
`C`-circuits in `2^n/n^k` time for every `k` yields lower bounds against
sparse symmetric functions of `C`.

### 3.2 What the existing engine actually provides

The inherited engine is not yet a Circuit-SAT theorem.

- V74 gives weighted residual dynamic programming.
- V75 compiles exact output-preimage counts into a monotone arithmetic DAG.
- V77 discovers a support-connectivity branch decomposition and gives an FPT
  runtime of the form

```text
2^{O(k^2)} poly(n,m)
```

up to the recorded affine-state and decomposition factors.
- V85 lifts the same arithmetic DAG to truncated distance polynomials.

This can already count assignments producing a prescribed output for local
multi-output circuits of bounded support branchwidth. It does not yet imply a
nontrivial worst-case `#SAT` algorithm for a standard circuit class.

The first required bridge is therefore:

```text
standard C-SAT or #C-SAT
        -> exact V74/V75 counting instance
        -> runtime T(n,s,k)
        -> theorem-qualified saving below 2^n.
```

Every arrow must preserve circuit size, number of variables, gate type, and the
structural parameter.

### 3.3 Candidate-class audit

V91 must rank candidate classes by implication value, compatibility, and
novelty risk.

#### A. Local circuits or CSPs of bounded support branchwidth

Compatibility is high. The existing dynamic program is closest to an exact
`#SAT` algorithm here. The likely novelty is low because treewidth and
branchwidth dynamic programming are mature. This class is the calibration
case, not automatically a publication target.

#### B. Sparse circuits

Plain sparsity is insufficient: sparse expander-like incidence structures can
have linear width. This target is allowed only with a new separator theorem or
another parameter reduction that converts sparsity into a theorem-qualified
saving.

#### C. Constant depth with bounded fan-in

Depth and fan-in alone do not imply small support branchwidth. This class is
allowed only if a restriction, decomposition, or algebraic reduction provably
shrinks the hard core while preserving satisfiability or exact count.

#### D. Bounded-width branching programs

The word `width` refers to a different model and cannot be identified with V77
support branchwidth. This is a candidate only after an explicit translation and
a literature comparison against existing branching-program SAT algorithms.

#### E. A sparse symmetric function over a compatible base class

This is the most direct use of an exact counting engine if the base class
satisfies the hypotheses of a `#SAT`-to-lower-bound theorem. It receives the
highest priority after the calibration case.

### 3.4 Quantitative worksheet

For every candidate class, V91 must fill in:

```text
n       = number of Boolean variables
s       = encoded circuit size
k       = structural parameter
T       = complete runtime including decomposition discovery and bit complexity
saving  = 2^n / T
closure = theorem-specific closure properties of C
result  = exact lower bound implied if the saving threshold is crossed
```

A parameterized algorithm is not counted as progress unless a worst-case
structural theorem for the whole target class makes `saving` satisfy the frozen
transference theorem.

### 3.5 Primary-front success conditions

V91 succeeds on this front if it produces at least one of:

1. a source-verified reduction from `C-SAT` or `#C-SAT` to the existing engine
   with all parameters explicit;
2. a theorem-qualified nontrivial SAT or `#SAT` runtime for a recognized class;
3. a rigorous no-go proving that support-width methods cannot reach the needed
   savings for the candidate classes;
4. a precise missing lemma whose proof would cross a named transference
   threshold.

A finite speedup on selected instances, a new bounded-width implementation, or
an unquantified claim of beating brute force is insufficient.

## 4. Secondary front — reduction algebra in meta-complexity

The secondary front replaces family-specific combinatorics by reductions,
completeness, and parameter ledgers.

### 4.1 Starting objects

The inventory must include:

- circuit range avoidance and its explicit-construction consequences;
- `NC0_3-Avoid` rigidity reductions at additive stretch;
- MCSP and gap variants;
- time-bounded Kolmogorov complexity, including `K^t`, `Kt`, and their promise
  or average-case variants;
- worst-case-to-average-case reductions;
- one-way-function characterizations;
- proof-complexity generators and dual weak pigeonhole principles.

These notions are not interchangeable. Each reduction must state the exact
variant, oracle use, promise gap, distribution, error model, stretch, and
uniformity.

### 4.2 V85 remote-point translation target

V85 constructs, for low support branchwidth, a point at distance

```text
Omega((m-n)/log m)
```

from the range. V91 must test whether this yields any new statement only through
an exact external reduction. The required ledger is:

```text
remote-point instance
  -> target meta-complexity object
  -> complexity or hardness guarantee
  -> parameter loss
  -> comparison with the strongest known theorem.
```

A string outside or far from a circuit range is not automatically a truth table
of high circuit, MCSP, `K^t`, or `Kt` complexity. That conclusion requires a
proved reduction.

### 4.3 Secondary-front success conditions

This front succeeds if it produces one of:

1. a new parameter-preserving reduction;
2. a strict strengthening or simplification of a known reduction;
3. a proof that the V85 remote-point guarantee is quantitatively insufficient
   for a named meta-complexity consequence;
4. a polished equivalence table preventing incorrect transfers among MCSP,
   `K^t`, `Kt`, and range avoidance.

No new combinatorial family search is allowed unless it is demanded by a
specific reduction instance.

## 5. Permanent external-validation front

Internal executable verification cannot certify novelty, literature coverage,
or the absence of a shared conceptual error. V91 establishes a permanent
external-validation queue.

The first two packets are:

1. V81 deficiency conservation and minimum-union theorem;
2. V87 rank-three primal-treewidth to support-branchwidth transfer lemma.

Each packet must contain:

- a self-contained statement and proof;
- exact definitions and parameter conventions;
- a complete prior-art comparison;
- small examples and boundary cases;
- an independent proof audit not generated from the original prose;
- a machine-checkable or executable supplement where useful;
- explicit nonclaims.

Posting to arXiv is public dissemination, not peer review. External validation
means at least one of: a workshop submission, communication with an identified
researcher, an open review request, or a formal referee process. Critical
feedback and a novelty rejection are successful validation outcomes because
they update the laboratory's direction.

## 6. Cuts and freezes

After the V90 stop rule fires:

- close the `Eval_H` constructor front unless it met a listed material-advance
  condition;
- do not open another generic polynomially verifiable certificate search;
- do not continue width optimization against the V87 resistant family;
- do not count finite censuses, verifier growth, or constant-factor state
  compression as trajectory progress;
- do not claim meta-complexity consequences without an exact variant-preserving
  reduction;
- do not claim publication value before a literature and novelty audit.

## 7. Required V91 deliverables

V91 is complete only when all of the following exist:

1. `TRAJECTORY_GATE_TEMPLATE.md`;
2. `NATURALNESS_AND_BARRIER_AUDIT.md`;
3. `ALGORITHM_TO_LOWER_BOUND_AUDIT.md` containing the frozen theorem and the
   runtime worksheet for every candidate class;
4. `METACOMPLEXITY_REDUCTION_LEDGER.md`;
5. `EXTERNAL_VALIDATION_PLAN.md`;
6. one go/no-go decision for the primary front;
7. one go/no-go decision for the V85 remote-point translation;
8. an updated `LAB_STATUS.json` that distinguishes infrastructure, barrier,
   bridge, and frontier progress.

## 8. Literature anchors

Primary anchors to verify and quote precisely in the V91 audit:

- Baker, Gill, and Solovay, *Relativizations of the P =? NP Question*, 1975.
- Razborov and Rudich, *Natural Proofs*, JCSS 1997; ECCC TR94-010.
- Aaronson and Wigderson, *Algebrization: A New Barrier in Complexity Theory*,
  ToCT 2009; ECCC TR08-005.
- Williams, *Improving Exhaustive Search Implies Superpolynomial Lower Bounds*,
  SICOMP 2013.
- Williams, *Nonuniform ACC Circuit Lower Bounds*, CCC 2011 / JACM 2014.
- Vyas and Williams, *Lower Bounds Against Sparse Symmetric Functions of ACC
  Circuits: Expanding the Reach of #SAT Algorithms*, STACS 2020.
- Ren, Santhanam, and Wang, and subsequent work on range avoidance and explicit
  constructions.
- Gajulapalli, Golovnev, Nagargoje, and Saraogi, *Range Avoidance for
  Constant-Depth Circuits: Hardness and Algorithms*, 2023.
- Hirahara's worst-case-to-average-case work for gap meta-complexity problems.
- Liu and Pass, *On One-way Functions and Kolmogorov Complexity*, ECCC
  TR20-052, together with later variant-specific refinements.

## 9. Nonclaims

V91 does not assert that the V85--V89 certificates formally satisfy the natural
proofs definition. It does not assert that every relativizing or algebrizing
result is useless. It does not assert that the V74--V77 engine already gives a
Williams-qualified SAT algorithm. It does not assert novelty for the V81 or V87
notes. It does not make P versus NP measurably closer.

Its purpose is narrower and enforceable: every future result must either live
inside a verified implication chain recognized by the field, document a real
barrier to such a chain, or be classified honestly as infrastructure.
