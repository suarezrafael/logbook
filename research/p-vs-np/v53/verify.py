#!/usr/bin/env python3
from __future__ import annotations
import json, time
from pathlib import Path
import v53_core as core
ROOT = Path(__file__).resolve().parent


def main() -> None:
    started = time.perf_counter()
    results=[]; union_checks=rank_checks=exact_checks=0

    # Preserved finite V53 examples.
    for name, case in core.FINITE_EXAMPLES.items():
        n, edges, t = case['n'], case['edges'], case['t']
        m=len(edges)
        assert m == n+1
        assert all(len(e)==3 and len(set(e))==3 for e in edges)
        ok, unions, collision = core.union_free_certificate(edges,t)
        assert ok and collision is None
        expected=sum(__import__('math').comb(m,j) for j in range(t+1))
        assert len(unions)==expected
        union_checks += len(unions)
        image=core.circuit_image(n,edges)
        degree=core.exact_syndrome_degree_gf2(image,m,t+2)
        assert degree==t+1
        exact_checks += 1
        mons=core.monomials(m,t)
        matrix=core.evaluation_matrix(image,m,t)
        ranks={}
        for prime in (2,3,5):
            rank=core.rank_mod(matrix,prime)
            assert rank==len(mons)
            ranks[str(prime)]=rank; rank_checks += 1
        flipped=core.circuit_image(n,edges,case['output_flip_mask'])
        assert core.exact_syndrome_degree_gf2(flipped,m,t+2)==degree
        results.append({'name':name,'n':n,'m':m,'t_union_free':t,'subset_unions_checked':len(unions),'range_size':len(image),'minimum_syndrome_degree_gf2':degree,'degree_t_evaluation_rank':ranks,'degree_t_monomials':len(mons),'output_flip_control_degree':degree,'edges':edges})

    # Mandatory regression for the theorem retracted by V54.
    # The incidence graph is a tree, yet an edge is covered by three others.
    nested_cover = [
        [0,1,2],
        [0,3,4],
        [1,5,6],
        [2,7,8],
    ]
    ok4, _, collision4 = core.union_free_certificate(nested_cover, 4)
    assert not ok4 and collision4 is not None
    left, right, _ = collision4
    assert set(left) == {1,2,3}
    assert set(right) == {0,1,2,3}

    output={
        'status':'passed_with_retraction_regression',
        'finite_examples':results,
        'retraction_regression':{
            'acyclic_nested_cover_detected': True,
            'four_union_free': False,
            'collision':[list(left),list(right)],
            'omega_log_claim_retracted': True,
        },
        'summary':{
            'examples':len(results),
            'union_values_checked':union_checks,
            'field_rank_checks':rank_checks,
            'exact_degree_checks':exact_checks,
            'retraction_regressions':1,
            'failures':0,
            'elapsed_seconds':round(time.perf_counter()-started,6),
        },
    }
    (ROOT/'RESULTS.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    (ROOT/'FINITE_EXAMPLES.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print('V53 corrected verification passed:')
    print(f'  {len(results)}/{len(results)} finite NC0_3 stretch-one examples preserved;')
    print(f'  {union_checks} distinct subset unions checked;')
    print(f'  {rank_checks} full-rank evaluations over GF(2), GF(3), GF(5);')
    print('  exact syndrome degrees 3 and 4 preserved;')
    print('  acyclic nested-cover counterexample rejects the retracted girth implication.')

if __name__=='__main__': main()
