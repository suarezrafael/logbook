#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def load(p):return json.loads(p.read_text(encoding='utf-8'))
def affine(points):
    if not points:return False
    b=min(points);d={x^b for x in points};return all((x^y) in d for x in d for y in d)
def all_affine(n):return [frozenset(x for x in range(1<<n) if (bits>>x)&1) for bits in range(1,1<<(1<<n)) if affine({x for x in range(1<<n) if (bits>>x)&1})]
def finite_set_theory():
    expected={1:6,2:286,3:316251};total=0
    for n in (1,2,3):
        sets=all_affine(n);count=0
        for indices in itertools.combinations_with_replacement(range(len(sets)),n+1):
            family=[sets[i] for i in indices];common=set.intersection(*(set(x) for x in family));count+=1
            if common:assert any(set.intersection(*(set(family[j]) for j in range(len(family)) if j!=i))<=family[i] for i in range(len(family)))
            else:assert any(not set.intersection(*(set(family[i]) for i in subset)) for r in range(1,n+2) for subset in itertools.combinations(range(n+1),r))
        assert count==expected[n];total+=count
    assert total==316543;return total
def proof_surface():
    tex=(HERE/'V56_AFFINE_FIBER_THEOREM.tex').read_text().lower();spec=load(HERE/'V56_AFFINE_FIBER_SPEC.json')
    assert '\\begin{theorem}' in tex and '\\begin{proof}' in tex and 'projection preserves affinity' in tex and 'general $nc^0_3$-avoid' in tex
    assert spec['branches']['inconsistent']['size_bound']=='|E|<=n+1' and spec['branches']['consistent']['source_bound']=='at most n other gate blocks are sufficient'
    assert spec['scientific_boundary']['p_vs_np_resolved'] is False;return 7
def route_surface():
    ledger=load(ROOT/'LEDGER.json');route=(HERE/'P_VS_NP_ROUTE_AUDIT.md').read_text().lower()
    assert ledger['program']['p_vs_np_research_active'] is True and ledger['program']['p_vs_np_route_active'] is False and ledger['program']['p_vs_np_resolved'] is False
    assert len(ledger['p_vs_np_route']['gates'])==4
    for phrase in ('does **not** currently possess a direct route','no such bridge in this repository','counterexamples must be promoted before conjectures'):assert phrase in route
    corpus='\n'.join(p.read_text().lower() for p in HERE.glob('*') if p.suffix in {'.md','.tex','.json'})
    assert all(x not in corpus for x in ('we prove p != np','p versus np is solved','silence confirms novelty','progress toward p versus np:'));return 8
def history_and_runner():
    ledger=load(ROOT/'LEDGER.json');runner=(ROOT/'verify_all.sh').read_text()
    assert int(ledger['promotion']['last_merged_laboratory'][1:])>=64 and ledger['promotion']['last_pr']>=6
    assert ledger['workflow_runtime']['checkout_action']=='actions/checkout@v6' and ledger['verification']['quick']['failures']==0 and ledger['verification']['full']['failures']==0
    assert runner.count('V65|')==2 and ledger['external_contact']['replies_received']==0 and ledger['external_contact']['followup_sent'] is False;return 7
def main():
    a=finite_set_theory();b=proof_surface();c=route_surface();d=history_and_runner();print(f'V65 independent verification passed: {a+b+c+d} checks; {a} exact set families; zero failures.')
if __name__=='__main__':main()
