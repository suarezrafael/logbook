#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from functional_anchor import build_results
ROOT=Path(__file__).resolve().parent

def main():
    committed=json.loads((ROOT/'RESULTS.json').read_text())
    rebuilt=build_results(); assert rebuilt==committed
    t=committed['theorem_status']
    for k in (
        'functional_fiber_safe_relaxation','acyclic_distinct_head_domain_size_2roots',
        'functional_anchor_avoider_O2mu','essential_ternary_functional_anchor_masks_186',
        'functional_anchor_free_exactly_32','functional_anchor_free_orbits_0x17_0x1b',
        'post_v100_new_functional_orbit_0x1e','strict_balanced_nonaffine_0x1e_lambda_n_roots_two'):
        assert t[k]
    assert not t['unrestricted_nc03_avoid_polynomial_time']
    assert not t['hlz_worst_case_runtime_improved']
    assert not t['p_vs_np_resolved']
    c=committed['ternary_functional_classification']
    assert c['essential_ternary_masks']==218
    assert c['functional_anchor_masks']==186
    assert c['anchor_free_masks']==32
    assert c['anchor_free_orbits']==['0x17','0x1b']
    for row in committed['strict_cyclic_0x1e_majority']['rows']:
        assert row['m']==row['n']+1
        assert row['min_input_degree']>=3
        assert row['v100_steps']==0
        assert row['selected_outputs']==row['n']-2
        assert row['roots']==2
        assert row['relaxed_assignments']==4
        assert row['lifted_word_absent']
    assert committed['random_small_audit']['cases']==100
    assert committed['random_small_audit']['absence_failures']==0
    imp=json.loads((ROOT/'IMPLICATION.json').read_text())
    assert imp['laboratory']=='V101'
    assert imp['classification']=='frontier_progress'
    assert imp['material_advance_rule_met']
    assert [x['proved'] for x in imp['bridge_lemmas'][:10]]==[True]*10
    assert [x['proved'] for x in imp['bridge_lemmas'][10:]]==[False]*3
    assert imp['next_front']=='majority_mux_and_cyclic_functional_dependencies'
    print('V101 verification passed: functional-anchor O(2^mu) compression, exact 186/32 split, and balanced-nonaffine 0x1e mu=2 family.')
if __name__=='__main__': main()
