#!/usr/bin/env python3
"""Independent audit.  Does not import v59_core."""
from __future__ import annotations
import itertools, json, math, random, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def local_mask(forbidden):
    mask=0; fl=forbidden&1; fr=(forbidden>>1)&1
    for loc in range(8):
        p=loc&1; a=(loc>>1)&1; b=(loc>>2)&1
        if p==0 and not(a==fl and b==fr): mask |= 1<<loc
    return mask

def gate(desc):
    p,a,b,f=desc; return local_mask(f),(p,a,b)
BASE=((0,1,2,1),(0,1,2,2),(0,1,3,1),(0,1,3,2),(0,2,3,3))
def family(k):
    desc=list(BASE); off=4
    for _ in range(k):
        desc += [(off+2,off,off+1,1),(off+2,off,off+1,2),(off+2,off,off+1,3)]; off+=3
    return 4+3*k,[gate(d) for d in desc]
def out(gates,x):
    bits=[]
    for mask,s in gates:
        loc=((x>>s[0])&1)|(((x>>s[1])&1)<<1)|(((x>>s[2])&1)<<2)
        bits.append((mask>>loc)&1)
    return tuple(bits)
def neighbours(y):
    for i in range(len(y)):
        z=list(y);z[i]^=1;yield tuple(z)
def forced(n,xs):
    aand=(1<<n)-1; oor=0
    for x in xs: aand&=x;oor|=x
    return n-(aand^oor).bit_count()

def main():
    started=time.perf_counter(); cases=[]
    for k in range(4):
        n,gates=family(k); by={}
        for x in range(1<<n): by.setdefault(out(gates,x),[]).append(x)
        S=set(by); boundary={y for y in S if any(z not in S for z in neighbours(y))}
        interior=S-boundary; one=(1,)*len(gates)
        assert interior=={one}
        assert len(by[one])==1
        assert forced(n,by[one])==n
        for z in neighbours(one):
            assert z in boundary and len(by[z])==1 and forced(n,by[z])==n
        cases.append({'k':k,'n':n,'m':len(gates),'image_size':len(S),'boundary_size':len(boundary)})

    constants=[]
    for m in range(2,25):
        value=math.comb(m,m//2)/(1<<(m-1))
        assert value*math.sqrt(m)>1.25
        constants.append(value)

    primary=json.loads((ROOT/'RESULTS.json').read_text(encoding='utf-8'))
    assert primary['status']=='passed'
    assert primary['validation']['direct_sum_cases']==4
    output={'status':'passed','direct_sum_cases':cases,'harper_checks':len(constants),'failures':0,
            'elapsed_seconds':round(time.perf_counter()-started,6)}
    (ROOT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print('V59 independent verification passed:')
    print('  4 direct-sum families reconstructed from scratch;')
    print(f'  {len(constants)} central-binomial expansion constants checked; zero failures.')
if __name__=='__main__':main()
