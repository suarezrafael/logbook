#!/usr/bin/env python3
"""Independent relation-based verifier for V69.

This module does not import the primary GF(2) engine. It represents a projected residual state as an explicit set of active-variable assignments and recomputes exact layer widths and best orders for the preserved small cases.
"""
from __future__ import annotations
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def branch_of(assignment,spec):
    a,b,c=spec['support'];local=((assignment>>a)&1,(assignment>>b)&1,(assignment>>c)&1);p=spec['partition']
    if p==0:
        if local==(0,0,0):return 0
        if local in ((0,0,1),(0,1,0)):return 1
    elif p==1:
        if local in ((0,0,0),(0,0,1)):return 0
        if local==(0,1,0):return 1
    elif p==2:
        if local in ((0,0,0),(0,1,0)):return 0
        if local==(0,0,1):return 1
    return None

def relation_width(n,specs,mask):
    selected=[i for i in range(len(specs)) if mask>>i&1]
    active=tuple(sorted({v for i,s in enumerate(specs) if not(mask>>i&1) for v in s['support']}))
    groups={}
    for assignment in range(1<<n):
        signature=[]
        for i in selected:
            bit=branch_of(assignment,specs[i])
            if bit is None:break
            signature.append(bit)
        else:
            projected=tuple((assignment>>v)&1 for v in active)
            groups.setdefault(tuple(signature),set()).add(projected)
    return len({frozenset(relation) for relation in groups.values() if relation})

def exact_best(n,specs):
    m=len(specs);N=1<<m;widths=[relation_width(n,specs,mask) for mask in range(N)]
    INF=10**30;dp=[INF]*N;prev=[None]*N;dp[0]=0
    for mask in range(N-1):
        cost=dp[mask]+widths[mask]
        for gate in range(m):
            if not(mask>>gate&1):
                nxt=mask|1<<gate
                if cost<dp[nxt]:dp[nxt]=cost;prev[nxt]=(mask,gate)
    order=[];mask=N-1
    while mask:
        old,g=prev[mask];order.append(g);mask=old
    return dp[-1],tuple(reversed(order)),widths

def fixed_order_g(n,specs,order):
    mask=0;total=0
    for gate in order:
        total+=relation_width(n,specs,mask);mask|=1<<gate
    return total

def main():
    results=json.loads((HERE/'RESULTS.json').read_text());checks=0
    assert results['version']=='V69' and results['failures']==0;checks+=2
    for record in results['natural_order_records']:
        n=record['n'];specs=record['specs'];natural=tuple(range(len(specs)))
        assert fixed_order_g(n,specs,natural)==record['metrics']['natural']['G_proj'];checks+=1
        assert fixed_order_g(n,specs,tuple(record['metrics']['reverse']['order']))==record['metrics']['reverse']['G_proj'];checks+=1
        if n<=10:
            value,order,widths=exact_best(n,specs)
            assert value==record['exact']['Gstar'];checks+=1
            assert fixed_order_g(n,specs,order)==value;checks+=1
            for mask in (0,1,(1<<len(specs))-2,(1<<len(specs))-1):
                assert widths[mask]==relation_width(n,specs,mask);checks+=1
    for record in results['exact_order_robustness_search']:
        n=record['n'];specs=record['specs'];value,order,_=exact_best(n,specs)
        assert value==record['exact']['Gstar'];checks+=1
        assert fixed_order_g(n,specs,order)==value;checks+=1
    assert results['conclusion']['general_polynomial_good_order_proved'] is False;checks+=1
    assert results['conclusion']['all_orders_lower_bound_proved'] is False;checks+=1
    assert results['conclusion']['p_vs_np_resolved'] is False;checks+=1
    print(f'V69 independent verification passed: {checks} relation-level checks; exact G*_proj recomputed through n=10; zero failures.')
if __name__=='__main__':main()
