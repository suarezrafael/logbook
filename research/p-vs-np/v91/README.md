# Laboratory V91 — post-Li Range-Avoidance calibration and width-engine no-go

## Classification

V91 is a **reproduction, calibration, barrier, and closure laboratory**. It is not a new circuit-lower-bound result.

The laboratory corrects the V90 handoff in three ways:

1. the natural depth-three Missing-String target was already reached by Li's all-length improvement of the CHR range-avoidance algorithm;
2. the Vyas–Williams source must be the July 2024 ECCC revision with the appended erratum, because the conference Theorem 1.10 is false;
3. the Chen–Hu–Ren ITCS 2026 algebrization barrier must be checked before any further Missing-String communication-complexity investment.

## Reproduction result

`reproduction.py` checks the deterministic Korten/GGM decoding kernel used inside the modern win-win line. It verifies that a leaf vector outside the iterated-generator image decodes, using lexicographically first preimages, to a word outside the original expanding map.

The committed finite audit covers:

```text
all n=1 maps C:{0,1}->{0,1}^2       16 maps
fixed deterministic n=2 sample       64 maps
all proper Missing-String subsets
through string length four        65,808 instances
```

This is deliberately weaker than reproducing the full CHR/Li algorithm. It does not implement the FS2P single-valued win-win, its nondeterministic consistency mechanism, or the lower-bound transfer.

## Calibrated chain

The checked chain is:

```text
CHR'23: range avoidance on infinitely many lengths
  -> relativizing exponential circuit lower bounds

Li'23: single-valued range avoidance on every length
  -> S2E not contained in i.o.-SIZE[2^n/n]
  -> uniform depth-3 AC0 circuits for Missing-String
     of quasipolynomial size in the explicit-list parameter
```

Therefore “obtain depth-three quasipolynomial Missing-String circuits” is not an open V91 target.

See `THEOREM_CALIBRATION.md` for theorem identifiers, parameter conventions, and what remains usable.

## Inherited-engine verdict

The inherited engine constructs remote points in polynomial time only under

```text
support branchwidth k = O(sqrt(log m)).
```

The transfer theorems require an algorithm on every input in a named standard circuit class, together with their exact single-valuedness, uniformity, size, and runtime requirements. The present engine has none of the following:

- an all-instance guarantee;
- a standard unrestricted class covered by the low-width promise;
- a high-width win branch that returns a canonical missing output;
- a proof that its output model is the single-valued model used by Li or the uniform circuit model used by Vyas–Williams;
- a nonalgebrizing ingredient identified against the 2026 barrier.

Consequently no published transfer is triggered.

## Stop-rule decision

The Williams/Missing-String branch is closed **for the inherited width-promised engine**. This is not a closure of Range Avoidance as a research area.

The branch may reopen only with at least one of:

1. a total win-win completion whose high-width branch also outputs a canonical avoided string;
2. a checked transfer target that remains open after Li and whose exact parameters are met;
3. an explicit nonalgebrizing ingredient outside the Chen–Hu–Ren barrier scope.

## Files

- `reproduction.py` — executable finite Korten/GGM and Missing-String audit;
- `REPRODUCTION_RESULTS.json` — immutable reproduction snapshot;
- `THEOREM_CALIBRATION.md` — CHR/Li/Vyas–Williams parameter table;
- `BARRIER_AUDIT.md` — relativization, erratum, and algebrization gates;
- `ENGINE_COMPATIBILITY.md` — requirement-by-requirement verdict;
- `RESULTS.json` — machine-readable scientific classification;
- `IMPLICATION.json` — implication ratio and fired stop rule;
- `verify.py` and `verify_independent.py` — primary and independent checks;
- `V92_CORE_CONTEXT.md` — narrowly scoped all-instance completion gate.

## Nonclaims

V91 does not reproduce the complete CHR or Li proof, prove a new lower bound, refute every Missing-String approach, establish novelty, supply peer review, or resolve P versus NP.
