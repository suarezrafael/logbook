# V89 theorem packet — eight-row addressing beyond primal four-colorability

## Setup

Let

```text
H=(S_1,...,S_m),  S_i={u_i,v_i,w_i} subseteq [n]
```

be a simple ternary support family. For `k` target rows, a witness family assigns
each input variable a bit pattern of length `k`. The local address at output
`i` and target row `a` is the three-bit word formed by the patterns on
`S_i`.

The V88 collision normal form says that a target matrix is coverable exactly
when every pair of rows requesting different output bits receives different
local addresses on that output.

## Theorem 1 — target-independent injective addressing

Suppose there are witness patterns for which the address map is injective on
all `k` rows for every support. Then every binary target matrix with `k` rows
is coverable.

### Proof

No local address is repeated, so every requested target bit may be assigned to
its own truth-table entry. Extend each partially assigned ternary truth table
arbitrarily to the unobserved addresses. The outputs are independent. `QED`

This is stronger than target-by-target coverability: one fixed witness family
works for every target matrix of that row count.

## Theorem 2 — the affine basis construction

Let

```text
a_v in F_2^3 \ {0}
```

for every variable `v`, and suppose that for every support `{u,v,w}` the three
vectors `a_u,a_v,a_w` form a basis of `F_2^3`.

Index eight target rows by `x in F_2^3` and define

```text
p_v(x) = <a_v,x> mod 2.
```

For support `{u,v,w}`, the address map is

```text
x -> (<a_u,x>, <a_v,x>, <a_w,x>).
```

Its matrix has rows `a_u,a_v,a_w`, hence is invertible. Therefore it is a
bijection of `F_2^3`; all eight local addresses occur exactly once.

Consequently every target matrix with at most eight rows is coverable.

## Corollary 3 — primal four-colorability is sufficient

The four vectors

```text
001, 010, 100, 111
```

form a cap in the Fano plane: every three of them are linearly independent.

A proper four-coloring of the primal graph assigns three distinct colors to
every ternary support, since each support induces a triangle. Replacing the
four colors by the four cap vectors gives the basis coloring required by
Theorem 2.

Thus primal four-colorability implies coverability of every target matrix with
at most eight rows.

## Theorem 4 — exact ceiling of the uniform injective mechanism

A ternary support has only eight local addresses. Hence no fixed witness family
can be injective on nine target rows at even one active output.

Conversely, Theorem 2 attains all eight addresses whenever a basis coloring
exists. Therefore eight is the exact ceiling for target-independent injective
addressing on ternary supports.

This does **not** rule out target-dependent coverage arguments for nine or more
rows. It identifies precisely where the uniform mechanism stops.

## Theorem 5 — uniform color tables are binary codes

Suppose a proper primal coloring uses `j` colors and one assigns a binary
length-`k` pattern to every color. Requiring every triple of color patterns to
distinguish all `k` columns is equivalent to requiring that every two columns
of the resulting `j x k` table agree in at most two coordinates.

Equivalently, the `k` columns form a binary code of length `j` and minimum
distance at least `j-2`.

The committed exact census gives:

```text
j = 3: maximum k = 8
j = 4: maximum k = 8
j = 5: maximum k = 4
j = 6: maximum k = 4
j >= 7: maximum k = 2
```

For `j=4`, the eight even-parity words form the `[4,3,2]` code and yield
`OA(8,4,2,3)`.

## Finite audit and correction to the proposed bridge

The proposed four-colorability bridge does not apply to the existing controls.

Exact primal chromatic numbers are:

```text
V80 controls:        6, 5, 5
V87 sample controls: 5, 6, 5, 5, 5, 5, 5, 6
```

Several controls contain explicit `K_5` or `K_6` primal cliques.

Nevertheless, all eleven support families admit an `F_2^3` basis coloring.
The affine construction therefore supplies an eight-row injective address
family for every committed control. The vector construction is strictly more
general than the four-color cap construction.

## Asymptotic boundary

The finite basis-coloring audit does not prove that the V87 random support
model is basis-colorable with high probability.

In particular, random-graph chromatic results for `G(n,d/n)` cannot be applied
directly to the primal graph. A V87 support inserts a correlated triangle, so
the primal graph is a random triangle graph rather than an Erdős–Rényi graph
with independent edges.

A nine-row constructor lower bound requires an asymptotic theorem showing that
a positive-probability V87 resistant family also admits the basis coloring (or
another eight-row injective address system). That bridge remains open in this
candidate.

## Research budget

This front has two laboratories, V89 and V90, to produce one of:

1. a superconstant support-only constructor lower bound;
2. a constructive `O(n^(1/3))` target list;
3. a rigorous asymptotic basis-addressing theorem that raises the lower bound
   from four to nine and materially changes the constructor landscape.

If none occurs by the end of V90, the `Eval_H` constructor front closes and the
laboratory returns to the rigidity/average-case bridge or proof complexity.

## Nonclaims

This packet does not prove that the V87 model is four-colorable or
basis-colorable with high probability, does not raise the promoted universal
list lower bound to nine, does not construct an avoided target list, does not
solve unrestricted `NC0_3-Avoid`, and does not resolve `P` versus `NP`.
