#!/usr/bin/env python3
"""Independent audit of the preserved V53 finite results and V54 retraction."""
import itertools, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent


def edge_mask(edge):
    value=0
    for v in edge: value |= 1<<v
    return value


def image(n,edges):
    answers=set()
    for x in range(1<<n):
        y=0
        for i,edge in enumerate(edges):
            bit=1
            for v in edge: bit &= (x>>v)&1
            y |= bit<<i
        answers.add(y)
    return sorted(answers)


def monomials(m,d):
    ans=[()]
    for size in range(1,d+1): ans.extend(itertools.combinations(range(m),size))
    return ans


def rank_columns(points,m,d):
    columns=[]
    for monomial in monomials(m,d):
        column=0
        for row,point in enumerate(points):
            if all((point>>i)&1 for i in monomial): column |= 1<<row
        columns.append(column)
    pivots={}; rank=0
    for value in columns:
        while value:
            pivot=value.bit_length()-1
            if pivot in pivots: value ^= pivots[pivot]
            else: pivots[pivot]=value; rank += 1; break
    return rank,len(columns)


def first_union_collision(edges,t):
    masks=[edge_mask(e) for e in edges]
    seen={}
    for size in range(t+1):
        for chosen in itertools.combinations(range(len(edges)),size):
            union=0
            for i in chosen: union |= masks[i]
            if union in seen:
                return seen[union], chosen
            seen[union]=chosen
    return None


def main():
    records=json.loads((ROOT/'FINITE_EXAMPLES.json').read_text(encoding='utf-8'))
    union_checks=0
    for record in records:
        edges=record['edges']; t=record['t_union_free']; m=record['m']
        seen={}; masks=[edge_mask(e) for e in edges]
        for size in range(t+1):
            for chosen in itertools.combinations(range(m),size):
                union=0
                for i in chosen: union |= masks[i]
                assert union not in seen
                seen[union]=chosen; union_checks += 1
        points=image(record['n'],edges)
        assert len(points)==record['range_size']
        for degree in range(t+1):
            rank,count=rank_columns(points,m,degree); assert rank==count
        rank,count=rank_columns(points,m,t+1); assert rank<count
        assert record['minimum_syndrome_degree_gf2']==t+1

    nested_cover=[(0,1,2),(0,3,4),(1,5,6),(2,7,8)]
    collision=first_union_collision(nested_cover,4)
    assert collision is not None
    left,right=collision
    assert set(left)=={1,2,3}
    assert set(right)=={0,1,2,3}

    print('V53 corrected independent verification passed:')
    print(f'  {len(records)} finite examples rebuilt from JSON;')
    print(f'  {union_checks} union values independently checked;')
    print('  exact GF(2) syndrome degrees independently reconstructed;')
    print('  acyclic nested-cover collision independently detected.')

if __name__=='__main__': main()
