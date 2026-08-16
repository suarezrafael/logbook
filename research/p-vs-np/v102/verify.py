from itertools import combinations, permutations, product
import random
from affine_backdoor import (
    avoid_with_backdoor, gate_value, is_backdoor, minimum_backdoor,
    prefix_preimage_count, strong_affine_local,
)


def npn_transform(mask, perm, negs, outneg):
    out = 0
    for x in product((0, 1), repeat=3):
        old = tuple(x[perm[k]] ^ negs[k] for k in range(3))
        y = gate_value(mask, old) ^ outneg
        idx = x[0] | (x[1] << 1) | (x[2] << 2)
        out |= y << idx
    return out


def orbit(mask):
    return sorted({npn_transform(mask, p, n, o)
                   for p in permutations(range(3))
                   for n in product((0,1), repeat=3)
                   for o in (0,1)})

MUX = orbit(0x1b)
MAJ = orbit(0x17)


def mux_selector(mask):
    hits = []
    for s in range(3):
        if not strong_affine_local(mask, 3, {s}):
            continue
        branches = []
        ok = True
        for sv in (0,1):
            vals = {}
            for pos in range(3):
                if pos == s:
                    continue
                sig=[]
                for b in (0,1):
                    bits0=[0,0,0]; bits1=[0,0,0]
                    bits0[s]=sv; bits1[s]=sv
                    bits0[pos]=0; bits1[pos]=1
                    other=next(j for j in range(3) if j not in (s,pos))
                    good=True
                    for ov in (0,1):
                        bits0[other]=ov; bits1[other]=ov
                        if gate_value(mask,bits0)==gate_value(mask,bits1):
                            good=False
                    if good: sig.append(pos)
                if sig: vals[pos]=True
            active=list(vals)
            if len(active)!=1:
                ok=False; break
            branches.append(active[0])
        if ok and branches[0] != branches[1]:
            hits.append(s)
    return hits

assert len(MUX) == 24
assert len(MAJ) == 8
for mask in MUX:
    sels = mux_selector(mask)
    assert len(sels) == 1, (hex(mask), sels)
    s = sels[0]
    data = set(range(3)) - {s}
    for r in range(4):
        for S in combinations(range(3), r):
            observed = strong_affine_local(mask, 3, set(S))
            predicted = s in S or data.issubset(S)
            assert observed == predicted, (hex(mask), s, S, observed, predicted)
for mask in MAJ:
    for r in range(4):
        for S in combinations(range(3), r):
            observed = strong_affine_local(mask, 3, set(S))
            predicted = len(S) >= 2
            assert observed == predicted, (hex(mask), S, observed, predicted)


def circuit_eval(circuit, x):
    out=[]
    for support,mask in circuit:
        out.append(gate_value(mask, tuple(x[v] for v in support)))
    return tuple(out)

rng = random.Random(102)
random_cases = 0
for n in range(3, 9):
    for _ in range(100):
        circuit=[]; B=set()
        for _i in range(n+1):
            support=tuple(rng.sample(range(n),3))
            mask=rng.choice(MUX)
            circuit.append((support,mask))
            B.add(support[mux_selector(mask)[0]])
        assert is_backdoor(circuit,B)
        y=avoid_with_backdoor(circuit,n,B)
        image={circuit_eval(circuit,x) for x in product((0,1),repeat=n)}
        assert y not in image
        for j in range(len(y)+1):
            brute=sum(1 for x in product((0,1),repeat=n)
                      if circuit_eval(circuit,x)[:j] == y[:j])
            exact=prefix_preimage_count(circuit,n,B,list(y[:j]))
            assert brute == exact
        random_cases += 1


def strict_mux_family(n):
    assert n >= 5
    data=list(range(1,n))
    edges=[]
    for j in range(len(data)):
        e=tuple(sorted((data[j],data[(j+1)%len(data)])))
        if e not in edges:
            edges.append(e)
    for a in data:
        for b in data:
            if a < b and (a,b) not in edges:
                edges.append((a,b))
                if len(edges) == n+1:
                    break
        if len(edges) == n+1:
            break
    return [((0,a,b),0x1b) for a,b in edges]

strict_rows=[]
for n in range(5, 11):
    circuit=strict_mux_family(n)
    assert len(circuit) == n+1
    degree=[0]*n
    for support,_ in circuit:
        for v in support: degree[v]+=1
    assert min(degree) >= 2
    assert minimum_backdoor(circuit,n) == frozenset({0})
    y=avoid_with_backdoor(circuit,n,{0})
    assert y not in {circuit_eval(circuit,x) for x in product((0,1),repeat=n)}
    strict_rows.append((n,len(circuit),min(degree),1))

majority_rows=[]
for n in range(4, 10):
    circuit=[]
    for i in range(n+1):
        v=2+(i%(n-2))
        circuit.append(((0,1,v), MAJ[i%len(MAJ)]))
    assert is_backdoor(circuit,{0,1})
    y=avoid_with_backdoor(circuit,n,{0,1})
    assert y not in {circuit_eval(circuit,x) for x in product((0,1),repeat=n)}
    majority_rows.append((n,2))

print('V102 primary verification OK')
print('mux_masks', len(MUX), 'majority_masks', len(MAJ))
print('random_mux_circuits', random_cases)
print('strict_mux_rows', strict_rows)
print('majority_rows', majority_rows)
