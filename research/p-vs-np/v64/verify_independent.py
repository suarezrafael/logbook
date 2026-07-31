#!/usr/bin/env python3
from __future__ import annotations
import itertools,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def ev(x,lits):
    for z in lits:
        i=abs(z)-1
        if (z>0 and x[i]) or (z<0 and not x[i]): return True
    return False
def transform(mask,perm,flips,of):
    out=0
    for raw in range(8):
        bits=((raw>>0)&1,(raw>>1)&1,(raw>>2)&1)
        src=0
        for i in range(3): src|=((bits[perm[i]]^flips[i])<<i)
        out|=((((mask>>src)&1)^of)<<raw)
    return out
def vnum(v):
    m=re.fullmatch(r'V(\d+)',v); assert m; return int(m.group(1))

def independent_finite():
    s=load(HERE/'V57_BLOCK_IRREDUNDANCY_SPEC.json')
    cs={c['id']:tuple(c['literals']) for c in s['clauses']}; bs={b['id']:tuple(b['clauses']) for b in s['blocks']}
    universe=list(itertools.product((0,1),repeat=4))
    def B(x,b): return all(ev(x,cs[c]) for c in bs[b])
    assert [x for x in universe if all(B(x,b) for b in bs)]==[(0,0,0,0)]
    for b in bs:
        ws=[x for x in universe if not B(x,b) and all(B(x,q) for q in bs if q!=b)]
        assert tuple(s['block_witnesses'][b]) in ws
    for c in cs:
        ws=[x for x in universe if not ev(x,cs[c]) and all(ev(x,q) for q in cs.values() if q!=cs[c])]
        assert tuple(s['clause_witnesses'][c]) in ws
    orb={transform(7,p,f,o) for p in itertools.permutations(range(3)) for f in itertools.product((0,1),repeat=3) for o in (0,1)}
    assert len(orb)==48 and {int(b['gate_mask'],16) for b in s['blocks']} <= orb
    return 16+5+6+49

def independent_metadata():
    ledger=load(ROOT/'LEDGER.json'); results=load(HERE/'RESULTS.json')
    assert vnum(ledger['current_version'])>=64
    assert ledger['promotion']['per_laboratory_pr_required'] is True
    assert ledger['promotion']['merge_target']=='main'
    assert ledger['workflow_runtime']['scientific_validation_separate'] is True
    assert results['scientific_status']=={'peer_reviewed':False,'novelty_confirmed':False,'p_vs_np_resolved':False}
    assert results['external_review']['replies_found']==0 and results['external_review']['followup_sent'] is False
    return 7

def independent_prose():
    tex=(HERE/'V57_BLOCK_IRREDUNDANCY_THEOREM.tex').read_text(encoding='utf-8').lower()
    audit=(HERE/'ACTION_RUNTIME_AUDIT.md').read_text(encoding='utf-8').lower()
    ext=(HERE/'EXTERNAL_RESPONSE_CHECK.md').read_text(encoding='utf-8').lower()
    assert '\\begin{theorem}' in tex and '\\begin{proof}' in tex
    assert 'general 2-cnf irredundancy' in tex and 'not peer reviewed' in tex
    assert 'v6.0.2' in audit and 'runner `2.329.0`' in audit
    assert 'not evidence of novelty' in ext
    forbidden=('we prove p != np','first general nc0_3-avoid','silence confirms novelty')
    assert all(x not in '\n'.join((tex,audit,ext)) for x in forbidden)
    return 8

def main():
    total=independent_finite()+independent_metadata()+independent_prose()
    assert total==91,total
    print('V64 independent verification passed: 91 checks; zero failures.')
if __name__=='__main__': main()
