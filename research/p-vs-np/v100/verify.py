#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from literal_peeling import build_results
ROOT = Path(__file__).resolve().parent

def main():
    committed=json.loads((ROOT/'RESULTS.json').read_text())
    rebuilt=build_results()
    assert rebuilt==committed
    t=committed['theorem_status']
    for k in (
        'literal_graph_fiber_safe_elimination','literal_substitution_preserves_locality_three',
        'positive_surplus_preserved_exactly','general_nc03_preprocesses_to_five_hard_ternary_npn_orbits',
        'all_literal_graph_peelable_ternary_circuits_reduce_to_nc02',
        'all_literal_graph_peelable_ternary_circuits_in_P_via_glw_nc02',
        'middle_unate_orbit_0x07_solved','strict_nonunate_pair_only_0x19_lambda_n_family_solved'):
        assert t[k]
    assert not t['unrestricted_nc03_avoid_polynomial_time']
    assert not t['hlz_worst_case_runtime_improved']
    assert not t['p_vs_np_resolved']
    c=committed['ternary_classification']
    assert c['essential_ternary_masks']==218
    assert c['literal_graph_peelable_masks']==144
    assert c['residual_hard_masks']==74
    assert c['peelable_orbits']==['0x01','0x06','0x07','0x18','0x19']
    assert c['hard_orbits']==['0x16','0x17','0x1b','0x1e','0x69']
    for row in committed['strict_0x19_family']['rows']:
        assert row['m']==row['n']+1
        assert row['min_input_degree']>=3
        assert row['representative_is_unate'] is False
        assert row['constant_forcing_option_exists'] is False
        assert row['residual_max_locality']<=2
        assert row['lifted_word_absent']
    assert committed['random_small_audit']=={'cases':100,'absence_failures':0}
    imp=json.loads((ROOT/'IMPLICATION.json').read_text())
    assert imp['laboratory']=='V100'
    assert imp['classification']=='frontier_progress'
    assert imp['material_advance_rule_met']
    assert [x['proved'] for x in imp['bridge_lemmas'][:11]]==[True]*11
    assert [x['proved'] for x in imp['bridge_lemmas'][11:]]==[False]*2
    assert imp['next_front']=='five_residual_ternary_npn_orbits'
    print('V100 verification passed: literal-substitution peeling, exact 144/74 NPN split, 0x07 closure, and strict non-unate 0x19 family.')

if __name__=='__main__': main()
