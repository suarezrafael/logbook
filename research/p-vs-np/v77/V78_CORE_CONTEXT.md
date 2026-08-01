# V78 core context — factor two versus width preservation

## Established starting point

V77 replaces the V76 four-edge top-tree cover by a restricted topology-tree
hierarchy. From a supplied width-`b` subcubic gate decomposition it obtains

```text
width <= 2b,
height = O(log m),
EPL = O(m log m),
```

and therefore

```text
O(m log m A(2b)^2 poly(n,m))
```

incremental prefix avoidance in the supplied-decomposition regime.

The logarithmic-height topology hierarchy is prior art. The V77 contribution
is the retained two-edge support-boundary lemma. A single valid cluster can
attain `2b`, but no global factor-two lower bound is known.

## Primary V78 question

Decide whether the remaining factor two is structural or an artifact:

```text
Can every supplied width-b support decomposition be balanced to O(log m)
height with width b, b+O(1), or (2-epsilon)b?
```

Priority routes:

1. exact dynamic programming over topology-tree merge choices, optimizing the
   actual support boundary rather than the number of boundary edges;
2. exploit overlap between the two boundary-edge middle sets;
3. use posimodularity or uncrossing to replace a two-edge cluster by a nearby
   one-edge cut without losing balance;
4. search for infinite families in which every logarithmic-height hierarchy
   must contain a cluster of width strictly above `b`;
5. connect the question to balanced branch decompositions of symmetric
   submodular connectivity functions.

## Required experiments

- exact minimum width under height caps `c ceil(log2 m)` for increasing `c`;
- source-tree-aware searches, not only support-family searches;
- isomorphism reduction on five and six variables at seven or more gates;
- optimization of `A(width)^2` and dynamic dependency-cone work;
- independent validation of any claimed lower-bound family;
- regressions on the V76 six witnesses and V77 two-edge tightness gadget.

## Proof discipline

- A cluster attaining `2b` does not imply every hierarchy needs `2b`.
- Perfect-height inflation is not an `O(log m)` lower bound.
- Topology-tree existence and height remain attributed to prior art.
- Supplied-decomposition transfer remains distinct from decomposition
  discovery.
- Keep the direct P-versus-NP route inactive absent an unrestricted,
  lower-bound-relevant consequence.
