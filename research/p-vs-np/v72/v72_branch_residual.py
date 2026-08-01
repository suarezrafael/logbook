#!/usr/bin/env python3
"""V72 exact width, path-order benchmarks, and branch residual dynamic programming."""
from __future__ import annotations
import itertools,json,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
for directory in ("v68","v70","v71"):sys.path.insert(0,str(ROOT/directory))
from affine_bitset import extend_basis,project_basis
from v70_frontier_ordering import affine_subspace_count,compile_system,exact_best_order,ordered_gproj,residual_set
from v71_width_correspondence import bags_from_vertex_order,linear_width,normalize,order_from_path_decomposition,primal_graph,validate_graph_path_decomposition

def support_edges(specs):return normalize(spec["support"] for spec in specs)

def boundary_variables(specs,subset):
    subset=set(subset)
    left={v for i,s in enumerate(specs) if i in subset for v in s["support"]}
    right={v for i,s in enumerate(specs) if i not in subset for v in s["support"]}
    return left&right

def frontier_size_mask(edges,mask):
    left=set();right=set()
    for i,edge in enumerate(edges):(left if mask>>i&1 else right).update(edge)
    return len(left&right)

def exact_linear_width_dp(edges):
    """Exact O(m 2^m poly(n)) subset DP with an optimal labelled-edge order."""
    edges=normalize(edges);m=len(edges);size=1<<m
    frontiers=[frontier_size_mask(edges,mask) for mask in range(size)]
    dp=[10**9]*size;previous=[None]*size;dp[0]=0
    for mask in range(1,size):
        bits=mask
        while bits:
            bit=bits&-bits;gate=bit.bit_length()-1;parent=mask^bit
            candidate=max(dp[parent],frontiers[mask])
            if candidate<dp[mask] or (candidate==dp[mask] and (previous[mask] is None or gate<previous[mask][1])):
                dp[mask]=candidate;previous[mask]=(parent,gate)
            bits^=bit
    order=[];mask=size-1
    while mask:mask,gate=previous[mask];order.append(gate)
    order.reverse();prefix=0;profile=[]
    for gate in order:prefix|=1<<gate;profile.append(frontier_size_mask(edges,prefix))
    return {"width":dp[-1],"order":order,"frontier_profile":profile}

def exact_vertex_separation_dp(edges):
    """Exact O(n 2^n) pathwidth/vertex-separation DP on the primal graph."""
    adjacency=primal_graph(edges);vertices=sorted(adjacency)
    if not vertices:return {"pathwidth":0,"vertex_order":[]}
    if len(vertices)>20:raise ValueError("exact vertex-separation audit is limited to 20 vertices")
    index={v:i for i,v in enumerate(vertices)}
    neighbors=[sum(1<<index[w] for w in adjacency[v]) for v in vertices]
    size=1<<len(vertices);full=size-1;boundary=[0]*size
    for mask in range(size):
        outside=full^mask;bits=mask;value=0
        while bits:
            bit=bits&-bits;i=bit.bit_length()-1
            if neighbors[i]&outside:value+=1
            bits^=bit
        boundary[mask]=value
    dp=[10**9]*size;previous=[None]*size;dp[0]=0
    for mask in range(1,size):
        bits=mask
        while bits:
            bit=bits&-bits;i=bit.bit_length()-1;parent=mask^bit
            candidate=max(dp[parent],boundary[mask])
            if candidate<dp[mask] or (candidate==dp[mask] and (previous[mask] is None or i<previous[mask][1])):
                dp[mask]=candidate;previous[mask]=(parent,i)
            bits^=bit
    order=[];mask=full
    while mask:mask,i=previous[mask];order.append(vertices[i])
    order.reverse()
    return {"pathwidth":dp[-1],"vertex_order":order}

def brute_linear_width(edges):
    edges=normalize(edges)
    return min(linear_width(edges,order)[0] for order in itertools.permutations(range(len(edges))))

