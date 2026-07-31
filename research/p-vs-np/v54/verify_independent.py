#!/usr/bin/env python3
from collections import deque
from itertools import combinations


def core(n,edges):
    inc=[set() for _ in range(n)]; alive=[True]*len(edges); va=[True]*n
    for i,e in enumerate(edges):
        for v in e:inc[v].add(i)
    q=deque(v for v in range(n) if len(inc[v])<=1)
    while q:
        v=q.popleft()
        if not va[v] or sum(alive[i] for i in inc[v])>1:continue
        va[v]=False
        for i in list(inc[v]):
            if not alive[i]:continue
            alive[i]=False
            for u in edges[i]:
                inc[u].discard(i)
                if va[u] and sum(alive[j] for j in inc[u])<=1:q.append(u)
    return [i for i,a in enumerate(alive) if a]

def output(x,edges):
    y=0
    for i,e in enumerate(edges):
        b=1
        for v in e:b&=(x>>v)&1
        y|=b<<i
    return y

def check(n,edges):
    ce=core(n,edges);assert ce
    e=ce[0];w=[]
    for v in edges[e]:
        f=next(j for j in ce if j!=e and v in edges[j])
        if f not in w:w.append(f)
    target=sum(1<<f for f in w)
    for x in range(1<<n):
        y=output(x,edges); val=1-((y>>e)&1)
        for f in w:val*=((y>>f)&1)
        assert val==0 and y!=target
    return len(w)+1

def main():
    triples=list(combinations(range(5),3));count=0;dist={}
    for r in range(6,11):
        for inds in combinations(range(10),r):
            d=check(5,[triples[i] for i in inds]);dist[d]=dist.get(d,0)+1;count+=1
    tree=[(0,1,2),(0,3,4),(1,5,6),(2,7,8)]
    assert set().union(*(set(tree[i]) for i in (1,2,3)))==set().union(*(set(tree[i]) for i in (0,1,2,3)))
    assert count==386 and dist=={3:359,4:27}
    print('V54 independent verification passed:',count,dist)
if __name__=='__main__':main()
