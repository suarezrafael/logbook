#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, random
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SEED=650065

def load(p:Path): return json.loads(p.read_text(encoding='utf-8'))
def parity(x:int)->int: return x.bit_count()&1

def is_affine(mask:int,n:int)->bool:
    if mask==0: return False
    pts=[x for x in range(1<<n) if (mask>>x)&1]
    b=pts[0]; diffs={x^b for x in pts}
    return 0 in diffs and all((u^v) in diffs for u in diffs for v in diffs)

def affine_masks(n:int):
    return [m for m in range(1,1<<(1<<n)) if is_affine(m,n)]

def intersection(fam,full):
    r=full
    for x in fam:r&=x
    return r

def redundant_indices(fam,full):
    ans=[]
    for i,f in enumerate(fam):
        o=full
        for j,g in enumerate(fam):
            if i!=j:o&=g
        if o & ~f == 0: ans.append(i)
    return ans

def annihilator(fmask:int,n:int,xstar:int):
    us=[x^xstar for x in range(1<<n) if (fmask>>x)&1]
    return [a for a in range(1<<n) if all(parity(a&u)==0 for u in us)]

def span(vectors):
    s={0}
    for v in vectors:s|={x^v for x in list(s)}
    return s

def exact_affine_families():
    expected={1:6,2:286,3:316251}; total=inc=red=0; by_n={}
    for n in (1,2,3):
        A=affine_masks(n); full=(1<<(1<<n))-1; count=ci=cr=0
        assert len(A)=={1:3,2:11,3:51}[n]
        for idxs in itertools.combinations_with_replacement(range(len(A)),n+1):
            fam=[A[i] for i in idxs]; common=intersection(fam,full); count+=1
            if common==0:
                ci+=1; best=None
                for r in range(1,len(fam)+1):
                    if any(intersection([fam[i] for i in S],full)==0 for S in itertools.combinations(range(len(fam)),r)):
                        best=r; break
                assert best is not None and best<=n+1
            else:
                cr+=1; R=redundant_indices(fam,full); assert R
                xstar=(common & -common).bit_length()-1
                Ws=[annihilator(f,n,xstar) for f in fam]
                assert any(set(Ws[i])<=span(v for j,W in enumerate(Ws) if j!=i for v in W) for i in R)
        assert count==expected[n]
        by_n[str(n)]={'affine_subsets':len(A),'families':count,'inconsistent':ci,'redundant':cr}
        total+=count; inc+=ci; red+=cr
    assert total==316543 and inc+red==total
    return total,inc,red,by_n

def gf2_rref(rows,width):
    rows=[r for r in rows if r]; pivots=[]; i=0
    for col in range(width-1,-1,-1):
        p=next((k for k in range(i,len(rows)) if (rows[k]>>col)&1),None)
        if p is None: continue
        rows[i],rows[p]=rows[p],rows[i]
        for k in range(len(rows)):
            if k!=i and ((rows[k]>>col)&1): rows[k]^=rows[i]
        pivots.append(col); i+=1
    return rows[:i],pivots

def consistent_solution(eqs,n):
    rows,_=gf2_rref([a | (b<<n) for a,b,_ in eqs],n+1)
    if any((r&((1<<n)-1))==0 and ((r>>n)&1) for r in rows): return None
    for x in range(1<<n):
        if all(parity(a&x)==b for a,b,_ in eqs): return x
    raise AssertionError('rref said consistent but no solution')

def rank(rows):
    rows=list(rows)
    return len(gf2_rref(rows,max([1,*[x.bit_length() for x in rows]]))[0])

