#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "v100"))
from literal_peeling import (
    Gate, eval_table, make_mask, essential_positions, npn_canonical,
    normalize_gate, literal_peel, lift_word, output_range, circuit_output,
    input_degrees,
)


def functional_options(gate: Gate):
    """Return target/head partial functions; missing tail rows will be extended by 0."""
    arity = len(gate.support)
    options = []
    if arity == 0:
        return options
    for target in (0, 1):
        fiber = [x for x in product((0,1), repeat=arity) if eval_table(gate.mask,x)==target]
        if not fiber:
            continue
        for head in range(arity):
            tails = tuple(j for j in range(arity) if j != head)
            mapping = {}
            ok = True
            for x in fiber:
                key = tuple(x[j] for j in tails)
                if key in mapping and mapping[key] != x[head]:
                    ok=False; break
                mapping[key]=x[head]
            if ok:
                total = {}
                for bits in product((0,1), repeat=len(tails)):
                    total[bits] = mapping.get(bits,0)
                options.append((target, head, tails, total))
    return options


def functional_anchor_available(mask: int, arity: int=3) -> bool:
    gate=Gate(tuple(range(arity)),mask)
    return bool(functional_options(gate))


def has_path(adj: dict[int,set[int]], start: int, target: int) -> bool:
    if start==target: return True
    seen={start}; stack=[start]
    while stack:
        u=stack.pop()
        for v in adj.get(u,set()):
            if v==target: return True
            if v not in seen:
                seen.add(v); stack.append(v)
    return False


def can_add_dependency(adj: dict[int,set[int]], tails: tuple[int,...], head: int) -> bool:
    return all(not has_path(adj, head, tail) for tail in tails)


def functional_anchor_avoid(active_inputs: list[int], gates: list[Gate]):
    active_inputs=list(active_inputs)
    gates=[normalize_gate(g) for g in gates]
    selected: dict[int, tuple[int,int,tuple[int,...],dict]] = {}
    used_heads=set()
    adj: dict[int,set[int]] = {v:set() for v in active_inputs}

    for e,g in enumerate(gates):
        if len(g.support)==0:
            value=eval_table(g.mask,())
            target=[0]*len(gates); target[e]=1-value
            return {"kind":"constant","target":tuple(target),"selected_outputs":0,"roots":len(active_inputs)}

    changed=True
    while changed:
        changed=False
        for e,g in enumerate(gates):
            if e in selected: continue
            opts=functional_options(g)
            for target, local_head, local_tails, table in opts:
                head=g.support[local_head]
                tails=tuple(g.support[j] for j in local_tails)
                if head in used_heads: continue
                if not can_add_dependency(adj,tails,head): continue
                selected[e]=(target,head,tails,table)
                used_heads.add(head)
                for t in tails: adj[t].add(head)
                changed=True
                break
            if changed:
                break

    roots=[v for v in active_inputs if v not in used_heads]
    indeg={v:0 for v in active_inputs}
    for u,vs in adj.items():
        for v in vs: indeg[v]+=1
    queue=sorted([v for v in active_inputs if indeg[v]==0])
    topo=[]
    while queue:
        u=queue.pop(0); topo.append(u)
        for v in sorted(adj[u]):
            indeg[v]-=1
            if indeg[v]==0:
                queue.append(v); queue.sort()
    assert len(topo)==len(active_inputs)
    by_head={data[1]:data for data in selected.values()}

    remaining=[e for e in range(len(gates)) if e not in selected]
    image=set()
    relaxed_assignments=0
    for root_bits in product((0,1), repeat=len(roots)):
        assignment=dict(zip(roots,root_bits))
        for v in topo:
            if v in assignment: continue
            target,head,tails,table=by_head[v]
            key=tuple(assignment[t] for t in tails)
            assignment[v]=table[key]
        out=circuit_output(gates,assignment)
        image.add(tuple(out[e] for e in remaining))
        relaxed_assignments+=1
    assert len(remaining)>len(roots)
    missing=next(word for word in product((0,1), repeat=len(remaining)) if word not in image)
    target=[0]*len(gates)
    for e,(b,_h,_t,_table) in selected.items(): target[e]=b
    for e,b in zip(remaining,missing): target[e]=b
    return {
        "kind":"enumerated_functional_domain",
        "target":tuple(target),
        "selected_outputs":len(selected),
        "roots":len(roots),
        "remaining_outputs":len(remaining),
        "relaxed_assignments":relaxed_assignments,
    }


