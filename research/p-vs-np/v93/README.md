# Laboratory V93 — global affine-syndrome certificates are not comparison oracles

## Classification

V93 is a **formal route-elimination laboratory**. It executes the mandatory affine-comparison falsification gate reserved by V92 and promotes the no-go track because the collision lifts to an explicit theorem for a precisely defined, polynomial-time constructible certificate model.

## Frozen target row

| Class | Stretch | Required complexity | Named baseline/consequence |
|---|---:|---|---|
| high-support-branchwidth `NC0_3` | `m=n+1` | improve the `O(n 2^(n/2))` all-instance baseline, or expose a polynomial certificate branch | Huang–Li–Zhong ITCS 2026, Theorem 1.14 (`k=3`) |

V93 does **not** achieve that runtime improvement. The row fixes what a constructive certificate would have needed to accomplish.

## Frozen certificate row

| Certificate model | Constructible from input? | Verifiable? | Determines canonical decision? |
|---|---:|---:|---:|
| `AS(C)=(essential supports, full constant-output-parity syndrome relation)` | yes | yes | **no — theorem** |

For constant locality, the certificate is obtained by ANF expansion plus Gaussian elimination.

## Track A — bounded positive milestone

The full syndrome relation can certify a zero child when a syndrome involving only the already-fixed prefix and the next output forces that next bit. This gives a polynomial-time **zero-detection subroutine** on such prefixes.

The committed control `(x0,x1,x0 xor x1)` with prefix `(0,1)` forces the next bit to one, and exact counts are `(0,2)` for children zero/one.

This is useful but does not compare two nonempty children.

## Track B — mandatory collision and theorem

For every non-affine ternary `f`, compare

```text
C_f(x)    = (f(x), x1, x2, x3)
C_notf(x) = (1 xor f(x), x1, x2, x3).
```

They have identical support systems and identical complete global constant-syndrome relations. Their ranges are disjoint and cover all of `{0,1}^4`, so the certificate cannot by itself determine any avoided output valid for both.

If `f` is unbalanced, their first child counts are swapped. For `AND3` versus `NAND3`:

```text
AND3 : (N(0),N(1))=(7,1) -> canonical bit 1
NAND3: (N(0),N(1))=(1,7) -> canonical bit 0.
```

Thus the mandatory gate returns **comparison collision**, not comparison sufficiency.

The collision lifts to minimal-stretch high-branchwidth circuits by disjointly adjoining a zero-stretch high-branchwidth ternary background. The V87 pair-shadow proof already uses only the first `3N/4` random supports, so its linear-width argument specializes from `m=N+ceil(N^(2/3))` to `m=N` without changing the proof mechanism.

## Exhaustive audit

`affine_certificate_no_go.py` checks the whole ternary family:

```text
256 ternary functions
16 affine
240 non-affine
56 balanced non-affine
184 unbalanced non-affine
240 same-certificate complement instances
120 non-affine complement pairs with no common avoided word
184 functions / 92 complement pairs with opposite canonical first decisions
0 support mismatches
0 syndrome mismatches on non-affine instances
0 range-partition mismatches
0 decision mismatches on unbalanced non-affine instances
```

The symbolic proof is in `THEOREMS.md`; the census is only its executable regression gate.

## Consequence for the laboratory

The V85/V92 global affine-syndrome route is now closed **as a general high-width comparison oracle**. More affine optimization of the same certificate is forbidden unless additional prefix-conditioned information is specified.

The surviving positive role is zero detection when a prefix-supported syndrome forces the next bit.

The next natural front is no longer “find more global syndromes.” It is to study the child-count sign itself as a fixed-language counting problem:

```text
sign( N(p0)-N(p1) )
```

for ternary local constraints, and determine whether a standard #CSP/PP/communication formulation gives either a new compressed evaluator on a meaningful subclass or a rigorous hardness/barrier theorem explaining why exact comparison is the wrong primitive.

## Files

- `affine_certificate_no_go.py` — exhaustive mandatory gate and Track-A zero-detection control;
- `THEOREMS.md` — certificate definition, no-go theorem, and high-width lift;
- `RESULTS.json` — immutable quantitative snapshot;
- `IMPLICATION.json` — exact implication and route-closure record;
- `verify.py`, `verify_independent.py` — primary and independent regression gates;
- `V94_CORE_CONTEXT.md` — next theorem-native counting/comparison target.

## Nonclaims

V93 does not improve the Huang–Li–Zhong runtime, prove hardness of the canonical prefix sequence, establish a new general circuit lower bound, prove `P!=NP`, establish novelty, or supply peer review.