def random_equation_cases():
    rng=random.Random(SEED); cases=inconsistent=redundant=0
    for n in range(4,13):
        for mode in ('consistent','inconsistent'):
            for _ in range(24):
                m=n+1+rng.randrange(3); blocks=[]; xstar=rng.randrange(1<<n)
                for i in range(m):
                    rows=[]
                    for __ in range(rng.randrange(0,4)):
                        a=rng.randrange(1<<n); rows.append((a,parity(a&xstar),i))
                    blocks.append(rows)
                if mode=='inconsistent':
                    i=rng.randrange(m); blocks[i]=blocks[i]+[(0,1,i)]
                eqs=[e for B in blocks for e in B]; sol=consistent_solution(eqs,n)
                if sol is None:
                    inconsistent+=1; cur=list(eqs); changed=True
                    while changed:
                        changed=False
                        for e in list(cur):
                            trial=cur.copy(); trial.remove(e)
                            if consistent_solution(trial,n) is None:
                                cur=trial; changed=True; break
                    assert len(cur)<=n+1; owners={e[2] for e in cur}
                    for x in range(1<<n):
                        assert not all(all(parity(a&x)==b for a,b,_ in blocks[i]) for i in owners)
                else:
                    redundant+=1; total_rows=[a for B in blocks for a,_,__ in B]; rtot=rank(total_rows)
                    candidates=[]
                    for i in range(m):
                        other=[a for j,B in enumerate(blocks) if j!=i for a,_,__ in B]
                        if rank(other)==rtot:candidates.append(i)
                    assert candidates; i=candidates[0]
                    others=[(a,j) for j,B in enumerate(blocks) if j!=i for a,_,__ in B]
                    basis=[]; owners=[]
                    for a,j in others:
                        if rank([x for x,_ in basis]+[a])>rank([x for x,_ in basis]): basis.append((a,j)); owners.append(j)
                    J=set(owners); assert len(J)<=n
                    for x in range(1<<n):
                        activeJ=all(all(parity(a&x)==b for a,b,_ in blocks[j]) for j in J)
                        if activeJ: assert all(parity(a&x)==b for a,b,_ in blocks[i])
                cases+=1
    assert cases==432 and inconsistent==216 and redundant==216
    return cases,inconsistent,redundant

def metadata_and_documents():
    spec=load(HERE/'V56_AFFINE_FIBER_SPEC.json'); ledger=load(ROOT/'LEDGER.json')
    assert spec['laboratory']=='V65' and spec['conclusions']['separator_degree']=='at most n+1'
    assert ledger['schema_version']>=6 and ledger['current_version']=='V65'
    assert ledger['program']['p_vs_np_research_active'] is True
    assert ledger['program']['p_vs_np_route_active'] is False and ledger['program']['p_vs_np_resolved'] is False
    assert ledger['p_vs_np_route']['progress_percentage_forbidden'] is True
    assert any(v['version']=='V65' for v in ledger['versions'])
    runner=(ROOT/'verify_all.sh').read_text(encoding='utf-8')
    assert 'V65|primary|v65/verify.py|quick|' in runner and 'V65|independent|v65/verify_independent.py|quick|' in runner
    tex=(HERE/'V56_AFFINE_FIBER_THEOREM.tex').read_text(encoding='utf-8')
    route=(HERE/'P_VS_NP_ROUTE_AUDIT.md').read_text(encoding='utf-8')
    lit=(HERE/'LITERATURE_UPDATE_2026.md').read_text(encoding='utf-8')
    ext=(HERE/'EXTERNAL_RESPONSE_CHECK.md').read_text(encoding='utf-8')
    for t in ('Affine-fiber range avoidance','Minimal affine inconsistency','Complete-block redundancy','no claim that P differs from NP'): assert t in tex
    for t in ('ECCC TR22-048','ECCC TR23-021','ECCC TR25-049','ECCC TR25-191','ECCC TR26-118'): assert t in route and t in lit
    assert 'Direct P-versus-NP route active:** no' in (ROOT/'STATE.md').read_text(encoding='utf-8')
    assert 'Incoming replies found:** 0' in ext and 'Follow-up sent:** no' in ext
    return 24

def main():
    total,inc,red,by_n=exact_affine_families(); rcases,rinc,rred=random_equation_cases(); docs=metadata_and_documents()
    result={'version':'V65','status':'passed','exact_validation':{'dimensions':[1,2,3],'families':total,'inconsistent':inc,'redundant':red,'by_dimension':by_n},'generated_equation_cases':{'total':rcases,'inconsistent':rinc,'redundant':rred},'document_and_metadata_checks':docs,'scientific_status':{'peer_reviewed':False,'novelty_confirmed':False,'p_vs_np_research_active':True,'p_vs_np_route_active':False,'p_vs_np_resolved':False},'failures':0}
    (HERE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    checks=total+rcases+docs
    print(f'V65 primary verification passed: {checks} checks; {total} exact affine families; zero failures.')
if __name__=='__main__': main()
