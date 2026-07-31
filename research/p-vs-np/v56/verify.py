#!/usr/bin/env python3
"""Repository-complete verifier for V56.

Self-contained: no private/generated module is required. It reproduces the
published exhaustive counts and independently checks the set-theoretic form of
the consistency-or-redundancy certificate on every tested circuit.
"""
from __future__ import annotations
import itertools, random, json, time
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SEED=560056

def transform(mask,perm,negs,outneg):
    out=0
    for x in range(8):
        b=[(x>>i)&1 for i in range(3)]
        old=[b[perm[i]]^negs[i] for i in range(3)]
        idx=old[0]|(old[1]<<1)|(old[2]<<2)
        out|=((((mask>>idx)&1)^outneg)<<x)
    return out

def orbit(mask):
    return tuple(sorted({transform(mask,p,n,o) for p in itertools.permutations(range(3)) for n in itertools.product((0,1),repeat=3) for o in (0,1)}))

def classes():
    rem=set(range(256)); ans=[]
    while rem:
        seed=min(rem); orb=orbit(seed); ans.append((min(orb),orb)); rem.difference_update(orb)
    return ans

def essential(mask):
    return sum(any(((mask>>x)&1)!=((mask>>(x^(1<<v)))&1) for x in range(8)) for v in range(3))

def affine(points):
    pts=set(points)
    if not pts: return False
    base=next(iter(pts)); lin={x^base for x in pts}
    if 0 not in lin or len(lin)&(len(lin)-1): return False
    return all(a^b in lin for a in lin for b in lin)

def fiber(mask,val): return frozenset(x for x in range(8) if ((mask>>x)&1)==val)

def orientation(mask):
    for val in (0,1):
        pts=fiber(mask,val)
        if pts and affine(pts): return val,pts
    return None

def local(x,support):
    return sum(((x>>v)&1)<<i for i,v in enumerate(support))

def active_set(n,mask,support):
    val,_=orientation(mask)
    return frozenset(x for x in range(1<<n) if ((mask>>local(x,support))&1)==val)

def certificate(n,gates):
    sets=[active_set(n,m,s) for m,s in gates]; U=set(range(1<<n))
    common=U.copy()
    for S in sets: common&=S
    if not common:
        return 'INCONSISTENT',tuple(1 for _ in gates),None
    for i,S in enumerate(sets):
        others=U.copy()
        for j,T in enumerate(sets):
            if i!=j: others&=T
        if others<=S:
            target=[1]*len(gates); target[i]=0
            return 'REDUNDANT',tuple(target),i
    raise AssertionError('affine stretch-one family should be inconsistent or redundant')

def output(n,gates,x): return tuple((m>>local(x,s))&1 for m,s in gates)

def absent(n,gates,target): return all(output(n,gates,x)!=target for x in range(1<<n))

def main():
    start=time.perf_counter(); rng=random.Random(SEED)
    cls=classes(); assert len(cls)==14 and sum(len(o) for _,o in cls)==256
    canonical=[c for c,_ in cls]
    assert canonical==[0x00,0x01,0x03,0x06,0x07,0x0f,0x16,0x17,0x18,0x19,0x1b,0x1e,0x3c,0x69]
    affine_cls=[c for c,o in cls if any(orientation(m) for m in o)]
    assert affine_cls==[0x00,0x01,0x03,0x06,0x0f,0x18,0x3c,0x69]
    essential_affine=[c for c,o in cls if essential(c)==3 and any(orientation(m) for m in o)]
    assert essential_affine==[0x01,0x06,0x18,0x69]
    affine_masks=tuple(sorted({m for c,o in cls if c in affine_cls for m in o}))
    assert len(affine_masks)==88

    branches=Counter(); count06=0
    for masks in itertools.combinations_with_replacement(orbit(0x06),4):
        gates=[(m,(0,1,2)) for m in masks]; branch,target,index=certificate(3,gates)
        assert absent(3,gates,tuple(orientation(m)[0] if t else 1-orientation(m)[0] for (m,_),t in zip(gates,target)))
        branches[branch]+=1; count06+=1
    assert count06==17550

    count01=0
    for masks in itertools.combinations_with_replacement(orbit(0x01),4):
        gates=[(m,(0,1,2)) for m in masks]; branch,target,index=certificate(3,gates)
        original=tuple(orientation(m)[0] if t else 1-orientation(m)[0] for (m,_),t in zip(gates,target))
        assert absent(3,gates,original); branches[branch]+=1; count01+=1
    assert count01==3876

    consistent=random_mixed=repeated=0
    for n in range(3,13):
        for _ in range(35):
            witness=random.Random(SEED+n+_).randrange(1<<n); gates=[]
            for __ in range(n+1):
                support=tuple(rng.sample(range(n),3))
                eligible=[m for m in affine_masks if local(witness,support) in orientation(m)[1]]
                gates.append((rng.choice(eligible),support))
            branch,target,index=certificate(n,gates); assert branch=='REDUNDANT'
            original=tuple(orientation(m)[0] if t else 1-orientation(m)[0] for (m,_),t in zip(gates,target))
            assert absent(n,gates,original); consistent+=1
        for _ in range(35):
            gates=[(rng.choice(affine_masks),tuple(rng.sample(range(n),3))) for __ in range(n+1)]
            branch,target,index=certificate(n,gates)
            original=tuple(orientation(m)[0] if t else 1-orientation(m)[0] for (m,_),t in zip(gates,target))
            assert absent(n,gates,original); random_mixed+=1
    for n in range(2,9):
        for _ in range(30):
            gates=[(rng.choice(affine_masks),tuple(rng.randrange(n) for __ in range(3))) for ___ in range(n+1)]
            branch,target,index=certificate(n,gates)
            original=tuple(orientation(m)[0] if t else 1-orientation(m)[0] for (m,_),t in zip(gates,target))
            assert absent(n,gates,original); repeated+=1

    abstract=0
    for d in range(1,13):
        for _ in range(60):
            blocks=[]
            for __ in range(d+1): blocks.append([rng.randrange(1<<d) for ___ in range(rng.randrange(4))])
            def rank(rows):
                piv={}
                for raw in rows:
                    v=raw
                    while v:
                        p=v.bit_length()-1
                        if p in piv: v^=piv[p]
                        else: piv[p]=v; break
                return len(piv)
            total=rank([v for b in blocks for v in b])
            assert any(rank([v for j,b in enumerate(blocks) if j!=i for v in b])==total for i in range(len(blocks)))
            abstract+=1

    result={'status':'passed','npn_classes':14,'affine_classes':8,'essential_affine':4,
            'distance_two_multisets':count06,'singleton_multisets':count01,
            'consistent_mixed':consistent,'unconditioned_mixed':random_mixed,
            'repeated_support':repeated,'abstract_block_checks':abstract,
            'branches':dict(branches),'failures':0,'elapsed_seconds':round(time.perf_counter()-start,6)}
    (ROOT/'REPO_VALIDATION_RESULTS.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print('V56 repository-complete verification passed:')
    print('  14/14 NPN classes; 8 affine-orientable; 4 essential affine;')
    print('  17550 distance-two and 3876 singleton multisets;')
    print('  350 consistent + 350 unconditioned mixed circuits;')
    print('  210 repeated-support circuits; 720 block checks; zero failures.')
if __name__=='__main__': main()
