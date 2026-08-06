# V91 barrier audit — relativization, erratum, and algebrization

## 1. Relativization is part of the achievement and part of the limit

The CHR and Li lower bounds are explicitly relativizing. That is important: their win-win method genuinely passes an oracle test that blocks many informal diagonalization arguments.

It also means V91 must not describe the inherited width dynamic program as automatically entering the same chain. A relativizing theorem still has exact quantifiers over all oracle-relative circuits and an exact algorithmic output model. The width promise is not discharged by relativization.

## 2. Mandatory Vyas–Williams erratum gate

The conference version contained an incorrect Theorem 1.10. Jiatu Li identified the problem, and the July 2024 ECCC revision TR24-113 appends an erratum proving the negation of that statement.

Repository rule from V91 onward:

```text
No implication may cite “Vyas–Williams Theorem 1.10” as a valid barrier.
Every Vyas–Williams transfer must name the TR24-113 theorem number,
revision, quantifiers, depth, uniformity, size regime, and list regime.
```

The verifier checks that this rule appears in both the calibration and implication declarations.

## 3. Chen–Hu–Ren algebrization checkpoint

Chen–Hu–Ren, ITCS 2026, develops algebrization barriers for circuit lower bounds through the communication complexity of Missing-String and its XOR variant. Their oracle constructions preserve access to suitable multilinear extensions while allowing unexpectedly small oracle circuits for exponential-time classes in the stated settings.

The correct consequence for this laboratory is limited but decisive:

- a new Missing-String communication lower bound is not, by itself, authorized as a lower-bound route;
- V91 must identify which step is nonalgebrizing or why the selected theorem lies outside the barrier's hypotheses;
- absence of such a step is a research-budget stop, not a theorem that every possible route fails.

## 4. Audit of the inherited engine

The inherited branchwidth engine uses exact combinatorial counting, decomposition, and dynamic programming. V91 has not identified a nonalgebrizing operation in it. More importantly, the engine already fails before this barrier becomes the only issue: it is not total on the theorem's input class.

Thus the ordered failure stack is:

```text
(1) no all-instance algorithm
(2) no exact single-valued/uniform transfer model
(3) no filled size and runtime parameters
(4) no identified nonalgebrizing ingredient
```

A future version should attack the first unmet condition rather than treating the deepest barrier as the immediate technical bug.

## 5. Source boundary

Primary source: Chen, Hu, Ren, *Algebrization Barriers for Circuit Lower Bounds via Missing-String*, ITCS 2026 / arXiv:2511.14038.

V91 imports the published barrier statement only. It does not reproduce the oracle construction or claim that the barrier applies to proof techniques not covered by the paper.
