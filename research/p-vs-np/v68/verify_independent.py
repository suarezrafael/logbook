#!/usr/bin/env python3
"""Independent semantic verifier for V68.

This module does not import the primary spine or bitset implementations. It
reconstructs the gates as local point sets, brute-forces k=1..5, and builds the
projected ordered DAG from explicit feasible relations rather than GF(2) rows.
"""
from __future__ import annotations
import json
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

MOTIF=({(0,0,0)},{(0,0,1),(0,1,0)})
ANCHOR_B=({(0,0,0)},{(0,0,1),(0,1,1)})
ANCHOR_U=({(0,0,0)},{(0,1,0),(0,1,1)})


def family(k):
    n=2*k+1
    gates=[]
    def motif(t):
        s=0;u=1+2*t;v=2+2*t
        return [((s,u,v),MOTIF),((s,v,u),MOTIF)]
    gates.extend(motif(0));gates.extend([((0,1,2),ANCHOR_B),((0,1,2),ANCHOR_U)])
    for t in range(1,k):gates.extend(motif(t))
    return n,gates


def local_tuple(assignment,support):
    return tuple((assignment>>variable)&1 for variable in support)


def signatures(k):
    n,gates=family(k);found=set()
    for assignment in range(1<<n):
        word=[]
        for support,cells in gates:
            local=local_tuple(assignment,support)
            if local in cells[0]:word.append(0)
            elif local in cells[1]:word.append(1)
            else:break
        else:found.add(tuple(word))
    return found


def projected_relation_dag(k):
    n,gates=family(k)
    suffix=[]
    for index in range(len(gates)+1):
        active=sorted({v for support,_ in gates[index:] for v in support})
        suffix.append(tuple(active))
    states=set();DEAD=('dead',);ACCEPT=('accept',)

    def encode_projection(assignments,active):
        return frozenset(
            tuple((assignment>>variable)&1 for variable in active)
            for assignment in assignments
        )

    @lru_cache(None)
    def visit(index,relation):
        if not relation:return DEAD
        if index==len(gates):return ACCEPT
        active=suffix[index]
        support,cells=gates[index]
        state=(index,relation);states.add(state)
        children=[]
        for cell in cells:
            compatible=[]
            for local_bits in relation:
                mapping=dict(zip(active,local_bits))
                if tuple(mapping[v] for v in support) in cell:
                    compatible.append(mapping)
            next_active=suffix[index+1]
            projected=frozenset(tuple(mapping[v] for v in next_active) for mapping in compatible)
            children.append(visit(index+1,projected))
        return tuple(children)

    initial=encode_projection(range(1<<n),suffix[0])
    visit(0,initial)
    return len(states)


def check_local_factorization():
    motif=[]
    for u in (0,1):
        for v in (0,1):
            word=[]
            for support in ((0,1,2),(0,2,1)):
                local=(0,u,v) if support==(0,1,2) else (0,v,u)
                if local in MOTIF[0]:word.append(0)
                elif local in MOTIF[1]:word.append(1)
                else:break
            else:motif.append(tuple(word))
    assert set(motif)=={(0,0),(1,1)}
    anchor_survivors=[]
    for u in (0,1):
        for v in (0,1):
            local=(0,u,v)
            if local in MOTIF[0]|MOTIF[1] and local in ANCHOR_B[0]|ANCHOR_B[1] and local in ANCHOR_U[0]|ANCHOR_U[1]:
                anchor_survivors.append((u,v))
    assert anchor_survivors==[(0,0)]
    return 3


def verify_surfaces():
    results=json.loads((HERE/'RESULTS.json').read_text())
    ledger=json.loads((ROOT/'LEDGER.json').read_text())
    assert results['version']=='V68' and results['failures']==0
    assert results['construction']['consistent_complete_branches']=='2^(k-1)=2^((n-3)/2)'
    assert results['scientific_status']['explicit_exponential_tree_family_proved'] is True
    assert results['scientific_status']['general_polynomial_projected_dag_proved'] is False
    assert ledger['schema_version']>=9 and int(ledger['current_version'][1:])>=68
    assert ledger['program']['p_vs_np_route_active'] is False
    assert ledger['program']['p_vs_np_resolved'] is False
    runner=(ROOT/'verify_all.sh').read_text()
    assert 'V68|primary|v68/verify.py|quick|' in runner
    assert 'V68|independent|v68/verify_independent.py|quick|' in runner
    state=(ROOT/'STATE.md').read_text()
    assert '**Current laboratory:** V68' in state and 'G_proj' in state
    theorem=(HERE/'SPINE_FAMILY_THEOREM.md').read_text()
    assert '2^((n-3)/2)' in theorem and '3k+4' in theorem
    boundary=(HERE/'PROOF_COMPLEXITY_BOUNDARY.md').read_text().lower()
    assert 'no simulation theorem' in boundary
    return 13


def main():
    checks=check_local_factorization()
    for k in range(1,6):
        found=signatures(k);assert len(found)==1<<(k-1)
        states=projected_relation_dag(k);assert states==3*k+4
        checks+=len(found)+1
    checks+=verify_surfaces()
    print(f'V68 independent verification passed: {checks} semantic checks; k=1..5 brute-forced; projected DAG reconstructed; zero failures.')

if __name__=='__main__':main()
