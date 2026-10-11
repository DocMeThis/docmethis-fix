#!/usr/bin/env python3
"""Contrat des workflows F20, exécuté par la CI publique docmethis-fix.

Deux fichiers distincts :
- `.github/workflows/fix.yml` : workflow officiel réutilisable (toutes les
  étapes privilégiées) ;
- `templates/.github/workflows/docmethis-fix.yml` : wrapper à copier dans le
  dépôt consommateur, sans étape exécutable.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "fix.yml"
WRAPPER = ROOT / "templates" / ".github" / "workflows" / "docmethis-fix.yml"

# Un helper Python non isolé (sans `-I`) importerait depuis le checkout de la
# PR : chaque invocation doit commencer par -I, quelle que soit la suite
# (`-m`, `-c`, `-`, script).
_BARE_PYTHON = re.compile(r"(?m)^\s*python(3(\.\d+)?)?\s+(?!-I\b)")
_APPROVED_REF = re.compile(r"uses: DocMeThis/docmethis-fix/\.github/workflows/fix\.yml@([0-9a-f]{40})$", re.MULTILINE)


def main() -> int:
    text = WORKFLOW.read_text(encoding="utf-8")
    wrapper = WRAPPER.read_text(encoding="utf-8")
    checks = {
        "workflow_call": "workflow_call:" in text,
        "guard PR interne": "github.event.pull_request.head.repo.full_name == github.repository" in text,
        "guard anti-boucle": "github.actor != 'docmethis-fix[bot]'" in text and "dependabot[bot]" in text,
        "checkout lecture seule": "persist-credentials: false" in text,
        "head figé": "ref: ${{ github.event.pull_request.head.sha }}" in text,
        "base matérialisée": "git worktree add --detach" in text and "DOCMETHIS_FIX_BASE_ROOT=" in text,
        "venv isolé": "python -I -m venv" in text,
        "pip isolé": '"$venv/bin/python" -I -m pip install --upgrade pip' in text,
        "OIDC isolé": "python -I - <<'PY'" in text,
        "aucun helper python nu": _BARE_PYTHON.search(text) is None,
        "check isolé": '"$FIX_PYTHON" -I -m docmethis_check .' in text,
        "fix isolé": '"$FIX_PYTHON" -I -m docmethis_fix rapport.json' in text,
        "push demandé": "--push" in text,
        "façade LLM générique": "DOCMETHIS_FIX_LLM_API_KEY: ${{ secrets.LLM_API_KEY }}" in text,
        "identité App": 'git config user.name "docmethis-fix[bot]"' in text,
        "jetons par émission": "docmethis-fix-tokens" in text and 'for token_file in "$token_dir"/token-*' in text,
        "révocation bornée": "--max-time 15" in text,
        "révocation signalée": "could not be revoked" in text,
        "artefacts always": "if: always()" in text,
        "pas de secrets:inherit": "secrets: inherit" not in text,
        "pas d'écriture github.token": "contents: write" not in text,
        "wrapper pull_request": "pull_request:" in wrapper and "types: [opened, reopened, synchronize]" in wrapper,
        "wrapper sans étape exécutable": "runs-on:" not in wrapper and "steps:" not in wrapper and "run:" not in wrapper,
        "wrapper appelle fix.yml par SHA": _APPROVED_REF.search(wrapper) is not None,
        "wrapper permissions minimales": "contents: read" in wrapper
        and "id-token: write" in wrapper
        and "contents: write" not in wrapper,
        "wrapper secrets nommés": "DOCMETHIS_FIX_API_KEY: ${{ secrets.DOCMETHIS_FIX_API_KEY }}" in wrapper
        and "LLM_API_KEY: ${{ secrets.OPENCODE_API_KEY }}" in wrapper
        and "secrets: inherit" not in wrapper,
    }
    failures = [name for name, ok in checks.items() if not ok]
    for name in failures:
        print(f"FAIL: {name}", file=sys.stderr)
    if failures:
        return 1
    print(f"Contrat workflow officiel : {len(checks)} vérifications OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