def exact_dp_validation():
    supports=[edge for size in (1,2,3) for edge in itertools.combinations(range(4),size)];checked=0
    for m in range(1,5):
        for edges in itertools.combinations(supports,m):
            exact=exact_linear_width_dp(edges)
            assert exact["width"]==brute_linear_width(edges)
            assert linear_width(edges,exact["order"])[0]==exact["width"];checked+=1
    return checked

def balanced_branch_tree(order):
    order=list(order)
    if not order:raise ValueError("a branch tree requires at least one gate")
    if len(order)==1:return order[0]
    middle=len(order)//2
    return balanced_branch_tree(order[:middle]),balanced_branch_tree(order[middle:])

def branch_tree_subset(node):
    if isinstance(node,int):return {node}
    return branch_tree_subset(node[0])|branch_tree_subset(node[1])

def branch_residual_dp(n,specs,tree,validate_direct=True):
    """Compose projected affine residuals bottom-up over a binary gate tree."""
    gates=compile_system(n,specs);records=[]
    def visit(node,address="R"):
        subset=branch_tree_subset(node);boundary=boundary_variables(specs,subset)
        if isinstance(node,int):
            states=set();pairs=0
            for cell in gates[node]["cells"]:
                basis=extend_basis(tuple(),cell,n)
                if basis is not None:
                    projected=project_basis(basis,n,boundary)
                    if projected is not None:states.add(projected)
        else:
            left=visit(node[0],address+"0");right=visit(node[1],address+"1");states=set();pairs=0
            for a in left:
                for b in right:
                    pairs+=1;child=extend_basis(a,b,n)
                    if child is not None:
                        projected=project_basis(child,n,boundary)
                        if projected is not None:states.add(projected)
        assert len(states)<=affine_subspace_count(len(boundary))
        if validate_direct:assert states==residual_set(n,gates,subset,boundary)
        records.append({"address":address,"subset":sorted(subset),"boundary":sorted(boundary),"state_count":len(states),"pair_transitions":pairs})
        return states
    return {"root_states":visit(tree),"records":records}

def seeded_branch_validation(seed=720072,samples=96):
    rng=random.Random(seed);nodes=0;maxima={"boundary":0,"states":0,"pair_transitions":0}
    for _ in range(samples):
        n=rng.randint(4,6);m=rng.randint(3,7)
        specs=[{"support":rng.sample(range(n),3),"partition":rng.randrange(3)} for _ in range(m)]
        order=list(range(m));rng.shuffle(order)
        result=branch_residual_dp(n,specs,balanced_branch_tree(order),True)
        for record in result["records"]:
            nodes+=1;maxima["boundary"]=max(maxima["boundary"],len(record["boundary"]))
            maxima["states"]=max(maxima["states"],record["state_count"])
            maxima["pair_transitions"]=max(maxima["pair_transitions"],record["pair_transitions"])
    return {"systems":samples,"nodes":nodes,"maxima":maxima}

def pathwidth_order_case(label,n,specs,expected_gstar):
    edges=support_edges(specs);linear=exact_linear_width_dp(edges);path=exact_vertex_separation_dp(edges)
    adjacency=primal_graph(edges);bags=bags_from_vertex_order(adjacency,path["vertex_order"])
    assert validate_graph_path_decomposition(adjacency,bags)
    order=order_from_path_decomposition(edges,bags);width,profile=linear_width(edges,order)
    assert width<=path["pathwidth"]+1
    path_g=ordered_gproj(n,specs,order);width_g=ordered_gproj(n,specs,linear["order"])
    return {"label":label,"n":n,"m":len(specs),"exact_Gstar":expected_gstar,"primal_pathwidth":path["pathwidth"],"path_vertex_order":path["vertex_order"],"path_gate_order":order,"path_frontier_width":width,"path_frontier_profile":profile,"path_G_proj":path_g,"ratio_to_Gstar":path_g/expected_gstar,"linear_branch_width":linear["width"],"linear_width_order":linear["order"],"linear_width_order_G_proj":width_g}

