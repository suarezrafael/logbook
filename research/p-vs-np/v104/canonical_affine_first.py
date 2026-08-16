from __future__ import annotations

from itertools import product

from hybrid_root_rank import (
    Gate,
    LinearSystem,
    canonical_target,
    functional_total_map,
    local_affine_hull_equations,
)


def _lift(g: Gate, local_rows):
    rows=[]
    for local_mask,rhs in local_rows:
        coeff=0
        for j,v in enumerate(g.support):
            if (local_mask>>j)&1:
                coeff |= 1<<v
        rows.append((coeff,rhs))
    return rows


def _try_add_relation(n, relations, head, relation):
    trial=dict(relations)
    trial[head]=relation
    out=[[] for _ in range(n)]
    indeg=[0]*n
    for h,(tails,_mapping) in trial.items():
        for tail in tails:
            out[tail].append(h)
            indeg[h]+=1
    queue=[i for i,d in enumerate(indeg) if d==0]
    seen=0
    while queue:
        u=queue.pop()
        seen+=1
        for v in out[u]:
            indeg[v]-=1
            if indeg[v]==0:
                queue.append(v)
    return trial if seen==n else None


def _topological_order(n, relations):
    out=[[] for _ in range(n)]
    indeg=[0]*n
    for h,(tails,_mapping) in relations.items():
        for tail in tails:
            out[tail].append(h)
            indeg[h]+=1
    queue=[i for i,d in enumerate(indeg) if d==0]
    order=[]
    while queue:
        u=queue.pop()
        order.append(u)
        for v in out[u]:
            indeg[v]-=1
            if indeg[v]==0:
                queue.append(v)
    assert len(order)==n
    return order


def canonical_affine_first_avoid(n:int,gates:list[Gate]):
    """Deterministic V104 preprocessing and avoider.

    1. Build a canonical affine-hull block basis.
    2. Protect every variable occurring in the retained affine equations.
    3. Greedily add canonical functional anchors whose heads are unprotected.
    4. Enumerate only the remaining root nullity eta.
    """
    m=len(gates)
    if m<=n:
        raise ValueError("requires m>n")
    targets=[canonical_target(g) for g in gates]

    # Affine-first phase.
    full_system=LinearSystem(n)
    affine_selected=[]
    protected=set()
    affine_rows={}
    for i,g in enumerate(gates):
        local=local_affine_hull_equations(g,targets[i])
        if local is None:
            y=[0]*m
            y[i]=targets[i]
            return tuple(y),{"case":"empty_canonical_fiber","eta":n}
        rows=_lift(g,local)
        affine_rows[i]=rows
        trial=full_system.copy()
        try:
            gain=trial.add_many(rows)
        except ValueError:
            y=[0]*m
            for j in affine_selected:
                y[j]=targets[j]
            y[i]=targets[i]
            return tuple(y),{"case":"inconsistent_canonical_hulls","eta":n-full_system.rank}
        if gain>0:
            full_system=trial
            affine_selected.append(i)
            for coeff,_rhs in rows:
                for v in range(n):
                    if (coeff>>v)&1:
                        protected.add(v)
    rank=full_system.rank

    # Functional-second phase. Canonical output order, then canonical head order.
    affine_set=set(affine_selected)
    relations={}
    functional_selected=[]
    for i,g in enumerate(gates):
        if i in affine_set:
            continue
        for head in sorted(g.support):
            if head in protected or head in relations:
                continue
            relation=functional_total_map(g,targets[i],head)
            if relation is None:
                continue
            trial=_try_add_relation(n,relations,head,relation)
            if trial is not None:
                relations=trial
                functional_selected.append(i)
                break

    heads=set(relations)
    roots=[v for v in range(n) if v not in heads]
    assert protected.issubset(roots)
    root_index={v:i for i,v in enumerate(roots)}

    # Re-express the already independent affine basis on the root coordinates.
    root_system=LinearSystem(len(roots))
    for coeff,rhs in full_system.rows.values():
        root_coeff=0
        for v in roots:
            if (coeff>>v)&1:
                root_coeff |= 1<<root_index[v]
        root_system.add(root_coeff,rhs)
    assert root_system.rank==rank

    eta=len(roots)-rank
    selected=affine_set | set(functional_selected)
    residual=[i for i in range(m) if i not in selected]
    assert len(affine_selected)<=rank
    assert len(residual)>eta

    topo=_topological_order(n,relations)
    observed=set()
    relaxed=0
    for root_bits in root_system.solutions():
        x=[None]*n
        for v,b in zip(roots,root_bits):
            x[v]=b
        for v in topo:
            if v in relations:
                tails,mapping=relations[v]
                x[v]=mapping[tuple(int(x[t]) for t in tails)]
        full=tuple(int(v) for v in x)
        observed.add(tuple(gates[i].value(full) for i in residual))
        relaxed+=1
    assert relaxed==1<<eta

    missing=None
    for z in range(len(observed)+1):
        word=tuple((z>>j)&1 for j in range(len(residual)))
        if word not in observed:
            missing=word
            break
    assert missing is not None

    y=[0]*m
    for i in affine_selected:
        y[i]=targets[i]
    for i in functional_selected:
        y[i]=targets[i]
    for i,b in zip(residual,missing):
        y[i]=b
    return tuple(y),{
        "case":"canonical_affine_first",
        "affine_rank":rank,
        "affine_blocks":len(affine_selected),
        "protected_variables":len(protected),
        "functional_blocks":len(functional_selected),
        "roots":len(roots),
        "eta":eta,
        "relaxed_assignments":relaxed,
        "residual_outputs":len(residual),
        "observed_residual":len(observed),
    }
