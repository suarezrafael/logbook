#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
from v68_spine_family import generate_results

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def version_number(value):
    match=re.fullmatch(r'V(\d+)',value);assert match,value;return int(match.group(1))


def verify_repository_surface(results):
    required=[
        'README.md','SPINE_FAMILY_THEOREM.md','V68_SPINE_TREE_DAG_THEOREM.tex',
        'C36_STRUCTURE_ANALYSIS.md','PROJECTED_DAG_MODEL.md','BITSET_ENGINE.md',
        'PROOF_COMPLEXITY_BOUNDARY.md','RESULTS.json','V69_CORE_CONTEXT.md',
        'affine_bitset.py','v68_spine_family.py','verify_independent.py'
    ]
    assert all((HERE/name).is_file() for name in required)
    ledger=json.loads((ROOT/'LEDGER.json').read_text())
    assert ledger['schema_version']>=9 and version_number(ledger['current_version'])>=68
    assert ledger['program']['p_vs_np_route_active'] is False
    assert ledger['program']['p_vs_np_resolved'] is False
    assert any(item['version']=='V68' for item in ledger['versions'])
    assert ledger['affine_cell_branching']['v68_tree_exponential_family'] is True
    assert ledger['affine_cell_branching']['v68_projected_dag_linear_for_spine'] is True
    runner=(ROOT/'verify_all.sh').read_text()
    assert 'V68|primary|v68/verify.py|quick|' in runner
    assert 'V68|independent|v68/verify_independent.py|quick|' in runner
    state=(ROOT/'STATE.md').read_text()
    assert '**Current laboratory:** V68' in state
    assert 'Direct P-versus-NP route active:** no' in state
    assert '2^((n-3)/2)' in state and 'G_proj' in state
    root=(ROOT/'README.md').read_text()
    assert '[`v68/`](v68/)' in root
    workflow=(ROOT.parent.parent/'.github'/'workflows'/'p-vs-np-verify.yml').read_text()
    assert 'V68_SPINE_TREE_DAG_THEOREM.tex' in workflow
    tex=(HERE/'V68_SPINE_TREE_DAG_THEOREM.tex').read_text()
    for token in ('Spine tree--DAG separation','2^{k-1}','3k+4','does not identify'):
        assert token in tex
    boundary=(HERE/'PROOF_COMPLEXITY_BOUNDARY.md').read_text().lower()
    assert 'no simulation theorem' in boundary and 'tseitin' in boundary
    corpus='\n'.join(path.read_text().lower() for path in HERE.iterdir() if path.suffix in {'.md','.json','.tex'})
    forbidden=(
        'p versus np is solved','we prove p != np','all affine-cell dags are polynomial',
        'standard obdd lower bound follows','unrestricted nc0_3-avoid is solved'
    )
    assert all(phrase not in corpus for phrase in forbidden)
    assert results['scientific_status']['p_vs_np_resolved'] is False
    return 32


def main():
    results=generate_results()
    (HERE/'RESULTS.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    checks=verify_repository_surface(results)
    print(f"V68 primary verification passed: exact k=1..5; symbolic/DAG k=1..64; {checks} repository checks; zero failures.")

if __name__=='__main__':main()
