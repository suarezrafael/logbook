#!/usr/bin/env python3
from __future__ import annotations

def bit(tt,x): return (tt>>x)&1

def projection(i):
    out=0
    for x in range(8): out |= ((x>>i)&1)<<x
    return out

def affine_by_enumeration(tt):
    aff=set()
    for a in range(16):
        t=0
        for x in range(8):
            v=(a&1)
            for i in range(3):
                if (a>>(i+1))&1: v ^= (x>>i)&1
            t |= v<<x
        aff.add(t)
    return tt in aff

def relation(outputs):
    rel=[]
    for lam in range(16):
        vals=[]
        for x in range(8):
            v=0
            for i,t in enumerate(outputs):
                if (lam>>i)&1: v ^= bit(t,x)
            vals.append(v)
        if len(set(vals))==1: rel.append((lam,vals[0]))
    return tuple(rel)

def image(outputs):
    out=set()
    for x in range(8):
        y=sum(bit(t,x)<<i for i,t in enumerate(outputs))
        out.add(y)
    return out

def chosen_first(tt):
    ones=sum(bit(tt,x) for x in range(8)); zeros=8-ones
    return 0 if zeros<=ones else 1

def main():
    tail=(projection(0),projection(1),projection(2))
    aff=0; nonaff=0; bal_nonaff=0; unbal_nonaff=0; opp=0; same=0; partitions=0
    for f in range(256):
        g=f^255
        A=(f,)+tail; B=(g,)+tail
        if affine_by_enumeration(f):
            aff+=1
            continue
        nonaff+=1
        w=sum(bit(f,x) for x in range(8))
        if w==4: bal_nonaff+=1
        else: unbal_nonaff+=1
        assert relation(A)==((0,0),)
        assert relation(B)==((0,0),)
        same+=1
        IA=image(A); IB=image(B)
        assert not (IA & IB) and IA|IB==set(range(16))
        partitions+=1
        if w!=4:
            assert chosen_first(f)!=chosen_first(g)
            opp+=1
    assert (aff,nonaff,bal_nonaff,unbal_nonaff)==(16,240,56,184)
    assert same==240 and partitions==240 and opp==184
    print('V93 independent verification passed: direct truth-vector enumeration reproduces 16/240/56/184 and all certificate/range/decision collisions.')

if __name__=='__main__': main()
