#!/usr/bin/env python3
from __future__ import annotations
import itertools,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
for directory in ("v68","v70"):sys.path.insert(0,str(ROOT/directory))
from affine_bitset import satisfies
from v70_frontier_ordering import compile_system,subset_widths_and_frontiers
from bicriteria import optimize_budgeted_from_tables
from multiplicity import balanced_branch_tree,branch_multiplicity_dp,synthetic_avoided_target_certificate
from tree_compression import edge_postorder,padded_binary_tree_specs,projected_order_layers

def signatures_by_assignments(n,gates):
    signatures=set()
    for assignment in range(1<<n):
        signature=0
        for index,gate in enumerate(gates):
            membership=[satisfies(cell,assignment,n) for cell in gate["cells"]]
            assert sum(membership)<=1
            if not any(membership):break
            if membership[1]:signature|=1<<index
        else:signatures.add(signature)
    return signatures

def check_bicriteria(seed=731073,samples=32):
    rng=random.Random(seed);checks=0
    for _ in range(samples):
        n=rng.randint(3,5);m=rng.randint(2,6)
        specs=[{"support":rng.sample(range(n),3),"partition":rng.randrange(3)} for _ in range(m)]
        widths,frontiers=subset_widths_and_frontiers(n,specs)
        for budget in range(max(frontiers)+1):
            dynamic=optimize_budgeted_from_tables(widths,frontiers,budget);best=None
            for order in itertools.permutations(range(m)):
                mask=0;cost=0;valid=frontiers[0]<=budget
                for gate in order:
                    if not valid:break
                    cost+=widths[mask];mask|=1<<gate;valid=frontiers[mask]<=budget
                if valid and (best is None or cost<best):best=cost
            assert (dynamic is None)==(best is None)
            if dynamic is not None:assert dynamic["G_proj"]==best
            checks+=1
    return checks

def check_multiplicity(seed=731074,samples=64):
    rng=random.Random(seed);nodes=0;signatures=0
    for _ in range(samples):
        n=rng.randint(3,6);m=rng.randint(3,7)
        specs=[{"support":rng.sample(range(n),3),"partition":rng.randrange(3)} for _ in range(m)]
        gates=compile_system(n,specs);direct=signatures_by_assignments(n,gates)
        dynamic=branch_multiplicity_dp(n,gates,balanced_branch_tree(range(m)))
        assert dynamic["consistent_complete_branches"]==len(direct)
        assert 0 in direct
        nodes+=len(dynamic["records"]);signatures+=len(direct)
    return nodes,signatures

def check_tree_family():
    checks=0
    for height in range(1,8):
        n,specs=padded_binary_tree_specs(height);m=len(specs)
        metrics=projected_order_layers(n,specs,edge_postorder(height))
        assert metrics["layer_widths"]==[1]*m and metrics["G_proj"]==m
        checks+=m
    return checks

def main():
    bicriteria=check_bicriteria();nodes,signatures=check_multiplicity();tree=check_tree_family()
    synthetic=synthetic_avoided_target_certificate();assert synthetic["consistent_complete_branches"]==0
    print(f"V73 independent verification passed: {bicriteria} brute-force budget checks; {nodes} semantic branch nodes; {signatures} assignment-derived signatures; {tree} tree layers; zero failures.")
if __name__=="__main__":main()
