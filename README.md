<p align="center">
  <a href="https://docmethis.com">
    <picture>
      <img src="branding/logo_docmethis_fix.png" alt="DocMeThis Fix logo" width="600">
    </picture>
  </a>
</p>

<p align="center">
  <em>DocMeThis Fix is a <a href="https://docmethis.com">DocMeThis</a> project, part of the <a href="https://github.com/orgs/DocMeThis/repositories">DocMeThis suite</a>.</em>
</p>

# DocMeThis Fix

**Your code changed. Fix makes sure your documentation changes with it.**

DocMeThis Fix is the AI documentation engineer for teams that ship. It turns a
structured [DocMeThis Check](https://github.com/DocMeThis/docmethis-check) finding
into a focused, validated and reviewable documentation change.

Fix uses extracted signatures, types and behavior to target the affected symbol.
It preserves unrelated documentation and validates each correction before
applying it.

> **Check tells you where documentation is stale. Fix gets you to review-ready.**

Run Fix [locally](#local-execution) to preview or apply corrections, or use
[GitHub Actions](#github-actions-setup) to commit and push them to your PR branch.

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-fix.png" alt="View team plans or subscribe to the free Solo plan">
  </a>
</p>

## Private By Architecture

DocMeThis does not perform inference and does not receive your source code,
prompts or provider credentials. Fix runs locally or in your CI and sends
inference requests directly to the endpoint you choose. With a local or private
endpoint, your source and prompts stay in your environment; with a hosted
provider, that provider's data policy applies.

The DocMeThis Gateway authorizes the run and manages credit reservations. It
receives no source or prompt. Your Fix API key authenticates these calls; your
provider key authenticates inference requests. GitHub Actions also supplies OIDC
identity for OSS eligibility and publication through the GitHub App.

## Free For Individual Users

Individual users can use DocMeThis Fix at no charge on their personal GitHub
workspace after free registration, within the monthly credit quota.

## Free For Eligible OSS

Eligible public open-source projects can use DocMeThis Fix at no charge after
validation and activation, within the OSS credit quota. Both personal and
organization repositories can qualify, subject to the account's access rights.
OSS runs use GitHub Actions so Gateway can verify the repository's identity and
public visibility.

See [account prerequisites](docs/en/installation.md#account-prerequisites) for
eligibility and organization access. Other uses follow the activated plan's
access rights and quotas.

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-oss.png" alt="Get free OSS Fix access, subject to eligibility and quota">
  </a>
</p>

## Why Fix

- **Surgical:** correct only changed or affected symbols, not the whole repository.
- **Context-preserving:** keep unrelated prose, sections and source behavior intact.
- **Governed:** apply policy, authorization and credit controls before generation.
- **Reviewable:** inspect a preview, an uncommitted diff or the workflow's correction commit.
- **Provider-neutral:** use the inference endpoint and model policy that fit your organization.

## "Lol My Agent Already Does This"

A coding agent can edit a docstring. Fix makes that edit production-grade:

- **Evidence, not guesswork:** start from a Check finding and optional
  Documentation Impact Analysis (DIA), not a vague request or repository-wide scan.
- **AST context:** use signatures, source locations, exceptions, I/O, inheritance,
  call relationships and affected symbols as structured evidence.
- **Budgeted execution:** make `token_budget`, `max_attempts` and concurrency
  explicit, while Gateway quotas bound the paid run.
- **Controlled delivery:** validate the candidate and patch before producing a
  branch or commit, with refusal paths instead of silent edits.
- **Auditable output:** report targets, skipped findings, token usage, attempts,
  latency, modified files and Git outcome.

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-fix.png" alt="View team plans or subscribe to the free Solo plan">
  </a>
</p>

## The Fix Loop

```text
Code change
    -> Check finds the affected contract and DIA impacts
        -> Fix selects the smallest eligible correction
            -> deterministic correction or inference-generated prose
                -> Fix validates the result
                    -> local diff or correction commit on the PR branch
```

1. Check emits a structured finding with the affected symbol, contract, evidence,
   diagnostic code and, when available, DIA impact evidence.
2. Fix validates the report and applies the configured scope and policy.
3. Gateway authorizes the run and validates the available credit quota.
4. Fix applies deterministic corrections or asks your inference endpoint to
   generate the required prose.
5. Fix runs candidate, AST, patch and documentation validation gates.
6. Locally, Fix previews or applies the correction. In GitHub Actions, the supplied
   workflow commits and pushes it to the PR branch and uploads the result artifacts.

Unsupported input, incomplete impact evidence, invalid authorization or failed
validation is a controlled refusal, never a silent rewrite. A run can retain
`rapport.json`, `fix-result.json` and `fix.patch` for review and audit.

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-fix.png" alt="View team plans or subscribe to the free Solo plan">
  </a>
</p>

## What Fix Fixes Today

The MVP targets Python (`.py`, `.pyw`, `.pyi`) with NumPy-style docstrings and
structured Check output. It handles:

- missing function, method, class or module documentation;
- missing, extra or incorrectly ordered parameters;
- missing parameter or return types and applicable `Returns` sections;
- missing class attribute documentation;
- missing or stale `Raises` entries;
- selected exception, I/O, observable-property, override and inheritance changes.

When Check supplies confirmed DIA evidence, Fix can target a propagated contract
change even when the affected public symbol itself was not edited.

Existing documentation is edited at the smallest useful granularity. A full
docstring rewrite is not the default. Findings that require changing executable
code or signatures are reported for manual correction.

## Install The Local Runtime

This setup is for the local CLI. The [GitHub Actions workflow](#github-actions-setup)
installs its own runtime automatically.

### 1. Install once, or when upgrading

Use CPython 3.12+ and Git. Select the exact **published** runtime version supplied
with your access; available wheels are listed on the
[package index](https://pkg.docmethis.com/docmethis-fix/). Use the documentation
and templates for that same release. Replace the version placeholder before
running these Bash commands on Linux or macOS:

```bash
FIX_VERSION="<published version supplied by DocMeThis>"
FIX_ENV="$HOME/.venvs/docmethis-fix"
python3.12 -m venv "$FIX_ENV"

"$FIX_ENV/bin/python" -I -m pip install --upgrade \
  --index-url https://pkg.docmethis.com \
  --extra-index-url https://pypi.org/simple \
  --only-binary=:all: \
  "docmethis-fix==$FIX_VERSION"
```

Check, Extract and Verify are installed as dependencies. You do not need to clone
this repository or install those packages separately. Reuse this environment for
later runs; repeat the installation with a new exact version when upgrading.

### 2. Configure the target project

Copy the [API template](templates/config/llm_api.toml.example) to
`.github/docmethis-fix/llm_api.toml` in your project, and the
[policy template](templates/config/llm_policies.toml.example) to
`.github/docmethis-fix/llm_policies.toml`. Replace the example endpoint and model
with values supported by your provider.

Add these settings to the project's `pyproject.toml`:

```toml
[tool.docmethis.fix]
profile = "example"
policy-profile = "example"
api-config-file = ".github/docmethis-fix/llm_api.toml"
policy-config-file = ".github/docmethis-fix/llm_policies.toml"
docstring-quote-style = "double"
include-existing-docstrings = true
```

Keep the profile names aligned with the TOML tables and the quote style aligned
with your formatter. See the [configuration guide](docs/en/configuration.md) for
other providers, model options, language and concurrency settings.

Save your Gateway API key in a file outside the repository, for example
`$HOME/.config/docmethis/fix-api-key`. The file contains the key itself.

## Local Execution

Local runs require an activated account that permits API-key-only Gateway
authorization. OSS access requiring GitHub OIDC uses the
[GitHub Actions setup](#github-actions-setup).

### 1. Prepare the terminal

In each new terminal, select the installed Python, the target Git repository and
the credentials. No installation is performed by these commands:

```bash
FIX_PYTHON="$HOME/.venvs/docmethis-fix/bin/python"
TARGET_ROOT="/absolute/path/to/project"
REPORT="$TARGET_ROOT/rapport.json"

export DOCMETHIS_FIX_API_KEY_FILE="$HOME/.config/docmethis/fix-api-key"
export DOCMETHIS_PROVIDER_API_KEY="<your provider API key>"
```

The `example` profile uses `DOCMETHIS_PROVIDER_API_KEY`. If you selected another
profile, export the variable named by its `api_key_env_var` instead. The Gateway
key and the provider key are separate credentials.

### 2. Generate the Check report

```bash
"$FIX_PYTHON" -I -m docmethis_check "$TARGET_ROOT" \
  --git-diff "main...HEAD" \
  --json-output-file "$REPORT"
```

This compares committed changes on your branch with `main`; replace `main` with
your base branch. Omit `--git-diff` to check staged and unstaged tracked changes
since `HEAD` instead. Regenerate the report after changing the source.

Check can exit with status `1` when it reports findings and still produce the
JSON report Fix needs. Status `2` indicates an execution error to resolve first.

### 3. Preview a correction

```bash
"$FIX_PYTHON" -I -m docmethis_fix "$REPORT" \
  --project-root "$TARGET_ROOT" \
  --preview
```

The JSON output includes the proposed patch for the first eligible symbol.
Preview leaves source files unchanged and creates no commit, but it still
contacts Gateway and can use inference and quota.

### 4. Apply corrections and inspect the diff

```bash
"$FIX_PYTHON" -I -m docmethis_fix "$REPORT" \
  --project-root "$TARGET_ROOT" \
  --no-commit \
  > "$TARGET_ROOT/fix-result.json"

git -C "$TARGET_ROOT" diff
```

This processes all eligible targets in the report and leaves the corrections
uncommitted. An apply run may generate new candidates.
Inspect `fix-result.json` for applied, skipped or failed targets and token usage.

To have Fix create a local commit, omit `--no-commit`. Local execution does not
push by default. The supplied GitHub Actions workflow requests the push explicitly.

Provider-specific setup is described in the
[configuration guide](docs/en/configuration.md#api-profiles).

## Built For Control

- The private Fix release pipeline blocks on Bandit and `pip-audit`.
- Actionlint validates workflow files; Dependabot keeps actions, dependencies
  and image pins current.
- Deployment installs an exact `docmethis-fix` version from
  `https://pkg.docmethis.com`, not a source checkout or GitHub Release.
- Gateway authorization is signed and scoped to the account, request and quota.
- Idempotent credit reservations distinguish consume from release, including
  failed or uncertain runs.
- API keys and provider credentials stay in the appropriate secret store or
  configured endpoint; they are never committed here.

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-fix.png" alt="View team plans or subscribe to the free Solo plan">
  </a>
</p>

## GitHub Actions Setup

The public repository provides the workflow and configuration templates. Runtime
access is activated through DocMeThis for individual, team or eligible OSS use.

1. Activate your Fix access through [DocMeThis](https://docmethis.com) and obtain a
   Fix API key.
2. Install the App from
   `https://github.com/apps/docmethis-fix/installations/new`, with **Only select
   repositories**. The consumer repository stores no App identifier or private
   key.
3. Copy [`templates/.github/workflows/docmethis-fix.yml`](templates/.github/workflows/docmethis-fix.yml)
   into the consumer repository as `.github/workflows/docmethis-fix.yml`.
4. Keep the copied wrapper pinned to the DocMeThis-approved workflow SHA; the
   private runtime version is controlled by that official workflow.
5. Configure the project on the base branch using the
   [installation guide](docs/en/installation.md). Add the repository secrets
   `DOCMETHIS_FIX_API_KEY` and `OPENCODE_API_KEY`. The supplied wrapper maps
   `OPENCODE_API_KEY` to the workflow's `LLM_API_KEY`; change that mapping to use a
   different provider secret name.
6. Open a pull request from the same repository: Check runs first and Fix pushes
   the validated correction back to the source branch, where CI and Check run
   again on the new commit.

The template is a thin wrapper: every privileged step lives in the official
reusable workflow
[`.github/workflows/fix.yml`](.github/workflows/fix.yml), pinned by full SHA. The
consumer file keeps its own name, `.github/workflows/docmethis-fix.yml`, and
only declares the call, the permissions and the named secrets. The official
workflow installs the pinned private runtime, runs Check, invokes Fix, and
uploads `rapport.json`, `fix-result.json` and `fix.patch` in the
`docmethis-fix-results` artifact. The endpoint and credential selection come from
the approved base commit; merge that configuration before enabling the workflow.

The runtime version pin is defined by `DOCMETHIS_FIX_VERSION` in the official
workflow. Consumer wrappers reference a published, approved workflow SHA.

The inference contract selects Chat Completions (`openai_compatible`), Responses
(`openai_responses`), Anthropic Messages or Gemini generateContent by `provider`.
`generation_options` contains native API parameters, without automatic renaming
or omission. The configuration guide describes the fields owned by the runtime.

Operational guides:

- [Installation](docs/en/installation.md)
- [Configuration](docs/en/configuration.md)

## Support

Use the [issue templates](.github/ISSUE_TEMPLATE/) for documentation,
configuration and facade questions. Never include secrets, prompts, customer
source code or unredacted Fix reports. Security issues belong in the private
process described by [SECURITY.md](SECURITY.md).

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-fix.png" alt="View team plans or subscribe to the free Solo plan">
  </a>
</p>

## Licensing and Commercial Terms

Prose documentation in this repository is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Code examples and files under [`templates/`](templates/) are licensed under the
[MIT License](LICENSE-MIT). The complete scope is documented in
[`LICENSE`](LICENSE).

The DocMeThis Fix runtime and implementation are proprietary commercial
software. They are not licensed under CC BY 4.0 or the MIT License; access and
use require the applicable written DocMeThis agreement. The DocMeThis name,
logos, screenshots and other branding are proprietary material and are not
covered by those licenses.
