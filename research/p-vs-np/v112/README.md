# Laboratory V112 — serial MUX phase-transfer compatibility

V112 attacks the exact gap left by V111: a minimum-overlap two-flow can be target-incompatible even when another flow with the same minimum overlap is compatible.

For a natural exact-stretch **serial two-lobe MUX chain**, this selection problem becomes local.  Each layer has two disjoint two-variable lobes meeting at one exit hub.  The hub's unique MUX output enters the next two lobes.  When the two routes use different lobes, their only shared outputs are the hub gates.

The target required on a shared hub depends only on the chosen hub branch and the source phase of the first branch in the next lobe.  Hence each layer exposes a constant-size phase-transfer relation.  These local choices are independent across layers, so the existence of a lobe-disjoint compatible pair is decided and a missing word is constructed in linear time after recognizing the template.

## Mixed optimum-face family

For every depth `d>=1` there is a periodic signed labeling with

```text
n = 5(d+1),
m = n+1,
minimum overlap = d,
beta_V102 = 3(d+1) = 3n/5.
```

The same instance has both:

- an incompatible pair of return flows with minimum overlap `d`, and
- a compatible pair with the same minimum overlap `d`.

Therefore target compatibility is not an invariant of the ordinary min-overlap objective.  V112 chooses the compatible phase transfer locally in every layer.

The deterministic V111 reference implementation is audited to reject the periodic family through depth 50; the rigorous all-depth claim is the stronger implementation-independent fact that the optimum face contains both compatible and incompatible minimum-overlap pairs.

## Additional structure

The serial support is Hall-minimal for every depth: deleting any output leaves a perfect output-to-input support matching.  The exact V102 backdoor is linear, `3n/5`, so the V112 construction is not explained by a small affine backdoor.

## Verification

`verify.py` exercises the actual recognizer/constructor, the periodic family through depth 50, complete original ranges for the small members, the current V111 rejection control, V110 nested-bottleneck separation, Hall matching audits, exact small beta, arbitrary variable/gate permutations, and random signed-template soundness.

`verify_independent.py` does not import V112.  It reconstructs the serial support and periodic signing, builds explicit compatible and incompatible minimum-overlap cycles, verifies the compatible target by an independent 2-SAT SCC engine through depth 100, brute-forces the first images, independently checks Hall matching and the beta formula, and audits the mixed optimum face.

## Boundary

V112 is complete for the **lobe-disjoint phase-transfer certificate class on recognized serial two-lobe chains**.  It is not a complete optimizer over all target-compatible flows in arbitrary MUX circuits.

All essential MUX/bijunctive `0x1b`, unrestricted `NC0_3-Avoid`, general circuit lower bounds, and P versus NP remain open.  No novelty, priority, or peer-review claim is made.
