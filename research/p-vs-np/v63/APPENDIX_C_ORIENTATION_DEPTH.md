# Appendix C — orientation depth and boundary localization

## Output-image geometry

Let

```text
C:{0,1}^n -> {0,1}^m
```

and let `S=Range(C)`. For an output word `y`, define the fiber formula

```text
F_y(x) = conjunction_i [C_i(x)=y_i].
```

When both fibers of every output gate are bijunctive, each block has a constant-size 2-CNF representation.

The internal boundary of the image is

```text
partial_in(S) = {y in S : exists i, y xor e_i notin S}.
```

For a baseline `b in S`, define orientation depth

```text
rho_S(b) = min_{y in partial_in(S)} d_H(b,y).
```

## Theorem C.1 — redundancy equals an outgoing boundary edge

For `y in S`, block `i` is implied by all other blocks in `F_y` if and only if

```text
y xor e_i notin S.
```

Proof: fixing all other output coordinates to `y` admits exactly the two possible values of coordinate `i`. If the flipped word is absent, every input satisfying the other blocks must also satisfy block `i`; conversely a present flipped word supplies a counterexample to entailment.

## Theorem C.2 — Hamming-ball criterion

For every `r>=0`,

```text
rho_S(b) > r
    iff
B_H(b,r+1) is contained in S.
```

Thus failure to find a boundary point within radius `r` is exactly containment of the radius-`r+1` Hamming ball in the image.

## Theorem C.3 — parameterized deterministic algorithm

Given a bound `d`, enumerate all words at Hamming distance at most `d` from `b`.

For each candidate `y`:

1. solve the 2-CNF formula `F_y`;
2. if unsatisfiable, return `y` as a missing output;
3. if satisfiable, test every complete block for entailment by the others;
4. when block `i` is redundant, return `y xor e_i`.

If `rho_S(b)<=d`, this procedure succeeds.

The running time is

```text
O((sum_{j=0}^d binom(m,j)) * m * poly(n+m)).
```

Equivalently, the running time is `m^{O(d)} poly(n+m)`. For constant `d`, this is polynomial.

## Universal cardinality bound

Since `|S|<=2^n`, let `d` be the least integer with

```text
sum_{j=0}^d binom(m,j) > 2^n.
```

Then

```text
rho_S(b) <= d-1.
```

At minimum stretch `m=n+1`, this gives

```text
rho_S(b) <= floor(n/2).
```

This bound is general but does not yield polynomial time.

## Finite evidence for orbit `0x07`

For homogeneous stretch-one circuits in the orbit `0x07`, oriented by the three-point fibers:

- exact normalized search covers `3<=n<=8`;
- every consistent baseline has depth at most one;
- the V57 twelve normalized obstructions form one variable-isomorphism class;
- all have depth exactly one;
- all 60 single flips succeed;
- after each successful flip, three or four blocks become redundant;
- the V57 direct-sum family also has depth exactly one.

The full exact verifier passed after `126607` DFS nodes.

## Interpretation

The V57 family is a barrier to fixed orientation, not a barrier to depth-one adaptive reorientation.

## Boundary and nonclaims

- No theorem establishes constant depth for all sizes.
- The `n=9` search remains incomplete and is not evidence.
- Exact equivalence to an established solution-graph parameter has not been located.
- The Hamming-ball enumeration algorithm is parameterized, not a polynomial-time algorithm for unbounded depth.
