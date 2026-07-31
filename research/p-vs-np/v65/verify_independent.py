#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def affine(points):
    if not points:return False
    b=min(points);D={x^b for x in points}
    return all((x^y) in D for x in D for y in D)
def all_affine(n):
    U=range(1<<n);out=[]
    for bits in range(1,1<<(1<<n)):
        P={x for x in U if (bits>>x)&1}
        if affine(P):out.append(frozenset(P))
    return out

def finite_set_theory():
    expected={1:6,2:286,3:316251}; total=0
    for n in (1,2,3):
        A=all_affine(n); c=0
        for idx in itertools.combinations_with_replacement(range(len(A)),n+1):
            F=[A[i] for i in idx]; common=set.intersection(*(set(x) for x in F)); c+=1
            if common:
                assert any(set.intersection(*(set(F[j]) for j in range(len(F)) if j!=i)) <= F[i] for i in range(len(F)))
            else:
                assert any(not set.intersection(*(set(F[i]) for i in S)) for r in range(1,n+2) for S in itertools.combinations(range(n+1),r))
        assert c==expected[n]; total+=c
    assert total==316543
    return total

def proof_surface():
    tex=(HERE/'V56_AFFINE_FIBER_THEOREM.tex').read_text(encoding='utf-8').lower()
    spec=load(HERE/'V56_AFFINE_FIBER_SPEC.json')
    assert '\\begin{theorem}' in tex and '\\begin{proof}' in tex
    assert 'projection preserves affinity' in tex and 'general $nc^0_3$-avoid' in tex
    assert spec['branches']['inconsistent']['size_bound']=='|E|<=n+1'
    assert spec['branches']['consistent']['source_bound']=='at most n other gate blocks are sufficient'
    assert spec['scientific_boundary']['p_vs_np_resolved'] is False
    return 7

def route_surface():
    ledger=load(ROOT/'LEDGER.json'); route=(HERE/'P_VS_NP_ROUTE_AUDIT.md').read_text(encoding='utf-8').lower()
    assert ledger['program']['p_vs_np_research_active'] is True
    assert ledger['program']['p_vs_np_route_active'] is False
    assert ledger['program']['p_vs_np_resolved'] is False
    assert len(ledger['p_vs_np_route']['gates'])==4
    for phrase in ('does **not** currently possess a direct route','no such bridge in this repository','counterexamples must be promoted before conjectures'):
        assert phrase.lower() in route
    forbidden=('we prove p != np','p versus np is solved','silence confirms novelty','progress toward p versus np:')
    corpus='\n'.join(p.read_text(encoding='utf-8').lower() for p in HERE.glob('*') if p.suffix in {'.md','.tex','.json'})
    assert all(x not in corpus for x in forbidden)
    return 8

def history_and_runner():
    ledger=load(ROOT/'LEDGER.json'); runner=(ROOT/'verify_all.sh').read_text(encoding='utf-8')
    assert ledger['promotion']['last_merged_laboratory']=='V64'
    assert ledger['promotion']['last_pr']==6
    assert ledger['workflow_runtime']['checkout_action']=='actions/checkout@v6'
    assert ledger['verification']['quick']['failures']==0 and ledger['verification']['full']['failures']==0
    assert runner.count('V65|')==2
    assert ledger['external_contact']['replies_received']==0 and ledger['external_contact']['followup_sent'] is False
    return 7

def main():
    a=finite_set_theory(); b=proof_surface(); c=route_surface(); d=history_and_runner(); total=a+b+c+d
    print(f'V65 independent verification passed: {total} checks; {a} exact set families; zero failures.')
if __name__=='__main__': main()
