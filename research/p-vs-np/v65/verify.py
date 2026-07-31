#!/usr/bin/env python3
from __future__ import annotations
import itertools,json,random
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;SEED=650065

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def parity(x):return x.bit_count()&1
def affine(points):
    if not points:return False
    b=min(points);d={x^b for x in points};return all((u^v) in d for u in d for v in d)
def affine_sets(n):
    return [frozenset(x for x in range(1<<n) if (mask>>x)&1) for mask in range(1,1<<(1<<n)) if affine({x for x in range(1<<n) if (mask>>x)&1})]
def rank(rows):
    basis={}
    for raw in rows:
        v=raw
        while v:
            p=v.bit_length()-1
            if p in basis:v^=basis[p]
            else:basis[p]=v;break
    return len(basis)
def consistent(eqs,n):
    for x in range(1<<n):
        if all(parity(a&x)==b for a,b,_ in eqs):return x
    return None
def exact_affine_families():
    expected={1:6,2:286,3:316251};total=inc=red=0;by_n={}
    for n in (1,2,3):
        sets=affine_sets(n);ci=cr=count=0;assert len(sets)=={1:3,2:11,3:51}[n]
        for indices in itertools.combinations_with_replacement(range(len(sets)),n+1):
            family=[sets[i] for i in indices];common=set.intersection(*(set(x) for x in family));count+=1
            if not common:
                ci+=1;assert any(not set.intersection(*(set(family[i]) for i in subset)) for r in range(1,n+2) for subset in itertools.combinations(range(n+1),r))
            else:
                cr+=1;assert any(set.intersection(*(set(family[j]) for j in range(n+1) if j!=i))<=family[i] for i in range(n+1))
        assert count==expected[n];by_n[str(n)]={'affine_subsets':len(sets),'families':count,'inconsistent':ci,'redundant':cr};total+=count;inc+=ci;red+=cr
    assert total==316543 and inc+red==total;return total,inc,red,by_n
def random_equation_cases():
    rng=random.Random(SEED);cases=bad=good=0
    for n in range(4,13):
        for mode in ('consistent','inconsistent'):
            for _ in range(24):
                m=n+1+rng.randrange(3);xstar=rng.randrange(1<<n);blocks=[]
                for i in range(m):blocks.append([(a,parity(a&xstar),i) for a in (rng.randrange(1<<n) for __ in range(rng.randrange(4)))])
                if mode=='inconsistent':blocks[rng.randrange(m)].append((0,1,rng.randrange(m)))
                eqs=[e for block in blocks for e in block];solution=consistent(eqs,n)
                if solution is None:
                    bad+=1;core=list(eqs);changed=True
                    while changed:
                        changed=False
                        for e in list(core):
                            trial=core.copy();trial.remove(e)
                            if consistent(trial,n) is None:core=trial;changed=True;break
                    assert len(core)<=n+1
                else:
                    good+=1;all_rows=[a for block in blocks for a,_,__ in block];total_rank=rank(all_rows)
                    assert any(rank([a for j,b in enumerate(blocks) if j!=i for a,_,__ in b])==total_rank for i in range(m))
                cases+=1
    assert (cases,bad,good)==(432,216,216);return cases,bad,good
def metadata_and_documents():
    spec=load(HERE/'V56_AFFINE_FIBER_SPEC.json');ledger=load(ROOT/'LEDGER.json')
    assert spec['laboratory']=='V65' and spec['conclusions']['separator_degree']=='at most n+1'
    assert ledger['schema_version']>=6 and int(ledger['current_version'][1:])>=65
    assert ledger['program']['p_vs_np_research_active'] is True and ledger['program']['p_vs_np_route_active'] is False and ledger['program']['p_vs_np_resolved'] is False
    assert ledger['p_vs_np_route']['progress_percentage_forbidden'] is True and any(v['version']=='V65' for v in ledger['versions'])
    runner=(ROOT/'verify_all.sh').read_text();assert 'V65|primary|v65/verify.py|quick|' in runner and 'V65|independent|v65/verify_independent.py|quick|' in runner
    tex=(HERE/'V56_AFFINE_FIBER_THEOREM.tex').read_text();route=(HERE/'P_VS_NP_ROUTE_AUDIT.md').read_text();lit=(HERE/'LITERATURE_UPDATE_2026.md').read_text();ext=(HERE/'EXTERNAL_RESPONSE_CHECK.md').read_text()
    for token in ('Affine-fiber range avoidance','Minimal affine inconsistency','Complete-block redundancy','no claim that P differs from NP'):assert token in tex
    for token in ('ECCC TR22-048','ECCC TR23-021','ECCC TR25-049','ECCC TR25-191','ECCC TR26-118'):assert token in route and token in lit
    assert 'P-versus-NP route active:** no' in (ROOT/'STATE.md').read_text() and 'Incoming replies found:** 0' in ext and 'Follow-up sent:** no' in ext
    return 24
def main():
    total,inc,red,by_n=exact_affine_families();cases,bad,good=random_equation_cases();docs=metadata_and_documents()
    result={'version':'V65','status':'passed','exact_validation':{'dimensions':[1,2,3],'families':total,'inconsistent':inc,'redundant':red,'by_dimension':by_n},'generated_equation_cases':{'total':cases,'inconsistent':bad,'redundant':good},'document_and_metadata_checks':docs,'scientific_status':{'peer_reviewed':False,'novelty_confirmed':False,'p_vs_np_research_active':True,'p_vs_np_route_active':False,'p_vs_np_resolved':False},'failures':0}
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(f'V65 primary verification passed: {total+cases+docs} checks; {total} exact affine families; zero failures.')
if __name__=='__main__':main()
