"""Independent V102 audit: no import from affine_backdoor.py."""
from itertools import combinations, permutations, product
import random


def val(mask,bits):
    idx=sum((b&1)<<j for j,b in enumerate(bits))
    return (mask>>idx)&1


def transform(mask,perm,neg,out):
    ans=0
    for x in product((0,1),repeat=3):
        old=[x[perm[i]]^neg[i] for i in range(3)]
        y=val(mask,old)^out
        ans |= y << (x[0] | x[1]<<1 | x[2]<<2)
    return ans


def orb(mask):
    return sorted({transform(mask,p,n,o)
                   for p in permutations(range(3))
                   for n in product((0,1),repeat=3)
                   for o in (0,1)})
MUX=orb(0x1b); MAJ=orb(0x17)


def moebius_degree(mask, free_positions, fixed):
    r=len(free_positions)
    table=[0]*(1<<r)
    for bits in product((0,1),repeat=r):
        x=[0,0,0]
        for i,v in fixed.items(): x[i]=v
        for j,pos in enumerate(free_positions): x[pos]=bits[j]
        idx=sum(bits[j]<<j for j in range(r))
        table[idx]=val(mask,x)
    coeff=table[:]
    for j in range(r):
        for s in range(1<<r):
            if s&(1<<j): coeff[s]^=coeff[s^(1<<j)]
    deg=0
    for s,c in enumerate(coeff):
        if c: deg=max(deg,s.bit_count())
    return deg


def strong_affine(mask,S):
    S=tuple(S); free=[i for i in range(3) if i not in S]
    for bits in product((0,1),repeat=len(S)):
        if moebius_degree(mask,free,dict(zip(S,bits)))>1:
            return False
    return True

for mask in MUX:
    good_single=[s for s in range(3) if strong_affine(mask,{s})]
    assert len(good_single)==1
    s=good_single[0]
    data=set(range(3))-{s}
    for r in range(4):
        for S in combinations(range(3),r):
            assert strong_affine(mask,S) == (s in S or data.issubset(S))
for mask in MAJ:
    for r in range(4):
        for S in combinations(range(3),r):
            assert strong_affine(mask,S) == (len(S)>=2)


def eval_circuit(circuit,x):
    return tuple(val(mask,[x[v] for v in supp]) for supp,mask in circuit)


def selector(mask):
    gs=[s for s in range(3) if strong_affine(mask,{s})]
    assert len(gs)==1
    return gs[0]


def branch_is_affine(circuit,B,sigma,n):
    free=[v for v in range(n) if v not in B]
    reps=[]
    for supp,mask in circuit:
        local_free=[v for v in supp if v not in B]
        def ev(assign):
            bits=[]
            for v in supp:
                bits.append(sigma[v] if v in B else assign.get(v,0))
            return val(mask,bits)
        c=ev({}); coef={v:ev({v:1})^c for v in local_free}
        for vals in product((0,1),repeat=len(local_free)):
            a=dict(zip(local_free,vals)); pred=c
            for v,b in a.items(): pred^=coef[v]&b
            assert pred==ev(a)
        reps.append((c,coef))
    return free,reps


def prefix_count_by_branch_enumeration(circuit,n,B,prefix):
    B=tuple(sorted(B)); total=0
    for sb in product((0,1),repeat=len(B)):
        sigma=dict(zip(B,sb)); free,_=branch_is_affine(circuit,set(B),sigma,n)
        for fb in product((0,1),repeat=len(free)):
            x=[0]*n
            for v,b in sigma.items(): x[v]=b
            for v,b in zip(free,fb): x[v]=b
            if eval_circuit(circuit,x)[:len(prefix)]==tuple(prefix): total+=1
    return total


def greedy(circuit,n,B):
    p=[]
    for _ in circuit:
        a=prefix_count_by_branch_enumeration(circuit,n,B,p+[0])
        b=prefix_count_by_branch_enumeration(circuit,n,B,p+[1])
        p.append(0 if a<=b else 1)
    return tuple(p)

rng=random.Random(204)
cases=0
for n in range(3,7):
    for _ in range(60):
        circuit=[]; B=set()
        for i in range(n+1):
            supp=tuple(rng.sample(range(n),3)); mask=rng.choice(MUX)
            circuit.append((supp,mask)); B.add(supp[selector(mask)])
        y=greedy(circuit,n,B)
        img={eval_circuit(circuit,x) for x in product((0,1),repeat=n)}
        assert y not in img
        cases+=1

for n in range(5,10):
    data=list(range(1,n)); edges=[]
    for i in range(len(data)):
        e=tuple(sorted((data[i],data[(i+1)%len(data)])))
        if e not in edges: edges.append(e)
    for a in data:
        for b in data:
            if a<b and (a,b) not in edges:
                edges.append((a,b))
                if len(edges)==n+1: break
        if len(edges)==n+1: break
    circuit=[((0,a,b),0x1b) for a,b in edges]
    degree=[0]*n
    for supp,_ in circuit:
        for v in supp: degree[v]+=1
    assert min(degree)>=2
    y=greedy(circuit,n,{0})
    assert y not in {eval_circuit(circuit,x) for x in product((0,1),repeat=n)}

print('V102 independent verification OK')
print('independent_random_mux_circuits',cases)
print('local_orbit_checks',len(MUX)+len(MAJ))
