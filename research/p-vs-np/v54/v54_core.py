#!/usr/bin/env python3
from __future__ import annotations
from collections import deque
from itertools import combinations, permutations, product


def peel_two_core(n, edges):
    inc=[set() for _ in range(n)]
    alive_e=[True]*len(edges); alive_v=[True]*n
    for i,e in enumerate(edges):
        for v in set(e): inc[v].add(i)
    q=deque(v for v in range(n) if len(inc[v])<=1)
    while q:
        v=q.popleft()
        if not alive_v[v] or sum(alive_e[i] for i in inc[v])>1: continue
        alive_v[v]=False
        for i in list(inc[v]):
            if not alive_e[i]: continue
            alive_e[i]=False
            for u in set(edges[i]):
                inc[u].discard(i)
                if alive_v[u] and sum(alive_e[j] for j in inc[u])<=1: q.append(u)
    return [i for i,a in enumerate(alive_e) if a]


def certificate(n, edges):
    core=peel_two_core(n,edges)
    if not core: raise ValueError('empty 2-core')
    e=core[0]; witnesses=[]
    for v in edges[e]:
        f=next(j for j in core if j!=e and v in edges[j])
        if f not in witnesses: witnesses.append(f)
    return {'edge':e,'witnesses':witnesses,'degree':len(witnesses)+1}


def output(x, edges):
    y=0
    for i,e in enumerate(edges):
        b=1
        for v in e: b&=(x>>v)&1
        y|=b<<i
    return y


def target(m, cert):
    return sum(1<<f for f in cert['witnesses'])


def relation(y, cert, p=2):
    value=(1-((y>>cert['edge'])&1))%p
    for f in cert['witnesses']: value=value*((y>>f)&1)%p
    return value


def union_free(edges,t):
    seen=set()
    for d in range(t+1):
        for chosen in combinations(range(len(edges)),d):
            u=frozenset(v for i in chosen for v in edges[i])
            if u in seen:return False
            seen.add(u)
    return True


def npn_transform(mask,perm,negs,outneg):
    out=0
    for x in range(8):
        bits=[(x>>i)&1 for i in range(3)]
        old=[bits[perm[i]]^negs[i] for i in range(3)]
        idx=old[0]|(old[1]<<1)|(old[2]<<2)
        out|=((((mask>>idx)&1)^outneg)<<x)
    return out


def npn_classes():
    classes={}
    for mask in range(256):
        canonical=min(npn_transform(mask,p,n,o) for p in permutations(range(3)) for n in product((0,1),repeat=3) for o in (0,1))
        classes.setdefault(canonical,[]).append(mask)
    return classes


def singleton_fiber(mask):
    ones=[x for x in range(8) if (mask>>x)&1]
    zeros=[x for x in range(8) if not((mask>>x)&1)]
    return len(ones)==1 or len(zeros)==1


UF2=[[1,3,5],[1,3,4],[1,3,7],[0,2,4],[0,5,6],[0,3,5],[1,2,7],[2,6,7],[0,2,6]]
UF3=[[4,7,11],[5,10,13],[1,4,10],[8,11,12],[0,1,7],[3,7,12],[2,4,5],[5,8,14],[2,3,14],[2,10,12],[3,9,13],[2,9,11],[0,6,12],[0,8,13],[4,6,9],[1,9,14]]
