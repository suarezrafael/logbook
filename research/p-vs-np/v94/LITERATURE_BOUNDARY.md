# V94 literature boundary

## Huang–Li–Zhong, ITCS 2026

Shengtang Huang, Xin Li, and Yan Zhong, *Range Avoidance and Remote Point: New
Algorithms and Hardness*, ITCS 2026, LIPIcs 362:79.

Their local-circuit range-avoidance algorithm gives, for `NC0_k-Avoid[n,n+1]`,

```text
O(n * 2^(((k-2)/(k-1))*n)).
```

At `k=3` this is `O(n*2^(n/2))`. V94 does not improve this runtime. It isolates
a reason that a much stronger subgoal — polynomial exact comparison for every
arbitrary prefix — is not a plausible generic replacement unless `P=PP`.

## Fenner–Fortnow–Kurtz, JCSS 1994

Stephen A. Fenner, Lance J. Fortnow, and Stuart A. Kurtz, *Gap-definable
counting classes*, JCSS 48(1):116–148, 1994.

V94 uses the standard facts that `GapP` is the subtraction closure of `#P` and
that `PP` is characterized by the sign of GapP functions. This calibrates both
membership of child-count comparison in PP and the source comparison problem.

## Creignou–Hermann, Information and Computation 1996

Nadia Creignou and Miki Hermann, *Complexity of Generalized Satisfiability
Counting Problems*, Information and Computation 125(1):1–12, 1996.

Their Boolean generalized-counting dichotomy places affine relation languages
in polynomial time and non-affine languages on the #P-complete side. V94's
affine branch is deliberately a concrete circuit/prefix implementation of the
tractable control. The explicit V94 PP-hard comparison compiler is proved
directly rather than inferred from #P-completeness, because the reduction type
and preservation of a pairwise comparison matter.

## Akmal–Williams, FOCS 2021

Shyan Akmal and Ryan Williams, *MAJORITY-3SAT (and Related Problems) in
Polynomial Time*, FOCS 2021.

They show that Majority-kSAT is polynomial-time for every fixed clause width.
This is an important warning against the slogan “bounded-width counting
threshold implies PP-hardness.” V94 does not make that claim. Its hard object
compares **two independently selected conditioned counts** encoded in one
circuit, rather than comparing one bounded-width formula's count with a fixed
fraction of all assignments.

## Exact boundary of the V94 theorem

Proved internally:

```text
arbitrary supplied prefix + fixed finite arity<=3 gate language + m=n+1
    -> exact child comparison is PP-complete.
```

Not proved:

```text
V92-generated canonical prefix
    -> PP-hard comparison,

NC0_3-Avoid[n,n+1]
    -> PP-hard search,

polynomial avoided-output construction
    -> polynomial arbitrary-prefix comparator.
```

Those missing implications are intentionally excluded from the V94 statement.