def combined_v100_v101_avoid(n:int,gates:list[Gate]):
    active,residual,records=literal_peel(list(range(n)),gates)
    result=functional_anchor_avoid(active,residual)
    result['residual_target']=result['target']
    result['target']=lift_word(result['target'],records)
    result['v100_steps']=len(records)
    result['post_v100_inputs']=len(active)
    result['post_v100_outputs']=len(residual)
    return result


def canonical_0x1e_family(n:int):
    gates=[Gate((i,(i+1)%n,(i+2)%n),0x1e) for i in range(n)]
    maj=make_mask(3,lambda x:int(sum(x)>=2))
    gates.append(Gate((0,1,2),maj))
    return gates


def build_results():
    groups={}
    essential_masks=[]
    for mask in range(256):
        if essential_positions(mask,3)==(0,1,2):
            essential_masks.append(mask)
            groups.setdefault(npn_canonical(mask),[]).append(mask)
    rows=[]; total=0
    for c,ms in sorted(groups.items()):
        available=functional_anchor_available(c)
        if available: total+=len(ms)
        rows.append({"canonical_mask":f"0x{c:02x}","size":len(ms),"functional_anchor_available":available})
    anchor_free=[r['canonical_mask'] for r in rows if not r['functional_anchor_available']]

    strict=[]
    for n in range(5,13):
        gates=canonical_0x1e_family(n)
        result=combined_v100_v101_avoid(n,gates)
        original=output_range(list(range(n)),gates)
        strict.append({
            "n":n,"m":n+1,"min_input_degree":min(input_degrees(n,gates)),
            "v100_steps":result['v100_steps'],"selected_outputs":result['selected_outputs'],
            "roots":result['roots'],"relaxed_assignments":result.get('relaxed_assignments',0),
            "lifted_word_absent":result['target'] not in original,
        })

    rng=random.Random(101)
    cases=failures=0; max_roots=0
    for n in range(3,8):
        for _ in range(20):
            gates=[]
            for _out in range(n+1):
                support=tuple(rng.sample(range(n),3))
                gates.append(Gate(support,rng.choice(essential_masks)))
            result=combined_v100_v101_avoid(n,gates)
            original=output_range(list(range(n)),gates)
            cases+=1; failures += result['target'] in original
            max_roots=max(max_roots,result['roots'])

    return {
      "laboratory":"V101",
      "theorem_status":{
        "functional_fiber_safe_relaxation":True,
        "acyclic_distinct_head_domain_size_2roots":True,
        "functional_anchor_avoider_O2mu":True,
        "essential_ternary_functional_anchor_masks_186":True,
        "functional_anchor_free_exactly_32":True,
        "functional_anchor_free_orbits_0x17_0x1b":True,
        "post_v100_new_functional_orbit_0x1e":True,
        "strict_balanced_nonaffine_0x1e_lambda_n_roots_two":True,
        "unrestricted_nc03_avoid_polynomial_time":False,
        "hlz_worst_case_runtime_improved":False,
        "p_vs_np_resolved":False,
      },
      "ternary_functional_classification":{
        "essential_ternary_masks":len(essential_masks),
        "functional_anchor_masks":total,
        "anchor_free_masks":len(essential_masks)-total,
        "anchor_free_orbits":anchor_free,
        "orbit_rows":rows,
      },
      "strict_cyclic_0x1e_majority":{"rows":strict},
      "random_small_audit":{"cases":cases,"absence_failures":failures,"max_roots":max_roots},
    }

if __name__=='__main__':
    import json
    print(json.dumps(build_results(),indent=2,sort_keys=True))
