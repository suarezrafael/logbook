# V116 implementation note

The promoted theorem is intentionally limited to feedback-gate number at most one per non-common dominator stage.

The local solver does not call a generic multi-commodity-flow oracle. It constructs a gate-split DAG after fixing the at-most-two special resources (feedback gate and optional unique excess shared gate), then solves at most five ordered requests with a product-state token DP.

The key invariant behind the history-free product state is topological monotonicity: after a token leaves a capacity-one gate resource, every unfinished token has current topological rank at least that resource's rank. No token can later reach the resource's selector predecessor, so the gate can never be reused later even though the DP stores no explicit used-gate set.

This invariant should be reviewed especially carefully. The primary verifier exercises the full public algorithm on seeded small instances against direct gate-simple route enumeration; the independent verifier deliberately avoids importing the V116 implementation.
