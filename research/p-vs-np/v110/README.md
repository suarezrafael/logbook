# Laboratory V110 — phase-compatible shared-gate MUX cycles

V110 attacks the one-output bottleneck branch left open by V109.

For a repeated selector `v`, V109 either finds two output-gate-disjoint opposite-phase return cycles or exposes one output gate `h` that lies on every return path from the two chosen branch destinations back to `v`. V110 asks whether both returns can pass through that same gate `h` without requiring contradictory target bits on `h`.

## Shared-gate certificate

Give every return-network output capacity one except the V109 bottleneck `h`, which receives capacity two. If the upgraded network has flow two, decompose it into two return routes. V110 accepts the certificate only when:

1. the two resulting cycles share exactly the output gate `h` and no other output gate; and
2. the target bit required at `h` is identical on both cycles.

All other selected outputs remain disjoint. The two cycles still start at the same selector with opposite source phases, so they force opposite Boolean values on that selector. Because the single shared output receives one compatible target bit, the combined fixed-output 2-CNF is inconsistent. A missing full output is therefore constructed in polynomial time.

If capacity two at `h` still does not permit two routes, V110 records a nested bottleneck. If two routes exist but demand different target bits at `h`, V110 rejects the certificate as a phase conflict. Neither residual is claimed solved.

## Strict exact-stretch family

For every `k>=2`, V110 uses

```text
v,
A_1,...,A_k,
B_1,...,B_k,
w,
C_1,...,C_k,
D_1,...,D_k
```

with

```text
n = 4k+2,
m = n+1.
```

Two distinct-support central gates leave `v`; the pre-lobes return only through selector `w`; one shared MUX at `w` branches into two post-lobes returning to `v`.

The family is Hall-minimal, is outside the entire V108 SCC-separated hierarchy, and forces V109 into the one-gate bottleneck `h`. Upgrading only `h` yields two otherwise gate-disjoint routes with a common compatible target. The V102 strong-affine backdoor is exactly

```text
beta = 2 + 4 ceil(k/2) = Theta(n).
```

Thus V110 gives a polynomial-time certificate on an infinite exact-stretch family where the earlier affine-backdoor parameter remains linear and V108/V109 do not already return a missing word.

## Verification

`verify.py` executes the actual V109 bottleneck search and V110 upgraded-flow implementation, checks the strict family, Hall minimality, exact small beta, exhaustive V108 absence on the first members, complete original ranges where feasible, and signed switching controls.

`verify_independent.py` does not import V110. It reconstructs the family, uses an independent 2-SAT SCC engine for the explicit target through `k=100`, brute-forces the first original ranges, checks Hall minimality through `k=60`, verifies beta by a separate dynamic program, reconstructs V108 absence for the first members, and audits the forced shared-gate structure.

An additional out-of-branch falsification sweep over thousands of small random signed MUX circuits found no case in which a V110 certificate produced a word inside the original image. That sweep is evidence only, not part of the theorem.

## Boundary

V110 does **not** solve every V109 bottleneck. Two residuals remain explicit:

- `phase-conflict`: two routes through the shared gate exist, but they require opposite target bits on that gate;
- `nested-bottleneck`: even capacity two on the first bottleneck does not yield two gate-disjoint returns apart from the shared gate.

Therefore V110 does not prove all essential MUX/bijunctive `0x1b` circuits are in P, unrestricted `NC0_3-Avoid`, a new general circuit lower bound, or P versus NP. Novelty, priority, and peer review remain unconfirmed.