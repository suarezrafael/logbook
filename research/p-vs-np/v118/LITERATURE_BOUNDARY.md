# V118 literature boundary

## Inherited hardness boundary

V117 uses Aleksandrs Slivkins, *Parameterized Tractability of Edge-Disjoint Paths on Directed Acyclic Graphs*, SIAM Journal on Discrete Mathematics 24(1), 146–157 (2010), DOI `10.1137/070697781`. The source gives W[1]-hardness parameterized by the number of requests even when the demand graph is the union of two sets of parallel edges.

V118 does not challenge that theorem. The V117 reduction is a generic gate-resource construction; V118 imposes an additional signed-MUX realizability promise that exact clone outputs can be loop-erased while preserving the relevant boundary phases.

## Internal result

The clone-bank loop-erasure lemma, the constant-interface bound, and the resulting signed-MUX polynomial algorithm are internal claims of this laboratory. No literature source is asserted to contain this exact theorem.

The proof depends only on exact equality of the complete signed MUX descriptions. It should not be generalized to near-clones, same-selector gates, or arbitrary parallel resources without a separate proof.

## Novelty status

Novelty is not confirmed. External validation should compare the normalization to routing results with interchangeable parallel resources and to parameterizations by feedback sets, module width, and neighborhood diversity-like equivalence classes.

## Global boundary

Neither the Slivkins barrier nor the V118 clone-bank theorem resolves unrestricted signed-MUX `Delta<=1`, unrestricted `NC0_3-Avoid`, circuit lower bounds, or P versus NP.
