# V89 validation record

## Local component execution

The candidate was generated and executed with Python 3 using only the standard
library.

The primary generator recomputes:

- `OA(8,4,2,3)` injectivity;
- the exact uniform-code table for `j=3,...,10`;
- maximum primal cliques and exact primal chromatic numbers;
- deterministic `F_2^3` basis-coloring witnesses;
- eight-row address injectivity on all eleven controls.

Expected finite chromatic sequence:

```text
6, 5, 5, 5, 6, 5, 5, 5, 5, 5, 6
```

Every control has a verified basis coloring and an injective eight-row affine
address family.

## Repository gates

V89 is a draft candidate. The integrated quick gate must execute the primary
and independent verifiers with no repository mutation. Compatibility and any
full replay required by runner changes remain promotion prerequisites.

No promotion or nine-row constructor lower bound is implied by the finite
audit.
