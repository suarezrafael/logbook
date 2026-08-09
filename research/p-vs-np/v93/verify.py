#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from affine_certificate_no_go import build_results

ROOT=Path(__file__).resolve().parent
STATUS=ROOT.parent/'LAB_STATUS.json'

def version_number(name:str)->int:
    assert name.startswith('V')
    return int(name[1:])

def verify_status(status:dict)->None:
    promoted=status['promoted_version']; candidate=status.get('candidate_version'); highest=status['highest_directory']
    if candidate=='V93':
        assert promoted=='V92'
        assert highest=='V93'
        assert status['promotion_state']=='candidate'
        assert status['next_laboratory_version']=='V93'
    else:
        assert version_number(promoted)>=93
        if candidate is None:
            assert highest==promoted
            assert status['promotion_state']=='promoted'
            assert status['next_laboratory_version']==f"V{version_number(promoted)+1}"
        else:
            assert version_number(candidate)==version_number(promoted)+1
            assert highest==candidate

def main():
    committed=json.loads((ROOT/'RESULTS.json').read_text())
    rebuilt=build_results()
    assert rebuilt==committed
    c=committed['mandatory_affine_comparison_census']
    assert c['ternary_functions']==256
    assert c['affine_functions']==16
    assert c['nonaffine_functions']==240
    assert c['nonaffine_balanced_functions']==56
    assert c['nonaffine_unbalanced_functions']==184
    assert c['same_certificate_nonaffine_functions']==240
    assert c['nonaffine_no_common_avoider_pairs']==120
    assert c['opposite_canonical_decision_pairs']==92
    assert c['support_mismatches']==0
    assert c['syndrome_mismatches_on_nonaffine']==0
    assert c['range_partition_mismatches']==0
    assert c['decision_mismatches_on_unbalanced_nonaffine']==0
    r=committed['representative_and_vs_nand']
    assert r['child_counts_f']==[7,1]
    assert r['child_counts_not_f']==[1,7]
    assert r['canonical_bit_f']==1 and r['canonical_bit_not_f']==0
    assert r['image_union_size']==16 and r['image_intersection_size']==0
    a=committed['track_a_zero_detection']
    assert a['forced_next_bit']==1
    assert [a['count_child_0'],a['count_child_1']]==[0,2]
    assert a['certificate_can_certify_empty_child_here']
    t=committed['theorem_status']
    assert t['global_affine_syndrome_comparison_oracle_closed']
    assert t['certificate_only_single_valued_avoider_closed']
    assert t['high_width_lift_symbolic']
    assert t['zero_detection_subroutine_survives']
    assert not t['all_instance_polynomial_time']
    assert not t['p_vs_np_resolved']
    implication=json.loads((ROOT/'IMPLICATION.json').read_text())
    assert implication['laboratory']=='V93'
    assert implication['classification']=='barrier_and_closure'
    assert implication['mandatory_affine_gate_outcome']=='comparison_collision'
    assert implication['stop_rule_fired']
    assert [x['proved'] for x in implication['bridge_lemmas'][:5]]==[True]*5
    assert implication['bridge_lemmas'][5]['proved'] is False
    if STATUS.exists(): verify_status(json.loads(STATUS.read_text()))
    print('V93 verification passed: 256-function affine-comparison gate, 92 opposite-decision complement pairs, no-common-avoider theorem controls, high-width lift contract, and Track-A zero detection.')

if __name__=='__main__': main()
