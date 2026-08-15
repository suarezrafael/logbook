#!/usr/bin/env python3
from __future__ import annotations
import json
from itertools import permutations, product
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def bit(mask,x): return (mask >> sum(x[i]<<i for i in range(len(x))))&1

def mask3(fn):
    m=0
    for x in product((0,1),repeat=3): m |= (fn(x)&1) << (x[0]+2*x[1]+4*x[2])
    return m

def essential(mask,j):
    for x in product((0,1),repeat=3):
        if x[j]: continue
        y=list(x); y[j]=1
        if bit(mask,x)!=bit(mask,tuple(y)): return True
    return False

def transform(mask,p,f,o): return mask3(lambda x: bit(mask,tuple(x[p[j]]^f[j] for j in range(3)))^o)
def canon(mask): return min(transform(mask,p,f,o) for p in permutations(range(3)) for f in product((0,1),repeat=3) for o in (0,1))
def peelable(mask):
    for b in (0,1):
        fib=[x for x in product((0,1),repeat=3) if bit(mask,x)==b]
        for v in range(3):
            if len({x[v] for x in fib})==1: return True
        for u in range(3):
            for v in range(u+1,3):
                if len({x[u]^x[v] for x in fib})==1: return True
    return False

def unate(mask,j):
    up=down=False
    for x in product((0,1),repeat=3):
        if x[j]: continue
        y=list(x); y[j]=1
        a,b=bit(mask,x),bit(mask,tuple(y));up|=b>a;down|=b<a
    return not (up and down)

def main():
    committed=json.loads((ROOT/'RESULTS.json').read_text())
    groups={}
    for mask in range(256):
        if all(essential(mask,j) for j in range(3)):
            groups.setdefault(canon(mask),[]).append(mask)
    sizes={c:len(ms) for c,ms in groups.items()}
    assert sum(sizes.values())==218
    good={c for c in groups if peelable(c)}
    assert good=={0x01,0x06,0x07,0x18,0x19}
    assert sum(sizes[c] for c in good)==144
    assert {c for c in groups if c not in good}=={0x16,0x17,0x1b,0x1e,0x69}
    assert not all(unate(0x19,j) for j in range(3))
    # 0x19 target-one fiber forces x0=x1 but fixes no coordinate.
    fib=[x for x in product((0,1),repeat=3) if bit(0x19,x)==1]
    assert all(x[0]==x[1] for x in fib)
    assert all(len({x[j] for x in fib})==2 for j in range(3))
    c=committed['ternary_classification']
    assert c['literal_graph_peelable_masks']==144 and c['residual_hard_masks']==74
    print('V100 independent verification passed: independent NPN classification and genuine pair-only 0x19 elimination witness.')
if __name__=='__main__': main()
