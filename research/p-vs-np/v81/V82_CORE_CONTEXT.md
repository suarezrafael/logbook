# V82 core context — exact complexity or explicit obstruction

## Established by V81

For every cut,

```text
delta(S)+delta(M\S)=stretch-lambda_C(S).
```

A supplied width-`w` decomposition constructively yields a balanced Hall
witness of deficiency at least `ceil((stretch-w)/2)`.

The minimum-neighborhood Hall problem is exactly the first below-diagonal point
of the Minimum `p`-Union curve `U(p)`. Lagrangian submodular minimization finds
only supported points and misses the optimum on every V80 obstruction
candidate.

## Priority one: resolve one exact combinatorial question

Choose one of the following and finish it before broadening the search.

### A. Algorithmic route

Find a polynomial-time method for

```text
min |N(S)| subject to |N(S)|<|S|
```

under rank-three supports, or under a clearly stated structural promise that is
forced by high branchwidth. The method must recover unsupported points, not
only the Lagrangian envelope.

### B. Hardness route

Prove NP-hardness of the exact Hall-diagonal crossing problem, preferably for
rank-three supports and a controlled stretch. The reduction must distinguish
this objective from generic Minimum `p`-Union approximation hardness.

### C. Explicit-obstruction route

Translate a primary-source lossless-expander construction into a family with
left degree at most three and the target side sizes, or prove why the available
constructions cannot meet those parameters without losing expansion.

## Census discipline

Before proposing a universal trichotomy, extend the V81 census with:

- sunflower core and petal profiles;
- affine-cell rank or a precise replacement invariant;
- `G*_proj` all-orders growth on the same finite instances;
- Minimum `p`-Union curves for explicit expander candidates;
- counterexamples to every proposed monotone inequality.

The obstruction outcome must have a polynomially checkable certificate or be
clearly labelled as an experimental record rather than an algorithmic output.

## Priority two: bounded arithmetic

Keep `APC^1` work limited to the V56 affine certificate. Escalate only if the
front-one program encounters a demonstrated formalization blocker or produces
a theorem whose proof-complexity interpretation is independently valuable.

## Nonclaims

No direct P-versus-NP route is active. V82 must not claim that explicit
lossless expanders automatically imply all-orders lower bounds, or that
Minimum `p`-Union hardness alone yields circuit lower bounds.
