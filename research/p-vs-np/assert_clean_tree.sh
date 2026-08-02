#!/usr/bin/env bash
set -euo pipefail

LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$LAB_ROOT/../.." && pwd)"
cd "$REPO_ROOT"

status="$(git status --porcelain --untracked-files=all)"
if [[ -z "$status" ]]; then
  echo "Clean-tree assertion passed: verification left the checkout unchanged."
  exit 0
fi

echo "Verification modified the repository checkout:" >&2
printf '%s\n' "$status" >&2

echo >&2
echo "Tracked diff summary:" >&2
git diff --stat >&2 || true

echo >&2
echo "Tracked diff:" >&2
git diff --no-ext-diff --text >&2 || true

exit 1
