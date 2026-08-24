# V116 frozen core context — bounded cyclic interaction after the DAG frontier

## Inherited facts

V113 completely decides target compatibility on the minimum-overlap face for each fixed opposite-phase signed-MUX first pair and proves `minimum_overlap = number_of_common_gate_dominators`.

V114 proves an NP-complete barrier for arbitrary one-extra opposite-compatible completion in general directed return graphs, but deliberately has a compatible zero-overlap bypass and therefore does not prove `Delta=1` hardness.

V115 proves polynomial-time decision of

```text
target-compatible overlap <= minimum_overlap + 1
```

when every non-common V113 dominator stage is acyclic. It also gives an infinite exact-stretch family with `Delta=1` that V113 rejects and V115 accepts.

## V116 primary question

How much directed cyclic interaction can be admitted while retaining a parameterized budget-one algorithm?

The preferred parameter is the cyclic complexity of each non-common dominator stage, not raw stage size.

### Track A — feedback vertex/gate set parameter

For each stage let `tau` be the size of a smallest set of stage variables or output gates whose removal makes the branch graph acyclic.

Target:

```text
f(tau) * poly(n,m)
```

time for fixed-pair `Delta<=1`, preserving signed phase compatibility and gate-simple routes.

A direct route is to enumerate how the two routes interact with the feedback set, cut the remaining pieces into DAG regions, and reuse the V115 prefix/suffix factorization. The proof must show that the interface state is bounded by a function of `tau` and that gate resources are not silently reused across DAG pieces.

### Track B — bounded number of cyclic SCCs

Compress each stage into its SCC condensation. If only `kappa` SCCs are nontrivial, test whether route interaction with those SCCs admits an FPT state space while the acyclic condensation is handled by V115.

Do not confuse `kappa` with SCC size: V114-style two-linkage hardness can live inside one large SCC.

### Track C — hardness at the first cyclic level

Try to strengthen the V114 gadget so that:

1. the V113 optimum face is entirely target-incompatible;
2. a compatible pair at `Delta=1` exists iff the source linkage instance is yes;
3. every hard stage has the smallest possible cyclic parameter (`tau=1`, one nontrivial SCC, or another explicitly bounded measure);
4. exact positive stretch and essential ternary signed-MUX semantics remain intact.

A proof that `tau=1` is already NP-hard would sharply close Track A. Failure of that construction should feed structural information back into the FPT attempt.

## Promotion rule

V116 is promotable only with at least one of:

- an FPT theorem in a clearly defined cyclic-stage parameter with implementation and independent verification;
- a polynomial theorem for a nontrivial cyclic class plus an infinite separation family outside V115;
- a correct hardness reduction at a bounded first-cyclic parameter;
- a different rigorous barrier that materially narrows the remaining signed-MUX frontier.

Larger finite tables alone are not promotable.

## Global boundary

Even a successful V116 result remains a structured signed-MUX theorem unless the structural parameter is proved bounded universally. Do not infer unrestricted `NC0_3-Avoid`, circuit lower bounds, or P versus NP.
