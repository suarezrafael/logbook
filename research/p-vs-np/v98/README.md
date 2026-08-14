# Laboratory V98 — switching-balanced unate kernels

V98 starts from the irreducible large-kernel regime left by V97 and tests the
Kuntewar--Sarma loose-X/Turan route beyond raw monotonicity.

The first strong generalization one might try is false: a loose-X support does
not by itself force a missing edge coloring for arbitrary ternary labels.
Parity-of-three labels give an explicit scalable counterexample. V98 therefore
adds a label condition rather than treating the support theorem as sufficient.

## Main positive result

Normalize every local output to its essential support. For an essential unate
gate `g_e` and an incident input `v`, let

```text
d(e,v)=0  if g_e is nondecreasing in v,
d(e,v)=1  if g_e is nonincreasing in v.
```

Call a component **switching-balanced unate** if the incidence equations

```text
d(e,v) = r_v XOR q_e
```

have a solution with one bit `r_v` per input and one bit `q_e` per output.

The equations are solved by one parity-BFS on the input/output incidence graph.
When they are consistent, change coordinates by

```text
z_v = x_v XOR r_v,
C'_e(z) = C_e(x) XOR q_e.
```

Every transformed local gate is monotone. Domain and codomain flips are
bijections, so a missing word for `C'` maps back to a missing word for `C`.

Kuntewar--Sarma (APPROX/RANDOM 2025) already give deterministic polynomial-time
range avoidance for monotone `NC0_3` whenever `m>n`. Therefore:

> If an exact-stretch `NC0_3` circuit has a positive-surplus connected component
> that is switching-balanced unate, a missing output is constructible in
> deterministic polynomial time.

Recognition adds only linear time in the incidence size (hence linear time for
3-local circuits), before invoking the published monotone avoider.

## Strict nonmonotone large-kernel family

For every `N>=5`, take cyclic supports

```text
{i,i+1,i+2} mod N
```

for `N` outputs and duplicate the first support once, giving `N+1` outputs.
Let every transformed gate be `MAJ_3`, but use the global coordinate change
`z_0=x_0 XOR 1` and `z_i=x_i` for `i>0`.

In the original coordinates the circuit is nonmonotone, every gate has essential
arity three, every input has incidence degree at least three, the component is
connected, and none of the V97 leaf/unary/constant reductions applies. Thus the
V97 peeling parameter is `lambda=N`, while V98 recognizes the switching in
linear time and reduces the family to the published polynomial monotone case.

This is a strict extension in the **raw label class**, not a claim that the
coordinate-change observation itself is novel.

## Main negative result

For every `ell>=3`, V98 builds a parity-labeled simple loose-X source with
`2*ell` edges. Two nonadjacent opposite-parity cycle edges receive a shared
third vertex and every other cycle edge receives a private third vertex.

For every requested edge word `y`, an explicit assignment realizes `y`:

```text
w=0,
v_0=y_0,
v_3=y_3,
all other cycle vertices=0,
p_i = y_i XOR v_i XOR v_{i+1}.
```

Hence the induced map on the loose-X edges is surjective. The construction is
embedded into an exact-stretch connected parity host in which every input has
degree at least two and every gate remains essential ternary. The host therefore
survives the V97 irreducibility rules.

Consequently, **existence of a loose X alone is not an arbitrary-label range
certificate**. Any extension of the Turan route must use a label invariant,
a larger substructure, or global algebra.

The global parity host is itself algebraically easy; it is used only to refute a
support-only loose-X generalization.

## Executable evidence

`switching_unate.py` checks:

- all 256 ternary truth tables;
- 218 have essential arity three;
- 72 of those are unate;
- the strict switching-balanced family for `N=5,...,10`;
- exact preservation of the finite ranges under the recovered input/output
  switching;
- parity loose-X surjectivity for lengths 6, 8, 10, and 12;
- an exact-stretch irreducible host with minimum input degree at least two.

`verify_independent.py` repeats the key finite checks without calling the primary
balance solver.

Finite audits are implementation evidence only. The switching theorem and
parity witness are symbolic.

## Files

- `switching_unate.py` — recognition, switching transformation, strict family,
  parity loose-X host, and audit builder;
- `RESULTS.json` — committed finite regression snapshot;
- `THEOREMS.md` — symbolic proofs;
- `LITERATURE_BOUNDARY.md` — prior-art and external-correspondence calibration;
- `IMPLICATION.json` — conservative frontier declaration;
- `verify.py`, `verify_independent.py` — primary and independent verification;
- `V98_SWITCHING_UNATE_THEOREM.tex` — formal theorem module;
- `V99_CORE_CONTEXT.md` — next label-cohomology / non-unate frontier.

## Nonclaims

V98 does not solve unrestricted `NC0_3-Avoid`, does not improve the
Huang--Li--Zhong worst-case bound, does not trigger a circuit-lower-bound
transfer, does not establish novelty or peer review, and does not resolve
P versus NP.
