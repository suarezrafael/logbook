#!/usr/bin/env python3
"""Core algorithms for Laboratory V55."""
from __future__ import annotations
from itertools import permutations, product
from typing import Iterable, Sequence


def xor_basis(vectors: Iterable[int]) -> list[int]:
    pivots={}
    for raw in vectors:
        value=int(raw)
        while value:
            pivot=value.bit_length()-1
            if pivot in pivots:value^=pivots[pivot]
            else:
                pivots[pivot]=value
                for p,row in list(pivots.items()):
                    if p!=pivot and ((row>>pivot)&1):pivots[p]=row^value
                break
    return [pivots[p] for p in sorted(pivots,reverse=True)]


def xor_rank(vectors):return len(xor_basis(vectors))


def in_span(vector,basis_vectors):
    basis={v.bit_length()-1:v for v in xor_basis(basis_vectors)};value=int(vector)
    while value:
        p=value.bit_length()-1
        if p not in basis:return False
        value^=basis[p]
    return True


def subspace_contained(subspace,spanning_rows):
    b=xor_basis(spanning_rows);return all(in_span(r,b) for r in subspace)


def npn_transform(mask,perm,negs,outneg):
    out=0
    for x in range(8):
        bits=[(x>>i)&1 for i in range(3)]
        old=[bits[perm[i]]^negs[i] for i in range(3)]
        idx=old[0]|old[1]<<1|old[2]<<2
        out|=((((mask>>idx)&1)^outneg)<<x)
    return out


def npn_orbit(mask):
    return tuple(sorted({npn_transform(mask,p,n,o) for p in permutations(range(3)) for n in product((0,1),repeat=3) for o in (0,1)}))


def npn_classes():
    remaining=set(range(256));classes={}
    while remaining:
        seed=min(remaining);orb=npn_orbit(seed);classes[min(orb)]=orb;remaining.difference_update(orb)
    return dict(sorted(classes.items()))


def essential_variables(mask):
    return tuple(i for i in range(3) if any(((mask>>x)&1)!=((mask>>(x^(1<<i)))&1) for x in range(8)))


def fiber(mask,value):return tuple(x for x in range(8) if ((mask>>x)&1)==value)


def affine_subset_info(points):
    pts=tuple(sorted(set(map(int,points))))
    if not pts:return None
    base=pts[0];translated={p^base for p in pts}
    if any((a^b) not in translated for a in translated for b in translated):return None
    db=xor_basis(translated)
    if len(translated)!=(1<<len(db)):return None
    annih=[q for q in range(1,8) if all(((q&d).bit_count()&1)==0 for d in db)]
    ab=xor_basis(annih)
    return {'base':base,'points':pts,'dimension':len(db),'codimension':3-len(db),'annihilator_basis':tuple(ab),'equations':tuple((q,(q&base).bit_count()&1) for q in ab)}


def oriented_affine_fiber(mask):
    candidates=[]
    for value in (1,0):
        info=affine_subset_info(fiber(mask,value))
        if info:candidates.append((len(info['points']),-value,value,info))
    if not candidates:return None
    _,_,value,info=min(candidates);return {'active_value':value,**info}


def classify_npn_classes():
    rows=[]
    for canonical,orb in npn_classes().items():
        info=oriented_affine_fiber(canonical);essential=essential_variables(canonical)
        row={'canonical_mask':f'0x{canonical:02x}','canonical_int':canonical,'orbit_size':len(orb),'ones':len(fiber(canonical,1)),'essential_arity':len(essential),'essential_variables':list(essential),'has_affine_orientation':info is not None}
        if info:row.update({'active_value':info['active_value'],'affine_fiber_size':len(info['points']),'affine_dimension':info['dimension'],'affine_codimension':info['codimension'],'affine_points':list(info['points']),'annihilator_basis':list(info['annihilator_basis'])})
        rows.append(row)
    return rows


def lift_local_equation(q,rhs,support,n):
    row=0
    for local in range(3):
        if (q>>local)&1:row^=1<<int(support[local])
    if rhs:row^=1<<n
    return row


def gate_affine_block(mask,support,n):
    if len(support)!=3 or len(set(support))!=3:raise ValueError('three distinct positions required')
    info=oriented_affine_fiber(mask)
    if not info:raise ValueError('non-affine fiber')
    rows=xor_basis(lift_local_equation(q,rhs,support,n) for q,rhs in info['equations'])
    return {'active_value':info['active_value'],'rows':tuple(rows),'codimension':len(rows)}


