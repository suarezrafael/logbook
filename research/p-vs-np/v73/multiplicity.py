#!/usr/bin/env python3
from __future__ import annotations
import itertools,random,sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
for directory in ("v68","v70"):sys.path.insert(0,str(ROOT/directory))
from affine_bitset import extend_basis,project_basis,row,satisfies
from v68_spine_family import spine_family
from v70_frontier_ordering import compile_system

def boundary_variables(gates,subset):
    subset=set(subset);left={v for i,g in enumerate(gates) if i in subset for v in g["support"]};right={v for i,g in enumerate(gates) if i not in subset for v in g["support"]}
    return tuple(sorted(left&right))
def tree_subset(node):return {node} if isinstance(node,int) else tree_subset(node[0])|tree_subset(node[1])
def balanced_branch_tree(order):
    order=list(order)
    if not order:raise ValueError("branch tree needs at least one gate")
    if len(order)==1:return order[0]
    middle=len(order)//2;return balanced_branch_tree(order[:middle]),balanced_branch_tree(order[middle:])

def branch_multiplicity_dp(n,gates,tree):
    records=[]
    def visit(node,address="R"):
        subset=tree_subset(node);boundary=boundary_variables(gates,subset)
        if isinstance(node,int):
            counts=Counter()
            for cell in gates[node]["cells"]:
                basis=extend_basis(tuple(),cell,n)
                if basis is not None:
                    projected=project_basis(basis,n,boundary)
                    if projected is not None:counts[projected]+=1
            pairs=0;leaf=True
        else:
            left=visit(node[0],address+"0");right=visit(node[1],address+"1");counts=Counter();pairs=0;leaf=False
            for a,ca in left.items():
                for b,cb in right.items():
                    pairs+=1;combined=extend_basis(a,b,n)
                    if combined is None:continue
                    projected=project_basis(combined,n,boundary)
                    if projected is not None:counts[projected]+=ca*cb
        records.append({"address":address,"leaf":leaf,"subset_size":len(subset),"boundary_size":len(boundary),
          "state_count":len(counts),"complete_branch_count":sum(counts.values()),"pair_transitions":pairs})
        return counts
    root=visit(tree)
    return {"consistent_complete_branches":sum(root.values()),"records":records}

def direct_complete_branch_count(n,gates):
    count=0
    for choices in itertools.product((0,1),repeat=len(gates)):
        basis=tuple()
        for index,branch in enumerate(choices):
            basis=extend_basis(basis,gates[index]["cells"][branch],n)
            if basis is None:break
        if basis is not None:count+=1
    return count

def normalized_zero_branch_certificate(n,specs):
    gates=compile_system(n,specs);assert all(satisfies(g["cells"][0],0,n) for g in gates)
    result=branch_multiplicity_dp(n,gates,balanced_branch_tree(range(len(gates))));assert result["consistent_complete_branches"]>=1
    return {"all_zero_input_satisfies_cell_zero_of_every_gate":True,
      "consistent_complete_branches":result["consistent_complete_branches"],
      "can_certify_current_selected_target_as_avoided":False}

def synthetic_avoided_target_certificate():
    n=2
    gate_zero={"support":(0,1),"cells":((row(n,(0,),0),row(n,(1,),0)),(row(n,(0,),0),row(n,(1,),1)))}
    gate_one={"support":(0,1),"cells":((row(n,(0,),1),row(n,(1,),0)),(row(n,(0,),1),row(n,(1,),1)))}
    result=branch_multiplicity_dp(n,(gate_zero,gate_one),balanced_branch_tree(range(2)));assert result["consistent_complete_branches"]==0
    return {"supplied_target":[1,1],"consistent_complete_branches":0,"target_is_certified_outside_image":True,
      "fiber_cells_are_disjoint":True,"scope":"generic affine decompositions for a supplied target, not target search"}

def seeded_multiplicity_validation(seed=730074,samples=96):
    rng=random.Random(seed);nodes=0
    for _ in range(samples):
        n=rng.randint(3,6);m=rng.randint(3,7)
        specs=[{"support":rng.sample(range(n),3),"partition":rng.randrange(3)} for _ in range(m)]
        gates=compile_system(n,specs);dynamic=branch_multiplicity_dp(n,gates,balanced_branch_tree(range(m)))
        assert dynamic["consistent_complete_branches"]==direct_complete_branch_count(n,gates)
        assert all(satisfies(g["cells"][0],0,n) for g in gates);nodes+=len(dynamic["records"])
    return {"seed":seed,"systems":samples,"branch_nodes":nodes}

def spine_multiplicity_checks(max_k=8):
    items=[]
    for k in range(1,max_k+1):
        family=spine_family(k);result=branch_multiplicity_dp(family["n"],family["gates"],balanced_branch_tree(range(family["m"])))
        expected=1<<(k-1);assert result["consistent_complete_branches"]==expected
        items.append({"k":k,"n":family["n"],"m":family["m"],"consistent_complete_branches":expected,
          "maximum_residual_states":max(item["state_count"] for item in result["records"])})
    return items
