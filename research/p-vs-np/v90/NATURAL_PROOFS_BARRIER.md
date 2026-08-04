# Natural-proofs audit of the certificate ladder

## Decision

The Hall-deficiency, constant-syndrome, and bounded-width ladder is closed as an open-ended certificate-discovery program after V90.

This is a governance decision supported by barrier analysis. It is **not** a theorem that every such certificate is ruled out by Razborov–Rudich.

## What the natural-proofs theorem actually requires

For a property of Boolean functions to be natural against a circuit class, one must establish all of the following in the relevant asymptotic model:

1. **Constructivity:** membership in the property is efficiently decidable from the truth table, in the precise model used by the theorem.
2. **Largeness:** the property contains a sufficiently large fraction of all Boolean functions.
3. **Usefulness:** functions in the target circuit class eventually fail the property.

Under standard pseudorandom-function hardness assumptions, a property with all three features cannot prove the corresponding strong general-circuit lower bounds.

## Why the laboratory ladder is not automatically a natural proof

The existing certificates are properties of circuit presentations or support hypergraphs, not obviously representation-independent properties of Boolean functions. Their verification time is measured in the presentation size, whereas natural-proof constructivity is normally measured against the truth-table representation. The laboratory has also not proved the required largeness and usefulness statements for one induced Boolean-function property.

Therefore the sentence “every polynomially verifiable certificate program is forbidden” is false.

## Why the barrier still changes the research policy

The ladder repeatedly sought certificates with the following profile:

- efficiently recognizable;
- common enough to be found on broad or random families;
- strong enough to separate a target circuit class.

That profile is natural-proof-like. V86 and V87 then constructed families resisting multiple broad certificate mechanisms. These results are best interpreted as evidence that continuing to add similarly broad certificates is unlikely to produce the needed unrestricted lower bound, unless the new proposal explicitly escapes at least one naturality axis.

## Required escape declaration

No later laboratory may reopen this certificate front without identifying one of:

- **nonconstructivity:** the property is not efficiently recognizable in the relevant model;
- **nonlargeness:** the property is deliberately sparse but still useful;
- **representation sensitivity with a valid transfer:** the argument exploits circuit descriptions and separately proves that this suffices for the desired lower bound;
- **uniform/nondeterministic escape:** the implication uses a Williams-style algorithmic contradiction rather than a large constructive property;
- **restricted class outside the claimed barrier regime:** the target and cryptographic assumptions are stated exactly.

## Consequence for V90

The finite entropy ball proved in V90 remains a correct mathematical result, but it does not satisfy the declared material-advance rule for the `Eval_H` front. The global bridge remains open, and the certificate ladder is not extended.

The next primary front is an algorithmic-method feasibility audit. A secondary translation audit will connect Range Avoidance and Missing-String to meta-complexity without claiming an implication that has not been proved.

## Primary references

- A. Razborov and S. Rudich, “Natural Proofs,” JCSS 55(1), 1997; ECCC TR94-010.
- M. Carmosino, R. Impagliazzo, V. Kabanets, and A. Kolokolova, “Algorithms from Natural Lower Bounds,” CCC 2016; ECCC TR16-008.
- N. Vyas and R. Williams, “On Oracles and Algorithmic Methods for Proving Lower Bounds,” ECCC TR24-113.
