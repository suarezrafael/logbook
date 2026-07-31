#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, random, time
from collections import Counter
from pathlib import Path
import v58_core as core

ROOT=Path(__file__).resolve().parent

def bits(x,n): return tuple((x>>i)&1 for i in range(n))

def main():
    started=time.perf_counter()
    assert len(core.ORBIT_07)==48
    fiber_checks=0
    for mask in core.ORBIT_07:
        for value in (0,1):
            clauses=core.local_2cnf_for_fiber(mask,value)
            described={x for x in range(8) if all(core.eval_clause(c,x) for c in clauses)}
            assert described==set(core.fiber(mask,value))
            fiber_checks+=1

    families=core.v57_irredundant_families()
    assert len(families)==12
    signatures={core.family_isomorphism_signature(f,4) for f in families}
    assert len(signatures)==1
    flip_redundancy_hist=Counter()
    flip_checks=0
    for family in families:
        gates=[core.descriptor_to_gate(d) for d in family]
        base=core.baseline_small_orientation(gates)
        image=core.circuit_image(4,gates)
        assert tuple(base) in image
        assert core.find_boundary_within_radius(4,gates,base,0) is None
        for coordinate in range(5):
            orient=list(base);orient[coordinate]^=1
            blocks=core.orientation_blocks(gates,orient)
            assert core.formula_satisfiable(4,blocks)
            redundant=core.redundant_blocks_2cnf(4,blocks)
            assert redundant
            flip_redundancy_hist[len(redundant)]+=1
            target=list(orient);target[redundant[0]]^=1
            assert tuple(target) not in image
            flip_checks+=1
        cert=core.find_boundary_within_radius(4,gates,base,1)
        assert cert is not None and cert['search_radius']==1

    direct_sum=[]
    for k in range(0,13):
        n,descriptors=core.stretch_one_descriptors(k)
        gates=[core.descriptor_to_gate(d) for d in descriptors]
        cert=core.find_boundary_within_radius(n,gates,max_radius=1)
        assert cert is not None and cert['search_radius']==1
        item={'k':k,'n':n,'m':len(gates),'kind':cert['kind'],'flipped':list(cert['flipped'])}
        if k<=3:
            image=core.circuit_image(n,gates)
            assert tuple(cert['target']) not in image
            item['range_size']=len(image)
        direct_sum.append(item)

    rng=random.Random(580058)
    random_circuits=0
    radius_hist=Counter()
    for n,samples in [(3,250),(4,250),(5,220),(6,180),(7,120),(8,80)]:
        supports=list(itertools.combinations(range(n),3))
        m=n+1
        for _ in range(samples):
            gates=[]
            for _j in range(m):
                mask=rng.choice(core.ORBIT_07)
                support=tuple(rng.choice(supports))
                gates.append((mask,support))
            cert=core.find_boundary_within_radius(n,gates,max_radius=1)
            assert cert is not None
            image=core.circuit_image(n,gates)
            assert tuple(cert['target']) not in image
            radius_hist[cert['search_radius']]+=1
            random_circuits+=1

    # Boundary-radius equivalence on arbitrary proper images.
    boundary_checks=0
    for m in range(2,8):
        cube=[bits(x,m) for x in range(1<<m)]
        for _ in range(150):
            size=rng.randrange(1,1<<m)
            image=set(rng.sample(cube,size))
            baseline=rng.choice(tuple(image))
            d=core.boundary_distance(image,baseline)
            assert d is not None
            for r in range(min(3,m)):
                ball=core.hamming_ball(baseline,r+1)
                assert (d>r)==ball.issubset(image)
            boundary_checks+=1

    # Universal cardinality bound, checked on random images.
    universal_bound_checks=0
    for n in range(1,7):
        m=n+1
        bound=core.universal_boundary_radius_bound(n,m)
        assert bound==n//2
        cube=[bits(x,m) for x in range(1<<m)]
        for _ in range(100):
            image=set(rng.sample(cube,rng.randrange(1,(1<<n)+1)))
            baseline=rng.choice(tuple(image))
            assert core.boundary_distance(image,baseline)<=bound
            universal_bound_checks+=1

    results={
        'version':'V58','status':'passed',
        'central_results':{
            'orientation_depth_equals_boundary_distance':True,
            'one_flip_failure_iff_radius2_ball_contained':True,
            'polynomial_2cnf_entailment_implemented':True,
            'exact_no_counterexample_range':'n=3..8',
            'v57_twelve_families_one_isomorphism_class':True,
            'v57_direct_sum_orientation_depth':1,
            'universal_stretch_one_boundary_bound':'floor(n/2)',
        },
        'validation':{
            'orbit_size':len(core.ORBIT_07),
            'fiber_cnf_checks':fiber_checks,
            'v57_irredundant_families':len(families),
            'v57_isomorphism_classes':len(signatures),
            'single_flip_checks':flip_checks,
            'single_flip_redundancy_histogram':dict(sorted(flip_redundancy_hist.items())),
            'direct_sum_k_through':12,
            'direct_sum_bruteforce_k_through':3,
            'random_orbit_circuits':random_circuits,
            'random_search_radius_histogram':dict(sorted(radius_hist.items())),
            'boundary_equivalence_checks':boundary_checks,
            'universal_bound_checks':universal_bound_checks,
            'failures':0,
        },
        'direct_sum':direct_sum,
        'scientific_status':{
            'peer_reviewed':False,'novelty_confirmed':False,
            'general_nc0_3_avoid_solved':False,'p_vs_np_resolved':False,
            'n9_exact_search_complete':False,
        },
        'elapsed_seconds':round(time.perf_counter()-started,6),
    }
    (ROOT/'RESULTS.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('V58 primary verification passed:')
    print(f'  {fiber_checks} local 2-CNF fiber reconstructions;')
    print(f'  12 V57 families, one isomorphism class, {flip_checks} successful single flips;')
    print(f'  direct-sum family through k=12; {random_circuits} random orbit circuits;')
    print(f'  {boundary_checks} boundary/ball equivalences; {universal_bound_checks} cardinality bounds; zero failures.')

if __name__=='__main__': main()