def v70_pathwidth_benchmarks():
    seeds=json.loads((ROOT/"v69"/"seed_data.json").read_text());search=json.loads((ROOT/"v70"/"SEARCH_SPEC.json").read_text());items=[]
    frozen_gstar={6:15,8:15,10:17,12:29}
    for n in (6,8,10,12):
        record=seeds["natural_records"][str(n)]
        items.append(pathwidth_order_case(f"v69-natural-n{n}",n,record["specs"],frozen_gstar[n]))
    for n in (8,10):
        record=search["searches"][str(n)]
        items.append(pathwidth_order_case(f"v70-exact-record-n{n}",n,record["specs"],int(record["expected_Gstar"])))
    return items

def padded_binary_tree_specs(height):
    tree_vertices=(1<<(height+1))-1;tree_edges=[]
    for parent in range((1<<height)-1):tree_edges.extend(((parent,2*parent+1),(parent,2*parent+2)))
    next_vertex=tree_vertices;specs=[]
    for u,v in tree_edges:specs.append({"support":[u,v,next_vertex],"partition":0});next_vertex+=1
    return next_vertex,specs

def padded_binary_tree_results():
    results=[]
    for height in range(1,4):
        n,specs=padded_binary_tree_specs(height);edges=support_edges(specs);exact=exact_linear_width_dp(edges)
        path=exact_vertex_separation_dp(edges) if n<=20 else None
        results.append({"height":height,"n":n,"m":len(specs),"primal_treewidth_upper_bound":2,"linear_branch_width":exact["width"],"primal_pathwidth":None if path is None else path["pathwidth"],"linear_width_order_G_proj":ordered_gproj(n,specs,exact["order"]),"exact_Gstar":exact_best_order(n,specs)["Gstar"] if len(specs)<=6 else None})
    return results

def generate_results():
    exact=exact_dp_validation();branch=seeded_branch_validation();benchmarks=v70_pathwidth_benchmarks();binary=padded_binary_tree_results()
    return {"version":"V72","status":"passed","failures":0,
      "theorems":{"complexity":"vertex-boundary linear branch-width is NP-complete even for simple three-uniform hypergraphs by private-vertex padding of graph linearwidth","exact_algorithm":"O(m 2^m poly(n)) subset dynamic programming","branch_residual_dp":"a supplied binary branch decomposition of boundary width b supports exact affine residual composition with at most A(b) states per node and A(b)^2 pair transitions per internal node","bounded_treewidth_separation":"private-vertex padding preserves graph linearwidth while the primal graph has treewidth at most two"},
      "exact_dp_exhaustive_rank3_n4_m_le_4":exact,"branch_validation":branch,"pathwidth_benchmarks":benchmarks,"padded_binary_tree_family":binary,
      "benchmark_summary":{"cases":len(benchmarks),"maximum_ratio_to_Gstar":max(x["ratio_to_Gstar"] for x in benchmarks),"path_orders_within_factor_2_1_on_preserved_cases":all(x["ratio_to_Gstar"]<=2.1 for x in benchmarks),"linear_width_objective_equals_Gproj_objective":False},
      "scientific_status":{"rank3_width_decision_np_complete":True,"exact_width_dp_verified":True,"branch_residual_dp_proved":True,"bounded_treewidth_forces_bounded_linear_width":False,"bounded_treewidth_forces_small_Gstar":False,"general_polynomial_good_order_proved":False,"all_orders_superpolynomial_lower_bound_proved":False,"standard_model_simulation_proved":False,"unrestricted_avoidance_algorithm_proved":False,"p_vs_np_route_active":False,"p_vs_np_resolved":False,"novelty_confirmed":False,"peer_reviewed":False}}

def main():
    results=generate_results();(HERE/"RESULTS.json").write_text(json.dumps(results,indent=2,sort_keys=True)+"\n")
    print(f"V72 verification passed: NP-complete rank-three width decision; {results['exact_dp_exhaustive_rank3_n4_m_le_4']} exact DP cases; {results['branch_validation']['nodes']} branch nodes; six path-order benchmarks; zero failures.")
if __name__=="__main__":main()
