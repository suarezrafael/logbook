# V99 core context — label cohomology and genuinely non-unate transfer

## Starting point

V98 proves a clean polynomial subclass inside the V97 large-kernel regime.

For an essential unate gate, record one incidence bit `d(e,v)` indicating
increasing/decreasing orientation. If

```text
d(e,v)=r_v XOR q_e
```

globally, input/output switching turns the component into monotone `NC0_3`, so
the Kuntewar--Sarma `m>n` algorithm applies.

V98 also proves that loose-X support alone is insufficient for arbitrary labels:
a parity-labeled loose X is surjective, even when embedded into an exact-stretch
V97-irreducible host.

## Residual regimes

There are now two qualitatively different frontiers.

### A. Unbalanced unate labels

The incidence directions form a binary 1-cochain on the bipartite incidence
graph. V98 solves exactly the zero/co-boundary class. Nonzero XOR around an
incidence cycle is the obstruction to global switching.

V99 should test whether a bounded number of nonzero cycle defects can be handled
by:

- deleting/fixing a small feedback set;
- localizing defects onto a cycle basis;
- transfer matrices along loose-X / Berge structures;
- an FPT algorithm parameterized by the dimension or support of the defect
  syndrome.

A useful theorem would be `poly(N)*2^tau` for an explicit defect parameter
`tau`, with a strict family where `tau=o(lambda)`.

### B. Genuinely non-unate ternary labels

There are 218 essential ternary truth tables but only 72 are unate. V99 should
work modulo NPN equivalence rather than raw tables.

Priority experiments:

1. classify which non-unate NPN orbits make the simple loose-X map always
   non-surjective, sometimes surjective, or always surjective;
2. derive a constant-state transfer system for one infinite family;
3. convert any finite pattern into a symbolic recurrence before promotion.

Parity/XOR is already algebraically easy and should be used only as a control.

## External-calibration rule

The 12 August 2026 Brakensiek reply weakens novelty expectations for generic
polynomial linear-dependence arguments by connecting them to CSP sparsification
folklore. Do not return to that route without a consequence not already
explained by linear algebra/sparsification.

## Stop rule

No finite census may be promoted. V99 requires one of:

- a symbolic unbalanced-unate algorithm or lower obstruction;
- a symbolic transfer theorem for a genuinely non-unate NPN class;
- a rigorous parameterized reduction whose parameter is asymptotically smaller
  than the V97 peeling kernel on an explicit family.

The unrestricted benchmark remains unchanged.
