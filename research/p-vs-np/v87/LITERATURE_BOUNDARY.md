# V87 literature boundary

## External theorem used

The only nonlocal asymptotic input in the linear-branchwidth proof is:

- Choongbum Lee, Joonkyung Lee, and Sang-il Oum,
  **Rank-width of random graphs**, Journal of Graph Theory 70(3), 2012,
  DOI `10.1002/jgt.20620`, arXiv `1001.0461`.

They prove that for `G(n,p)` with `p=c/n` and every fixed `c>1`, rank-width
and therefore treewidth are linear in `n` asymptotically almost surely.

A later direct treatment and parameter refinement is:

- Tuan Anh Do, Joshua Erde, and Mihyun Kang,
  **A note on the width of sparse random graphs**,
  Journal of Graph Theory, DOI `10.1002/jgt.23081`,
  arXiv `2202.06087`.

V87 uses only the qualitative consequence `tw=Omega(n)` in the supercritical
regime.

## Internal contributions of the laboratory step

The following arguments are proved inside V87:

1. a random pair selected from a random ternary support is exactly uniform;
2. the rank-three transfer
   `tw(primal(H))+1 <= max(3,ceil(3 bw(H)/2))`;
3. the intersection of the V86 Hall/simplicity event with the high-width
   event;
4. the McDiarmid exponent no-go;
5. the correction from `0.4968...` to the fixed-cut expectation
   `0.54657...`.

The transfer inequality is structurally close to standard relations between
treewidth and branchwidth of graphs and hypergraphs. No novelty claim is
made without a dedicated publication search.

## Model conversion

The selected-pair shadow initially samples graph edges with replacement.
The number of collisions among `Theta(n)` draws from `Theta(n^2)` possible
pairs is `O_p(1)`. Conditional on its number of distinct pairs, the distinct
edge set is uniform. Standard monotone coupling transfers the supercritical
`G(n,p)` result to this random-graph-process formulation.

This conversion must remain explicit in any manuscript; the selected pairs
are not literally independent Bernoulli graph edges after duplicate removal.

## What the literature does not supply automatically

The random-graph theorem does not:

- give an explicit deterministic hypergraph;
- construct an avoided output;
- solve `Eval_H`;
- prove a new circuit lower bound;
- imply `P != NP`.

It only supplies the high-width property needed to intersect the three
certificate barriers.

## Novelty status

Repository-internal verification is complete. External novelty, optimal
constants, and publication status remain unconfirmed.
