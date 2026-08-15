# Laboratory V99 — unbalanced singleton cores and signed-majority X dichotomy

## 1. Ternary unate NPN boundary

After essential-support normalization, there are 218 ternary Boolean truth
tables that depend on all three inputs. Exactly 72 are unate. Under NPN
equivalence those 72 tables split into three orbits:

```text
canonical 0x01   size 16   singleton core (AND/OR/NAND/NOR of literals),
canonical 0x07   size 48   x AND (y OR z) core and its NPN images,
canonical 0x17   size  8   MAJ_3 of literals.
```

The finite orbit census is only bookkeeping. The promoted mathematical targets
below are symbolic and hold for infinite circuit/X families.

## 2. Singleton-core orientation

Let `g_e` be an essential local gate whose NPN orbit is the singleton core.
Exactly one of `g_e^{-1}(1)` and `g_e^{-1}(0)` has size one. Choose an output
orientation bit `q_e` such that

```text
h_e = g_e XOR q_e
```

has exactly one satisfying local assignment `alpha_e`. Therefore

```text
h_e(x)=1  iff  x_v = alpha_e(v) for every v in supp(e),
```

so `h_e` is a conjunction of signed literals.

### Lemma 2.1 — conflict certificate

Suppose two oriented singleton-core gates `h_e,h_f` share an input `v` but

```text
alpha_e(v) != alpha_f(v).
```

Then a missing output is constructible in linear time: request oriented target
bits `h_e=h_f=1` and set all other target bits arbitrarily.

**Proof.** Any input realizing both target ones would have to assign `v` both
`alpha_e(v)` and `alpha_f(v)`, contradiction. Mapping every oriented target bit
back by XOR with `q` gives a missing word for the original circuit. QED.

### Lemma 2.2 — conflict-free switching

If no such conflict exists, then there is one demanded bit `r_v` for every
active input `v`, common to every incident gate. The coordinate change

```text
z_v = 1 iff x_v = r_v
```

turns every oriented local gate into the positive conjunction of its essential
inputs.

**Proof.** Every gate is the conjunction of literals `x_v=r_v`; the displayed
bijection maps each such literal to `z_v=1`. QED.

### Theorem 2.3 — singleton-core range avoidance is in P

Let a positive-surplus connected component of an `NC0_3` circuit have only
singleton-core essential gates. A missing output for the whole circuit is
constructible in deterministic polynomial time.

**Proof.** Orient all gates as above and scan incidences for a conflict. If one
is found, Lemma 2.1 gives the missing word immediately. Otherwise Lemma 2.2
switches the component to a monotone `NC0_3` circuit without changing its
numbers of inputs or outputs. Since the component has `m>n`, apply the
Kuntewar--Sarma deterministic polynomial-time monotone `NC0_3` avoider, undo
the output orientation, and fill outputs outside the component arbitrarily.
QED.

### Corollary 2.4

`NC0_3-Avoid[m>n]` is in deterministic polynomial time for the class in which
every essential local gate is in the singleton NPN orbit.

## 3. Strict extension beyond V98 balance

### Theorem 3.1

For every `N>=5` there is a connected exact-stretch singleton-core circuit with

```text
N inputs,
N+1 outputs,
V97 lambda = N,
```

that is not switching-balanced in the V98 sense but has an immediate V99
conflict certificate.

**Construction.** Use cyclic supports

```text
S_i={i,i+1,i+2} mod N,  i=0,...,N-1,
```

and one extra copy of `S_0`. Put positive `AND_3` on every cyclic support. On
the duplicate use

```text
(NEG x_0) AND x_1 AND x_2.
```

All gates are essential ternary. Every input has incidence degree at least
three, the support component is connected, and there is no constant/unary/leaf
reduction, hence `lambda=N`.

The original `S_0` gate demands `x_0=1` when its oriented output is one, while
the duplicate demands `x_0=0`, so Lemma 2.1 applies. The V98 balance equations
are inconsistent: the positive `S_0` gate forces the same switching potential
on `x_0,x_1,x_2`, while the duplicate has direction pattern `(1,0,0)` and
forces `x_0` to differ from `x_1,x_2`. QED.

Thus V99 strictly enlarges the raw unate class solved without enumerating the
V97 kernel.

## 4. Signed-majority simple X

Let `L=2 ell >= 6`. Define the simple `X_L` with cycle vertices
`v_0,...,v_{L-1}`. Edges `e_0` and `e_3` have the extra common vertex `w`:

```text
e_0={v_0,v_1,w},
e_3={v_3,v_4,w}.
```

Every other cycle edge

```text
e_i={v_i,v_{i+1},p_i}
```

has its own private third vertex `p_i`. This is a 3-uniform linear
`X_{2 ell}` of the type used in the Kuntewar--Sarma majority argument.

A signed-majority label is

```text
MAJ_3(x_a XOR s_a, x_b XOR s_b, x_c XOR s_c).
```

Because

```text
NOT MAJ_3(a,b,c)=MAJ_3(NOT a,NOT b,NOT c),
```

output complementation is the same as toggling all three local incidence signs.
Input complementation toggles every incidence sign at that input. Hence
input/output switching acts exactly as vertex switching on the bipartite
incidence graph.

### Lemma 4.1 — four switching classes

