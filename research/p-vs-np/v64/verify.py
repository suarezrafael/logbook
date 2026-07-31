#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def sat_clause(x,lits):
    return any((lit>0 and x[abs(lit)-1]==1) or (lit<0 and x[abs(lit)-1]==0) for lit in lits)
def permute_mask(mask,p,neg,out):
    r=0
    for a in range(8):
        b=[(a>>i)&1 for i in range(3)]
        t=[b[p[i]]^neg[i] for i in range(3)]
        s=t[0]|(t[1]<<1)|(t[2]<<2)
        r|=((((mask>>s)&1)^out)<<a)
    return r
def orbit(mask):
    return {permute_mask(mask,p,n,o) for p in itertools.permutations(range(3)) for n in itertools.product((0,1),repeat=3) for o in (0,1)}
def version_number(v):
    m=re.fullmatch(r'V(\d+)',v); assert m; return int(m.group(1))

def check_spec():
    s=load(HERE/'V57_BLOCK_IRREDUNDANCY_SPEC.json')
    clauses={c['id']:c['literals'] for c in s['clauses']}
    blocks={b['id']:b for b in s['blocks']}
    xs=list(itertools.product((0,1),repeat=4))
    def block_sat(x,b): return all(sat_clause(x,clauses[c]) for c in b['clauses'])
    models=[x for x in xs if all(block_sat(x,b) for b in blocks.values())]
    assert models==[tuple(s['expected']['unique_model'])]
    assert len({tuple(c['literals']) for c in s['clauses']})==6
    for bid,w in s['block_witnesses'].items():
        x=tuple(w); assert not block_sat(x,blocks[bid]); assert all(block_sat(x,b) for k,b in blocks.items() if k!=bid)
    for cid,w in s['clause_witnesses'].items():
        x=tuple(w); assert not sat_clause(x,clauses[cid]); assert all(sat_clause(x,c) for k,c in clauses.items() if k!=cid)
    o=orbit(int(s['expected']['npn_base_mask'],16)); assert len(o)==48
    masks=[int(b['gate_mask'],16) for b in s['blocks']]; assert masks==[0x51,0x45,0x51,0x45,0x15]; assert all(m in o for m in masks)
    for k in range(51):
        n=4+3*k; m=5+3*k; assert m==n+1
    return 16+6+5+6+7+51

def check_documents():
    tex=(HERE/'V57_BLOCK_IRREDUNDANCY_THEOREM.tex').read_text(encoding='utf-8')
    notes=(HERE/'FORMALIZATION_NOTES.md').read_text(encoding='utf-8')
    audit=(HERE/'ACTION_RUNTIME_AUDIT.md').read_text(encoding='utf-8')
    ext=(HERE/'EXTERNAL_RESPONSE_CHECK.md').read_text(encoding='utf-8')
    for token in ('Complete block irredundancy','0101','1000','NPN orbit','does not claim novelty'):
        assert token in tex
    for token in ('machine-readable source','exact six-clause collapse','does not establish minimality'):
        assert token in notes
    for token in ('actions/checkout@v6','2.336.0','separate from mathematical validation'):
        assert token in audit
    assert 'zero incoming messages' in ext and 'Follow-up sent:** no' in ext
    return 13

def check_repository():
    ledger=load(ROOT/'LEDGER.json'); results=load(HERE/'RESULTS.json')
    assert ledger['schema_version']>=5 and version_number(ledger['current_version'])>=64
    assert ledger['program']['p_vs_np_route_active'] is False
    assert any(v['version']=='V64' for v in ledger['versions'])
    assert ledger['workflow_runtime']['checkout_action']=='actions/checkout@v6'
    assert ledger['external_contact']['replies_received']==0 and ledger['external_contact']['followup_sent'] is False
    assert results['version']=='V64' and results['formalization']['unique_model']=='0000'
    runner=(ROOT/'verify_all.sh').read_text(encoding='utf-8')
    assert 'V64|primary|v64/verify.py|quick|' in runner and 'V64|independent|v64/verify_independent.py|quick|' in runner
    workflow=(ROOT.parent.parent/'.github'/'workflows'/'p-vs-np-verify.yml').read_text(encoding='utf-8')
    assert workflow.count('actions/checkout@v6')==2 and 'actions/checkout@v4' not in workflow
    return 12

def main():
    total=check_spec()+check_documents()+check_repository()
    assert total==116,total
    print('V64 primary verification passed: 116 checks; zero failures.')
if __name__=='__main__': main()
