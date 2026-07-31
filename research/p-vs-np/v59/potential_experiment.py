from __future__ import annotations
import itertools, random, math, json
from collections import Counter, defaultdict
from functools import lru_cache

Gate=tuple[int,tuple[int,int,int]]

def npn_transform(mask, perm, negs, outneg):
    t=0
    for x in range(8):
        nb=[(x>>i)&1 for i in range(3)]; ob=[nb[perm[i]]^negs[i] for i in range(3)]
        idx=ob[0]|(ob[1]<<1)|(ob[2]<<2); t|=((((mask>>idx)&1)^outneg)<<x)
    return t
ORBIT07=sorted({npn_transform(0x07,p,n,o) for p in itertools.permutations(range(3)) for n in itertools.product((0,1),repeat=3) for o in (0,1)})

def local_assignment(x,s): return ((x>>s[0])&1)|(((x>>s[1])&1)<<1)|(((x>>s[2])&1)<<2)
def output(gates,x): return tuple((mask>>local_assignment(x,s))&1 for mask,s in gates)
def neighbors(y):
    for i in range(len(y)):
        z=list(y); z[i]^=1; yield tuple(z)

def eval_lit(lit,x): v,pos=lit; return bool((x>>v)&1) if pos else not bool((x>>v)&1)
def eval_clause(cl,x): return any(eval_lit(l,x) for l in cl)
@lru_cache(None)
def local_2cnf(mask,val):
    pts=[x for x in range(8) if ((mask>>x)&1)==val]
    cand=[]
    for v in range(3):
        for s in (False,True): cand.append(((v,s),))
    for a,b in itertools.combinations(range(3),2):
        for sa in (False,True):
            for sb in (False,True): cand.append(((a,sa),(b,sb)))
    valid=[cl for cl in cand if all(eval_clause(cl,x) for x in pts)]
    red=list(valid); changed=True
    while changed:
        changed=False
        for i,cl in enumerate(tuple(red)):
            others=red[:i]+red[i+1:]
            models=[x for x in range(8) if all(eval_clause(c,x) for c in others)]
            if all(eval_clause(cl,x) for x in models): red.pop(i); changed=True; break
    return tuple(red)
def global_clauses(gates,y):
    out=[]
    for (mask,supp),val in zip(gates,y):
        for cl in local_2cnf(mask,val): out.append(tuple((supp[v],sgn) for v,sgn in cl))
    return out
def unit_forced(n,clauses):
    val=[None]*n; changed=True
    while changed:
        changed=False
        for cl in clauses:
            sat=False; undec=[]
            for v,pos in cl:
                if val[v] is None: undec.append((v,pos))
                elif bool(val[v])==pos: sat=True; break
            if sat: continue
            if not undec: return n+1
            if len(undec)==1:
                v,pos=undec[0]; need=int(pos)
                if val[v] is not None and val[v]!=need: return n+1
                if val[v] is None: val[v]=need; changed=True
    return sum(v is not None for v in val)
def exact_forced(n,xs):
    aand=(1<<n)-1; oor=0
    for x in xs: aand&=x; oor|=x
    varying=aand^oor
    return n-varying.bit_count()
def analyze(n,gates):
    by=defaultdict(list)
    for x in range(1<<n): by[output(gates,x)].append(x)
    S=set(by); bnd={y for y in S if any(z not in S for z in neighbors(y))}
    forced={y:exact_forced(n,xs) for y,xs in by.items()}
    unit={y:unit_forced(n,global_clauses(gates,y)) for y in S}
    badF=[]; badU=[]; badI=[]
    for y in S-bnd:
        ns=list(neighbors(y))
        if max(forced[z] for z in ns)<=forced[y]: badF.append(y)
        if max(unit[z] for z in ns)<=unit[y]: badU.append(y)
        if min(len(by[z]) for z in ns)>=len(by[y]): badI.append(y)
    counts={y:len(xs) for y,xs in by.items()}
    return dict(n=n,m=len(gates),image_size=len(S),boundary_size=len(bnd),boundary_fraction_image=len(bnd)/len(S),
                boundary_probability_uniform_input=sum(counts[y] for y in bnd)/(1<<n),occupancy_alpha=len(S)/(1<<n),
                bad_forced_count=len(badF),bad_unit_count=len(badU),bad_exact_fiber_count=len(badI),
                forced_counterexample=badF[0] if badF else None,unit_counterexample=badU[0] if badU else None,
                fiber_counterexample=badI[0] if badI else None, counts=counts,forced=forced,unit=unit,boundary=bnd)
