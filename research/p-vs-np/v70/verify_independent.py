#!/usr/bin/env python3
"""Independent relation-level verifier for V70.

No primary GF(2) implementation is imported. Residual relations are represented
as Python-integer bitsets over explicit assignments to active variables.
"""
from __future__ import annotations
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def branch_of(assignment,spec):
    a,b,c=map(int,spec['support']);local=((assignment>>a)&1,(assignment>>b)&1,(assignment>>c)&1);p=int(spec['partition'])
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

def gaussian_binomial_2(n,k):
    if k<0 or k>n:return 0
    a=b=1
    for i in range(k):a*=2**(n-i)-1;b*=2**(k-i)-1
    return a//b

def affine_count(n):return sum(2**(n-d)*gaussian_binomial_2(n,d) for d in range(n+1))

def overlap_components(specs,selected):
    selected=set(selected)
    if not selected:return []
    supp=[set(item['support']) for item in specs];adj={i:set() for i in selected};items=sorted(selected)
    for pos,i in enumerate(items):
        for j in items[pos+1:]:
            if supp[i]&supp[j]:adj[i].add(j);adj[j].add(i)
    seen=set();answer=[]
    for root in items:
        if root in seen:continue
        stack=[root];seen.add(root);component=[]
        while stack:
            current=stack.pop();component.append(current)
            for nxt in adj[current]:
                if nxt not in seen:seen.add(nxt);stack.append(nxt)
        answer.append(component)
    return answer

class RelationOracle:
    def __init__(self,n,specs):
        self.n=n;self.specs=specs;self.m=len(specs);self.supports=[set(item['support']) for item in specs]
        self.assignments=[]
        for assignment in range(1<<n):
            valid=branches=0
            for gate,spec in enumerate(specs):
                bit=branch_of(assignment,spec)
                if bit is not None:
                    valid|=1<<gate
                    if bit:branches|=1<<gate
            self.assignments.append((assignment,valid,branches))
        self.width_cache={}
    def active(self,mask):return tuple(sorted({v for i,s in enumerate(self.supports) if not(mask>>i&1) for v in s}))
    @staticmethod
    def project(assignment,variables):
        value=0
        for index,variable in enumerate(variables):value|=((assignment>>variable)&1)<<index
        return value
    def width_for(self,selected_mask,active_variables):
        groups={}
        for assignment,valid,branches in self.assignments:
            if valid&selected_mask!=selected_mask:continue
            signature=branches&selected_mask;projected=self.project(assignment,active_variables)
            groups[signature]=groups.get(signature,0)|(1<<projected)
        return len(set(groups.values()))
    def width(self,mask):
        if mask not in self.width_cache:self.width_cache[mask]=self.width_for(mask,self.active(mask))
        return self.width_cache[mask]
    def frontier(self,mask):
        left=set();right=set()
        for i,support in enumerate(self.supports):(left if mask>>i&1 else right).update(support)
        return left&right
    def component_product(self,mask):
        selected={i for i in range(self.m) if mask>>i&1};active=set(self.active(mask));product=1
        for component in overlap_components(self.specs,selected):
            component_mask=sum(1<<i for i in component);variables={v for i in component for v in self.supports[i]}
            product*=self.width_for(component_mask,tuple(sorted(active&variables)))
        return product
    def exact_best(self):
        size=1<<self.m;widths=[self.width(mask) for mask in range(size)];INF=10**30;dp=[INF]*size;previous=[None]*size;dp[0]=0
        for mask in range(size-1):
            candidate=dp[mask]+widths[mask]
            for gate in range(self.m):
                if mask>>gate&1:continue
                nxt=mask|1<<gate
                if candidate<dp[nxt]:dp[nxt]=candidate;previous[nxt]=(mask,gate)
        order=[];mask=size-1
        while mask:mask0,gate=previous[mask];order.append(gate);mask=mask0
        return dp[-1],list(reversed(order)),widths
    def fixed_order(self,order):
        mask=total=0
        for gate in order:total+=self.width(mask);mask|=1<<gate
        return total

