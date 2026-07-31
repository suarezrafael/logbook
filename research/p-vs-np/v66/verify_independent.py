#!/usr/bin/env python3
"""Independent finite audit for Laboratory V66.

This verifier rederives the affine-cell partitions, the V57 branch counts, and
the complete three-variable signature-state census without importing the primary
verifier. It treats the n=4 sample as regression metadata only; the primary
verifier reproduces that deterministic stress run.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
CLASSES=(0x07,0x16,0x17,0x19,0x1B,0x1E)

def affine(points):
    if not points:return False
    origin=min(points);translated={x^origin for x in points}
    return len(translated)&(len(translated)-1)==0 and all(a^b in translated for a in translated for b in translated)
def all_affine_sets(n):
    return tuple(frozenset(x for x in range(1<<n) if mask&(1<<x)) for mask in range(1,1<<(1<<n)) if affine(frozenset(x for x in range(1<<n) if mask&(1<<x))))
def affine_partitions(fiber,sets):
    lookup=set(sets);out=set()
    for first in sets:
        if first and first<fiber:
            second=fiber-first
            if second in lookup:out.add(tuple(sorted((tuple(sorted(first)),tuple(sorted(second))))))
    return tuple((frozenset(a),frozenset(b)) for a,b in sorted(out))
def transform(mask,perm,flips,out_flip):
    result=0
    for target in range(8):
        bits=tuple((target>>i)&1 for i in range(3));source=sum((bits[perm[i]]^flips[i])<<i for i in range(3))
        result|=((((mask>>source)&1)^out_flip)<<target)
    return result
def orbit(mask):
    return {transform(mask,p,f,o) for p in itertools.permutations(range(3)) for f in itertools.product((0,1),repeat=3) for o in (0,1)}
def fibers_and_variants():
    affine3=all_affine_sets(3);fibers=set()
    for representative in CLASSES:
        for mask in orbit(representative):
            for value in (0,1):
                fiber=frozenset(x for x in range(8) if ((mask>>x)&1)==value)
                if not affine(fiber):fibers.add(fiber)
    ordered=tuple(sorted(fibers,key=lambda x:(len(x),tuple(sorted(x)))))
    variants=tuple(part for fiber in ordered for part in affine_partitions(fiber,affine3))
    return ordered,variants
def v57_fibers():
    predicates=(lambda x0,x1,x2,x3:(not x0)and((not x1)or x2),lambda x0,x1,x2,x3:(not x0)and(x1 or(not x2)),lambda x0,x1,x2,x3:(not x0)and((not x1)or x3),lambda x0,x1,x2,x3:(not x0)and(x1 or(not x3)),lambda x0,x1,x2,x3:(not x0)and((not x2)or(not x3)))
    return tuple(frozenset(x for x in range(16) if predicate(*tuple((x>>i)&1 for i in range(4)))) for predicate in predicates)
def signatures(parts,universe):
    found=set()
    for point in range(universe):
        word=[]
        for left,right in parts:
            if point in left:word.append(0)
            elif point in right:word.append(1)
            else:break
        else:found.add(tuple(word))
    return frozenset(found)
def tree_metrics(parts,universe):
    @lru_cache(None)
    def solve(feasible,remaining):
        if not feasible or not remaining:return 1,0,0,None
        candidates=[]
        for gate in remaining:
            tail=tuple(x for x in remaining if x!=gate);a=solve(feasible&parts[gate][0],tail);b=solve(feasible&parts[gate][1],tail)
            candidates.append((a[0]+b[0],1+a[1]+b[1],1+max(a[2],b[2]),gate))
        return min(candidates,key=lambda x:x[:3])
    seen=set()
    def walk(feasible,remaining):
        state=(feasible,remaining)
        if state in seen:return
        seen.add(state)
        if not feasible or not remaining:return
        gate=solve(feasible,remaining)[3];tail=tuple(x for x in remaining if x!=gate)
        walk(feasible&parts[gate][0],tail);walk(feasible&parts[gate][1],tail)
    remaining=tuple(range(len(parts)));root=solve(frozenset(range(universe)),remaining);walk(frozenset(range(universe)),remaining)
    return root[0],root[1],root[2],len(seen)
def check_v57():
    affine4=all_affine_sets(4);options=tuple(affine_partitions(f,affine4) for f in v57_fibers());assert tuple(map(len,options))==(3,3,3,3,3)
    consistent=Counter();metrics=Counter()
    for selection in itertools.product(range(3),repeat=5):
        system=tuple(options[i][selection[i]] for i in range(5));consistent[len(signatures(system,16))]+=1;metrics[tree_metrics(system,16)]+=1
    assert consistent==Counter({1:243})
    assert metrics==Counter({(8,7,5,11):3,(8,7,5,12):34,(8,7,5,13):75,(8,7,5,14):124,(9,8,5,12):1,(9,8,5,15):6})
    return 243
def check_complete_state_census():
    fibers,variants=fibers_and_variants();assert len(fibers)==168 and Counter(map(len,fibers))==Counter({3:56,4:56,5:56}) and len(variants)==392
    affine3=all_affine_sets(3);assert Counter(len(affine_partitions(f,affine3)) for f in fibers)==Counter({3:112,1:56})
    states={(tuple(range(8)),)};counts=[1]
    for _ in range(4):
        next_states=set()
        for groups in states:
            for left,right in variants:
                successor=[]
                for group in groups:
                    a=tuple(x for x in group if x in left);b=tuple(x for x in group if x in right)
                    if a:successor.append(a)
                    if b:successor.append(b)
                next_states.add(tuple(sorted(successor)))
        states=next_states;counts.append(len(states))
    distribution=Counter(map(len,states));assert counts==[1,392,919,919,919]
    assert distribution==Counter({0:1,1:50,2:420,3:392,4:56})
    return sum(counts)
def check_canonical_tree_extrema():
    affine3=all_affine_sets(3);variants=[]
    for representative in CLASSES:
        for output in (0,1):
            fiber=frozenset(x for x in range(8) if ((representative>>x)&1)==output);variants.extend(affine_partitions(fiber,affine3))
    assert len(variants)==30;distribution=Counter();max_leaves=max_states=systems=0
    for indices in itertools.combinations_with_replacement(range(30),4):
        system=tuple(variants[i] for i in indices);distribution[len(signatures(system,8))]+=1
        leaves,_,_,residual=tree_metrics(system,8);max_leaves=max(max_leaves,leaves);max_states=max(max_states,residual);systems+=1
    assert systems==40920 and distribution==Counter({0:26658,1:9111,2:3122,3:1908,4:121})
    assert max_leaves==11 and max_states==17
    return systems
def check_results_and_boundaries():
    results=json.loads((HERE/'RESULTS.json').read_text());assert results['version']=='V66' and results['status']=='passed'
    assert results['n4_deterministic_stress']['seed']==660066 and results['n4_deterministic_stress']['samples']==50000
    assert results['n4_deterministic_stress']['consistent_full_branch_distribution']=={'0':32433,'1':14200,'2':2841,'3':433,'4':84,'5':9}
    status=results['scientific_status'];assert status['theorem_claimed'] is False and status['counterexample_to_polynomial_pruning_found'] is False
    assert status['p_vs_np_route_active'] is False and status['p_vs_np_resolved'] is False
    corpus='\n'.join(path.read_text() for path in HERE.glob('*.md'))
    assert '2026-08-24' in corpus and 'not an exhaustive n=4 theorem' in corpus and 'does not establish polynomial branching' in corpus
    return 12
def main():
    v57=check_v57();states=check_complete_state_census();canonical=check_canonical_tree_extrema();boundaries=check_results_and_boundaries()
    print(f'V66 independent verification passed: {v57} V57 partition systems; {states} state-layer checks; {canonical} canonical n=3 systems; {boundaries} boundary checks; zero failures.')
if __name__=='__main__':main()
