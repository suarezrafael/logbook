#!/usr/bin/env bash
set -u -o pipefail

export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="quick"
FOCUSED_VERSIONS=(V53 V54 V55 V56 V57 V58 V59 V78 V79 V80 V81 V82 V83 V84 V85 V86 V87)

case "${1:-}" in
  "") ;;
  --compat) MODE="compat" ;;
  --full) MODE="full" ;;
  --list) MODE="list" ;;
  -h|--help)
    cat <<'HELP'
Usage: ./verify_all.sh [--compat|--full|--list]

  default   Run the focused regression gate for V53-V59 and V78-V87.
  --compat  Run every ordinary historical verifier, excluding exact replay tier.
  --full    Run the complete historical suite including exact replay tier.
  --list    Print every registered check without executing it.

The compatibility gate protects promotion against historical status and contract
regressions. Exact replays remain available for CI-sensitive changes, weekly
scheduled verification, and manual dispatch.
HELP
    exit 0
    ;;
  *) echo "Unknown option: $1" >&2; exit 2 ;;
esac

if command -v python3 >/dev/null 2>&1; then PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then PYTHON="$(command -v python)"
else echo "Python 3 is required." >&2; exit 2
fi

is_focused_version() {
  local candidate="$1"
  local version
  for version in "${FOCUSED_VERSIONS[@]}"; do
    [[ "$candidate" == "$version" ]] && return 0
  done
  return 1
}

"$PYTHON" "$ROOT/check_runner_coverage.py" || exit 1
"$PYTHON" "$ROOT/check_latex_manifest.py" || exit 1
"$PYTHON" "$ROOT/check_ci_contract.py" || exit 1

CHECKS=(
  "V20|historical|v20/verify.py|quick|"
  "V22|primary|v22/verify.py|skip|missing v22/full_certificate_cases.json; aggregate RESULTS.json cannot reconstruct the original 125 certificates"
  "V25|index|v25/verify_index.py|quick|"
  "V26|primary|v26/verify.py|quick|"
  "V27|index|v27/verify_index.py|quick|"
  "V53|primary|v53/verify.py|quick|"
  "V53|independent|v53/verify_independent.py|quick|"
  "V54|primary|v54/verify.py|quick|"
  "V54|independent|v54/verify_independent.py|quick|"
  "V55|primary|v55/verify.py|quick|"
  "V55|independent|v55/verify_independent.py|quick|"
  "V56|primary|v56/verify.py|quick|"
  "V56|independent|v56/verify_independent.py|quick|"
  "V56|index|v56/verify_index.py|full|"
  "V57|primary|v57/verify.py|quick|"
  "V57|independent|v57/verify_independent.py|quick|"
  "V58|primary|v58/verify.py|quick|"
  "V58|independent|v58/verify_independent.py|quick|"
  "V58|exact|v58/verify_exact.py|full|"
  "V59|primary|v59/verify.py|quick|"
  "V59|independent|v59/verify_independent.py|quick|"
  "V60|primary|v60/verify.py|quick|"
  "V60|independent|v60/verify_independent.py|quick|"
  "V61|primary|v61/verify.py|quick|"
  "V61|independent|v61/verify_independent.py|quick|"
  "V62|primary|v62/verify.py|quick|"
  "V62|independent|v62/verify_independent.py|quick|"
  "V63|primary|v63/verify.py|quick|"
  "V63|independent|v63/verify_independent.py|quick|"
  "V64|primary|v64/verify.py|quick|"
  "V64|independent|v64/verify_independent.py|quick|"
  "V65|primary|v65/verify.py|quick|"
  "V65|independent|v65/verify_independent.py|quick|"
  "V66|primary|v66/verify.py|quick|"
  "V66|independent|v66/verify_independent.py|quick|"
  "V67|primary|v67/verify.py|quick|"
  "V67|independent|v67/verify_independent.py|quick|"
  "V68|primary|v68/verify.py|quick|"
  "V68|independent|v68/verify_independent.py|quick|"
  "V69|primary|v69/verify.py|quick|"
  "V69|independent|v69/verify_independent.py|quick|"
  "V70|primary|v70/verify.py|quick|"
  "V70|independent|v70/verify_independent.py|quick|"
  "V70|search-replay|v70/verify_search_reproduction.py|full|"
  "V71|primary|v71/verify.py|quick|"
  "V71|independent|v71/verify_independent.py|quick|"
  "V72|primary|v72/verify.py|quick|"
  "V72|independent|v72/verify_independent.py|quick|"
  "V73|primary|v73/verify.py|quick|"
  "V73|independent|v73/verify_independent.py|quick|"
  "V74|primary|v74/verify.py|quick|"
  "V74|independent|v74/verify_independent.py|quick|"
  "V75|primary|v75/verify.py|quick|"
  "V75|independent|v75/verify_independent.py|quick|"
  "V76|primary|v76/verify.py|quick|"
  "V76|independent|v76/verify_independent.py|quick|"
  "V77|primary|v77/verify.py|quick|"
  "V77|independent|v77/verify_independent.py|quick|"
  "V77|composition|v77/verify_composition.py|quick|"
  "V77|composition-independent|v77/verify_composition_independent.py|quick|"
  "V78|primary|v78/verify.py|quick|"
  "V78|independent|v78/verify_independent.py|quick|"
  "V79|primary|v79/verify.py|quick|"
  "V79|independent|v79/verify_independent.py|quick|"
  "V80|primary|v80/verify.py|quick|"
  "V80|independent|v80/verify_independent.py|quick|"
  "V81|primary|v81/verify.py|quick|"
  "V81|independent|v81/verify_independent.py|quick|"
  "V82|primary|v82/verify.py|quick|"
  "V82|independent|v82/verify_independent.py|quick|"
  "V83|primary|v83/verify.py|quick|"
  "V83|independent|v83/verify_independent.py|quick|"
  "V84|primary|v84/verify.py|quick|"
  "V84|independent|v84/verify_independent.py|quick|"
  "V85|primary|v85/verify.py|quick|"
  "V85|independent|v85/verify_independent.py|quick|"
  "V86|primary|v86/verify.py|quick|"
  "V86|independent|v86/verify_independent.py|quick|"
  "V87|primary|v87/verify.py|quick|"
  "V87|independent|v87/verify_independent.py|quick|"
)

