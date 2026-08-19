# V110 theorem ledger — phase-compatible shared-gate MUX cycles

## Setting

For a signed essential ternary MUX output

```text
g = o XOR MUX(s XOR p_s, a XOR p_a, b XOR p_b),
```

fixing the output target gives two exact 2-CNF clauses. Selecting branch `r` yields an implication

```text
x_s = alpha_r  ->  x_d = beta_r(target),
```

where the two source phases are opposite and the target bit chooses the arrival phase.

## Lemma 1 — compatible shared-output composition

Let two directed branch cycles start at the same selector variable `v` with opposite source phases. Suppose their output-gate sets intersect in exactly one gate `h`. If the target bit required at `h` is the same on both cycles, then the two cycle target assignments are jointly consistent and force opposite values of `x_v`.

### Proof

On each cycle, target every selected implication so it arrives at the source phase of the next selected branch, except the final implication, which arrives at the complement of the first source phase. A cycle starting at phase `alpha` therefore contains

```text
x_v = alpha -> x_v = 1 XOR alpha,
```

and every satisfying assignment would need `x_v=1 XOR alpha`. Opposite initial phases force the two Boolean values of `v`. All outputs other than `h` are distinct between the cycles; by hypothesis both cycles require the same target on `h`. Hence one full target word contains both contradictions simultaneously. Unselected clauses of fixed MUX outputs can only strengthen the formula. QED.

## Definition — upgraded V109 return network

Start from a V109 `GateBottleneck` certificate for selector `v`, first gates `g_0,g_1`, opposite first source phases, destinations `d_0,d_1`, and bottleneck gate `h`.

Remove outputs whose selector is `v`, as in V109. Split each remaining output gate into an in/out edge. Give every gate edge capacity one except `h`, which receives capacity two. Give all non-gate internal arcs capacity two. A super-source sends one unit to each `d_i`; the sink is `v`.

## Theorem 2 — V110 shared-gate avoider

If the upgraded network has an integral flow of value two, the two decomposed return routes share exactly the bottleneck output `h`, and both lifted cycles require the same target bit on `h`, then a missing output is constructible in deterministic polynomial time.

### Proof

V109's bottleneck property says every return path from either destination uses `h`. Raising only the capacity of `h` to two allows two units to traverse it. Every other output gate retains capacity one, so the two flow paths are output-gate-disjoint outside `h`. Prepending the two prescribed first branches gives the cycles in Lemma 1. Equality of the required target at `h` completes the compatible composition. Max-flow, path decomposition, target comparison, and lifting are polynomial. QED.

## Residual alternatives

The V110 search distinguishes two failures after a V109 bottleneck:

1. `nested-bottleneck`: the upgraded network still has maximum flow one;
2. `phase-conflict`: flow two exists, but the two routes demand different target bits on the shared gate.

No theorem in V110 converts either alternative into a missing output.

## Theorem 3 — strict exact-stretch separation family

For every `k>=2`, take variables

```text
v,
A_1,...,A_k,
B_1,...,B_k,
w,
C_1,...,C_k,
D_1,...,D_k,
```

so `n=4k+2`. Add two distinct-support central gates

```text
MUX(v,A_1,B_1),
MUX(v,A_2,B_2).
```

For each pre-lobe `X in {A,B}`, add `k` outputs that move forward inside the lobe and expose `w` as the alternate data input, with the final output pointing to both `w` and `X_1`. Add the shared gate

```text
h = MUX(w,C_1,D_1).
```

For each post-lobe `X in {C,D}`, add the analogous `k` outputs with hub `v`. The total is

```text
m = 2 + 2k + 1 + 2k = 4k+3 = n+1.
```

Then:

- the branch graph is strongly connected;
- `v` is the only repeated selector and every return from either central destination to `v` uses `h`, so V109 yields the one-gate bottleneck rather than a gate-disjoint double cycle;
- after raising only `h` to capacity two, one return can use the `C` post-lobe and the other the `D` post-lobe, so the routes share exactly `h`;
- both traversals require the same target on `h`, and V110 constructs a missing output;
- the support family is Hall-minimal;
- no ignored-output set exposes a V108 SCC-separated bridge certificate;
- the exact V102 strong-affine backdoor is

```text
beta = 2 + 4 ceil(k/2).
```

### Backdoor proof

Selecting both hubs `v,w` reduces each of the four lobe constraints to a minimum vertex cover of a `k`-cycle, costing `ceil(k/2)` per lobe, for an upper bound `2+4 ceil(k/2)`.

If `v` is absent from the backdoor, every post-lobe selector must be selected because an unselected post selector would require the absent hub `v` among its two data variables; the two distinct-support central gates additionally force their data variables. If `w` is absent, every pre-lobe selector must be selected and the shared gate forces the first variables of both post lobes, after which the remaining post constraints still require a cycle-cover amount. The cases with one or both hubs absent are therefore no cheaper than the construction with both hubs selected. Thus the displayed value is exact.

### Hall-minimality sketch

Deleting a central output allows the other central gate to match `v`, the shared gate to match `w`, and all lobe outputs to match their selectors. Deleting the shared gate is repaired by matching one central gate to `v`, the other into one pre-lobe, and shifting the displaced matching along that lobe until `w` is reached. Deleting a lobe output is repaired by the analogous alternating-path shift from the redundant central/shared structure through the missing selector. The primary and independent verifiers reconstruct perfect matchings after every single-output deletion over growing `k`.

### V108 separation sketch

Every non-hub selector has exactly one output. Removing such an output as the V108 bridge makes its selector acyclic. Removing `h` makes selector `w` acyclic. Removing a central bridge leaves the other central output; if all unique lobe outputs needed for cyclicity remain, the relevant terminal stays in the same global cyclic component, while ignoring a unique lobe output to separate components breaks that lobe's cycle. Hence two distinct cyclic SCCs cannot be exposed by the V108 bridge rule.

## Boundary

V110 is a polynomial certificate class strictly extending the gate-disjoint branch of V109. It does not solve `phase-conflict` or `nested-bottleneck`, does not prove all essential MUX/bijunctive `0x1b` circuits are in P, does not solve unrestricted `NC0_3-Avoid`, and does not resolve P versus NP.