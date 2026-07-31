#!/usr/bin/env python3
from __future__ import annotations
import itertools,random
from collections import Counter
from branching_core import *
SEED=660066


def verify_v57_branching():
    affine4=affine_subsets(4);blocks=v57_blocks();assert [len(x) for x in blocks]==[6]*5
    options=tuple(partitions(block,affine4) for block in blocks);assert [len(x) for x in options]==[3]*5
    metrics=Counter();consistent=Counter()
    for selected in itertools.product(range(3),repeat=5):
        system=tuple(options[i][choice] for i,choice in enumerate(selected))
        consistent[len(branch_signatures(system,range(16)))]+=1;metrics[optimal_pruned_tree(system,range(16))]+=1
    expected={(8,7,5,11):3,(8,7,5,12):34,(8,7,5,13):75,(8,7,5,14):124,(9,8,5,12):1,(9,8,5,15):6}
    assert consistent==Counter({1:243}) and dict(metrics)==expected
    return {'partition_systems':243,'consistent_full_branches':{'1':243},'optimal_tree_metric_distribution':{'/'.join(map(str,k)):v for k,v in sorted(metrics.items())},'leaf_range':[8,9],'interpretation':'Every affine-cell partition system has one consistent full branch; inconsistency pruning reduces 32 syntactic branches to 8 or 9 leaves under an optimal adaptive order.'}


def transition(groups,variant):
    _,(cell0,cell1)=variant;answer=[]
    for group in groups:
        a=tuple(sorted(set(group)&cell0));b=tuple(sorted(set(group)&cell1))
        if a:answer.append(a)
        if b:answer.append(b)
    return tuple(sorted(answer))


def verify_complete_n3_state_space():
    affine3=affine_subsets(3);fibers=non_affine_fibers();assert len(fibers)==168 and Counter(map(len,fibers))==Counter({3:56,4:56,5:56})
    variants=tuple((fiber,part) for fiber in fibers for part in partitions(fiber,affine3));assert len(variants)==392
    assert Counter(len(partitions(f,affine3)) for f in fibers)==Counter({3:112,1:56})
    states={(tuple(range(8)),):()};counts=[1]
    for _ in range(4):
        nxt={}
        for state,witness in states.items():
            for index,variant in enumerate(variants):nxt.setdefault(transition(state,variant),witness+(index,))
        states=nxt;counts.append(len(states))
    distribution=Counter(map(len,states));assert counts==[1,392,919,919,919]
    assert distribution==Counter({0:1,1:50,2:420,3:392,4:56})
    max_state=next(state for state in states if len(state)==4);witness=states[max_state]
    return {'distinct_non_affine_fibers':168,'affine_cell_gate_variants':392,'reachable_signature_states_after_k_gates':counts,'final_consistent_branch_distribution_over_reachable_states':{str(k):v for k,v in sorted(distribution.items())},'maximum_consistent_full_branches':4,'maximum_witness_variant_indices':list(witness),'maximum_witness_signature_groups':[list(x) for x in max_state],'scope':'All ordered four-gate systems over all NPN transforms, both output fibers, and every disjoint two-affine-cell partition on the three-variable cube, compressed by exact signature-state dynamic programming.'}


def verify_canonical_n3_trees():
    variants=canonical_variants(affine_subsets(3));assert len(variants)==30
    branches=Counter();metrics=Counter();max_leaves=(-1,());max_states=(-1,());systems=0
    for indices in itertools.combinations_with_replacement(range(30),4):
        system=tuple(variants[i][1] for i in indices);tree=optimal_pruned_tree(system,range(8))
        branches[len(branch_signatures(system,range(8)))]+=1;metrics[tree]+=1;systems+=1
        if tree[0]>max_leaves[0]:max_leaves=(tree[0],indices)
        if tree[3]>max_states[0]:max_states=(tree[3],indices)
    expected=Counter({(4,3,2,4):14880,(4,3,2,5):10630,(5,4,3,6):693,(5,4,3,7):455,(6,5,4,9):4770,(6,5,4,10):4660,(7,6,4,10):236,(7,6,4,11):613,(7,6,4,12):71,(8,7,4,12):1380,(8,7,4,13):679,(8,7,4,14):458,(8,7,4,15):290,(9,8,4,14):473,(9,8,4,15):563,(9,8,4,16):26,(10,9,4,15):36,(10,9,4,16):1,(10,9,4,17):2,(11,10,4,17):4})
    assert systems==40920 and branches==Counter({0:26658,1:9111,2:3122,3:1908,4:121}) and metrics==expected
    assert max_leaves[0]==11 and max_states[0]==17
    return {'gate_variants':30,'multisets_of_four_gates':systems,'consistent_full_branch_distribution':{str(k):v for k,v in sorted(branches.items())},'maximum_optimal_leaf_count':11,'maximum_optimal_residual_state_count':17,'maximum_leaf_witness_indices':list(max_leaves[1]),'maximum_state_witness_indices':list(max_states[1]),'metric_distribution':{'/'.join(map(str,k)):v for k,v in sorted(metrics.items())},'scope':'Canonical representatives only; this tree-size census is not claimed to cover all global affine transforms.'}


def verify_n4_stress(sample_count=50000):
    variants=lifted_n4_variants();assert len(variants)==352 and Counter(len(x[0]) for x in variants)==Counter({6:84,8:240,10:28})
    rng=random.Random(SEED);distribution=Counter();max_cons=(-1,());max_leaves=(-1,());max_states=(-1,())
    for _ in range(sample_count):
        indices=tuple(rng.randrange(352) for _ in range(5));system=tuple(variants[i][1] for i in indices)
        count=len(branch_signatures(system,range(16)));tree=optimal_pruned_tree(system,range(16));distribution[count]+=1
        if count>max_cons[0]:max_cons=(count,indices)
        if tree[0]>max_leaves[0]:max_leaves=(tree[0],indices)
        if tree[3]>max_states[0]:max_states=(tree[3],indices)
    assert distribution==Counter({0:32433,1:14200,2:2841,3:433,4:84,5:9})
    assert (max_cons[0],max_leaves[0],max_states[0])==(5,14,23)
    return {'seed':SEED,'samples':sample_count,'distinct_lifted_gate_variants':352,'consistent_full_branch_distribution':{str(k):v for k,v in sorted(distribution.items())},'maximum_consistent_full_branches_observed':5,'maximum_optimal_leaf_count_observed':14,'maximum_optimal_residual_states_observed':23,'maximum_consistent_witness_indices':list(max_cons[1]),'maximum_leaf_witness_indices':list(max_leaves[1]),'maximum_state_witness_indices':list(max_states[1]),'scope':'Deterministic falsification/regression sample, not an exhaustive n=4 theorem.'}