The incidence graph of `X_L` is connected, has `3L-1` vertices and `3L`
incidences, hence cycle rank two. Its signings modulo input/output switching
therefore form four classes, naturally `F_2^2`.

Choose the following two cycle parities:

1. the parity around the base Berge cycle;
2. the parity around the short chi cycle
   `w-e_0-v_1-e_1-v_2-e_2-v_3-e_3-w`.

Every switching class has a representative in which all incidence signs are
positive except possibly

```text
(e_0,v_0) = B,
(e_0,w)   = A,
```

with `(B,A) in {0,1}^2`. The four pairs are distinct by the two displayed cycle
parities. QED.

## 5. Transfer lemma for private majority edges

Fix a target bit on a positive majority edge with two cycle endpoints `a,b` and
a private third input `p`.

For target zero, some choice of `p` works unless `(a,b)=(1,1)`. For target one,
some choice of `p` works unless `(a,b)=(0,0)`. Therefore the endpoint relations
are the Boolean matrices

```text
R0 = [[1,1],
      [1,0]],

R1 = [[0,1],
      [1,1]].
```

Matrix multiplication below is over the Boolean semiring.

### Lemma 5.1 — path collapse

Let a private-edge path carry target word `t`.

- If `t` contains two equal adjacent bits, its endpoint relation is the universal
  matrix `J`.
- If `t` is alternating and has even positive length, its relation is

```text
P01 = [[1,1],[0,1]]   when t starts with 0,
P10 = [[1,0],[1,1]]   when t starts with 1.
```

**Proof.** Direct Boolean multiplication gives

```text
R0 R0 = R1 R1 = J,
J Rb = Rb J = J,
R0 R1 = P01,
R1 R0 = P10,
P01^2=P01,
P10^2=P10.
```

The claims follow by splitting at an equal adjacent pair or grouping an
alternating even word into two-letter blocks. QED.

The two private paths in `X_L` have even lengths: edges `e_1,e_2`, and edges
`e_4,...,e_{L-1}`. Thus each collapses to one of only

```text
J, P01, P10.
```

## 6. Exact signed-majority X dichotomy

After Lemma 5.1 the entire target-realizability question depends only on the two
path relations, target bits `y_0,y_3`, and five boundary variables
`v_0,v_1,v_3,v_4,w`.

### Lemma 6.1 — exact boundary table

For canonical sign class `(B,A)`, the only infeasible boundary types are

```text
(B,A)   infeasible (short,long,y_0,y_3)
------------------------------------------------
(0,0)   (P01,P10,1,0), (P10,P01,0,1)
(0,1)   none
(1,0)   none
(1,1)   none
```

If either path relation is `J`, every boundary type is feasible.

**Proof.** Substitute the three possible path relations into the two special
constraints

```text
MAJ(v_0 XOR B, v_1, w XOR A)=y_0,
MAJ(v_3,       v_4, w      )=y_3.
```

There are only five Boolean boundary variables. Exhausting their 32 assignments
gives the table above; equivalently each row is checked by direct inspection of
the displayed two majority equations and the two 2-by-2 endpoint relations.
This is a constant symbolic boundary calculation independent of `L`. QED.

### Theorem 6.2 — switching-class dichotomy

For every even `L>=6`, a signed-majority simple `X_L` has:

```text
balanced switching class: exactly 2 missing edge words,
nonzero switching class:  no missing edge word (surjective map).
```

In the all-positive representative, the two missing words are precisely

```text
010101...01,
101010...10.
```

For an arbitrary balanced signing, output switching transports this unordered
pair to the two missing words of that signing.

**Proof.** In class `(0,0)`, Lemma 6.1 can fail only when both private paths are
alternating with opposite relation types and `(y_0,y_3)` is the corresponding
opposite pair. Since both path lengths are even, these two boundary cases are
exactly the two globally alternating edge words. Every other target has a
boundary realization and then private third inputs are chosen edge by edge.

For each of `(0,1),(1,0),(1,1)`, Lemma 6.1 has no failing boundary type, so
every target edge word is realizable. Finally, switching is a bijection on the
input cube together with coordinate complements on the output cube, so it
preserves range cardinality and surjectivity. QED.

### Corollary 6.3 — exact local obstruction

The Kuntewar--Sarma alternating-coloring certificate for ordinary `MAJ_3` is
not merely fragile under arbitrary signed literals: on each nontrivial
switching class of this simple `X`, **no** forbidden edge coloring exists at
all. Thus any range-avoidance extension to unbalanced signed-majority kernels
must use a different/larger substructure or global information.

This is not a hardness theorem for signed-majority circuits.

## 7. Executable audit

The primary implementation verifies:

```text
256 ternary masks,
218 essential ternary masks,
72 essential-unate masks,
three unate NPN orbits of sizes 16,48,8,
strict singleton family N=5,...,10,
zero strict-family missing-word failures,
V98 balance rejection on every strict-family row,
exact constant boundary table for all four signed-MAJ classes,
all output words for L=6,8,10,12,14 through the transfer system,
brute-force equality of transfer and full range for L=6.
```

The length audit is regression evidence. The infinite-family claims are the
symbolic lemmas and theorems above.

## 8. Boundary

V99 does not solve the 48-table unate NPN orbit represented by
`x AND (y OR z)`, does not solve all unate `NC0_3-Avoid`, does not improve the
unrestricted Huang--Li--Zhong exponent, and does not resolve P versus NP.