def random_circuit(rng,n): return [(rng.choice(ORBIT07),tuple(rng.sample(range(n),3))) for _ in range(n+1)]
def local_mask_for_forbidden(f):
    fl=f&1; fr=(f>>1)&1; mask=0
    for loc in range(8):
        p=loc&1;l=(loc>>1)&1;r=(loc>>2)&1
        if p==0 and not(l==fl and r==fr): mask|=1<<loc
    return mask
def desc_gate(d): p,a,b,f=d; return local_mask_for_forbidden(f),(p,a,b)
G4=((0,1,2,1),(0,1,2,2),(0,1,3,1),(0,1,3,2),(0,2,3,3))
def stretch(k):
    r=list(G4);off=4
    for _ in range(k):
        r += [(off+2,off,off+1,1),(off+2,off,off+1,2),(off+2,off,off+1,3)];off+=3
    return 4+3*k,[desc_gate(d) for d in r]
def slim(a): return {k:v for k,v in a.items() if k not in ('counts','forced','unit','boundary')}

def main():
    rng=random.Random(5902026); rows=[]; first={}
    for n in range(4,9):
        for t in range(60):
            gates=random_circuit(rng,n); a=analyze(n,gates); rows.append(slim(a))
            for typ,key in [('forced','forced_counterexample'),('unit','unit_counterexample'),('fiber','fiber_counterexample')]:
                if typ not in first and a[key] is not None:
                    y=a[key]; pot=a['forced'] if typ=='forced' else a['unit'] if typ=='unit' else {q:-math.log2(c) for q,c in a['counts'].items()}
                    first[typ]={'n':n,'gates':[(m,list(s)) for m,s in gates],'orientation':list(y),'potential':pot[y],
                                'neighbor_potentials':[pot[z] for z in neighbors(y)],'image_size':a['image_size']}
    agg=[]
    for n in range(4,9):
        rr=[r for r in rows if r['n']==n]
        agg.append({'n':n,'cases':len(rr),'mean_boundary_fraction_image':sum(r['boundary_fraction_image'] for r in rr)/len(rr),
                    'min_boundary_fraction_image':min(r['boundary_fraction_image'] for r in rr),
                    'mean_input_boundary_probability':sum(r['boundary_probability_uniform_input'] for r in rr)/len(rr),
                    'min_input_boundary_probability':min(r['boundary_probability_uniform_input'] for r in rr),
                    'mean_alpha':sum(r['occupancy_alpha'] for r in rr)/len(rr),
                    'forced_fail_cases':sum(r['bad_forced_count']>0 for r in rr),
                    'unit_fail_cases':sum(r['bad_unit_count']>0 for r in rr),
                    'ideal_fiber_fail_cases':sum(r['bad_exact_fiber_count']>0 for r in rr)})
    adv=[]
    for k in range(3):
        n,g=stretch(k); adv.append(slim(analyze(n,g)))
    out={'orbit_size':len(ORBIT07),'aggregate':agg,'first_counterexamples':first,'adversarial_direct_sum':adv,'raw_cases':len(rows)}
    json.dump(out,open('/mnt/data/p_vs_np_lab_v59/EXPLORATION_RESULTS.json','w'),indent=2)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