printf '%-6s | %-24s | %-6s | %s\n' "LAB" "CHECK" "STATUS" "DETAIL"
printf '%-6s-+-%-24s-+-%-6s-+-%s\n' "------" "------------------------" "------" "----------------------------------------"

failures=0
executed=0
skipped=0

for item in "${CHECKS[@]}"; do
  IFS='|' read -r version kind relative tier reason <<<"$item"
  path="$ROOT/$relative"

  if [[ "$tier" == "skip" ]]; then
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "SKIP" "$reason"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ "$MODE" == "list" ]]; then
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "PLAN" "$relative ($tier)"
    continue
  fi
  if [[ "$MODE" == "quick" ]] && ! is_focused_version "$version"; then
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "SKIP" "requires --compat or --full"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ "$tier" == "full" && "$MODE" != "full" ]]; then
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "SKIP" "exact replay requires --full"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ ! -f "$path" ]]; then
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "SKIP" "script not present"
    skipped=$((skipped + 1))
    continue
  fi

  log_file="$(mktemp)"
  if (cd "$(dirname "$path")" && "$PYTHON" "$(basename "$path")") >"$log_file" 2>&1; then
    detail="$(tail -n 1 "$log_file" | tr '\t' ' ' | cut -c1-120)"
    [[ -n "$detail" ]] || detail="completed"
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "PASS" "$detail"
  else
    detail="$(tail -n 1 "$log_file" | tr '\t' ' ' | cut -c1-120)"
    [[ -n "$detail" ]] || detail="verifier exited nonzero"
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "FAIL" "$detail"
    echo "---- $version $kind log ----" >&2
    cat "$log_file" >&2
    echo "----------------------------" >&2
    failures=$((failures + 1))
  fi
  rm -f "$log_file"
  executed=$((executed + 1))
done

if [[ "$MODE" == "list" ]]; then
  exit 0
fi

echo
printf 'Summary: mode=%s executed=%d skipped=%d failures=%d\n' \
  "$MODE" "$executed" "$skipped" "$failures"
if (( failures > 0 )); then
  exit 1
fi
