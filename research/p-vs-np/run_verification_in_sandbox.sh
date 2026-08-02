#!/usr/bin/env bash
set -euo pipefail

LAB_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$LAB_ROOT/../.." && pwd)"
TEMP_ROOT="${RUNNER_TEMP:-${TMPDIR:-/tmp}}"

if ! git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "A Git worktree is required to create the verification sandbox." >&2
  exit 2
fi

sandbox="$(mktemp -d "$TEMP_ROOT/p-vs-np-verification.XXXXXX")"
cleanup() {
  rm -rf "$sandbox"
}
trap cleanup EXIT

# Build the sandbox from the exact checked-out commit. The historical verifiers
# may regenerate snapshots inside this disposable tree, but they cannot mutate
# the source checkout guarded by assert_clean_tree.sh.
git -C "$REPO_ROOT" archive --format=tar HEAD | tar -xf - -C "$sandbox"
SANDBOX_LAB="$sandbox/research/p-vs-np"

printf 'Verification sandbox: commit %s\n' "$(git -C "$REPO_ROOT" rev-parse --short HEAD)"

set +e
(
  cd "$SANDBOX_LAB"
  export PYTHONDONTWRITEBYTECODE=1
  bash ./verify_all.sh "$@"
)
verification_status=$?
set -e

# Preserve the firewall's diagnostic value. Every mutation made by a legacy
# verifier is reported, even though it is confined to the disposable sandbox.
python3 - "$REPO_ROOT" "$sandbox" <<'PY'
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

source = Path(sys.argv[1]).resolve()
sandbox = Path(sys.argv[2]).resolve()


def inventory(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


before = inventory(source)
after = inventory(sandbox)
modified = sorted(path for path in before.keys() & after.keys() if before[path] != after[path])
created = sorted(after.keys() - before.keys())
deleted = sorted(before.keys() - after.keys())

print()
print("Sandbox mutation inventory:")
if not (modified or created or deleted):
    print("  clean: no verifier-generated mutations")
else:
    for label, paths in (("modified", modified), ("created", created), ("deleted", deleted)):
        if not paths:
            continue
        print(f"  {label}: {len(paths)}")
        for path in paths:
            print(f"    {path}")
PY

exit "$verification_status"
