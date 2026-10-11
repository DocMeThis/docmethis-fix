"""F20 workflow contracts enforced by public docmethis-fix CI.

Two distinct files:
- `.github/workflows/fix.yml`: the official reusable workflow owning all
  privileged steps.
- `templates/.github/workflows/docmethis-fix.yml`: the wrapper copied into a
  consumer repository, with no executable steps.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "fix.yml"
WRAPPER = ROOT / "templates" / ".github" / "workflows" / "docmethis-fix.yml"

# Without isolation (-I), a Python helper could import from the PR checkout.
# Every invocation must start with -I, before any subsequent arguments
# (-m, -c, -, or a script).
_BARE_PYTHON = re.compile(r"(?m)^\s*python(3(\.\d+)?)?\s+(?!-I\b)")
_APPROVED_REF = re.compile(r"uses: DocMeThis/docmethis-fix/\.github/workflows/fix\.yml@([0-9a-f]{40})$", re.MULTILINE)


def main() -> int:
    """Check the official workflow and wrapper without executing their steps."""
    text = WORKFLOW.read_text(encoding="utf-8")
    wrapper = WRAPPER.read_text(encoding="utf-8")
    version_pin = re.search(r'(?m)^\s*DOCMETHIS_FIX_VERSION:\s*"[0-9]+\.[0-9]+\.[0-9]+"\s*$', text)
    checks = {
        "workflow_call": "workflow_call:" in text,
        "exact runtime version pin": version_pin is not None and '"docmethis-fix==${DOCMETHIS_FIX_VERSION}"' in text,
        "server-side GitHub admission": "DOCMETHIS_FIX_ACCOUNT_TYPE" not in text and "account_type" not in text,
        "same-repository PR guard": "github.event.pull_request.head.repo.full_name == github.repository" in text,
        "bot loop guard": "github.actor != 'docmethis-fix[bot]'" in text and "dependabot[bot]" in text,
        "read-only checkout": "persist-credentials: false" in text,
        "pinned PR head": "ref: ${{ github.event.pull_request.head.sha }}" in text,
        "trusted base worktree": "git worktree add --detach" in text and "DOCMETHIS_FIX_BASE_ROOT=" in text,
        "isolated venv": "python -I -m venv" in text,
        "isolated pip": '"$venv/bin/python" -I -m pip install --upgrade pip' in text,
        "isolated OIDC helper": "python -I - <<'PY'" in text,
        "no unisolated Python helpers": _BARE_PYTHON.search(text) is None,
        "isolated Check": '"$FIX_PYTHON" -I -m docmethis_check .' in text,
        "isolated Fix": '"$FIX_PYTHON" -I -m docmethis_fix rapport.json' in text,
        "push requested": "--push" in text,
        "generic LLM secret": "DOCMETHIS_FIX_LLM_API_KEY: ${{ secrets.LLM_API_KEY }}" in text,
        "App identity": 'git config user.name "docmethis-fix[bot]"' in text,
        "per-issuance token files": "docmethis-fix-tokens" in text and 'for token_file in "$token_dir"/token-*' in text,
        "bounded revocation": "--max-time 15" in text,
        "revocation warning": "could not be revoked" in text,
        "always-upload artifacts": "if: always()" in text,
        "no inherited secrets": "secrets: inherit" not in text,
        "read-only GITHUB_TOKEN": "contents: write" not in text,
        "wrapper pull_request": "pull_request:" in wrapper and "types: [opened, reopened, synchronize]" in wrapper,
        "wrapper has no executable steps": "runs-on:" not in wrapper and "steps:" not in wrapper and "run:" not in wrapper,
        "wrapper has no client account type": "DOCMETHIS_FIX_ACCOUNT_TYPE" not in wrapper and "account_type" not in wrapper,
        "wrapper calls fix.yml by SHA": _APPROVED_REF.search(wrapper) is not None,
        "minimal wrapper permissions": "contents: read" in wrapper
        and "id-token: write" in wrapper
        and "contents: write" not in wrapper,
        "named wrapper secrets": "DOCMETHIS_FIX_API_KEY: ${{ secrets.DOCMETHIS_FIX_API_KEY }}" in wrapper
        and "LLM_API_KEY: ${{ secrets.OPENCODE_API_KEY }}" in wrapper
        and "secrets: inherit" not in wrapper,
    }
    failures = [name for name, ok in checks.items() if not ok]
    for name in failures:
        print(f"FAIL: {name}", file=sys.stderr)
    if failures:
        return 1
    print(f"Official workflow contract: {len(checks)} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
