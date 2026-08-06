# External-validation gate before V93

## Decision

V93 is **reserved but frozen**. No V93 experiment, theorem-development branch, or candidate promotion may begin until both short external-review packets below have been sent to independent researchers and the submission evidence has been recorded in `EXTERNAL_VALIDATION_GATE.json`:

1. `v90/EXTERNAL_REVIEW_V81.md` — deficiency conservation and balanced width/deficiency consequence;
2. `v90/EXTERNAL_REVIEW_V87.md` — rank-three primal-treewidth/hyperedge-branchwidth transfer.

The gate requires submission, not a favorable answer. Responses may take time; waiting for them must not be disguised as another internal laboratory. Every received confirmation, counterexample, convention correction, or prior-art citation must later be logged.

## Why the gate exists

The project has produced internally verified mathematical modules faster than it has exposed them to independent checking. That creates a systematic-risk asymmetry: internal volume grows while correlated proof or novelty errors can remain invisible.

The V81 and V87 packets are already small enough for first-pass expert review. Each isolates definitions, one narrow claim, a supplied proof, scope limitations, finite evidence, and explicit reviewer questions. Preparing another laboratory has lower expected information value than sending these packets.

## Submission evidence

For each packet, record all of the following:

- date and time sent;
- recipient description sufficient to establish independence and relevant expertise, without publishing private contact information;
- channel used, such as direct email, research-forum request, or formal review service;
- a stable private or public evidence reference;
- later response state: no response, acknowledged, proof confirmed, correction requested, counterexample, or prior-art citation.

A self-review, another model run, repository CI, or review by a person already directing the laboratory does not satisfy the external-submission condition.

## V93 cadence after release

V93 is managed in **weeks and milestones**, not as one laboratory per session.

### M0 — external release gate

Both V81 and V87 packets are submitted and evidenced.

### M1 — affine comparison falsification

Fill the exact transfer target and certificate-model rows, then test whether the proposed affine certificate determines the comparison `N(p0) <= N(p1)`, only detects a zero child, or admits identical certificates with opposite canonical decisions.

`M1 completed; research question still open` is a legitimate state. It must not trigger a smaller substitute promotion.

### M2 — theorem lift

Promotable progress requires one of:

- a quantified no-go theorem lifting a comparison collision to a precisely defined certificate class;
- a constructive comparison decoder;
- a certified zero-detection lemma with a transfer-compatible single-valued output interface;
- another standard-model upper or lower bound satisfying the frozen V93 promotion contract.

Finite evidence alone cannot promote V93, and same-day closure is not a target.

## Authority

`EXTERNAL_VALIDATION_GATE.json` is the machine-readable state. `LAB_STATUS.json` records the program-level hold. The V92 independent verifier checks that both sources agree before V93 is released.
