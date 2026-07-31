#!/usr/bin/env python3
from __future__ import annotations
import itertools
from functools import lru_cache

NON_AFFINE_CLASSES = (0x07, 0x16, 0x17, 0x19, 0x1B, 0x1E)


def affine_set(points):
    points=set(points)
    if not points:return False
    base=next(iter(points));linear={x^base for x in points}
    return 0 in linear and all((u^v) in linear for u in linear for v in linear)


def affine_subsets(n):
    return {frozenset(x for x in range(1<<n) if (mask>>x)&1) for mask in range(1,1<<(1<<n)) if affine_set(frozenset(x for x in range(1<<n) if (mask>>x)&1))}


def partitions(fiber,affine):
    found=set()
    for left in affine:
        if left<fiber:
            right=fiber-left
            if right and right in affine:found.add(tuple(sorted((tuple(sorted(left)),tuple(sorted(right))))))
    return tuple((frozenset(a),frozenset(b)) for a,b in sorted(found))


def permute_mask(mask,permutation,negations,output_flip):
    result=0
    for assignment in range(8):
        bits=[(assignment>>i)&1 for i in range(3)]
        transformed=[bits[permutation[i]]^negations[i] for i in range(3)]
        source=transformed[0]|(transformed[1]<<1)|(transformed[2]<<2)
        result|=((((mask>>source)&1)^output_flip)<<assignment)
    return result


def orbit(mask):
    return frozenset(permute_mask(mask,p,n,o) for p in itertools.permutations(range(3)) for n in itertools.product((0,1),repeat=3) for o in (0,1))


def non_affine_fibers():
    values=set()
    for representative in NON_AFFINE_CLASSES:
        for mask in orbit(representative):
            for output in (0,1):
                fiber=frozenset(x for x in range(8) if ((mask>>x)&1)==output)
                if not affine_set(fiber):values.add(fiber)
    return tuple(sorted(values,key=lambda s:(len(s),tuple(sorted(s)))))


def branch_signatures(parts,universe):
    signatures=set()
    for point in universe:
        word=[]
        for cell0,cell1 in parts:
            if point in cell0:word.append(0)
            elif point in cell1:word.append(1)
            else:break
        else:signatures.add(tuple(word))
    return frozenset(signatures)


def optimal_pruned_tree(parts,universe):
    @lru_cache(None)
    def solve(feasible,remaining):
        current=frozenset(feasible)
        if not current or not remaining:return 1,0,0,None
        best=None
        for gate in remaining:
            tail=tuple(x for x in remaining if x!=gate)
            a=solve(tuple(sorted(current&parts[gate][0])),tail)
            b=solve(tuple(sorted(current&parts[gate][1])),tail)
            candidate=(a[0]+b[0],1+a[1]+b[1],1+max(a[2],b[2]),gate)
            if best is None or candidate[:3]<best[:3]:best=candidate
        return best
    reached=set()
    def walk(feasible,remaining):
        state=(feasible,remaining)
        if state in reached:return
        reached.add(state);current=frozenset(feasible)
        if not current or not remaining:return
        gate=solve(feasible,remaining)[3];tail=tuple(x for x in remaining if x!=gate)
        walk(tuple(sorted(current&parts[gate][0])),tail);walk(tuple(sorted(current&parts[gate][1])),tail)
    remaining=tuple(range(len(parts)));root=solve(tuple(universe),remaining);walk(tuple(universe),remaining)
    return root[0],root[1],root[2],len(reached)


def v57_blocks():
    blocks=[set() for _ in range(5)]
    for raw in range(16):
        x0,x1,x2,x3=((raw>>i)&1 for i in range(4))
        values=((not x0)and((not x1)or x2),(not x0)and(x1 or(not x2)),(not x0)and((not x1)or x3),(not x0)and(x1 or(not x3)),(not x0)and((not x2)or(not x3)))
        for i,value in enumerate(values):
            if value:blocks[i].add(raw)
    return tuple(frozenset(x) for x in blocks)


def canonical_variants(affine3):
    variants=[]
    for representative in NON_AFFINE_CLASSES:
        for output in (0,1):
            fiber=frozenset(x for x in range(8) if ((representative>>x)&1)==output)
            for index,part in enumerate(partitions(fiber,affine3)):variants.append((fiber,part,(representative,output,index)))
    return tuple(variants)


def lift(local,support,n=4):
    return frozenset(point for point in range(1<<n) if sum(((point>>v)&1)<<i for i,v in enumerate(support)) in local)


def lifted_n4_variants():
    unique={};affine3=affine_subsets(3)
    for fiber,part,meta in canonical_variants(affine3):
        for support in itertools.permutations(range(4),3):
            global_fiber=lift(fiber,support)
            cells=tuple(sorted((lift(part[0],support),lift(part[1],support)),key=lambda s:tuple(sorted(s))))
            unique.setdefault((global_fiber,cells),[]).append(meta+(support,))
    return tuple((fiber,cells,tuple(sorted(meta))) for (fiber,cells),meta in sorted(unique.items(),key=lambda item:(len(item[0][0]),tuple(sorted(item[0][0])),tuple(sorted(item[0][1][0])),tuple(sorted(item[0][1][1])))))
