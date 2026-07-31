#!/usr/bin/env python3
"""Isolated full-tier replay of the deterministic V70 exact-objective search."""
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
from v70_frontier_ordering import exact_objective_search
HERE=Path(__file__).resolve().parent

def check_one(n:int):
    search=json.loads((HERE/'SEARCH_SPEC.json').read_text());v69=json.loads((HERE.parent/'v69'/'seed_data.json').read_text())
    config=search['searches'][str(n)];start=v69['robust_search'][str(n)]['specs']
    found=exact_objective_search(n,start,config['seed'],config['steps'],config['temperature'])
    assert found['Gstar']==config['expected_Gstar'];assert found['step']==config['expected_step'];assert found['specs']==config['specs']
    print(f'V70 isolated n={n} search replay passed: G*={found["Gstar"]}, step={found["step"]}.')

def main():
    if len(sys.argv)==3 and sys.argv[1]=='--n':check_one(int(sys.argv[2]));return
    for n in (8,10):subprocess.run([sys.executable,str(Path(__file__).resolve()),'--n',str(n)],check=True)
    print('V70 isolated search replay passed: 6 deterministic record checks; G*=29 and 30 reproduced; zero failures.')
if __name__=='__main__':main()
