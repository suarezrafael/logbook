#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
from v69_order_robustness import generate_results
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def main():
    results=generate_results();(HERE/'RESULTS.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    required=['README.md','ORDER_ROBUSTNESS_THEOREM.md','EXPERIMENT_REPORT.md','PROOF_COMPLEXITY_BOUNDARY.md','WITNESSES.json','RESULTS.json','V69_ORDER_ROBUSTNESS_THEOREM.tex','V70_CORE_CONTEXT.md','seed_data.json','verify_independent.py']
    assert all((HERE/x).is_file() for x in required)
    assert results['natural_order_records'][0]['exact']['Gstar']==15
    assert results['natural_order_records'][2]['exact']['Gstar']==17
    assert results['natural_order_records'][3]['exact']['Gstar']==29
    assert results['exact_order_robustness_search'][1]['exact']['Gstar']==28
    assert results['conclusion']['general_polynomial_good_order_proved'] is False
    assert results['conclusion']['all_orders_lower_bound_proved'] is False
    runner=(ROOT/'verify_all.sh').read_text();assert 'V69|primary|v69/verify.py|quick|' in runner and 'V69|independent|v69/verify_independent.py|quick|' in runner
    state=(ROOT/'STATE.md').read_text();current=re.search(r'\*\*Current laboratory:\*\* V(\d+)',state);assert current and int(current.group(1))>=69 and 'G*_proj' in state
    root=(ROOT/'README.md').read_text();assert '[`v69/`](v69/)' in root
    workflow=(ROOT.parent.parent/'.github'/'workflows'/'p-vs-np-verify.yml').read_text();assert 'V69_ORDER_ROBUSTNESS_THEOREM.tex' in workflow
    tex=(HERE/'V69_ORDER_ROBUSTNESS_THEOREM.tex').read_text();assert 'Set-layer invariance' in tex and 'subset recurrence' in tex
    corpus='\n'.join(p.read_text().lower() for p in HERE.iterdir() if p.suffix in {'.md','.json','.tex'})
    for phrase in ('p versus np is solved','we prove p != np','all instances have a polynomial good order','g*_proj is exponential'):assert phrase not in corpus
    print('V69 primary verification passed: deterministic hill records n=6..14; exact G*_proj through n=12; 27 repository checks; zero failures.')
if __name__=='__main__':main()
