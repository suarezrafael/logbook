# P versus NP Laboratory V53

> **Superseded and corrected by V54.** The V53 union-free substitution lemma remains valid. The claimed implication from incidence girth to full `t`-union-freeness, and the derived stretch-one `Omega(log n)` syndrome-degree family, are retracted. They failed because nested equal-union collisions need not create cycles.

## Valid result preserved

For a 3-uniform hypergraph `H=(V,E)`, define

```text
C_H(x)_e = product_{v in e} x_v.
```

If all edge subfamilies of size at most `t` have distinct vertex unions, then substituted output monomials through degree `t` become distinct input monomials. Therefore no nonzero output polynomial of degree at most `t` vanishes on the image, over any field.

The finite examples remain correct:

- UF2 has exact syndrome degree 3;
- UF3 has exact syndrome degree 4.

## Retracted result

Incidence girth alone does **not** imply full `t`-union-freeness. An edge may be contained in the union of other edges without producing any incidence cycle. V54 proves a stronger opposite ceiling for positive-stretch pure `AND3`: the support hypergraph has a nonempty 2-core and therefore an explicit vanishing relation and missing target of degree at most four.

Use `research/p-vs-np/v54` as the current scientific record.

## Reproduce preserved finite checks

```bash
python verify.py
python verify_independent.py
```

These scripts still validate the two finite union-free examples. They do not validate the retracted asymptotic implication.
