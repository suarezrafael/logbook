#!/usr/bin/env python3
"""Independent repository audit for V56; no import from verify.py."""
import itertools, json, random
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def tr(mask,p,n,o):
 out=0
 for x in range(8):
  b=[(x>>i)&1 for i in range(3)]; old=[b[p[i]]^n[i] for i in range(3)]; j=old[0]|old[1]<<1|old[2]<<2
  out|=((((mask>>j)&1)^o)<<x)
 return out

def orb(mask): return sorted({tr(mask,p,n,o) for p in itertools.permutations(range(3)) for n in itertools.product((0,1),repeat=3) for o in (0,1)})
def aff(P):
 P=set(P)
 if not P:return False
 a=next(iter(P)); L={x^a for x in P}
 return len(L)&(len(L)-1)==0 and all(x^y in L for x in L for y in L)
def orient(m):
 for v in (0,1):
  P={x for x in range(8) if ((m>>x)&1)==v}
  if P and aff(P):return v,P
 return None
def aset(m):
 v,P=orient(m); return P
def good(masks):
 sets=[aset(m) for m in masks]; U=set(range(8)); I=U.copy()
 for S in sets:I&=S
 if not I:return True
 for i,S in enumerate(sets):
  J=U.copy()
  for j,T in enumerate(sets):
   if i!=j:J&=T
  if J<=S:return True
 return False

def main():
 rem=set(range(256)); cls=[]
 while rem:
  o=orb(min(rem)); cls.append((min(o),o)); rem-=set(o)
 assert len(cls)==14
 assert [c for c,o in cls if any(orient(m) for m in o)]==[0,1,3,6,15,24,60,105]
 c06=sum(1 for ms in itertools.combinations_with_replacement(orb(6),4) if good(ms)); assert c06==17550
 c01=sum(1 for ms in itertools.combinations_with_replacement(orb(1),4) if good(ms)); assert c01==3876
 rng=random.Random(5657); fresh=0
 affine=[m for m in range(256) if orient(m)]
 for _ in range(240):
  n=rng.randrange(3,9); masks=[rng.choice(affine) for __ in range(n+1)]
  sets=[aset(m) for m in masks]; U=set(range(8)); I=U.copy()
  for S in sets:I&=S
  assert (not I) or any((lambda i: (lambda J: J<=sets[i])(__import__('functools').reduce(set.intersection,[sets[j] for j in range(len(sets)) if j!=i],U.copy())))(i) for i in range(len(sets)))
  fresh+=1
 result={'status':'passed','npn_classes':14,'distance_two_multisets':c06,'singleton_multisets':c01,'fresh_cases':fresh,'failures':0}
 (ROOT/'REPO_INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print('V56 independent repository audit passed: 14 classes, 21426 exhaustive multisets, 240 fresh cases, zero failures.')
if __name__=='__main__':main()
