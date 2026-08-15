#!/usr/bin/env python3
from __future__ import annotations
from itertools import product
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def bit(mask,x): return (mask >> sum(x[i]<<i for i in range(len(x))))&1

def essential(mask,j):
    for x in product((0,1),repeat=3):
        if x[j]: continue
        y=list(x);y[j]=1
        if bit(mask,x)!=bit(mask,tuple(y)): return True
    return False

def functional(mask):
    for b in (0,1):
        fib=[x for x in product((0,1),repeat=3) if bit(mask,x)==b]
        for h in range(3):
            tails=[j for j in range(3) if j!=h]; seen={}; ok=True
            for x in fib:
                key=(x[tails[0]],x[tails[1]])
                if key in seen and seen[key]!=x[h]: ok=False;break
                seen[key]=x[h]
            if ok: return True
    return False

def balanced(mask): return sum((mask>>i)&1 for i in range(8))==4

def affine(mask):
    vals=[(mask>>i)&1 for i in range(8)]; a=vals[:]
    for j in range(3):
        for i in range(8):
            if i&(1<<j): a[i]^=a[i^(1<<j)]
    return all(not a[i] or (i&(i-1))==0 for i in range(8))

def main():
    committed=json.loads((ROOT/'RESULTS.json').read_text())
    ess=[m for m in range(256) if all(essential(m,j) for j in range(3))]
    yes=[m for m in ess if functional(m)]; no=[m for m in ess if not functional(m)]
    assert len(ess)==218 and len(yes)==186 and len(no)==32
    assert all(functional(m) for m in ess if not balanced(m))
    assert all(balanced(m) and not affine(m) for m in no)
    c=committed['ternary_functional_classification']
    assert c['functional_anchor_masks']==186 and c['anchor_free_masks']==32
    for b in (0,1):
        fib=[x for x in product((0,1),repeat=3) if bit(0x1e,x)==b]
        mapping={}
        for x in fib:
            key=(x[0],x[1]); assert key not in mapping or mapping[key]==x[2]; mapping[key]=x[2]
        assert len(mapping)==4
    print('V101 independent verification passed: independent 186/32 functional census and total 0x1e graph witness.')
if __name__=='__main__': main()
