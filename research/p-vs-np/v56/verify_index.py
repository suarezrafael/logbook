#!/usr/bin/env python3
"""Compact standalone index verifier for Laboratory V56.

The full archive contains exhaustive primary and independent verifiers. This
repository entry point independently recomputes the ternary NPN/affine frontier
and the block-subspace dimension lemma using only the standard library.
"""
from __future__ import annotations
import itertools, json, random
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EXPECTED=[0x00,0x01,0x03,0x06,0x07,0x0f,0x16,0x17,0x18,0x19,0x1b,0x1e,0x3c,0x69]
AFFINE=[0x00,0x01,0x03,0x06,0x0f,0x18,0x3c,0x69]
ESSENTIAL_AFFINE=[0x01,0x06,0x18,0x69]
NONAFFINE=[0x07,0x16,0x17,0x19,0x1b,0x1e]


def transform(mask,perm,negs,outneg):
    out=0
    for x in range(8):
        nb=[(x>>i)&1 for i in range(3)]
        old=[nb[perm[i]]^negs[i] for i in range(3)]
        idx=old[0]|old[1]<<1|old[2]<<2
        out|=((((mask>>idx)&1)^outneg)<<x)
    return out


def orbit(mask):
    return {transform(mask,p,n,o) for p in itertools.permutations(range(3)) for n in itertools.product((0,1),repeat=3) for o in (0,1)}


def classes():
    remaining=set(range(256)); ans=[]
    while remaining:
        orb=orbit(min(remaining)); ans.append(min(orb)); remaining-=orb
    return sorted(ans)


def essential(mask):
    return sum(any(((mask>>x)&1)!=((mask>>(x^(1<<i)))&1) for x in range(8)) for i in range(3))


def xor_basis(values):
    piv={}
    for value in values:
        while value:
            p=value.bit_length()-1
            if p in piv:value^=piv[p]
            else:piv[p]=value;break
    return list(piv.values())


def affine(points):
    points=set(points)
    if not points:return False
    b=min(points); translated={x^b for x in points}
    return all((x^y) in translated for x in translated for y in translated)


def fiber(mask,value):
    return [x for x in range(8) if ((mask>>x)&1)==value]


def majority_closed(points):
    pts=set(points)
    return all(((a&b)|(a&c)|(b&c)) in pts for a in pts for b in pts for c in pts)


def rank(rows):
    return len(xor_basis(rows))


def block_redundant(blocks):
    total=rank([x for b in blocks for x in b])
    return any(rank([x for j,b in enumerate(blocks) if j!=i for x in b])==total for i in range(len(blocks)))


def main():
    cls=classes(); assert cls==EXPECTED
    affine_cls=[c for c in cls if affine(fiber(c,0)) or affine(fiber(c,1))]
    assert affine_cls==AFFINE
    assert [c for c in affine_cls if essential(c)==3]==ESSENTIAL_AFFINE
    assert [c for c in cls if essential(c)==3 and c not in affine_cls]==NONAFFINE
    assert [c for c in NONAFFINE if majority_closed(fiber(c,0)) and majority_closed(fiber(c,1))]==[0x07,0x17,0x1b]

    rng=random.Random(560057); checks=0
    for d in range(1,13):
        for _ in range(100):
            blocks=[[rng.randrange(1<<d) for _ in range(rng.randrange(4))] for _ in range(d+1)]
            assert block_redundant(blocks); checks+=1

    results=json.loads((ROOT/'RESULTS.json').read_text())
    assert results['version']=='V56' and results['status']=='passed'
    assert results['theorems']['consistency_or_redundancy_threshold']=='m>n'
    assert results['frontier']['essential_nonaffine_classes']==[f'0x{x:02x}' for x in NONAFFINE]
    assert results['validation']['failures']==0
    assert results['scientific_status']['general_nc0_3_avoid_solved'] is False
    assert results['scientific_status']['p_vs_np_resolved'] is False

    print(json.dumps({'npn_classes':len(cls),'affine_classes':len(affine_cls),'essential_affine':len(ESSENTIAL_AFFINE),'remaining_nonaffine':len(NONAFFINE),'block_checks':checks,'all_passed':True},indent=2))

if __name__=='__main__':main()
