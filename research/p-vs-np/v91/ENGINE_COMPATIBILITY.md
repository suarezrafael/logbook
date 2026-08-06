# V91 inherited-engine compatibility verdict

## Engine contract inherited from V74–V90

For a supplied local map and a support branch decomposition of width `k`, the laboratory can perform exact preimage/prefix counting and remote-point construction with parameter dependence containing

```text
2^{O(k^2)} poly(n,m)
```

plus the committed arithmetic-DAG and composition costs. The proved polynomial regime is

```text
k = O(sqrt(log m)).
```

V87 also records relevant families with support branchwidth linear in the natural size parameter. Substituting linear `k` into the current decomposition term is not a saving over exhaustive methods.

## Requirement matrix

| Transfer requirement | Required value | Inherited value | Verdict |
|---|---|---|---|
| input coverage | every circuit/list in one named standard class | structurally promised low-width local maps | fail |
| output guarantee | total canonical avoided string, or the theorem's exact single-valued model | deterministic output only after the low-width promise is met | fail |
| representation | theorem-native Missing-String or SAT/#SAT encoding | local multi-output support representation | missing reduction |
| size range | theorem-specific polynomial/subexponential/list range | no filled standard-class range | fail |
| runtime saving | theorem-specific quantified saving | FPT in `k`; polynomial only at `O(sqrt(log m))` | fail |
| high-width branch | another outcome that completes a win-win | linear-width obstruction only | fail |
| barrier status | identified route outside applicable oracle/algebraic barrier | none identified | fail |

## Formal no-go

This is a no-go for **direct insertion of the present engine**, not a lower bound against future algorithms.

Suppose a selected transfer theorem quantifies over every input in a class `C`. The current algorithm has a proved guarantee only on the subclass

```text
C_low = {F in C : support-branchwidth(F)=O(sqrt(log m))}.
```

Unless one proves either `C=C_low` or a total procedure for `C\C_low`, the universal premise of the transfer is false. V87's linear-width families rule out the first equality for the inherited local-map universe. No procedure for the complement is known. Therefore the theorem cannot be instantiated.

## First required improvement

The next useful object is not a better constant in `2^{O(k^2)}`. It is a **completion theorem**:

```text
On every input F, either
  A. produce a branch decomposition in the polynomial-width regime and run
     the current remote-point algorithm, or
  B. from a certified high-width structure, produce the same theorem-native
     canonical avoided string (or another outcome explicitly accepted by a
     checked transfer theorem).
```

Only after such a total win-win exists do constant optimization, depth conversion, or Missing-String communication bounds become transfer-relevant.
