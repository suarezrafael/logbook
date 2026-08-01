#!/usr/bin/env python3
from __future__ import annotations
import json,math,re
from pathlib import Path
from v73_bicriteria_avoidance import generate_results
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent

def main():
    committed=json.loads((HERE/"RESULTS.json").read_text())
    results=generate_results()
    assert committed==results,"committed V73 RESULTS.json differs from generate_results()"
    required=["README.md","BICRITERIA_AND_MULTIPLICITY.md","BICRITERIA_BENCHMARK.md",
      "V73_BICRITERIA_AVOIDANCE_THEOREM.tex","V74_CORE_CONTEXT.md","bicriteria.py","multiplicity.py",
      "tree_compression.py","v73_bicriteria_avoidance.py","verify.py","verify_independent.py","RESULTS.json"]
    assert all((HERE/name).is_file() for name in required)
    assert results["version"]=="V73" and results["status"]=="passed" and results["failures"]==0
    assert results["bicriteria_validation"]=={"seed":730073,"systems":48,"budget_checks":211}
    assert results["multiplicity_validation"]=={"seed":730074,"systems":96,"branch_nodes":808}
    expected={"v69-natural-n6":(4,18,15,6,2),"v69-natural-n8":(4,16,15,5,1),
      "v69-natural-n10":(4,24,17,7,3),"v69-natural-n12":(4,52,29,7,3),
      "v70-exact-record-n8":(4,31,29,6,2),"v70-exact-record-n10":(5,32,30,7,2)}
    records={x["label"]:x for x in results["frozen_bicriteria_benchmarks"]};assert set(records)==set(expected)
    for label,values in expected.items():
        item=records[label];actual=(item["qstar"],item["minimum_width_cost"],item["Gstar"],
          item["minimum_budget_for_Gstar"],item["budget_slack_to_Gstar"])
        assert actual==values,(label,actual,values)
    assert math.isclose(results["benchmark_summary"]["maximum_price_of_minimum_width"],52/29,rel_tol=0,abs_tol=1e-12)
    assert results["benchmark_summary"]["maximum_budget_slack_to_Gstar"]==3
    binary=results["binary_tree_compression"];assert [x["m"] for x in binary]==[2,6,14,30,62,126,254]
    assert all(x["postorder_G_proj"]==x["proved_Gstar"]==x["m"] for x in binary)
    assert all(x["maximum_postorder_layer_width"]==1 and x["maximum_internal_residual_states"]==1 for x in binary)
    assert all(x["maximum_leaf_residual_states"]<=2 for x in binary)
    spine=results["spine_multiplicity"];assert [x["consistent_complete_branches"] for x in spine]==[1,2,4,8,16,32,64,128]
    interface=results["avoidance_interface"];assert interface["searches_target_words_without_dual_fiber_data"] is False
    assert interface["normalized_example"]["can_certify_current_selected_target_as_avoided"] is False
    assert interface["synthetic_supplied_target"]["target_is_certified_outside_image"] is True
    scientific=results["scientific_status"]
    assert scientific["bicriteria_optimum_computed_exactly"] and scientific["complete_branch_multiplicities_counted_exactly"]
    assert scientific["current_normalized_schema_constructs_avoidance_witness"] is False
    assert scientific["binary_tree_family_Gstar_linear_proved"] is True
    assert scientific["p_vs_np_resolved"] is False
    proof=(HERE/"BICRITERIA_AND_MULTIPLICITY.md").read_text()
    for token in ("C_B(S) = min","root multiplicity = 0","all-zero input","G*_proj = m","support-width hardness does not lower-bound"):assert token in proof
    benchmark=(HERE/"BICRITERIA_BENCHMARK.md").read_text()
    for token in ("52/29","1.793","minimum budget attaining"):assert token in benchmark
    tex=(HERE/"V73_BICRITERIA_AVOIDANCE_THEOREM.tex").read_text()
    for token in ("Exact bicriteria dynamic program","Exact branch multiplicities","Normalized-schema barrier","Unbounded width with minimum residual cost"):assert token in tex
    runner=(ROOT/"verify_all.sh").read_text();assert "V73|primary|v73/verify.py|quick|" in runner and "V73|independent|v73/verify_independent.py|quick|" in runner
    state=(ROOT/"STATE.md").read_text();current=re.search(r"\*\*Current laboratory:\*\* V(\d+)(?: candidate)?",state)
    assert current and int(current.group(1))>=73 and "all-zero" in state.lower() and "G*_proj=m" in state
    root=(ROOT/"README.md").read_text();assert "[`v73/`](v73/)" in root
    publication=(ROOT/"PUBLICATION_INDEX.md").read_text();assert "V73_BICRITERIA_AVOIDANCE_THEOREM.tex" in publication
    workflow=(ROOT.parent.parent/".github"/"workflows"/"p-vs-np-verify.yml").read_text();assert "V73_BICRITERIA_AVOIDANCE_THEOREM.tex" in workflow
    ledger=json.loads((ROOT/"LEDGER.json").read_text());assert int(ledger["current_version"][1:])>=70
    assert ledger["program"]["p_vs_np_route_active"] is False and ledger["program"]["p_vs_np_resolved"] is False
    corpus="\n".join(path.read_text().lower() for path in HERE.iterdir() if path.suffix in {".md",".json",".tex"})
    for forbidden in ("p versus np is solved","we prove p != np","unrestricted nc0_3-avoid is solved",
      "peer reviewed theorem","novelty confirmed: true","all orders force superpolynomial"):assert forbidden not in corpus
    print("V73 primary verification passed: deterministic snapshot; 211 bicriteria budget checks; 808 branch nodes; six exact Pareto records; supplied-target barrier; binary-tree G*=m; repository and LaTeX gates; zero failures.")
if __name__=="__main__":main()
