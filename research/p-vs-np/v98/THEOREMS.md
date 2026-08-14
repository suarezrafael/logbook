# Laboratory V98 — switching-balanced unate kernels

## 1. Setup

Let a connected component of an explicit local Boolean circuit be

```text
C : {0,1}^n -> {0,1}^m,    m>n,
```

with every local output depending on at most three input bits. As in V97,
remove inessential coordinates from every listed support first.

For an essential local gate `g_e` and an incident variable `v`, say that the
incidence `(e,v)` has **unate direction** `d(e,v)=0` when `g_e` is nondecreasing
in `v`, and `d(e,v)=1` when it is nonincreasing in `v`. Because `v` is
essential, an unate gate cannot have both choices: the direction is unique.

## 2. Switching-balance

### Definition 2.1

A unate labeled component is **switching-balanced** if there are bits `r_v` for
input vertices and `q_e` for output vertices such that every incidence satisfies

```text
d(e,v)=r_v XOR q_e.        (1)
```

### Lemma 2.2 — linear-time recognition

For locality at most three, switching-balance is recognizable in deterministic
linear time in the circuit size.

**Proof.** Regard (1) as parity constraints on the bipartite incidence graph
whose left vertices are inputs and right vertices are outputs. Fix one potential
to zero in each connected component and propagate potentials by BFS. A conflict
is exactly an inconsistent XOR cycle. There are at most three incidences per
output, so the work is `O(n+m)`. Local unateness and essentiality are checked
from constant-size truth tables. QED.

Equivalent formulation: switching-balance holds iff the XOR of incidence
directions around every cycle of the bipartite incidence graph is zero.

## 3. Switching theorem

### Theorem 3.1 — balanced unate implies monotone after switching

Suppose (1) has a solution. Define new input coordinates by

```text
z_v = x_v XOR r_v
```

and transformed outputs by

```text
C'_e(z)=C_e(x) XOR q_e.
```

Then every local output of `C'` is monotone nondecreasing in every essential
input coordinate.

**Proof.** Complementing input `v` toggles the unate direction at incidence
`(e,v)` by `r_v`. Complementing output `e` toggles all directions of gate `e`
by `q_e`. Thus the transformed direction is

```text
d'(e,v)=d(e,v) XOR r_v XOR q_e = 0
```

by (1). Hence every transformed incidence is nondecreasing. QED.

### Lemma 3.2 — range equivalence

Let `R(C)` and `R(C')` denote the two ranges. Then

```text
y in R(C)  iff  y XOR q in R(C').
```

**Proof.** `x -> z=x XOR r` is a bijection of the domain and
`y -> y XOR q` is a bijection of the codomain. The defining identity for `C'`
therefore transports the range exactly. QED.

### Theorem 3.3 — deterministic polynomial avoidance

If a positive-surplus connected component of an `NC0_3` circuit is
switching-balanced unate, a missing output for the whole circuit is
constructible in deterministic polynomial time.

**Proof.** Recognize and solve (1) by Lemma 2.2. By Theorem 3.1 switch the
component to a monotone `NC0_3` circuit with the same numbers `n,m`, hence
`m>n`. Kuntewar--Sarma (APPROX/RANDOM 2025) give a deterministic
polynomial-time avoider for monotone `NC0_3` for every `m>n`. Apply their
algorithm to obtain `y'` outside `R(C')`, map back to `y=y' XOR q` using
Lemma 3.2, and fill outputs outside the selected connected component
arbitrarily. Any full input realizing the completed word would realize `y` on
the selected component, contradiction. QED.

The published monotone algorithm is used as a black box; V98 does not re-claim
its Turan theorem.

## 4. Strict irreducible nonmonotone family

### Theorem 4.1

For every `N>=5` there is a connected exact-stretch `NC0_3` circuit with

```text
N inputs,
N+1 outputs,
lambda=N
```

under the V97 deterministic peeling rules, such that the raw circuit is
nonmonotone but is switching-balanced unate.

**Construction.** Use supports `S_i={i,i+1,i+2} mod N`, `i=0,...,N-1`, and one
extra copy of `S_0`. Let `r_0=1`, `r_i=0` for `i>0`, `q_e=0` for all `e`, and
define every local output by

```text
g_e(x)=MAJ_3( x_v XOR r_v : v in S_e ).
```