def row(n,variables,rhs):
    value=(rhs&1)<<n
    for variable in variables:value^=1<<variable
    return value

def rref(equations,n,column_order=None):
    rows=[int(v) for v in equations if v];column_order=tuple(range(n)) if column_order is None else column_order;lead=0
    for column in column_order:
        chosen=next((i for i in range(lead,len(rows)) if (rows[i]>>column)&1),None)
        if chosen is None:continue
        rows[lead],rows[chosen]=rows[chosen],rows[lead];pivot=rows[lead]
        for i in range(len(rows)):
            if i!=lead and ((rows[i]>>column)&1):rows[i]^=pivot
        lead+=1
    coeff=(1<<n)-1
    if any(not(v&coeff) and ((v>>n)&1) for v in rows):return None
    rows=[v for v in rows if v&coeff];rows.sort(key=lambda v:((v&coeff)&-(v&coeff)).bit_length()-1);return tuple(rows)

def project(basis,n,active):
    active=tuple(sorted(active));aset=set(active);dead=tuple(v for v in range(n) if v not in aset);reduced=rref(basis,n,dead+active)
    if reduced is None:return None
    deadmask=sum(1<<v for v in dead);return rref(tuple(v for v in reduced if not(v&deadmask)),n,active)

def cells_for_spec(n,spec):
    a,b,c=map(int,spec['support']);p=int(spec['partition'])
    if p==0:return ((row(n,(a,),0),row(n,(b,),0),row(n,(c,),0)),(row(n,(a,),0),row(n,(b,c),1)))
    if p==1:return ((row(n,(a,),0),row(n,(b,),0)),(row(n,(a,),0),row(n,(b,),1),row(n,(c,),0)))
    return ((row(n,(a,),0),row(n,(c,),0)),(row(n,(a,),0),row(n,(b,),0),row(n,(c,),1)))

def fixed_order_affine(n,specs,order):
    ordered=[specs[i] for i in order];suffix=[{v for spec in ordered[index:] for v in spec['support']} for index in range(len(ordered)+1)];states={tuple()};total=0
    for index,spec in enumerate(ordered):
        total+=len(states);next_states=set()
        for basis in states:
            for cell in cells_for_spec(n,spec):
                child=rref(basis+cell,n)
                if child is not None:
                    child=project(child,n,suffix[index+1])
                    if child is not None:next_states.add(child)
        states=next_states
    return total

def main():
    results=json.loads((HERE/'RESULTS.json').read_text());witnesses=json.loads((HERE/'WITNESSES.json').read_text());checks=0
    assert results['version']=='V70' and results['failures']==0;checks+=2
    assert [affine_count(i) for i in range(6)]==[1,3,11,51,307,2451];checks+=6
    oracles={}
    for record in witnesses['new_exact_objective_records']:
        oracle=RelationOracle(record['n'],record['specs']);oracles[record['n']]=oracle;value,order,widths=oracle.exact_best()
        assert value==record['Gstar'];checks+=1;assert oracle.fixed_order(order)==value;checks+=1
        for mask,width in enumerate(widths):
            assert width<=min(1<<mask.bit_count(),affine_count(len(oracle.frontier(mask))));checks+=1
    improved=witnesses['improved_fixed_order_upper_bound'];assert fixed_order_affine(improved['n'],improved['specs'],improved['order'])==41;checks+=1
    v69=json.loads((HERE.parent/'v69'/'seed_data.json').read_text());systems=[RelationOracle(6,v69['natural_records']['6']['specs']),oracles[8]];component_checks=0
    for oracle in systems:
        for mask in range(1<<oracle.m):assert oracle.width(mask)==oracle.component_product(mask);checks+=1;component_checks+=1
    assert component_checks==640
    assert results['scientific_status']['general_polynomial_good_order_proved'] is False;checks+=1
    assert results['scientific_status']['p_vs_np_resolved'] is False;checks+=1
    print(f'V70 independent verification passed: {checks} relation-level checks; exact G*=29 and 30; support bounds and 640 component cuts; zero failures.')
if __name__=='__main__':main()
