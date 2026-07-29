# V53 direction change — from NC⁰₄ to NC⁰₃

The initial V53 context proposed searching for growing syndrome degree inside `NC⁰₄`. Rafael challenged that target using the published hierarchy:

- `NC⁰₂-Avoid` has a polynomial-time algorithm;
- stretch-one `NC⁰₃-Avoid` remains open;
- important explicit-construction problems already reduce to `NC⁰₄-Avoid`;
- cryptographic work gives evidence against overly general deterministic Avoid algorithms.

The criticism was correct in its main strategic conclusion. The best risk/return target for the syndrome method is `NC⁰₃`, not `NC⁰₄`.

## Bibliographic refinements

Two qualifications were added during verification:

1. The Ilango–Li–Williams barrier concerns general Avoid under cryptographic assumptions; it is not a theorem that directly rules out a polynomial algorithm for stretch-one `NC⁰₃-Avoid`.
2. Monotone `NC⁰₃-Avoid` is now known to be polynomial-time solvable. Therefore an `AND₃` family with high syndrome degree is a barrier to the **syndrome method**, not evidence of Avoid hardness.

## New V53 question

The revised falsifiable question became:

> Can a stretch-one `NC⁰₃` image require polynomial identities of unbounded degree, even though the underlying Avoid instance may be easy by another method?

V53 answers yes, with a logarithmic lower bound from union-free high-girth hypergraphs.

## Methodological lesson

A negative result against one certificate family can be valuable on an open problem only when it is positioned precisely:

```text
high syndrome degree
    does not imply
hard Range Avoidance.
```

It says that progress on `NC⁰₃-Avoid` must combine or replace constant-degree global identities with other tools such as Turán-type structure, recursive elimination, hitting sets, pseudodeterminism, or interactive counting.
