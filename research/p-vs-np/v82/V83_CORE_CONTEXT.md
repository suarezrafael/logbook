# V83 core context — degree-three transversal girth

## Frozen input from V82

For every dependent transversal presentation,

```text
h* = min{|N(S)| : |N(S)|<|S|} = transversal girth - 1.
```

Every inclusion-minimal `h*` minimizer is a circuit and has deficiency
exactly one.

The unrestricted girth problem is NP-hard by the published
Colbourn–Elmallah theorem. Presentations of left degree at most two are
bicircular and polynomial-time tractable when the presenting graph is
supplied. The exact degree-three boundary was not settled by the
sources audited in V82.

Parameterized algorithms based on rank, solution size, and field
parameters do not directly yield polynomial time in the target regime,
where rank and girth can grow with `n`.

## Priority one: degree-three exact complexity

Work only on

```text
transversal girth for presentations with left degree <= 3.
```

### Preferred route: hardness gadgets

Start from the verified Colbourn–Elmallah Clique reduction. Identify
every left element whose neighborhood is unbounded and replace that
incidence by a bounded-degree gadget.

A candidate gadget is admissible only if exact finite enumeration
verifies all of the following:

1. intended circuits survive with the predicted size shift;
2. no unintended shorter circuit is introduced;
3. the left degree is at most three;
4. the threshold transformation is polynomially bounded;
5. the reverse direction decodes every short circuit.

Do not call the route complete until both reduction directions and the
threshold accounting are formal.

### Equal-status algorithmic route

A polynomial algorithm exploiting degree three is an equally valid
outcome. It must recover unsupported points of the Minimum `p`-Union
curve and cannot be only a Lagrangian-envelope method.

## Three-iteration stopping rule

Count a focused iteration only when it delivers one of:

- a complete gadget with exhaustive small-instance validation;
- a proved structural lemma eliminating a class of gadgets;
- an algorithmic decomposition theorem with a verified subroutine.

If three such iterations do not close either route, stop the direct
complexity attack and promote an extended census containing:

- sunflower core/petal profiles;
- affine-cell rank or a precise replacement invariant;
- `G*_proj` all-orders growth;
- explicit degree-three expander candidates;
- counterexamples to every proposed monotone inequality.

That census becomes input to an explicit-obstruction laboratory rather
than evidence for a universal algorithmic trichotomy.

## Priority two: bounded arithmetic

`APC^1` remains limited to the V56 affine certificate. Escalate only
after a demonstrated front-one blocker or a theorem with independent
proof-complexity value.

## Nonclaims

No direct P-versus-NP route is active. General transversal-girth
hardness does not establish the degree-three case, and degree-three
hardness alone would not imply circuit lower bounds.
