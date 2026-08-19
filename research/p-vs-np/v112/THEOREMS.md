# V112 theorem ledger — serial MUX phase-transfer compatibility

## Setting

V111 reduced the remaining MUX obstruction to target compatibility among alternative return flows.  V112 isolates a natural exact-stretch support class where that compatibility question is completely local.

A **serial two-lobe chain** has one root selector with two central outputs.  Each layer consists of two disjoint two-variable lobes.  The four lobe-selector outputs return to one common exit variable.  Every non-final exit is the selector of one shared MUX gate whose two data branches enter the next layer, one branch per lobe.  The final layer exits back to the root.

For `d` shared hubs the template has

```text
n = 5(d+1),
m = n+1.
```

All gates may be arbitrary signed essential MUX functions on their prescribed supports.

## Lemma 1 — linear-time support recognition

The exact serial template is recognizable in linear time.

### Proof sketch

The root is the unique input selecting two outputs; every other input selects exactly one.  The two central gates expose four first-layer variables.  Their selector gates have one common outside data variable, the first exit hub, and pair the four variables into two mutual lobes.

At an internal hub `z`, its unique selector gate exposes one start variable from each next lobe.  The two start-selector supports intersect in the next exit hub; their other data variables are the two lobe partners.  The partner-selector supports verify the same pair/exit pattern.  Repeating this walk either returns to the root after using every variable/output exactly once in the template or rejects.  Every gate and variable is processed a constant number of times.

## Definition 2 — lobe-disjoint phase-transfer certificate

Choose one branch from each central gate so their selector source phases are opposite and their destinations lie in different lobes of the first layer.

Inside a two-variable lobe, use a simple branch path from the entry variable to the layer exit.  At each shared hub `h`, the two routes choose branches entering different next lobes and then choose simple paths through those lobes.

For a hub traversal `(h,b)` followed by first lobe branch `(g,c)`, the target required on `h` is

```text
t_h = alpha(g,c) XOR p_data(h,b) XOR out_flip(h).
```

The phase-transfer condition is that the two routes require the same `t_h` at every shared hub.

## Lemma 3 — local independence

For the serial two-lobe template, phase-transfer feasibility at one shared hub is independent of all later hubs.

### Proof

The two routes leave the hub into distinct lobes.  Those lobes have disjoint output gates and meet only at the common exit variable.  Therefore no lobe output creates a cross-route target equality constraint.  The target requirement on the current shared hub depends only on its chosen branch and the source phase of the first chosen lobe branch.  Both routes then arrive at the next common exit hub, erasing all other local route information.  Hence a compatible local choice can be concatenated with any compatible choice in the next layer.

## Theorem 4 — exact phase-transfer decision on serial chains

There is a deterministic linear-time algorithm, after recognition, that decides whether a serial two-lobe chain admits a lobe-disjoint phase-transfer certificate and constructs a missing output whenever one exists.

### Proof

There are only four central branch pairs and a constant number of simple paths through a two-variable lobe.  Enumerate the opposite-phase central choices entering distinct first lobes.  At every shared hub enumerate the constant number of branch pairs entering distinct next lobes and the constant number of local lobe paths.  By Lemma 3, the first locally compatible choice can be committed without backtracking across layers.

After all layers are concatenated, assign each selected MUX output the target that propagates to the source phase of the next selected branch, except the final branch of each cycle, which propagates to the complement of that cycle's initial root phase.  Hub compatibility guarantees one target bit per shared output.  The two initial phases are opposite, so the two cycles force opposite Boolean values on the root selector.  Thus the fixed-output 2-CNF is unsatisfiable and the target word is outside the circuit range.

The algorithm is complete for this **lobe-disjoint serial certificate class**.  It does not claim that every serial signing has such a certificate.

## Theorem 5 — minimum overlap on the serial template

For the intended two root-return routes in a depth-`d` serial chain, every pair uses all `d` shared hub outputs.  Hence their output-gate overlap is at least `d`.  Lobe-disjoint routes share only those hubs, so their overlap is exactly `d` and is minimum.

### Proof

Every path leaving layer `j` reaches its common exit hub.  If that hub is not the root, the unique output selected by the hub is the only branch-graph edge leaving it toward later layers.  Therefore every root-return route must traverse every shared hub gate.  Distinct lobes have disjoint output gates, giving the matching upper bound.

## Theorem 6 — a mixed optimum face for every depth

There is a periodic signed MUX labeling of the serial template for every `d>=1` with both:

1. a target-compatible minimum-overlap pair, and
2. a target-incompatible minimum-overlap pair.

Thus target compatibility is **not an invariant of minimum overlap**, even on a Hall-minimal exact-stretch serial family.

### Periodic signing

The shared hub gate repeats

```text
polarity = (0,1,1), out_flip = 0.
```

The first gate of the next left lobe repeats selector polarity one, while the first gate of the next right lobe repeats selector polarity zero; the complete fixed five-gate block is recorded in `mux_phase_transfer.py`.

For the compatible pair, one route takes hub branch one followed by right-lobe branch one; the other takes hub branch zero followed by left-lobe branch zero.  Both require target zero on every shared hub:

```text
route 0: 1 XOR 1 = 0,
route 1: 1 XOR 1 = 0.
```

For the incompatible pair, route zero takes hub branch zero followed by left-lobe branch one, while route one takes hub branch one followed by right-lobe branch one.  Their hub requirements are respectively one and zero.  The conflict occurs at every shared hub.

Both pairs use exactly the `d` mandatory shared hubs and no common lobe output, so both are minimum-overlap by Theorem 5.  V112 selects the compatible local transfer in every layer.

The primary verifier additionally checks that the deterministic V111 reference implementation rejects this periodic family through depth 50.  That finite implementation audit is not elevated into an implementation-independent all-depth theorem; the rigorous all-depth statement is the mixed optimum-face separation above.

## Theorem 7 — Hall minimality for all depths

The serial support family is Hall-minimal: it has `m=n+1`, and deleting any one output leaves a perfect matching from the remaining `n` outputs to the `n` inputs.

### Proof

Match one central output to the root and every non-central output to its selector.  This is a size-`n` matching leaving only the second central output unmatched.

If the deleted output is either central output, use the other central output at the root and retain all selector matches.

Otherwise delete the unique selector output of some non-root input `x`, freeing `x`.  Starting from the unmatched second central output, an alternating path reaches every non-root input: its two data variables enter the first left/right lobes; the matched gate of a lobe's second variable reaches its partner and the layer exit; each matched hub output reaches both starts of the next layer; induction reaches every later lobe variable and hub.  Choose an alternating path ending at `x` and flip its matching edges.  This matches the formerly unmatched central output and the free variable `x`, producing a perfect matching after the deletion.

## Theorem 8 — exact V102 backdoor

The periodic V112 family has the same support as the V111 `k=2` nested chain, hence

```text
beta_V102 = 3(d+1) = 3n/5.
```

The lower/upper-bound proof is support-only and is unchanged by the V112 signed labeling: with an exit hub selected, each two-variable lobe needs one selected lobe variable; without it, both are forced.  Selecting all `d+1` exit hubs and one variable per lobe attains equality.

## Boundary

V112 completely handles target compatibility only for the recognized serial two-lobe phase-transfer class.  It does not decide compatibility over the full optimum-flow polytope of an arbitrary MUX circuit.  In general, an optimum flow may be incompatible while another equal-cost optimum is compatible; selecting among those alternatives remains the next front.

V112 does not prove all essential MUX/bijunctive `0x1b` circuits are in P, unrestricted `NC0_3-Avoid`, a new general circuit lower bound, or P versus NP.  Novelty and priority are not established.
