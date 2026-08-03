# V86 theorem packet

## Theorem 1 — NOR3 destroys constant syndromes on simple ternary supports

Let `H=(S_1,...,S_m)` be a simple 3-uniform support family: every `S_i` has size three and no two supports are equal. Assign to every output the ternary function

```text
NOR3(u,v,w)=1 iff (u,v,w)=(0,0,0).
```

Then the resulting circuit has no nonzero constant output-parity syndrome.

### Proof

Over `F_2`,

```text
NOR3(u,v,w)=(1+u)(1+v)(1+w)
           =1+u+v+w+uv+uw+vw+uvw.
```

The cubic monomial of gate `i` is exactly the product of the three variables in `S_i`. Because the support family is simple, this cubic monomial occurs in no other output. In the XOR of any nonempty selected set of outputs, choose any selected gate `i`; its cubic monomial occurs once and cannot cancel. The selected XOR is therefore nonconstant. `QED`

### Consequence

The V85 C4 theorem is one-way at the support level. A C4 is necessary for nonlinear cancellation between distinct gates, but a support family may contain many C4s and still admit truth tables with no constant syndrome.

## Theorem 2 — asymptotic simultaneous resistance to small Hall and syndrome certificates

At

```text
m=n+ceil(n^(2/3)),
```

for all sufficiently large `n`, there exists a simple 3-uniform support family with no Hall-deficient output set of size at most

```text
n/(16e^2).
```

After assigning `NOR3` to every gate, the resulting circuit has no nonzero constant syndrome.

### Proof

Choose each support independently and uniformly from the 3-subsets of `[n]`. For fixed `s` gates and a fixed variable set of size `t<s`, the probability that every selected support lies inside those variables is

```text
(binom(t,3)/binom(n,3))^s <= (t/n)^(3s).
```

Thus the V80 union-bound calculation applies unchanged and bounds the probability of a Hall-deficient set of size at most `n/(16e^2)` by `8/49`.

The probability of a duplicate support is at most

```text
binom(m,2)/binom(n,3)=O(1/n).
```

For sufficiently large `n`, the sum of these two bad-event bounds is below one. Therefore a simple support family with the required local Hall expansion exists. Apply Theorem 1 to eliminate every nonzero constant syndrome. `QED`

### Missing property

The argument does not prove that the same support family has high support branchwidth. It therefore blocks two certificate mechanisms, not all three.

## Proposition 3 — the three V80 finite controls are not simultaneous obstructions

For the seven-, eight-, and nine-variable V80 examples:

```text
C4 counts:                 15, 17, 18
minimum Hall set sizes:     7,  8,  9
minimum Hall neighborhoods: 6,  7,  8
support branchwidths:       5,  5,  6
```

Under the `NOR3` assignment, their nonconstant ANF ranks are `11`, `12`, and `14`, and all nonzero selector syndromes are nonconstant.

Therefore the syndrome mechanism fails, but both small-neighborhood Hall enumeration and bounded-width exact enumeration remain available.

## Proposition 4 — restriction has no avoidance pullback

There is no general rule converting an output avoided by an input-restricted circuit into an output avoided by the original circuit.

### Proof by example

Let

```text
C(x)=(x,0).
```

After fixing `x=0`, the restricted range is `{(0,0)}`, so `(1,0)` is avoided. The unrestricted range is `{(0,0),(1,0)}`, so the same word is not avoided by `C`. `QED`

## Proposition 5 — width optimization does not approach the V84 balanced-Hall branch

If every balanced output subset Hall-expands, V80 proves

```text
branchwidth >= sigma=m-n.
```

At the target stretch, `sigma=Theta(n^(2/3))`. The V85 polynomial regime is `O(sqrt(log m))`. Hence even improvements to polylogarithmic branchwidth remain asymptotically separated from the balanced-Hall hard branch.

This does not diminish the bounded-width remote-point theorem; it calibrates it as an algorithmic structural result rather than a direct crossing of the lower-bound-sensitive branch.
