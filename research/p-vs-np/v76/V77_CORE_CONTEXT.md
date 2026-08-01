# V77 core context — tighten the top-tree transfer

## Established starting point

V76 combines standard logarithmic-height labelled top trees with a proved
support-boundary cover lemma. From a supplied width-`b` subcubic branch tree it
obtains a rooted binary gate tree with

```text
width <= 4b,
height = O(log m),
EPL = O(m log m).
```

The V75 symbolic circuit can therefore be rebuilt to give

```text
O(m log m A(4b)^2 poly(n,m))
```

incremental prefix-avoidance time in the supplied-decomposition regime.

The prior centroid-based `2b` proof attempt was rejected because recursive
components need not remain single original edge sides.

## Primary V77 question

Improve the parameter transfer or prove a genuine obstruction:

```text
Can 4b be replaced by 2b, 3b, b+O(1), or b?
```

Priority routes:

1. exploit more structure of retained label-bearing top-tree clusters to reduce
   the four-edge cover;
2. use a top-tree variant whose relevant clusters have at most two boundary
   **edges**, not merely two boundary vertices;
3. formulate an exact dynamic program over top-tree cluster certificates;
4. search for support systems that realize four nearly disjoint middle sets in
   one valid cluster;
5. construct an infinite family forcing width inflation for every chosen
   logarithmic-depth constant, or prove width preservation with a larger
   constant.

## Required experiments

- isomorphism-reduced exact Pareto frontiers beyond four variables;
- exact tradeoff searches on larger V72 private-vertex trees;
- adversarial optimization of `A(width)^2`, not only raw width;
- exhaustive connected-cluster audits categorized by one versus two boundary
  vertices and by the number of crossing branch edges;
- an independently checkable static top-tree certificate format;
- regressions against the six seven-gate perfect-height witnesses.

## Proof discipline

- Do not revive the discarded centroid invariant without a boundary-complexity
  proof.
- Keep perfect height distinct from `O(log m)` height.
- Attribute logarithmic-height top trees to prior art.
- Distinguish supplied-decomposition transfer from decomposition discovery.
- Keep the direct P-versus-NP route inactive absent an unrestricted,
  lower-bound-relevant consequence.
