# V54 versus Kuntewar–Sarma 2025

## Sources compared

- V54: internal forcing-core theorem for pure `AND_k` and signed singleton fibers.
- Neha Kuntewar and Jayalal Sarma, *Range Avoidance in Boolean Circuits via Turan-type Bounds*, arXiv:2503.17114 / ECCC TR25-034, 2025.

## Comparison table

| Dimension | V54 | Kuntewar–Sarma 2025 |
|---|---|---|
| Main problem | Construct an explicit missing target and low-degree separator for pure `AND_k` support hypergraphs | Deterministic Range Avoidance for monotone local circuits through Turán-type hypergraph structure |
| Ternary threshold | Pure `AND3`, `m>n` | `MONOTONE-NC0_3-Avoid`, `m>n` |
| General gate class | Pure monomials; signed singleton-fiber extension under additional literal-count conditions | Arbitrary monotone ternary output functions covered by the paper's framework |
| Structural object | Nonempty 2-core in a support hypergraph | Forbidden subhypergraphs and loose chi-cycles |
| Output | Explicit target plus polynomial separator | Deterministic avoided output |
| Certificate | `(1-Y_e) product_{f in F_e} Y_f`, degree at most `k+1` | Algorithmic certificate induced by the identified hypergraph structure; not stated as the same low-degree separator |
| General `k` | Pure `AND_k` certificate at positive excess | The linear-stretch theorem highlighted in the paper is monotone ternary; broader Turán bounds are also studied |
| Novelty position | Certificate form may be distinct; algorithmic primacy for monotone ternary is not claimed | Prior algorithmic result for monotone ternary at minimum positive stretch |

## Exact overlap

For pure monotone `AND3` circuits with `m>n`, both lines imply a deterministic missing output. Therefore V54 must not be advertised as the first polynomial-time algorithm for monotone ternary Range Avoidance at positive stretch.

## Distinctive V54 statement

V54 proves a compact forcing certificate. If `e` lies in the 2-core and `F_e` contains at most one witness edge for each input of `e`, then

```text
Q_e(Y) = (1-Y_e) product_{f in F_e} Y_f
```

vanishes on the circuit range and has degree at most `k+1`. For `AND3`, the degree is at most four, over every field.

This is a different theorem statement from merely placing the search problem in polynomial time. Whether the separator is already implicit in the Turán/loose-cycle proof requires specialist comparison.

## Class containment caution

Pure `AND3` is a strict subcase of monotone `NC0_3`. Consequently:

- Kuntewar–Sarma is algorithmically more general in the ternary monotone setting;
- V54 is potentially more explicit about algebraic certificate form;
- the signed singleton-fiber extension is not a monotone theorem and has its own thresholds (`m>n` for coherent signs, `m>2n` for arbitrary signs in V54; later strengthened for affine singleton fibers by V56).

## Recommended manuscript language

> Kuntewar and Sarma independently give a deterministic polynomial-time algorithm for monotone `NC0_3-Avoid` at `m>n`, subsuming the algorithmic conclusion of our pure-`AND3` case. We retain the forcing-core argument because it yields a direct degree-at-most-four separator and extends verbatim to pure `AND_k` with degree at most `k+1`. We do not claim algorithmic priority for the monotone ternary regime.

## Open comparison question sent to the authors

The external message asks whether the V54 2-core witness certificate is already a direct special case or implicit corollary of the loose-chi-cycle framework. Until a response or a complete proof comparison is available, the repository labels the relationship `direct algorithmic overlap; certificate equivalence unresolved`.
