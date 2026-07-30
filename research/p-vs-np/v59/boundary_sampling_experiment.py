from __future__ import annotations
import itertools, random, json, math
from collections import Counter

def npn_transform(mask, perm, negs, outneg):
    t=0
    for x in range(8):
        nb=[(x>>i)&1 for i in range(3)]; ob=[nb[perm[i]]^negs[i] for i in range(3)]
        idx=ob[0]|(ob[1]<<1)|(ob[2]<<2); t |= ((((mask>>idx)&1)^outneg)<<x)
    return t
ORBIT=sorted({npn_transform(0x07,p,n,o) for p in itertools.permutations(range(3)) for n in itertools.product((0,1),repeat=3) for o in (0,1)})
def out(gates,x):
    yy=[]
    for mask,s in gates:
        loc=((x>>s[0])&1)|(((x>>s[1])&1)<<1)|(((x>>s[2])&1)<<2)
        yy.append((mask>>loc)&1)
    return tuple(yy)
def neigh(y,i):
    z=list(y);z[i]^=1;return tuple(z)
def run(seed=59059,cases=4000):
    rng=random.Random(seed); rows=[]
    for case in range(cases):
        n=rng.randint(5,10);m=n+1
        gates=[(rng.choice(ORBIT),tuple(rng.sample(range(n),3))) for _ in range(m)]
        counts=Counter(out(gates,x) for x in range(1<<n)); S=set(counts)
        bnd={y for y in S if any(neigh(y,i) not in S for i in range(m))}
        alpha=len(S)/(1<<n); p=sum(counts[y] for y in bnd)/(1<<n); q=len(bnd)/len(S)
        lower=alpha*(math.comb(m,m//2)/(2**(m-1)))
        rows.append((n,len(S),len(bnd),alpha,p,q,lower,p/lower if lower else None))
    byn=[]
    for n in range(5,11):
        rr=[r for r in rows if r[0]==n]
        byn.append({'n':n,'cases':len(rr),'mean_alpha':sum(r[3] for r in rr)/len(rr),'min_alpha':min(r[3] for r in rr),
                    'mean_input_boundary_probability':sum(r[4] for r in rr)/len(rr),'min_input_boundary_probability':min(r[4] for r in rr),
                    'mean_uniform_image_boundary_fraction':sum(r[5] for r in rr)/len(rr),'min_uniform_image_boundary_fraction':min(r[5] for r in rr),
                    'min_ratio_to_harper_sampling_bound':min(r[7] for r in rr)})
    outj={'cases':cases,'by_n':byn,'global':{'min_input_boundary_probability':min(r[4] for r in rows),
          'min_uniform_image_boundary_fraction':min(r[5] for r in rows),
          'min_ratio_to_harper_sampling_bound':min(r[7] for r in rows),
          'all_harper_bounds_pass':all(r[4]+1e-12>=r[6] for r in rows)}}
    json.dump(outj,open('/mnt/data/p_vs_np_lab_v59/BOUNDARY_SAMPLING_RESULTS.json','w'),indent=2)
    print(json.dumps(outj,indent=2))
if __name__=='__main__': run()
