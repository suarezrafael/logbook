#!/usr/bin/env python3
"""Fail when a promoted-era laboratory verifier is omitted from verify_all.sh."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
POLICY_VERSION = 63

def version_number(name):
    match=re.fullmatch(r'v(\d+)',name)
    if not match:raise ValueError(name)
    return int(match.group(1))
def main():
    runner=(ROOT/'verify_all.sh').read_text();ledger=json.loads((ROOT/'LEDGER.json').read_text())
    entries=re.findall(r'"(V\d+)\|([^|]+)\|([^|]+)\|',runner);keys=[(v,k) for v,k,_ in entries]
    assert len(keys)==len(set(keys)),'duplicate version/kind entries in runner'
    registered={(v,k,p) for v,k,p in entries};required=[]
    for directory in sorted(ROOT.glob('v[0-9]*'),key=lambda p:version_number(p.name)):
        number=version_number(directory.name)
        if number<POLICY_VERSION:continue
        version=f'V{number}'
        if (directory/'verify.py').is_file():required.append((version,'primary',f'{directory.name}/verify.py'))
        if (directory/'verify_independent.py').is_file():required.append((version,'independent',f'{directory.name}/verify_independent.py'))
    missing=[item for item in required if item not in registered]
    assert not missing,f'promoted-era verifier omitted from runner: {missing}'
    current=ledger['current_version'];number=int(current[1:]);directory=f'v{number}'
    assert (current,'primary',f'{directory}/verify.py') in registered
    assert (current,'independent',f'{directory}/verify_independent.py') in registered
    print(f'Runner coverage passed: {len(required)} promoted-era verifier entries; current={current}.')
if __name__=='__main__':main()
