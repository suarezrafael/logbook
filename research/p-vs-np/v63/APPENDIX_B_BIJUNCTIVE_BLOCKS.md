# Appendix B — orbit-constrained bijunctive block irredundancy

## Five-block gadget

Use variables `x0,x1,x2,x3` and the five blocks

```text
B1 = ¬x0 ∧ (¬x1 ∨  x2)
B2 = ¬x0 ∧ ( x1 ∨ ¬x2)
B3 = ¬x0 ∧ (¬x1 ∨  x3)
B4 = ¬x0 ∧ ( x1 ∨ ¬x3)
B5 = ¬x0 ∧ (¬x2 ∨ ¬x3)
```

Each block is the selected three-point fiber of an essential ternary gate in the NPN orbit of `0x07`.

The local truth-table masks in the verifier convention are

```text
0x51, 0x45, 0x51, 0x45, 0x15,
```

and all lie in the 48-element NPN orbit of `0x07`.

## Collapsed 2-CNF

After duplicate copies of the common unit clause are removed, the conjunction is

```text
¬x0
∧ (¬x1 ∨  x2)
∧ ( x1 ∨ ¬x2)
∧ (¬x1 ∨  x3)
∧ ( x1 ∨ ¬x3)
∧ (¬x2 ∨ ¬x3).
```

Its unique satisfying assignment is

```text
x0x1x2x3 = 0000.
```

## Complete-block irredundancy witnesses

For every block, the other four blocks are satisfiable while the removed block is false.

| Removed block | Witness |
|---|---|
| `B1` | `0101` |
| `B2` | `0010` |
| `B3` | `0110` |
| `B4` | `0001` |
| `B5` | `0111` |

Therefore no complete gate block is entailed by the other four.

## Clause-level irredundancy witnesses

The six-clause collapsed formula is also clause-irredundant.

| Removed clause | Witness |
|---|---|
| `¬x0` | `1000` |
| `¬x1 ∨ x2` | `0101` |
| `x1 ∨ ¬x2` | `0010` |
| `¬x1 ∨ x3` | `0110` |
| `x1 ∨ ¬x3` | `0001` |
| `¬x2 ∨ ¬x3` | `0111` |

This clause-level fact uses established IES terminology and is not claimed as a new concept.

## Minimality scope

Under the search convention of essential ternary gates with three distinct inputs:

- `n=3,m=4` was exhaustively checked over `249900` multisets from the orbit;
- every consistent orientation by the small fibers had a redundant block;
- the `n=4,m=5` gadget is therefore minimal in that finite searched universe.

The minimality statement is computer-assisted and scoped to that convention.

## Infinite stretch-one family

For every `k>=0`, take the direct sum of the five-block gadget with `k` copies of a balanced three-variable, three-block gadget using masks

```text
0x07, 0x0b, 0x0d.
```

The result has

```text
n = 4+3k,
m = 5+3k = n+1,
```

is jointly satisfiable, and remains completely block-irredundant.

## Consequence

The direct affine-style implication is false:

```text
m>n and consistent bijunctive blocks
    => some complete block is implied by the others.
```

It fails at minimum positive stretch and inside one ternary NPN orbit.

## Boundary and nonclaims

This obstruction rules out only fixed-orientation complete-block redundancy. It does not rule out:

- adaptive reorientation;
- branching between cells;
- inconsistency certificates;
- more refined implication-graph measures;
- algorithms specific to the remaining bijunctive orbits;
- general polynomial-time `NC0_3-Avoid`.