Every gate has essential arity three. Each input lies in at least three
supports, the incidence graph is connected, and there is no constant or unary
output. Therefore V97 performs no unused-input, leaf-pair, constant, or unary
reduction, so `lambda=N`.

Any gate incident to input zero is decreasing in that coordinate, so the raw
circuit is nonmonotone. Its incidence directions satisfy
`d(e,v)=r_v XOR q_e`, hence the component is switching-balanced and Theorem 3.3
solves it in polynomial time. QED.

This proves a strict extension of the *raw monotone label class* on irreducible
large kernels. It is intentionally not phrased as a novelty claim: the family
is coordinate-isomorphic to a monotone circuit.

## 5. A support-only loose-X obstruction

### Construction 5.1

Fix `ell>=3` and write `L=2*ell`. Start with cycle vertices
`v_0,...,v_{L-1}`. For every `i` except `0,3`, add a private vertex `p_i` and
let `e_i={v_i,v_{i+1},p_i}`. For `i=0,3`, replace the private vertices by one
shared vertex `w`:

```text
e_0={v_0,v_1,w},
e_3={v_3,v_4,w}.
```

Indices on the `v_i` are modulo `L`. The cycle edges form an even Berge cycle,
while `e_0` and `e_3` are nonadjacent opposite-parity edges with the additional
intersection `w`; this is the simple loose-X source used by V98.

Label every `e_i` by parity of its three inputs.

### Theorem 5.2 — parity-labeled loose X is surjective

The map `{0,1}^{V(X)} -> {0,1}^{E(X)}` induced by these parity gates is
surjective for every `ell>=3`.

**Proof.** Let arbitrary target bits be `y_0,...,y_{L-1}`. Set

```text
w=0,
v_0=y_0,
v_3=y_3,
v_i=0 for all other i.
```

Then the special parity equations on `e_0` and `e_3` already equal `y_0` and
`y_3`. For each other edge choose

```text
p_i = y_i XOR v_i XOR v_{i+1}.
```

Its parity is then exactly `y_i`. Thus every target edge coloring is induced by
a vertex coloring. QED.

### Corollary 5.3

The existence of a loose-X support does not, by itself, imply a forbidden edge
coloring for arbitrary essential ternary gate labels. This is a label
obstruction, not a hardness result.

## 6. Irreducible exact-stretch embedding

### Lemma 6.1

The parity-labeled loose X from Section 5 can be embedded in a connected
exact-stretch parity circuit that survives every V97 peeling rule.

**Construction.** The loose X has `2L-1` inputs and `L` distinguished outputs.
For each private `p_i`, add one essential parity gate on
`{p_i, v_{i+2}, v_{i+4}}`, and add two more parity gates
`{v_0,v_2,w}`, `{v_1,v_4,w}`. There are exactly `L` added outputs, hence

```text
m=2L=(2L-1)+1=n+1.
```

Every formerly private input now has degree two; cycle vertices already had
degree two in the X; `w` has degree at least two. All gates remain essential
ternary, and the component remains connected. Therefore no V97
unused/degree-one/constant/unary rule applies.

The distinguished X map remains surjective because adding outputs does not
change the functions on the distinguished edge set. QED.

The entire parity host is globally easy by linear algebra. Its only purpose is
to show that the local Turan structure plus arbitrary labels is insufficient,
even inside a V97-irreducible positive-surplus host.

## 7. Executable audit

The primary audit verifies:

```text
256 ternary truth tables,
218 essential ternary tables,
72 essential ternary unate tables,
strict family N=5,...,10,
parity loose-X lengths 6,8,10,12,
0 switching/range-transport failures,
0 loose-X target-realization failures.
```

For the smallest parity host (`ell=3`) brute force gives range size `1024` from
`2^11=2048` inputs into `2^12` output words, as expected for a non-surjective
exact-stretch circuit.

The finite audit supports the implementation only; Theorems 3.1, 3.3, 4.1,
5.2, and Lemma 6.1 are symbolic.

## 8. Boundary

V98 does not classify non-unate ternary labels, does not prove that every
irreducible kernel contains a switching-balanced positive-surplus component,
does not improve the unrestricted Huang--Li--Zhong exponent, and does not
resolve P versus NP.
