# External-validation gate before V93

## Decision

V93 is **reserved but frozen**. No V93 experiment, theorem-development branch, or candidate promotion may begin until both short external-review packets below have been submitted to an independent external audience and the evidence has been recorded in `EXTERNAL_VALIDATION_GATE.json`:

1. `v90/EXTERNAL_REVIEW_V81.md` — deficiency conservation and balanced width/deficiency consequence;
2. `v90/EXTERNAL_REVIEW_V87.md` — rank-three primal-treewidth/hyperedge-branchwidth transfer.

The preferred first move is not a generic email. For V81 it is a public, self-contained technical question asking for a standard name, reference, correction, or counterexample. A stable public permalink counts as submission evidence. A favorable answer is not required to release V93, but every later response must be logged.

## Why the gate exists

The project has produced internally verified mathematical modules faster than it has exposed them to independent checking. That creates a systematic-risk asymmetry: internal volume grows while correlated proof or novelty errors can remain invisible.

The V81 and V87 packets are already small enough for first-pass expert review. Each isolates definitions, one narrow claim, a supplied proof, scope limitations, finite evidence, and explicit reviewer questions. Preparing another laboratory has lower expected information value than submitting these packets.

## Outreach order

The authoritative sequence is `EXTERNAL_OUTREACH_SEQUENCE.md`:

1. public narrow technical question;
2. citable preprint when genuinely ready;
3. Brazilian or regional academic contact;
4. targeted author email tied to a named theorem or convention.

The title, subject, and opening must not mention P versus NP, the forty-seven-laboratory history, a breakthrough, or an unverified novelty claim. Direct email must never ask for review of the entire program.

## Submission evidence

For each packet, record all of the following:

- date and time submitted;
- channel used;
- audience or recipient description sufficient to establish independence and relevant expertise, without publishing private contact information;
- a stable public URL or other auditable evidence reference;
- later response state: no response, acknowledged, proof confirmed, correction requested, counterexample, or prior-art citation.

A public technical question qualifies. A prepared draft, repository post without a question, self-review, another model run, CI, or review by a person already directing the laboratory does not.

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
