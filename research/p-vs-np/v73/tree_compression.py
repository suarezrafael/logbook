#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
for directory in ("v68","v70"):sys.path.insert(0,str(ROOT/directory))
from affine_bitset import extend_basis,project_basis
from v70_frontier_ordering import compile_system
from multiplicity import branch_multiplicity_dp

def padded_binary_tree_specs(height):
    vertices=(1<<(height+1))-1;edges=[]
    for parent in range((1<<height)-1):edges.extend(((parent,2*parent+1),(parent,2*parent+2)))
    next_vertex=vertices;specs=[]
    for parent,child in edges:
        specs.append({"support":[parent,child,next_vertex],"partition":0});next_vertex+=1
    return next_vertex,specs

def edge_postorder(height):
    children={};edge=0
    for parent in range((1<<height)-1):children[parent]=((2*parent+1,edge),(2*parent+2,edge+1));edge+=2
    def visit(vertex):
        answer=[]
        for child,index in children.get(vertex,()):answer.extend(visit(child));answer.append(index)
        return answer
    return visit(0)

def aligned_branch_tree(height):
    children={};edge=0
    for parent in range((1<<height)-1):children[parent]=((2*parent+1,edge),(2*parent+2,edge+1));edge+=2
    def visit(vertex):
        branches=[]
        for child,index in children.get(vertex,()):
            subtree=visit(child);branches.append(index if subtree is None else (subtree,index))
        if not branches:return None
        current=branches[0]
        for branch in branches[1:]:current=current,branch
        return current
    return visit(0)

def projected_order_layers(n,specs,order):
    gates=compile_system(n,specs);suffix=[]
    for position in range(len(order)+1):
        suffix.append(tuple(sorted({v for index in order[position:] for v in gates[index]["support"]})))
    states={tuple()};widths=[]
    for position,index in enumerate(order):
        widths.append(len(states));next_states=set()
        for basis in states:
            for cell in gates[index]["cells"]:
                child=extend_basis(basis,cell,n)
                if child is not None:
                    child=project_basis(child,n,suffix[position+1])
                    if child is not None:next_states.add(child)
        states=next_states
    return {"G_proj":sum(widths),"layer_widths":widths,"terminal_residuals":len(states)}

def binary_tree_compression(max_height=7):
    results=[]
    for height in range(1,max_height+1):
        n,specs=padded_binary_tree_specs(height);order=edge_postorder(height);ordered=projected_order_layers(n,specs,order);m=len(specs)
        assert ordered["layer_widths"]==[1]*m
        branch=branch_multiplicity_dp(n,compile_system(n,specs),aligned_branch_tree(height))
        leaves=[x for x in branch["records"] if x["leaf"]];internal=[x for x in branch["records"] if not x["leaf"]]
        assert max(x["state_count"] for x in leaves)<=2 and all(x["state_count"]==1 for x in internal)
        assert branch["consistent_complete_branches"]==1<<m
        results.append({"height":height,"n":n,"m":m,"support_linear_width_unbounded_family":True,
          "postorder_G_proj":ordered["G_proj"],"proved_Gstar":m,"maximum_postorder_layer_width":1,
          "branch_complete_choices":branch["consistent_complete_branches"],
          "maximum_leaf_residual_states":max(x["state_count"] for x in leaves),
          "maximum_internal_residual_states":max((x["state_count"] for x in internal),default=1)})
    return results
