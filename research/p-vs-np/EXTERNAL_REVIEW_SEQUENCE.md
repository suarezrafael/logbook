# External review sequence before V93

## Objective

The current bottleneck is independent validation of two isolated structural claims, not production of another internal laboratory. Outreach must preserve the narrow scope of the packets and must not present the wider P-versus-NP program as the object under review.

## Order of operations

1. **Public, narrow technical question.** Start with the V81 conservation identity and balanced-cut consequence as a self-contained question suitable for cstheory.stackexchange or MathOverflow. Ask whether the identity or quantitative consequence is standard and request a citation, correction, or counterexample.
2. **Citable preprint.** Prepare a short preprint containing only independently checkable structural statements, definitions, proofs, nonclaims, and literature questions. Do not claim novelty before external feedback.
3. **Brazilian academic contact.** Seek a brief conversation with a theory-of-computation or discrete-mathematics researcher, preferably through a nearby university or an established Brazilian theory venue/community. The goal is technical triage and possible literature guidance, not endorsement of the full program.
4. **Direct author email.** Use only after a stable public object exists, and ask one theorem-specific question. Never request review of the entire laboratory.

## Qualifying submission evidence

For the external-validation gate, a submission may be evidenced by one of:

- a public technical-question URL with date and immutable text snapshot;
- a preprint submission identifier;
- a conference/workshop submission receipt;
- a targeted email to an independent academic, with recipient role, date, and message-id or archived copy.

Posting repository material without a question, CI review, another agent review, or discussion with someone already directing the laboratory does not qualify.

## Framing constraints

- Do not mention P versus NP in the title or opening paragraph.
- Do not attach or link the full laboratory history unless specifically requested.
- Do not assert novelty.
- Ask for one of: known reference, confirmation under the stated definitions, corrected statement, or counterexample.
- Keep V81 and V87 as separate requests.

## First action

Publish the V81 public question from `outreach/V81_PUBLIC_QUESTION.md`. Record the resulting URL and date in `EXTERNAL_VALIDATION_GATE.json`. The V87 packet remains separately required before V93 is released.