def redundant_block(blocks):
    allrows=[r for b in blocks for r in b['rows']];total=xor_rank(allrows)
    for i in range(len(blocks)):
        other=[r for j,b in enumerate(blocks) if j!=i for r in b['rows']]
        if xor_rank(other)==total:return i
    return None


def minimal_implying_blocks(blocks,target_index):
    chosen=[j for j in range(len(blocks)) if j!=target_index];target=list(blocks[target_index]['rows'])
    for j in list(chosen):
        trial=[k for k in chosen if k!=j]
        if subspace_contained(target,[r for k in trial for r in blocks[k]['rows']]):chosen=trial
    return chosen


def affine_block_certificate(n,gates,ambient_dimension_bound=None):
    blocks=[gate_affine_block(g['mask'],g['support'],n) for g in gates];i=redundant_block(blocks)
    if i is None:raise ValueError('no redundant block')
    js=minimal_implying_blocks(blocks,i);z=[0]*len(blocks)
    for j in js:z[j]=1
    y=[b['active_value'] if z[k] else 1-b['active_value'] for k,b in enumerate(blocks)]
    allrows=[r for b in blocks for r in b['rows']];other=[r for j,b in enumerate(blocks) if j!=i for r in b['rows']]
    return {'redundant_gate':i,'implying_gates':js,'normalized_target':z,'original_target':y,'active_values':[b['active_value'] for b in blocks],'block_rows':[list(b['rows']) for b in blocks],'global_row_rank':xor_rank(allrows),'rank_without_redundant':xor_rank(other),'ambient_dimension_bound':ambient_dimension_bound,'separator_degree_bound':len(js)+1}


def gate_value(mask,support,assignment):
    local=sum(((assignment>>int(v))&1)<<i for i,v in enumerate(support));return (mask>>local)&1


def circuit_output_bits(gates,assignment):return tuple(gate_value(g['mask'],g['support'],assignment) for g in gates)


def target_is_absent(n,gates,target):return all(circuit_output_bits(gates,x)!=tuple(target) for x in range(1<<n))


def verify_affine_certificate(n,gates,cert,exhaustive=True):
    blocks=[gate_affine_block(g['mask'],g['support'],n) for g in gates];i=cert['redundant_gate'];js=cert['implying_gates']
    if not subspace_contained(blocks[i]['rows'],[r for j in js for r in blocks[j]['rows']]):return False
    if cert['rank_without_redundant']!=cert['global_row_rank']:return False
    return (not exhaustive) or target_is_absent(n,gates,cert['original_target'])


def antipodal_row_invariant(row,n):return ((row&((1<<n)-1)).bit_count()&1)==0


def parity3_affine_form(mask,support,n):
    values=[gate_value(mask,support,x) for x in range(1<<n)];constant=values[0];coeff=0
    for v in range(n):
        if values[1<<v]^constant:coeff|=1<<v
    if any((constant^((coeff&x).bit_count()&1))!=values[x] for x in range(1<<n)):raise ValueError('not affine')
    return coeff,constant


def left_null_vector(rows,ncols):
    piv={}
    for i,row in enumerate(rows):
        value=int(row);combo=1<<i
        while value:
            p=value.bit_length()-1
            if p in piv:value^=piv[p][0];combo^=piv[p][1]
            else:piv[p]=(value,combo);break
        if value==0 and combo:return combo
    return None


def parity3_certificate(n,gates):
    forms=[parity3_affine_form(g['mask'],g['support'],n) for g in gates];dep=left_null_vector([a for a,_ in forms],n)
    if dep is None:raise ValueError('independent')
    rhs=0;indices=[]
    for i,(_,c) in enumerate(forms):
        if (dep>>i)&1:rhs^=c;indices.append(i)
    target=[0]*len(gates);target[indices[0]]=1^rhs
    return {'dependency_mask':dep,'dependency_support':indices,'required_range_parity':rhs,'target':target}


AFFINE_CANONICALS=(0x00,0x01,0x03,0x06,0x0F,0x18,0x3C,0x69)
NONAFFINE_ESSENTIAL_CANONICALS=(0x07,0x16,0x17,0x19,0x1B,0x1E)
