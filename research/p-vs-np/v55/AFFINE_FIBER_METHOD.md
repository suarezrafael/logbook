# Affine-fiber method — algorithmic specification

## Input

A Boolean circuit with `n` inputs and `m` ternary outputs. For every gate, choose an output value whose local fiber is affine over `GF(2)`.

## Algorithm

1. Compute affine equations for each active fiber.
2. Lift each local equation to the `n` global variables plus one constant coordinate.
3. Group the lifted rows by output gate.
4. Compute the total row rank.
5. Find a gate whose removal does not reduce the rank.
6. Reduce the remaining gates to a small set whose rows still span that gate's row space.
7. Request the selected gates to be active and the redundant gate to be inactive.
8. Undo each gate's output orientation.

## Certificate

The serialized certificate records the redundant gate, implying gates, lifted rows, ranks, orientations, and missing target. A verifier checks row-space containment and, on finite audit cases, enumerates the complete input cube.

## Thresholds

- arbitrary affine-fiber mixture: `m>n+1`;
- antipodal-pair NPN orbit `0x18`: `m>n`;
- parity NPN orbit `0x69`: `m>n` by affine output rank.

The thresholds are sufficient and not claimed necessary.
