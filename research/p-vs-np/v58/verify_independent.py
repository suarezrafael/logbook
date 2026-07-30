#!/usr/bin/env python3
"""Independent audit for V58. Does not import v58_core."""
from __future__ import annotations
import itertools, json, math, random, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def active_mask(n,d):
    p,l,r,f=d;v=0
    for x in range(1<<n):
        if (x>>p)&1: continue
        pair=((x>>l)&1)|(((x>>r)&1)<<1)
        if pair!=f:v|=1<<x
    return v

def descs(n):
    out=[]
    for p in range(n):
        o=[v for v in range(n) if v!=p]
        for l,r in itertools.combinations(o,2):
            for f in (1,2,3):out.append((p,l,r,f))
    return out

def redundants(sets,full):
    ans=[]
    for i,a in enumerate(sets):
        z=full
        for j,b in enumerate(sets):
            if i!=j:z&=b
        if z&~a==0:ans.append(i)
    return ans

def canon(family,n):
    best=None
    for perm in itertools.permutations(range(n)):
        cur=[]
        for p,l,r,f in family:
            p,a,b=perm[p],perm[l],perm[r]
            if a>b:a,b=b,a;f={1:2,2:1,3:3}[f]
            cur.append((p,a,b,f))
        cur=tuple(sorted(cur))
        best=cur if best is None or cur<best else best
    return best

def required(m,t,z):
    if z>2:return 0
    return sum(math.comb(m-t,j) for j in range(3-z))

def exact_no_ball2(n,cf):
    m=n+1;D=descs(n);first=(0,1,2,cf);D=[first]+[d for d in D if d!=first]
    masks=[active_mask(n,d) for d in D];full=(1<<(1<<n))-1
    cells={1:masks[0],0:full^masks[0]};nodes=0
    def rec(t,start,cells):
        nonlocal nodes;nodes+=1
        if t==m:return False # counterexample found => False means property fails
        for idx in range(start,len(D)):
            a=masks[idx];nextcells={};ok=True
            for pref,rows in cells.items():
                z=t-pref.bit_count();yes=rows&a;no=rows&~a&full
                ry=required(m,t+1,z);rn=required(m,t+1,z+1)
                if yes.bit_count()<ry or no.bit_count()<rn:ok=False;break
                if ry:nextcells[(pref<<1)|1]=yes
                if rn:nextcells[pref<<1]=no
            if ok and not rec(t+1,idx+1,nextcells):return False
        return True
    return rec(1,1,cells),nodes

def main():
    st=time.perf_counter();D=descs(4);M=[active_mask(4,d) for d in D];full=(1<<16)-1;fams=[]
    for ids in itertools.combinations(range(36),5):
        ss=[M[i] for i in ids]
        if not redundants(ss,full):fams.append(tuple(D[i] for i in ids))
    assert len(fams)==12 and len({canon(f,4) for f in fams})==1
    flips=0
    for fam in fams:
        ss=[active_mask(4,d) for d in fam]
        for i in range(5):
            oriented=[(full^a) if j==i else a for j,a in enumerate(ss)]
            z=full
            for a in oriented:z&=a
            assert z!=0
            assert redundants(oriented,full)
            flips+=1

    exact=[]
    for n in range(3,8):
        for cf in (1,3):
            ok,nodes=exact_no_ball2(n,cf)
            assert ok
            exact.append({'n':n,'canonical_type':cf,'nodes':nodes})

    # Independent direct-sum set audit through k=5.
    g4=((0,1,2,1),(0,1,2,2),(0,1,3,1),(0,1,3,2),(0,2,3,3))
    direct=0
    for k in range(6):
        ds=list(g4);off=4
        for _ in range(k):
            ds.extend(((off+2,off,off+1,1),(off+2,off,off+1,2),(off+2,off,off+1,3)));off+=3
        n=4+3*k;fulln=(1<<(1<<n))-1;sets=[active_mask(n,d) for d in ds]
        # Flipping the first G4 block always yields redundancy inside that component.
        oriented=[(fulln^a) if i==0 else a for i,a in enumerate(sets)]
        assert redundants(oriented,fulln)
        direct+=1

    # Independent combinatorial boundary equivalence.
    rng=random.Random(5858);boundary=0
    for m in range(2,7):
        cube=list(range(1<<m));allmask=(1<<m)-1
        for _ in range(100):
            image=set(rng.sample(cube,rng.randrange(1,1<<m)));base=rng.choice(tuple(image))
            bd=min(( (y^base).bit_count() for y in image if any((y^(1<<i)) not in image for i in range(m)) ),default=None)
            assert bd is not None
            for r in range(min(3,m)):
                ball={base^sum(1<<i for i in S) for s in range(r+2) for S in itertools.combinations(range(m),s)}
                assert (bd>r)==ball.issubset(image)
            boundary+=1

    output={'status':'passed','v57_families':12,'isomorphism_classes':1,'single_flips':flips,'independent_exact_cases':exact,'direct_sum_cases':direct,'boundary_checks':boundary,'failures':0,'elapsed_seconds':round(time.perf_counter()-st,6)}
    (ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print('V58 independent verification passed:')
    print('  12 V57 families collapsed to one isomorphism class;')
    print(f'  {flips} single flips independently checked;')
    print('  exact no-counterexample search independently rebuilt for n=3..7;')
    print(f'  {boundary} boundary/ball checks; zero failures.')
if __name__=='__main__':main()
