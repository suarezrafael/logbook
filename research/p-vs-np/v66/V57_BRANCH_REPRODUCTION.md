# V57 affine-cell branch reproduction

The five V57 blocks from the V64 normative specification are evaluated on all 16 assignments. Each six-point block has exactly three disjoint partitions into two nonempty affine cells. Hence there are

```text
3^5 = 243 partition systems
```

and every system has 32 syntactic complete cell branches.

## Exact result

For every one of the 243 partition systems:

- exactly one complete branch has nonempty intersection;
- the other complete branches are inconsistent;
- the surviving branch is a consistent affine system and therefore receives the V56 certificate.

The adaptive optimal-tree distribution, written as

```text
L_aff / internal nodes / D_aff / G_aff : number of systems
```

is:

```text
8/7/5/11 :   3
8/7/5/12 :  34
8/7/5/13 :  75
8/7/5/14 : 124
9/8/5/12 :   1
9/8/5/15 :   6
```

Thus the branch-level obstruction is not the existence of an affine certificate at a leaf. In this gadget, the union-level block irredundancy disappears after a complete cell choice, and inconsistency pruning reduces 32 branches to 8 or 9 leaves.

This is a property of the exact V57 gadget and its 243 affine partitions. It does not establish a general polynomial-size branching tree.
