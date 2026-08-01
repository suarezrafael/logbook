#!/usr/bin/env python3
from __future__ import annotations
import itertools,json,random,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/"v70"))
from v70_frontier_ordering import subset_widths_and_frontiers

def optimize_budgeted_from_tables(widths,frontiers,budget):
    m=len(widths).bit_length()-1
    if len(widths)!=(1<<m) or len(frontiers)!=len(widths):raise ValueError("subset tables must have length 2^m")
    INF=10**30;cost=[INF]*len(widths);previous=[None]*len(widths)
    if frontiers[0]<=budget:cost[0]=0
    for mask in range(len(widths)):
        if cost[mask]==INF:continue
        candidate=cost[mask]+widths[mask]
        for gate in range(m):
            if mask>>gate&1:continue
            nxt=mask|1<<gate
            if frontiers[nxt]>budget:continue
            record=previous[nxt]
            if candidate<cost[nxt] or (candidate==cost[nxt] and (record is None or gate<record[1])):
                cost[nxt]=candidate;previous[nxt]=(mask,gate)
    if cost[-1]==INF:return None
    order=[];mask=len(widths)-1
    while mask:
        mask,gate=previous[mask];order.append(gate)
    order.reverse();prefix=0;profile=[frontiers[0]]
    for gate in order:
        prefix|=1<<gate;profile.append(frontiers[prefix])
    return {"budget":budget,"G_proj":cost[-1],"order":order,"frontier_width":max(profile),"frontier_profile":profile}

def bicriteria_frontier(n,specs):
    widths,frontiers=subset_widths_and_frontiers(n,specs);feasible=[]
    for budget in range(max(frontiers,default=0)+1):
        item=optimize_budgeted_from_tables(widths,frontiers,budget)
        if item is not None:feasible.append(item)
    assert feasible
    gstar=min(item["G_proj"] for item in feasible);qstar=feasible[0]["budget"]
    gstar_item=next(item for item in feasible if item["G_proj"]==gstar)
    breakpoints=[];last=None
    for item in feasible:
        if item["G_proj"]!=last:
            breakpoints.append({"budget":item["budget"],"G_proj":item["G_proj"],"order":item["order"]});last=item["G_proj"]
    return {"qstar":qstar,"Gstar":gstar,"minimum_width_cost":feasible[0]["G_proj"],
      "minimum_width_order":feasible[0]["order"],"minimum_budget_for_Gstar":gstar_item["budget"],
      "Gstar_order":gstar_item["order"],"budget_slack_to_Gstar":gstar_item["budget"]-qstar,
      "price_of_minimum_width":feasible[0]["G_proj"]/gstar,"pareto_breakpoints":breakpoints}

def seeded_bicriteria_validation(seed=730073,samples=48):
    rng=random.Random(seed);budget_checks=0
    for _ in range(samples):
        n=rng.randint(3,5);m=rng.randint(2,6)
        specs=[{"support":rng.sample(range(n),3),"partition":rng.randrange(3)} for _ in range(m)]
        widths,frontiers=subset_widths_and_frontiers(n,specs)
        for budget in range(max(frontiers)+1):
            dynamic=optimize_budgeted_from_tables(widths,frontiers,budget);brute=None
            for order in itertools.permutations(range(m)):
                mask=0;cost=0;feasible=frontiers[0]<=budget
                if not feasible:continue
                for gate in order:
                    cost+=widths[mask];mask|=1<<gate
                    if frontiers[mask]>budget:feasible=False;break
                if feasible and (brute is None or cost<brute):brute=cost
            assert (dynamic is None)==(brute is None)
            if dynamic is not None:assert dynamic["G_proj"]==brute
            budget_checks+=1
    return {"seed":seed,"systems":samples,"budget_checks":budget_checks}

def frozen_bicriteria_benchmarks():
    v69=json.loads((ROOT/"v69"/"seed_data.json").read_text());v70=json.loads((ROOT/"v70"/"SEARCH_SPEC.json").read_text())
    records=[];expected={6:15,8:15,10:17,12:29}
    for n in (6,8,10,12):
        result=bicriteria_frontier(n,v69["natural_records"][str(n)]["specs"]);assert result["Gstar"]==expected[n]
        records.append({"label":f"v69-natural-n{n}",**result})
    for n in (8,10):
        config=v70["searches"][str(n)];result=bicriteria_frontier(n,config["specs"]);assert result["Gstar"]==config["expected_Gstar"]
        records.append({"label":f"v70-exact-record-n{n}",**result})
    return records
