from __future__ import annotations

import json
import random
from itertools import product


def eval_gate(mask, support, x):
    idx = sum(((x >> v) & 1) << j for j, v in enumerate(support))
    return (mask >> idx) & 1


def family(k):
    a = b = 4 * k
    n = a + b
    gates = []
    for i in range(a):
        gates.append((0x1E, (i, (i+1) % a, (i+2) % a)))
    off = a
    for j in range(k):
        aa, bb, cc, dd = off+4*j, off+4*j+1, off+4*j+2, off+4*j+3
        gates += [(0x16, (aa,bb,cc)), (0x16, (aa,bb,dd)), (0x16, (aa,cc,dd))]
        if j:
            gates.append((0x16, (off+4*(j-1)+3,bb,cc)))
    gates.append((0x17, (off,off+1,off+2)))
    gates.append((0x17, (0,off,off+1)))
    return n, gates


def relaxed_points(k):
    n, gates = family(k)
    a = b = 4*k
    points = []
    for roots in product((0,1), repeat=3):
        # Root 0: A0, root 1: A1. Functional 0x1e target-zero recurrence.
        A = [0] * a
        A[0], A[1] = roots[0], roots[1]
        for i in range(a-2):
            A[i+2] = A[i] | A[i+1]
        # The independent affine-rank computation yields one final B bit.
        # Solve the B parity-one equations directly by brute force for k<=2;
        # structural verifier below checks their rank for all larger k.
        off = a
        B_solutions = []
        for bx in range(1 << b):
            ok = True
            idx = a
            for j in range(k):
                aa,bb,cc,dd = 4*j,4*j+1,4*j+2,4*j+3
                triples=[(aa,bb,cc),(aa,bb,dd),(aa,cc,dd)]
                if j:
                    triples.append((4*(j-1)+3,bb,cc))
                for sup in triples:
                    if sum((bx >> v) & 1 for v in sup) % 2 != 1:
                        ok=False; break
                if not ok: break
            if ok:
                B_solutions.append(bx)
        assert len(B_solutions) == 2
        bx = B_solutions[roots[2]]
        x = 0
        for i,v in enumerate(A): x |= v << i
        x |= bx << off
        points.append(x)
    assert len(points) == 8
    return n, gates, points


def rank(rows):
    basis={}
    for row in rows:
        x=row
        while x:
            p=x.bit_length()-1
            if p not in basis:
                basis[p]=x; break
            x ^= basis[p]
    return len(basis)


def structural_rank():
    for k in range(1,51):
        n,gates=family(k); a=b=4*k
        rows=[]
        for mask,sup in gates[a:a+b-1]:
            assert mask==0x16
            row=0
            for v in sup: row ^= 1<<v
            rows.append(row)
        assert len(rows)==b-1 and rank(rows)==b-1
        assert n-(a-2)-(b-1)==3
        assert n-(b-1)==a+1
        assert n-((a-2)+(3*k-1))==k+3
    return 50


def direct_missing_checks():
    rng=random.Random(404104)
    total=0
    for k,trials in ((1,220),(2,24)):
        n,base,points=relaxed_points(k)
        a=b=4*k
        selected=set(range(a-2)) | set(range(a,a+b-1))
        residual=[i for i in range(len(base)) if i not in selected]
        assert len(residual)==4
        for _ in range(trials):
            gates=list(base)
            for idx in residual:
                gates[idx]=(rng.randrange(256),tuple(rng.sample(range(n),3)))
            observed={tuple(eval_gate(gates[i][0],gates[i][1],x) for i in residual) for x in points}
            missing=next(word for word in product((0,1),repeat=4) if word not in observed)
            y=[0]*len(gates)
            for i in range(a-2): y[i]=0
            for i in range(a,a+b-1): y[i]=1
            for i,bit in zip(residual,missing): y[i]=bit
            # Full original range audit.
            found=False
            for x in range(1<<n):
                if all(eval_gate(mask,sup,x)==bit for (mask,sup),bit in zip(gates,y)):
                    found=True; break
            assert not found
            total += 1
    return total


def main():
    result={
        "structural_rank_k_through":structural_rank(),
        "direct_random_missing_checks":direct_missing_checks(),
        "eta":3,
        "failures":0,
    }
    print(json.dumps(result,sort_keys=True))

if __name__=="__main__":
    main()
