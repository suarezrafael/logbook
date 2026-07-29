# P versus NP Laboratory V54

## Quartic separators, forcing cores, and a formal correction to V53

**Scientific status:** internally verified theorem package, not peer reviewed. V54 corrects a false implication in V53. It does not solve general `NC0_3-Avoid`, prove a circuit lower bound, or resolve P versus NP.

## Main result

For a pure `AND_k` circuit with more outputs than inputs, the support hypergraph has a nonempty 2-core. A core edge and at most one witness edge per input variable produce

```text
Q=(1-Y_e) product_f Y_f,
```

a degree-at-most-`k+1` polynomial vanishing on the range and rejecting an explicit target.

For `AND3`, this gives a quartic target separator over every field.

## V53 correction

The V53 implication

```text
large incidence girth => t-union-free
```

was false because nested equal-union collisions do not create cycles. The V53 logarithmic syndrome-degree family is retracted. The original union-free-to-injectivity theorem remains correct.

## Nonmonotone extension

The forcing-core method extends to the NPN orbit of `AND3`, consisting of ternary gates with a singleton output fiber, through signed input literals.

## Reproduce

```bash
python verify.py
python verify_independent.py
```

Expected:

```text
V54 primary verification passed:
  386 exhaustive n=5 positive-stretch AND3 hypergraphs;
  600 random larger AND3 hypergraphs;
  exact sepdeg UF2=3, UF3=4;
  250 coherent and 250 arbitrary signed-minterm circuits;
  V53 girth implication counterexample verified; zero failures.

V54 independent verification passed:
  386 exhaustive n=5 hypergraphs rebuilt;
  certificate degree distribution {3: 359, 4: 27};
  acyclic nested-union counterexample rebuilt; zero failures.
```
