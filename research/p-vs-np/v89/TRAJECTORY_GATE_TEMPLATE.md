# Laboratory trajectory gate template

Copy this file into every post-V90 laboratory proposal and complete it before
writing code.

## A. Exact result

```text
Proposed theorem:
Input model:
Output/conclusion:
Parameters:
Uniformity:
Randomness/error model:
```

## B. Recognized frontier

```text
Named open problem or frontier:
Why the field recognizes it:
Strongest known result:
Primary sources:
```

## C. Explicit implication chain

Write every arrow separately.

```text
proposed theorem
  -> [external or internal lemma 1]
  -> [external or internal lemma 2]
  -> recognized consequence
```

For each arrow record:

| Arrow | Proven? | Source | Parameter input | Parameter output | Missing assumption |
|---|---:|---|---|---|---|
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |

The first unproved arrow is the actual research target.

## D. Quantitative threshold

```text
Current bound:
Required bound:
Gap:
Does a constant-factor improvement matter? yes/no, with proof
Does a finite-scale improvement matter? yes/no, with proof
```

## E. Barrier audit

### Relativization

```text
Does the proof relativize? yes/no/unknown
Oracle model:
Known opposite oracle worlds relevant to the target:
Consequence for scope:
```

### Natural proofs

```text
Property universe:
Representation:
Constructivity statement:
Largeness statement:
Usefulness statement:
Circuit class and size:
Cryptographic assumption:
Status: formal/candidate/warning/not applicable/unknown
```

### Algebrization

```text
Does the proof algebrize? yes/no/unknown
Low-degree extension model:
Known algebrization barrier relevant to the target:
Consequence for scope:
```

## F. Existing-engine fit

```text
Reusable theorem/code from prior versions:
Required translation:
Runtime after all overheads:
Why the engine is not merely infrastructure here:
```

## G. Falsifier and stop rule

```text
Fastest decisive counterexample or no-go test:
Maximum theory budget:
Maximum implementation budget:
Stop condition:
Fallback front:
```

## H. Output classification

Choose exactly one primary label.

```text
[ ] infrastructure
[ ] barrier
[ ] bridge
[ ] frontier progress
```

Justification:

```text

```

## I. Nonclaims

List every tempting stronger conclusion that the proposed theorem would not
establish.

## J. Approval gate

A proposal may open implementation work only when:

- the implication chain names a recognized target;
- the first unproved arrow is explicit;
- the quantitative threshold is computed;
- the three barrier audits are complete or honestly marked unknown;
- the falsifier and stop rule are finite;
- the output classification is chosen.

An unanswered item returns the proposal to theory design. It does not authorize
a exploratory census by default.
