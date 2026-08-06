# V93 core context — high-width child-count compression gate with equal no-go track

## Mission

V93 may study only the first open bridge left by V92:

```text
Given a canonical prefix p, compare the exact child counts N(p0) and N(p1),
or certify that one child is empty, on high-width local circuits faster than
the Huang–Li–Zhong traversed-space bound.
```

The output policy is frozen by V92. Changing coordinate order, tie breaking, or suffix completion is not progress.

## Equal research budget

V93 has two coequal tracks. Neither is a fallback.

### Track A — constructive positive route

Find a high-width certificate that is computable from the explicit circuit and that deterministically supports at least one of:

- the canonical comparison `N(p0) <= N(p1)`;
- certified zero detection for one child;
- a theorem-native single-valued avoided output accepted by a checked transfer.

A positive certificate must be local or explicitly decomposable, efficiently verifiable, and accompanied by a deterministic map from the certificate to the required child decision or output. Affine-syndrome structure in the spirit of V85 is an admissible starting point; it is not assumed sufficient.

### Track B — no-go and closure route

Prove that a precisely defined class of high-width certificates cannot determine a unique canonical child decision or single-valued avoided output. A theorem of this form is a first-class promotable result, with the same budget and evidentiary standard as Track A.

Before expanding either track, V93 must spend one bounded milestone on each. Failure of Track A does not authorize indefinite positive experimentation, and an informal lack of construction does not count as Track B.

## Certificate admissibility gate

A lower bound on width is not automatically an output-producing certificate.

The V87 linear-branchwidth families use an existential/probabilistic obstruction through pair shadows and the Lee–Lee–Oum width connection. That result certifies the existence of high width, but it does not expose a deterministic local object from which the canonical output can be computed. Therefore:

```text
V87 existential width obstruction
!= constructive high-width branch
!= canonical single-valued output certificate.
```

Using the V87 obstruction alone predetermines the negative conclusion and cannot count as an attempted positive completion. Track A must introduce a constructive certificate available from the input instance. Track B may use the V87 distinction as motivation, but must prove an impossibility statement for a formally specified certificate model rather than merely restating existentiality.

## Admissible promotion outcomes

V93 is promotable with any one of the following, with outcomes 1–3 positive and outcome 4 equally weighted:

1. a quantified compression theorem for constructive connected-preimage certificates that improves the worst-case exponent in a named locality/stretch regime;
2. a zero-detection procedure that avoids exact counting but still implements the canonical policy or a checked transfer-accepted single-valued policy;
3. a reduction to a standard counting, communication, proof, tensor, or branching model with a rigorous upper or lower bound and an explicit output interface;
4. a no-go theorem proving that a precisely defined high-width certificate class cannot determine the canonical child comparison or any required single-valued output, followed by closure of that certificate class.

Outcome 4 is not a consolation result. It is successful route elimination when proved in a standard model with explicit quantifiers and scope.

## Required parameter target

Before coding, V93 must choose one exact target row:

| Class | Stretch | Required complexity | Consequence |
|---|---|---|---|
| selected `NC0_k` class | explicit `m(n)-n` | explicit time/oracle class | named theorem number |

It must also declare one certificate row:

| Certificate model | Constructible from input? | Verifiable? | Determines canonical decision? |
|---|---:|---:|---:|
| precisely defined model | yes/no | yes/no | theorem target |

No experiment is authorized until all cells in both rows are filled.

## Barrier gate

A communication-complexity route must pass the Chen–Hu–Ren algebrization audit from V91. A new component census, another low-width optimization, or a nonconstructive width lower bound does not satisfy the V93 implication rule.

## Stop rule

After the equal-budget milestones, continue only the track that has a formal lemma with a quantified route to one of the four promotion outcomes. If neither track produces such a lemma, close the high-width certificate front and move to a different theorem-native target rather than accumulating finite support examples.
