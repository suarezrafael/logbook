#!/usr/bin/env python3
"""Independent V55 verifier; does not import v55_core."""
import itertools,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent


def transform(mask,p,n,o):
    out=0
    for x in range(8):
        b=[(x>>i)&1 for i in range(3)];old=[b[p[i]]^n[i] for i in range(3)];idx=old[0]|old[1]<<1|old[2]<<2;out|=((((mask>>idx)&1)^o)<<x)
    return out


def orbit(mask):return tuple(sorted({transform(mask,p,n,o) for p in itertools.permutations(range(3)) for n in itertools.product((0,1),repeat=3) for o in (0,1)}))


def basis(rows):
    piv={}
    for v in rows:
        while v:
            p=v.bit_length()-1
            if p in piv:v^=piv[p]
            else:piv[p]=v;break
    return list(piv.values())


def rank(rows):return len(basis(rows))


def contains(rows,targets):
    b={v.bit_length()-1:v for v in basis(rows)}
    for v in targets:
        while v:
            p=v.bit_length()-1
            if p not in b:return False
            v^=b[p]
    return True


def affine(mask):
    opts=[]
    for active in (1,0):
        pts=[x for x in range(8) if ((mask>>x)&1)==active]
        if not pts:continue
        p=pts[0];t={x^p for x in pts}
        if any((a^b) not in t for a in t for b in t):continue
        db=basis(t)
        if len(t)!=(1<<len(db)):continue
        ab=basis(q for q in range(1,8) if all(((q&d).bit_count()&1)==0 for d in db));opts.append((len(pts),-active,active,p,pts,ab))
    return min(opts) if opts else None


def block(mask,support,n):
    _,_,active,p,pts,ab=affine(mask);rows=[]
    for q in ab:
        row=0
        for i,v in enumerate(support):
            if (q>>i)&1:row^=1<<v
        if ((q&p).bit_count()&1):row^=1<<n
        rows.append(row)
    return active,basis(rows)


def gate(mask,support,x):
    local=sum(((x>>v)&1)<<i for i,v in enumerate(support));return (mask>>local)&1


def absent(n,gates,target):return all(tuple(gate(g['mask'],g['support'],x) for g in gates)!=tuple(target) for x in range(1<<n))


def certificate(n,gates):
    blocks=[block(g['mask'],g['support'],n) for g in gates];allrows=[r for _,rs in blocks for r in rs];total=rank(allrows);i=None
    for k in range(len(blocks)):
        if rank([r for j,(_,rs) in enumerate(blocks) if j!=k for r in rs])==total:i=k;break
    assert i is not None;js=[j for j in range(len(blocks)) if j!=i]
    for j in list(js):
        trial=[k for k in js if k!=j]
        if contains([r for k in trial for r in blocks[k][1]],blocks[i][1]):js=trial
    z=[0]*len(gates)
    for j in js:z[j]=1
    y=[blocks[j][0] if z[j] else 1-blocks[j][0] for j in range(len(gates))]
    return total,y


def main():
    rem=set(range(256));cls={}
    while rem:
        seed=min(rem);o=orbit(seed);cls[min(o)]=o;rem.difference_update(o)
    assert list(cls)==[0x00,0x01,0x03,0x06,0x07,0x0f,0x16,0x17,0x18,0x19,0x1b,0x1e,0x3c,0x69]
    assert [c for c in cls if affine(c)]==[0x00,0x01,0x03,0x06,0x0f,0x18,0x3c,0x69]
    orb=orbit(0x18);assert len(orb)==8
    for m in orb:
        info=affine(m);assert len(info[4])==2 and info[4][0]^info[4][1]==7
    exhaustive=0
    for masks in itertools.product(orb,repeat=4):
        gates=[{'mask':m,'support':(0,1,2)} for m in masks];total,y=certificate(3,gates);assert total<=3 and absent(3,gates,y);exhaustive+=1
    rng=random.Random(919155);fresh=0
    for n in range(4,11):
        for _ in range(20):
            gates=[{'mask':rng.choice(orb),'support':tuple(rng.sample(range(n),3))} for __ in range(n+1)];total,y=certificate(n,gates);assert total<=n and absent(n,gates,y);fresh+=1
    print('V55 independent verification passed:')
    print('  14 ternary NPN classes rebuilt;')
    print(f'  {exhaustive} antipodal-pair circuits rechecked exhaustively;')
    print(f'  {fresh} fresh random stretch-one circuits; zero failures.')

if __name__=='__main__':main()
