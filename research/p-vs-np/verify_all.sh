#!/usr/bin/env bash
set -u -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="quick"

case "${1:-}" in
  "") ;;
  --full) MODE="full" ;;
  --list) MODE="list" ;;
  -h|--help)
    cat <<'HELP'
Usage: ./verify_all.sh [--full|--list]

  default  Run curated primary and independent verifiers.
  --full   Also run exact/extended verifiers where available.
  --list   Print the planned checks without executing them.

A missing script or required historical artifact is reported as SKIP with a
reason. Any executed verifier failure makes the script exit nonzero.
HELP
    exit 0
    ;;
  *)
    echo "Unknown option: $1" >&2
    exit 2
    ;;
esac

if command -v python3 >/dev/null 2>&1; then
  PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON="$(command -v python)"
else
  echo "Python 3 is required." >&2
  exit 2
fi

CHECKS=(
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
)

printf '%-6s | %-12s | %-6s | %s\n' "LAB" "CHECK" "STATUS" "DETAIL"
printf '%-6s-+-%-12s-+-%-6s-+-%s\n' "------" "------------" "------" "----------------------------------------"

failures=0
executed=0
skipped=0

for item in "${CHECKS[@]}"; do
  IFS='|' read -r version kind relative tier reason <<<"$item"
  path="$ROOT/$relative"

  if [[ "$tier" == "skip" ]]; then
    printf '%-6s | %-12s | %-6s | %s\n' "$version" "$kind" "SKIP" "$reason"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ "$tier" == "full" && "$MODE" != "full" ]]; then
    printf '%-6s | %-12s | %-6s | %s\n' "$version" "$kind" "SKIP" "requires --full"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ ! -f "$path" ]]; then
    printf '%-6s | %-12s | %-6s | %s\n' "$version" "$kind" "SKIP" "script not present"
    skipped=$((skipped + 1))
    continue
  fi
  if [[ "$MODE" == "list" ]]; then
    printf '%-6s | %-12s | %-6s | %s\n' "$version" "$kind" "PLAN" "$relative"
    continue
  fi

  log_file="$(mktemp)"
  if (cd "$(dirname "$path")" && "$PYTHON" "$(basename "$path")") >"$log_file" 2>&1; then
    detail="$(tail -n 1 "$log_file" | tr '\t' ' ' | cut -c1-120)"
    [[ -n "$detail" ]] || detail="completed"
    printf '%-6s | %-12s | %-6s | %s\n' "$version" "$kind" "PASS" "$detail"
  else
    detail="$(tail -n 1 "$log_file" | tr '\t' ' ' | cut -c1-120)"
    [[ -n "$detail" ]] || detail="verifier exited nonzero"
    printf '%-6s | %-12s | %-6s | %s\n' "$version" "$kind" "FAIL" "$detail"
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
printf 'Summary: mode=%s executed=%d skipped=%d failures=%d\n' "$MODE" "$executed" "$skipped" "$failures"
if (( failures > 0 )); then
  exit 1
fi
