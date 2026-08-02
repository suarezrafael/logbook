#!/usr/bin/env bash
set -euo pipefail

LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$LAB_ROOT/../.." && pwd)"
TEMP_ROOT="${RUNNER_TEMP:-${TMPDIR:-/tmp}}"
BASELINE="$LAB_ROOT/v79/EXPECTED_MUTATIONS.tsv"
MODE="quick"
[[ "${1:-}" == "--full" ]] && MODE="full"

if ! git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "A Git worktree is required to create the verification sandbox." >&2
  exit 2
fi
if [[ ! -f "$BASELINE" ]]; then
  echo "Missing mutation baseline: $BASELINE" >&2
  exit 2
fi

sandbox="$(mktemp -d "$TEMP_ROOT/p-vs-np-verification.XXXXXX")"
cleanup() {
  rm -rf "$sandbox"
}
trap cleanup EXIT

git -C "$REPO_ROOT" archive --format=tar HEAD | tar -xf - -C "$sandbox"
SANDBOX_LAB="$sandbox/research/p-vs-np"

printf 'Verification sandbox: commit %s; mode=%s\n' \
  "$(git -C "$REPO_ROOT" rev-parse --short HEAD)" "$MODE"

set +e
(
  cd "$SANDBOX_LAB"
  export PYTHONDONTWRITEBYTECODE=1
  bash ./verify_all.sh "$@"
)
verification_status=$?
set -e

set +e
python3 - "$REPO_ROOT" "$sandbox" "$BASELINE" "$MODE" <<'PY'
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
sandbox = Path(sys.argv[2]).resolve()
baseline_path = Path(sys.argv[3]).resolve()
mode = sys.argv[4]


def inventory(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def load_full_baseline(path: Path) -> set[tuple[str, str]]:
    expected: set[tuple[str, str]] = set()
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 2 or fields[0] not in {"modified", "created", "deleted"}:
            raise SystemExit(f"invalid mutation baseline line {line_number}: {raw!r}")
        entry = (fields[0], fields[1])
        if entry in expected:
            raise SystemExit(f"duplicate mutation baseline entry: {entry}")
        expected.add(entry)
    return expected


before = inventory(source)
after = inventory(sandbox)
modified = sorted(path for path in before.keys() & after.keys() if before[path] != after[path])
created = sorted(after.keys() - before.keys())
deleted = sorted(before.keys() - after.keys())
actual = {
    *(("modified", path) for path in modified),
    *(("created", path) for path in created),
    *(("deleted", path) for path in deleted),
}
expected = load_full_baseline(baseline_path) if mode == "full" else set()

print()
print("Sandbox mutation inventory:")
if not actual:
    print("  clean: no verifier-generated mutations")
else:
    for label, paths in (("modified", modified), ("created", created), ("deleted", deleted)):
        if not paths:
            continue
        print(f"  {label}: {len(paths)}")
        for path in paths:
            print(f"    {path}")

unexpected = sorted(actual - expected)
missing = sorted(expected - actual)
if unexpected or missing:
    print()
    print(f"Mutation baseline mismatch in {mode} mode:", file=sys.stderr)
    if unexpected:
        print("  unexpected mutations:", file=sys.stderr)
        for kind, path in unexpected:
            print(f"    {kind}\t{path}", file=sys.stderr)
    if missing:
        print("  expected mutations not observed:", file=sys.stderr)
        for kind, path in missing:
            print(f"    {kind}\t{path}", file=sys.stderr)
    raise SystemExit(1)

print(f"Mutation baseline passed: mode={mode}; expected_paths={len(expected)}.")
PY
inventory_status=$?
set -e

if (( verification_status != 0 )); then
  exit "$verification_status"
fi
exit "$inventory_status"
