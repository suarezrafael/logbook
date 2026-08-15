# Laboratory V100 — literal-substitution peeling

V100 replaces the planned fixed-target 2-SAT attack on the remaining ternary
unate orbit with a stronger safe-relaxation theorem.

## Main idea

For an essential ternary local gate `g`, call a fiber **literal-graph
peelable** if there is a target bit `b` for which every local input with
`g=b` satisfies either

```text
x_v = a
```

or

```text
x_v = x_u XOR c.
```

The first form fixes one input. The second identifies one input with a copy or
negation of another.

Target output `b`, delete that output, impose only the forced literal relation,
and forget the rest of the selected fiber. This deliberately enlarges the
remaining feasible input set. Therefore a word missing from the relaxed
residual circuit is still missing after lifting to the original circuit.

Each step removes exactly one output and one input, preserves `m-n`, and never
increases locality above three. Repeating it gives a polynomial-time
preprocessor for arbitrary `NC0_3-Avoid`.

## Ternary classification

Among the 218 essential ternary truth tables, exactly 144 are literal-graph
peelable. They are precisely five NPN orbits:

```text
0x01   16 tables
0x06   24 tables
0x07   48 tables
0x18    8 tables
0x19   48 tables
----------------
       144 tables
```

After exhaustive V100 peeling, every residual essential ternary gate belongs
to only five NPN orbits:

```text
0x16   16 tables
0x17    8 tables   (MAJ_3 orbit)
0x1b   24 tables
0x1e   24 tables
0x69    2 tables
----------------
        74 tables
```

Thus V100 narrows the unrestricted ternary label universe from 218 to 74 truth
tables without worsening stretch or locality.

## Polynomial class

If every essential ternary gate of the input circuit is literal-graph
peelable, exhaustive peeling leaves an `NC0_2` circuit with positive surplus.
Guruswami--Lyu--Wang (APPROX/RANDOM 2022) give deterministic polynomial-time
range avoidance for `NC0_2` when `m>n`. Calling that published algorithm on the
residual circuit and reversing the V100 reductions gives a deterministic
polynomial-time avoider for the whole five-orbit class.

Consequences include:

- the previously open 48-table unate orbit `0x07` is in P;
- every essential ternary **unate non-MAJ** gate class is therefore covered, so the only unate ternary orbit left outside this theorem is signed `MAJ_3`;
- the V99 singleton orbit is subsumed by the more general peeling theorem;
- three genuinely non-unate orbits (`0x06`, `0x18`, `0x19`) are also covered.

## Why this bypasses the V56--V62 bijunctive barrier

The old `0x07` barrier proved that a fixed consistent collection of 2-CNF gate
fibers need not contain a redundant complete block, even at stretch one. V100
does not seek redundancy. It selects a fiber, extracts only one forced literal
relation, and then **relaxes away the rest of that fiber**. The V62
block-irredundant direct-sum family therefore does not obstruct this reduction.

## Strict non-unate family

For every `N>=5`, put the canonical `0x19` gate on cyclic triple supports and
duplicate the first support once. The resulting circuit is connected,
exact-stretch, essential ternary, non-unate, and has minimum input degree at
least three, so V97 leaves `lambda=N`. The canonical `0x19` gate has no
constant-coordinate forcing fiber, but its target-one fiber forces equality of
its first two inputs. V100 therefore solves this family by genuine pair
substitution, not by the earlier constant-fixing special case.

## Nonclaims

V100 does not solve the five residual hard NPN orbits, unrestricted
`NC0_3-Avoid`, the unbalanced signed-majority circuit class, or P versus NP. It
does not improve the Huang--Li--Zhong unrestricted worst-case exponent. The
safe-relaxation pattern is closely related to the monotone gate-elimination
reduction of Kuntewar--Sarma; novelty of the nonmonotone abstraction is not
claimed without external review.
