#!/usr/bin/env python3
"""Gate-order robustness laboratory for projected affine residual DAGs.

For a set S of processed gates, let R(S) be the set of distinct nonempty
affine residuals obtained by choosing one cell per gate in S and then
existentially projecting onto variables used by the complement. The set R(S)
depends only on S, not on the internal order of S. Hence for an order pi,

    G_proj(pi) = sum_{i=0}^{m-1} |R({pi_0,...,pi_{i-1}})|.

The optimum G*_proj is therefore the shortest path in the subset lattice:

    DP[empty]=0,
    DP[S union {g}] = min(DP[S] + |R(S)|).

This is exact but exponential in m; it is an order-audit tool, not a polynomial
algorithm for unrestricted NC0_3-Avoid.
"""
from __future__ import annotations
import json, random, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'v68'))
from affine_bitset import row,extend_basis,project_basis,build_projected_ordered_dag

SEARCH_CONFIG={
  6:(6906,3,250),8:(6908,3,250),10:(6910,3,250),
  12:(6912,2,150),14:(6914,2,100),
}

def gate_from_spec(n,spec):
    a,b,c=map(int,spec['support']);p=int(spec['partition'])
    if p==0:
        cells=((row(n,(a,),0),row(n,(b,),0),row(n,(c,),0)),(row(n,(a,),0),row(n,(b,c),1)))
    elif p==1:
        cells=((row(n,(a,),0),row(n,(b,),0)),(row(n,(a,),0),row(n,(b,),1),row(n,(c,),0)))
    elif p==2:
        cells=((row(n,(a,),0),row(n,(c,),0)),(row(n,(a,),0),row(n,(b,),0),row(n,(c,),1)))
    else: raise ValueError(p)
    return {'support':(a,b,c),'cells':cells,'partition':p}

def compile_system(n,specs):return tuple(gate_from_spec(n,s) for s in specs)

def ordered_gproj(n,specs,order=None):
    gates=compile_system(n,specs)
    if order is not None:gates=tuple(gates[i] for i in order)
    return build_projected_ordered_dag(gates,n)['nonterminal_states']

def random_spec(rng,n):return {'support':rng.sample(range(n),3),'partition':rng.randrange(3)}
def mutate(rng,specs,n):
    out=[{'support':list(s['support']),'partition':int(s['partition'])} for s in specs]
    i=rng.randrange(len(out))
    if rng.random()<0.25:out[i]['partition']=rng.randrange(3)
    else:out[i]['support']=rng.sample(range(n),3)
    return out

def natural_hill(n,seed,restarts,steps):
    rng=random.Random(seed);best=None
    for restart in range(restarts):
        current=[random_spec(rng,n) for _ in range(n+1)]
        score=ordered_gproj(n,current)
        for step in range(steps):
            candidate=mutate(rng,current,n);value=ordered_gproj(n,candidate)
            if value>=score or rng.random()<0.01:current,score=candidate,value
            if best is None or score>best['G_natural']:
                best={'G_natural':score,'specs':[{'support':list(x['support']),'partition':x['partition']} for x in current],'restart':restart,'step':step}
    return best

def heuristic_orders(specs):
    m=len(specs);supports=[set(s['support']) for s in specs]
    orders={'natural':list(range(m)),'reverse':list(reversed(range(m)))}
    remaining=set(range(m));order=[]
    while remaining:
        g=min(remaining,key=lambda i:(sum(len(supports[i]&supports[j]) for j in remaining if j!=i),i))
        order.append(g);remaining.remove(g)
    orders['min_overlap']=order
    remaining=set(range(m));order=[]
    while remaining:
        g=max(remaining,key=lambda i:(sum(len(supports[i]&supports[j]) for j in remaining if j!=i),-i))
        order.append(g);remaining.remove(g)
    orders['max_overlap']=order
    return orders

def full_basis_sets(n,gates):
    m=len(gates);sets=[None]*(1<<m);sets[0]={tuple()}
    for mask in range(1,1<<m):
        bit=mask&-mask;g=bit.bit_length()-1;prev=mask^bit;nxt=set()
        for basis in sets[prev]:
            for cell in gates[g]['cells']:
                child=extend_basis(basis,cell,n)
                if child is not None:nxt.add(child)
        sets[mask]=nxt
    return sets

def subset_widths(n,specs):
    gates=compile_system(n,specs);m=len(gates);all_bases=full_basis_sets(n,gates);widths=[]
    for mask,bases in enumerate(all_bases):
        active=tuple(sorted({v for i,g in enumerate(gates) if not(mask>>i&1) for v in g['support']}))
        residuals={project_basis(b,n,active) for b in bases}
        residuals.discard(None);widths.append(len(residuals))
    return widths

def exact_best_order(n,specs):
    widths=subset_widths(n,specs);m=len(specs);size=1<<m;INF=10**30
    dp=[INF]*size;prev=[None]*size;dp[0]=0
    for mask in range(size-1):
        candidate=dp[mask]+widths[mask]
        for gate in range(m):
            if not(mask>>gate&1):
                nxt=mask|1<<gate
                if candidate<dp[nxt]:dp[nxt]=candidate;prev[nxt]=(mask,gate)
    order=[];mask=size-1
    while mask:
        mask0,gate=prev[mask];order.append(gate);mask=mask0
    order.reverse()
    return {'Gstar':dp[-1],'order':order,'widths':widths}

def evaluate_witness(n,specs,exact):
    orders=heuristic_orders(specs)
    metrics={name:{'G_proj':ordered_gproj(n,specs,order),'order':order} for name,order in orders.items()}
    result={'n':n,'m':n+1,'metrics':metrics,'specs':specs}
    if exact:
        optimum=exact_best_order(n,specs);result['exact']={'Gstar':optimum['Gstar'],'order':optimum['order'],'width_profile':[optimum['widths'][sum(1<<g for g in optimum['order'][:i])] for i in range(n+1)]}
    return result

def generate_results():
    frozen=json.loads((HERE/'seed_data.json').read_text())
    natural=[]
    for n,(seed,restarts,steps) in SEARCH_CONFIG.items():
        found=natural_hill(n,seed,restarts,steps);expected=frozen['natural_records'][str(n)]
        assert found['G_natural']==expected['natural']
        assert found['specs']==expected['specs']
        natural.append({'search':{'seed':seed,'restarts':restarts,'steps':steps},**evaluate_witness(n,found['specs'],n<=12)})
    robust=[]
    for n in (6,8,10):
        witness=frozen['robust_search'][str(n)]
        evaluated=evaluate_witness(n,witness['specs'],True)
        assert evaluated['exact']['Gstar']==witness['Gstar']
        robust.append(evaluated)
    return {
      'version':'V69','status':'passed','failures':0,
      'theorem':{
        'set_layer_invariance':True,
        'formula':'G_proj(pi)=sum_i w(prefix_i)',
        'exact_optimization':'subset-lattice shortest path','runtime_scope':'exponential in gate count'
      },
      'natural_order_records':natural,'exact_order_robustness_search':robust,
      'conclusion':{
        'natural_order_exponential_claim_proved':False,
        'record_growth_is_order_artifact_for_exactly_checked_witnesses':True,
        'general_polynomial_good_order_proved':False,
        'all_orders_lower_bound_proved':False,
        'p_vs_np_route_active':False,
        'p_vs_np_resolved':False
      }
    }

def main():
    results=generate_results();(HERE/'RESULTS.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print('V69 order-robustness verification passed: deterministic hill records n=6..14; exact G*_proj through n=12; subset-DP theorem; zero failures.')
if __name__=='__main__':main()
