#!/usr/bin/env python3
from __future__ import annotations
import itertools,json,random,time
from pathlib import Path
import v55_core as c
ROOT=Path(__file__).resolve().parent;SEED=550055


def gate(rng,n,orb):return {'mask':rng.choice(orb),'support':tuple(rng.sample(range(n),3))}


def main():
    start=time.perf_counter();rng=random.Random(SEED)
    cls=c.classify_npn_classes();assert len(cls)==14 and sum(r['orbit_size'] for r in cls)==256
    assert [r['canonical_int'] for r in cls]==[0x00,0x01,0x03,0x06,0x07,0x0f,0x16,0x17,0x18,0x19,0x1b,0x1e,0x3c,0x69]
    aff=[r['canonical_int'] for r in cls if r['has_affine_orientation'] and r['essential_arity']==3]
    non=[r['canonical_int'] for r in cls if not r['has_affine_orientation'] and r['essential_arity']==3]
    assert aff==[0x01,0x06,0x18,0x69] and non==list(c.NONAFFINE_ESSENTIAL_CANONICALS)

    orb18=c.npn_orbit(0x18);assert len(orb18)==8
    for mask in orb18:
        info=c.oriented_affine_fiber(mask);assert info and len(info['points'])==2 and info['points'][0]^info['points'][1]==7
        for support in itertools.combinations(range(5),3):
            b=c.gate_affine_block(mask,support,5);assert all(c.antipodal_row_invariant(r,5) for r in b['rows'])

    hist={};exhaustive=0
    for masks in itertools.product(orb18,repeat=4):
        gates=[{'mask':m,'support':(0,1,2)} for m in masks]
        cert=c.affine_block_certificate(3,gates,3);assert cert['global_row_rank']<=3 and c.verify_affine_certificate(3,gates,cert,True)
        hist[cert['separator_degree_bound']]=hist.get(cert['separator_degree_bound'],0)+1;exhaustive+=1

    random_antipodal=0
    for n in range(4,13):
        for _ in range(40):
            gates=[gate(rng,n,orb18) for __ in range(n+1)];cert=c.affine_block_certificate(n,gates,n)
            assert cert['global_row_rank']<=n and c.verify_affine_certificate(n,gates,cert,True);random_antipodal+=1

    affine_masks=tuple(sorted({m for can in c.AFFINE_CANONICALS for m in c.npn_orbit(can)}));mixed=0
    for n in range(3,11):
        for _ in range(35):
            gates=[gate(rng,n,affine_masks) for __ in range(n+2)];cert=c.affine_block_certificate(n,gates,n+1)
            assert cert['global_row_rank']<=n+1 and c.verify_affine_certificate(n,gates,cert,True);mixed+=1

    orb06=c.npn_orbit(0x06);dist=0
    for n in range(3,11):
        for _ in range(20):
            gates=[gate(rng,n,orb06) for __ in range(n+2)];cert=c.affine_block_certificate(n,gates,n+1)
            assert c.verify_affine_certificate(n,gates,cert,True);dist+=1

    orb69=c.npn_orbit(0x69);parity=0
    for n in range(3,13):
        for _ in range(25):
            gates=[gate(rng,n,orb69) for __ in range(n+1)];cert=c.parity3_certificate(n,gates)
            assert c.target_is_absent(n,gates,cert['target']);parity+=1

    abstract=0
    for d in range(1,12):
        for _ in range(50):
            blocks=[{'rows':tuple(c.xor_basis(rng.randrange(1<<d) for __ in range(rng.randrange(1,4))))} for ___ in range(d+1)]
            assert c.redundant_block(blocks) is not None;abstract+=1

    result={'version':'V55','status':'passed','seed':SEED,'theorems':{'general_affine_fiber_threshold':'m>n+1','antipodal_pair_threshold':'m>n','antipodal_canonical_mask':'0x18','antipodal_orbit_size':8,'parity3_threshold':'m>n','remaining_nonaffine_essential_classes':[f'0x{x:02x}' for x in c.NONAFFINE_ESSENTIAL_CANONICALS]},'classification':{'boolean_functions':256,'npn_classes':14,'essential_affine_classes':[f'0x{x:02x}' for x in aff],'essential_nonaffine_classes':[f'0x{x:02x}' for x in non]},'validation':{'exhaustive_antipodal_n3_m4':exhaustive,'random_antipodal_stretch_one':random_antipodal,'random_mixed_affine_n_plus_2':mixed,'distance_two_pair_n_plus_2':dist,'parity3_stretch_one':parity,'abstract_block_subspace_cases':abstract,'failures':0},'constructed_separator_degree_histogram_n3':{str(k):v for k,v in sorted(hist.items())},'scientific_status':{'peer_reviewed':False,'novelty_confirmed':False,'general_nc0_3_avoid_solved':False,'p_vs_np_resolved':False},'elapsed_seconds':round(time.perf_counter()-start,6)}
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2));(ROOT/'CLASSIFICATION.json').write_text(json.dumps(cls,indent=2))
    print('V55 primary verification passed:')
    print('  14/14 ternary NPN classes classified;')
    print(f'  {exhaustive} exhaustive antipodal-pair stretch-one circuits;')
    print(f'  {random_antipodal} random antipodal-pair stretch-one circuits;')
    print(f'  {mixed} mixed affine-fiber n+2 circuits;')
    print(f'  {dist} distance-two-pair n+2 circuits;')
    print(f'  {parity} parity3 stretch-one circuits;')
    print(f'  {abstract} abstract block-subspace regressions; zero failures.')

if __name__=='__main__':main()
