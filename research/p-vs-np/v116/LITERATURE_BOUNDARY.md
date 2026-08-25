# V116 literature boundary

V116's contribution is the signed-MUX / V113-dominator transfer at the first cyclic stage level. It does not claim the underlying directed-disjoint-path facts as new.

## General directed linkage hardness

Fortune, Hopcroft and Wyllie, *The directed subgraph homeomorphism problem*, Theoretical Computer Science 10(2), 111–121 (1980), DOI `10.1016/0304-3975(80)90009-2`.

This is the classical hardness boundary already used by V114: unrestricted directed two-linkage is hard. V116 avoids that regime by requiring a one-gate deletion to make every relevant non-common stage acyclic.

## Parameterized routing on DAGs

Aleksandrs Slivkins, *Parameterized Tractability of Edge-Disjoint Paths on Directed Acyclic Graphs*, SIAM Journal on Discrete Mathematics 24(1), 146–157 (2010), DOI `10.1137/070697781`.

The relevant boundary for V117 is that allowing the number of DAG requests to grow with a parameter does not automatically yield FPT. V116 uses a self-contained product-state DP only after proving that the residual request count is at most five, a fixed constant.

A modern strengthening of this parameterized hardness landscape is:

Ken-ichi Kawarabayashi, Nicola Lorenz, Marcelo Garlet Milani and Jacob Stegemann, *Directed Disjoint Paths Remains W[1]-Hard on Acyclic Digraphs Without Large Grid Minors*, IPEC 2025, LIPIcs, DOI `10.4230/LIPIcs.IPEC.2025.2`.

The V116 theorem does not depend on this later strengthening; it is recorded to prevent V117 from mistaking a variable-dimensional product DP for an FPT result.

## What V116 proves internally

The laboratory proves internally that, after the V113 dominator decomposition and under feedback-gate number at most one per non-common stage:

1. a `Delta<=1` witness has only one possible shared non-common gate;
2. fixing that gate and the single feedback gate leaves at most five gate-disjoint requests in a DAG;
3. those fixed-five requests are decided by a product-state token DP on a gate-split DAG;
4. signed target compatibility is local to the shared gates; and
5. an infinite exact-stretch cyclic family separates V116 from V115.

No novelty or priority claim is made until external specialist review compares this exact signed-MUX formulation with the broader linkage literature.
