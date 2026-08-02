#!/usr/bin/env bash
set -u -o pipefail

export PYTHONDONTWRITEBYTECODE=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="quick"

case "${1:-}" in
  "") ;;
  --full) MODE="full" ;;
  --list) MODE="list" ;;
  -h|--help)
    cat <<'HELP'
Usage: ./verify_all.sh [--full|--list]

  default  Run the focused regression gate for the active infrastructure boundary.
  --full   Run the complete historical and exact verification suite.
  --list   Print the planned checks without executing them.

Draft pull requests use the focused gate. Full verification is reserved for a
ready pull request, main, or manual dispatch. Any executed failure exits nonzero.
HELP
    exit 0
    ;;
  *) echo "Unknown option: $1" >&2; exit 2 ;;
esac

if command -v python3 >/dev/null 2>&1; then PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then PYTHON="$(command -v python)"
else echo "Python 3 is required." >&2; exit 2
fi

"$PYTHON" "$ROOT/check_runner_coverage.py"
"$PYTHON" "$ROOT/check_latex_manifest.py"

CHECKS=(
  "V20|historical|v20/verify.py|full|"
  "V22|primary|v22/verify.py|skip|missing v22/full_certificate_cases.json; aggregate RESULTS.json cannot reconstruct the original 125 certificates"
  "V25|index|v25/verify_index.py|full|"
  "V26|primary|v26/verify.py|full|"
  "V27|index|v27/verify_index.py|full|"
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
  "V60|primary|v60/verify.py|full|"
  "V60|independent|v60/verify_independent.py|full|"
  "V61|primary|v61/verify.py|full|"
  "V61|independent|v61/verify_independent.py|full|"
  "V62|primary|v62/verify.py|full|"
  "V62|independent|v62/verify_independent.py|full|"
  "V63|primary|v63/verify.py|full|"
  "V63|independent|v63/verify_independent.py|full|"
  "V64|primary|v64/verify.py|full|"
  "V64|independent|v64/verify_independent.py|full|"
  "V65|primary|v65/verify.py|full|"
  "V65|independent|v65/verify_independent.py|full|"
  "V66|primary|v66/verify.py|full|"
  "V66|independent|v66/verify_independent.py|full|"
  "V67|primary|v67/verify.py|full|"
  "V67|independent|v67/verify_independent.py|full|"
  "V68|primary|v68/verify.py|full|"
  "V68|independent|v68/verify_independent.py|full|"
  "V69|primary|v69/verify.py|full|"
  "V69|independent|v69/verify_independent.py|full|"
  "V70|primary|v70/verify.py|full|"
  "V70|independent|v70/verify_independent.py|full|"
  "V70|search-replay|v70/verify_search_reproduction.py|full|"
  "V71|primary|v71/verify.py|full|"
  "V71|independent|v71/verify_independent.py|full|"
  "V72|primary|v72/verify.py|full|"
  "V72|independent|v72/verify_independent.py|full|"
  "V73|primary|v73/verify.py|full|"
  "V73|independent|v73/verify_independent.py|full|"
  "V74|primary|v74/verify.py|full|"
  "V74|independent|v74/verify_independent.py|full|"
  "V75|primary|v75/verify.py|full|"
  "V75|independent|v75/verify_independent.py|full|"
  "V76|primary|v76/verify.py|full|"
  "V76|independent|v76/verify_independent.py|full|"
  "V77|primary|v77/verify.py|full|"
  "V77|independent|v77/verify_independent.py|full|"
  "V77|composition|v77/verify_composition.py|full|"
  "V77|composition-independent|v77/verify_composition_independent.py|full|"
  "V78|primary|v78/verify.py|quick|"
  "V78|independent|v78/verify_independent.py|quick|"
  "V79|primary|v79/verify.py|quick|"
  "V79|independent|v79/verify_independent.py|quick|"
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
  if [[ "$tier" == "full" && "$MODE" != "full" ]]; then
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "SKIP" "requires --full"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ ! -f "$path" ]]; then
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "SKIP" "script not present"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ "$MODE" == "list" ]]; then
    printf '%-6s | %-24s | %-6s | %s\n' "$version" "$kind" "PLAN" "$relative"
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
