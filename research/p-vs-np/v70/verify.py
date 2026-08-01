#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
from v70_frontier_ordering import generate_results
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def version_number(value):
    match=re.fullmatch(r'V(\d+)',value);assert match,value;return int(match.group(1))

def main():
    results=generate_results();(HERE/'RESULTS.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    required=['README.md','SUPPORT_FRONTIER_THEOREM.md','COMPONENT_FACTORISATION.md','HEURISTIC_BENCHMARK.md','PUBLICATION_READINESS.md','SEARCH_SPEC.json','WITNESSES.json','RESULTS.json','V70_SUPPORT_FRONTIER_THEOREM.tex','V71_CORE_CONTEXT.md','v70_frontier_ordering.py','verify_independent.py','verify_search_reproduction.py']
    assert all((HERE/name).is_file() for name in required)
    assert results['theorem']['parameterized_consequence']=='bounded support-frontier width gives an FPT-size projected DAG'
    assert results['component_factorisation_subset_checks']==640
    natural={item['n']:item for item in results['natural_record_benchmarks']}
    assert natural[14]['heuristics']['natural']['G_proj']==583
    assert natural[14]['heuristics']['support_lookahead_2']['G_proj']==41
    assert natural[12]['exact']['Gstar']==29
    records={item['n']:item for item in results['new_exact_objective_records']}
    assert records[8]['exact']['Gstar']==29 and records[10]['exact']['Gstar']==30
    assert results['scientific_status']['general_polynomial_good_order_proved'] is False
    assert results['scientific_status']['all_orders_superpolynomial_lower_bound_proved'] is False
    ledger=json.loads((ROOT/'LEDGER.json').read_text())
    assert ledger['schema_version']>=11 and version_number(ledger['current_version'])>=70
    assert ledger['program']['p_vs_np_route_active'] is False and ledger['program']['p_vs_np_resolved'] is False
    assert any(item['version']=='V70' for item in ledger['versions'])
    assert ledger['affine_cell_branching']['v70_support_frontier_bound'] is True
    runner=(ROOT/'verify_all.sh').read_text()
    assert 'V70|primary|v70/verify.py|quick|' in runner and 'V70|independent|v70/verify_independent.py|quick|' in runner
    assert 'V70|search-replay|v70/verify_search_reproduction.py|full|' in runner
    state=(ROOT/'STATE.md').read_text();current=re.search(r'\*\*Current laboratory:\*\* V(\d+)(?: candidate)?',state);lower=state.lower()
    assert current and int(current.group(1))>=70 and ('support frontier' in lower or 'support-frontier' in lower)
    root=(ROOT/'README.md').read_text();assert '[`v70/`](v70/)' in root and 'PUBLICATION_INDEX.md' in root
    assert (ROOT/'PUBLICATION_INDEX.md').is_file()
    workflow=(ROOT.parent.parent/'.github'/'workflows'/'p-vs-np-verify.yml').read_text();assert 'V70_SUPPORT_FRONTIER_THEOREM.tex' in workflow
    tex=(HERE/'V70_SUPPORT_FRONTIER_THEOREM.tex').read_text()
    for token in ('Support-frontier bound','Component factorisation','mA(q'):assert token in tex
    publication=(HERE/'PUBLICATION_READINESS.md').read_text().lower();assert 'eccc' in publication and 'zenodo' in publication and 'does not submit' in publication
    corpus='\n'.join(path.read_text().lower() for path in HERE.iterdir() if path.suffix in {'.md','.json','.tex'})
    for phrase in ('p versus np is solved','we prove p != np','all instances have a polynomial good order','g*_proj is exponential for all orders','accepted by eccc','peer reviewed theorem'):assert phrase not in corpus
    print('V70 primary verification passed: support-frontier theorem; 640 component cuts; heuristic n=14 upper bound 41; exact records 29 and 30; 32 repository checks; zero failures.')
if __name__=='__main__':main()
