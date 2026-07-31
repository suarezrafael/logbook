#!/usr/bin/env python3
from __future__ import annotations
import csv, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
source=ROOT/'exact_single_flip_search.cpp'
binary=ROOT/'exact_single_flip_search'
cmd=['g++','-O3','-std=c++17','-fopenmp',str(source),'-o',str(binary)]
try:
    subprocess.run(cmd,check=True,capture_output=True,text=True)
except (FileNotFoundError,subprocess.CalledProcessError) as exc:
    raise SystemExit(f'cannot compile exact verifier: {exc}')
threads=max(1,min(8,os.cpu_count() or 1))
run=subprocess.run([str(binary),'3','8','500000000',str(threads)],check=True,capture_output=True,text=True,timeout=240)
(ROOT/'EXACT_SEARCH_RESULTS.csv').write_text(run.stdout,encoding='utf-8')
rows=list(csv.DictReader(run.stdout.splitlines()))
assert len(rows)==12
assert all(r['found_counterexample']=='0' and r['complete']=='1' for r in rows)
summary={'n_min':3,'n_max':8,'canonical_types':[1,3],'cases':len(rows),'counterexamples':0,'all_complete':True,'total_nodes':sum(int(r['nodes']) for r in rows),'threads':threads}
(ROOT/'EXACT_SEARCH_SUMMARY.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('V58 exact verifier passed:')
print('  complete symmetry-reduced search for n=3..8;')
print('  both normalized first-block types checked;')
print(f"  {summary['total_nodes']} DFS nodes; zero one-flip counterexamples.")
