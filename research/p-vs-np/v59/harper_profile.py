from __future__ import annotations
import math, json

def simplicial_order(m):
    xs=list(range(1<<m))
    xs.sort(key=lambda x:(x.bit_count(), tuple(-((x>>i)&1) for i in range(m-1,-1,-1))))
    return xs

def profile(m):
    order=simplicial_order(m); S=set(); bnd=set(); best=(2,None,None)
    half=1<<(m-1)
    for idx,x in enumerate(order[:half],1):
        S.add(x)
        for y in [x]+[x^(1<<i) for i in range(m) if (x^(1<<i)) in S]:
            if any((y^(1<<j)) not in S for j in range(m)): bnd.add(y)
            else: bnd.discard(y)
        r=len(bnd)/idx
        if r<best[0]-1e-15: best=(r,idx,len(bnd))
    central=math.comb(m,m//2)
    exact=central/half
    return {'m':m,'minimum_ratio_in_simplicial_profile':best[0],'attained_size':best[1],'boundary':best[2],
            'half_size':half,'central_binomial_ratio':exact,'matches_half':best[1]==half and best[2]==central,
            'scaled_ratio_sqrt_m':exact*math.sqrt(m)}

def main():
    rows=[profile(m) for m in range(2,19)]
    out={'rows':rows,'all_match_half':all(r['matches_half'] for r in rows),'min_scaled_constant':min(r['scaled_ratio_sqrt_m'] for r in rows)}
    json.dump(out,open('/mnt/data/p_vs_np_lab_v59/HARPER_PROFILE.json','w'),indent=2)
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
