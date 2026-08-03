# V88 theorem packet — Property B blocks every three-row constructor

## Lemma 1 — a proper two-coloring covers every three-row target

Let `H` be a simple 3-uniform support hypergraph and suppose `H` has Property
B: its variables admit a two-coloring in which no support is monochromatic.

In the exact three-row reduction, variable patterns may be represented by
three active colors. Map the two colors of a proper Property-B coloring to any
two of those active colors. Every support remains nonmonochromatic, so no
labeled support can violate its three-row constraint, independently of the
labels.

Therefore **every** three-row target matrix on `H` is coverable.

## External random-hypergraph theorem

Achlioptas and Moore, *On the 2-Colorability of Random Hypergraphs* (RANDOM
2002), study `H_k(n,m)`, obtained by drawing `m` uniform `k`-subsets
independently with replacement. They prove that if

```text
r <= 2^(k-1) ln 2 - (ln 2)/2 - 1,
```

then `H_k(n,rn)` is two-colorable with high probability.

For `k=3`, the certified lower density is

```text
(7/2) ln 2 - 1 = 1.4260151319... .
```

## Theorem 2 — the V87 random model has Property B with high probability

The V87 model uses

```text
m_n = n + ceil(n^(2/3)),
```

so `m_n/n -> 1`.

Fix the denser constant ratio `r_0=5/4`. It satisfies

```text
1 < 5/4 < (7/2) ln 2 - 1.
```

For all sufficiently large `n`, `m_n <= r_0 n`. Couple the V87 sample to the
first `m_n` edge draws of `H_3(n,ceil(r_0 n))`. Two-colorability is monotone
under deletion of edges. Since the denser fixed-ratio model is two-colorable
with high probability, the V87 model is also two-colorable with high
probability. `QED`

## Corollary 3 — one family has four simultaneous properties

V86 bounds failure of the local Hall event by `8/49`. V87 proves that support
branchwidth is linear with probability tending to one and that repeated
supports occur with probability tending to zero. Theorem 2 adds Property B
with probability tending to one.

Hence, for every sufficiently large `n`, there exists a simple ternary support
family at the target stretch satisfying simultaneously:

1. no Hall-deficient gate set of size at most `n/(16e^2)`;
2. support branchwidth `Omega(n)`;
3. Property B;
4. after assigning `NOR3`, no nonzero constant output-parity syndrome.

The intersection remains nonempty because the Hall-success probability is
bounded away from zero while all three additional failure probabilities tend
to zero.

## Corollary 4 — universal support-only lists need at least four rows

Apply Lemma 1 to the family from Corollary 3. Every target matrix with at most
three rows is coverable. Therefore no procedure that receives only the support
family and always outputs at most three candidate targets can be universal for
`Eval_H` at the target stretch.

Equivalently,

```text
universal support-only Eval_H list size >= 4.
```

This is a rigorous lower bound for the precisely specified constructor model
whose output is an ordered support-dependent list of at most three target rows.
It strengthens the V85 pair lower bound and meets the V88 constructor-model
stop condition, but it is still far below the existential `O(n^(1/3))` upper
bound.

## Finite controls

Exact enumeration confirms Property B for every committed finite control used
in the recent obstruction program:

- V80 seven-variable control: `4` proper two-colorings;
- V80 eight-variable control: `20`;
- V80 nine-variable control: `30`;
- eight deterministic V87 random samples: `42, 10, 36, 56, 36, 60, 70, 128`.

Consequently, every three-row target matrix is coverable on each of those
finite controls, even though the controls were selected to audit Hall,
syndrome, connectivity, and width behavior.

## Strategic consequence

The V87 three-certificate obstruction cannot itself force a three-row missing
output. Any continuation toward a constructive `Eval_H` list must do at least
one of the following:

1. use four or more target rows;
2. exploit support properties not implied by Hall expansion, syndrome
   resistance, and linear branchwidth;
3. construct a non-Property-B family while preserving the target stretch and
   the other required barriers.

The most direct next experiment is therefore an exact four-row search on the
V80 controls and on small target-stretch support families.

## Nonclaims

This result does not construct a four-row obstruction, produce the
`O(n^(1/3))` list, prove that every V87 Hall-expander instance has Property B,
solve unrestricted `NC0_3-Avoid`, derandomize V87, establish a circuit lower
bound, confirm novelty, pass peer review, or resolve `P` versus `NP`.
