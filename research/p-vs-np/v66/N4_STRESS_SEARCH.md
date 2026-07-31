# Four-variable deterministic stress search

Canonical ternary cells are lifted to ordered three-variable supports inside a four-variable cube and deduplicated. This produces 352 global gate variants:

```text
84 fibers of size 6
240 fibers of size 8
28 fibers of size 10
```

Using seed `660066`, the verifier samples exactly 50,000 ordered five-gate systems. The number of consistent complete branches is:

```text
0 : 32,433
1 : 14,200
2 :  2,841
3 :    433
4 :     84
5 :      9
```

Observed maxima:

```text
consistent complete branches : 5
L_aff                       : 14
G_aff                       : 23
```

The exact witness indices are stored in `RESULTS.json` and regenerated from deterministic variant ordering.

This is not an exhaustive n=4 theorem. It is a fixed-seed falsification and regression experiment. The absence of a larger example in 50,000 samples does not establish polynomial branching or rule out exponential families.
