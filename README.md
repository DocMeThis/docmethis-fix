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

This is not your regular chatbot bolted onto your repository: through AST context,
Fix understands the symbol affected by the change, the contract that became stale
and the smallest useful correction. It prepares the patch, validates it before
delivery and leaves your team with something they can review like any other code
change.

> **Check tells you where documentation is stale. Fix gets you to review-ready.**

Or if you wish, Fix can also be configured to commit straight.

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-fix.png" alt="View team plans or subscribe to the free Solo plan">
  </a>
</p>

## Private By Architecture

DocMeThis does not perform inference and does not receive your source code,
prompts or provider credentials. Fix runs in your CI and sends them directly to
the inference endpoint you choose. With local or private inference, they remain
in your environment; with a hosted provider, that provider's data policy applies.

The DocMeThis Gateway only authorizes the account and validates or reserves
credit quotas. It receives no source or prompt. The Fix API key authenticates
that call. OSS eligibility requires GitHub OIDC; publication through the GitHub
App requires fresh OIDC from an approved official workflow for every account.

## Free For Individual Users

Individual users can use DocMeThis Fix at no charge on their personal GitHub
workspace after free registration, within the monthly credit quota.

## Free For Eligible OSS

Eligible public open-source projects can use DocMeThis Fix at no charge after validation
and activation. The repository
must meet the OSS conditions, including public visibility, and every run remains
subject to the OSS credit quota and any configured subscription-scoped workflow
policy. App publication always requires the globally approved official workflow.
Private and commercial repositories use the commercial entitlement and its quota rules.

OSS grants may cover a public personal repository or a public organization
repository. The subscription's `organization_workspace` capability allows a
User only when false or expired, and either User or Organization when active.
OSS alone never requires an Organization. The client supplies no account type.
Reservations skip the GitHub lookup on exact replay or when the pre-read sees an
active capability, since both owner types are accepted. The App broker always
performs the server-side lookup for every type. If the capability expires or is
revoked before final reserve admission, GitHub facts are missing and OIDC is
present, the API returns retryable `503 UPSTREAM_UNAVAILABLE`, not a fatal User denial.

DocMeThis administrators manage the exact `cf_is_OSS` checkbox and generic
`cf_docmethis_github_owner_id` / `cf_docmethis_github_repository_id` bindings on
the Chargebee **subscription**. The checkbox alone selects OSS, independently of
plan names, coupons or price. Both IDs are required and must match the attested
public repository for OSS; they are optional and do not restrict other
subscriptions even when populated. A removed field is projected as `NULL`.
The signed technical mode remains `paid`/`oss_free`; `paid` can include free access.

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-oss.png" alt="Get free OSS Fix access, subject to eligibility and quota">
  </a>
</p>

## Why Fix

- **Surgical:** correct only changed or affected symbols, not the whole repository.
- **Context-preserving:** keep unrelated prose, sections and source behavior intact.
- **Governed:** apply policy, authorization and credit controls before generation.
- **Reviewable:** deliver a patch or dedicated branch, never an unexplained rewrite.
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
            -> your inference endpoint generates the candidate
                -> Fix validates the result
                    -> patch or dedicated branch for review
```

1. Check emits a structured finding with the affected symbol, contract, evidence,
   diagnostic code and, when available, DIA impact evidence.
2. Fix validates the report and applies the configured scope and policy.
3. Gateway authorizes the run and validates the available credit quota.
4. Your configured inference endpoint generates the documentation candidate.
5. Fix runs candidate, AST, patch and documentation validation gates.
6. The workflow publishes a patch or dedicated branch with structured JSON.

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

- missing function, method or class documentation;
- missing, extra or incorrectly ordered parameters;
- missing parameter or return types;
- missing or stale `Raises` entries;
- selected exception, I/O, observable-property, override and inheritance changes.

When Check supplies confirmed DIA evidence, Fix can target a propagated contract
change even when the affected public symbol itself was not edited.

Existing documentation is edited at the smallest useful granularity. A full
docstring rewrite is not the default.

## Local Execution

Install the exact `docmethis-fix` package version supplied during onboarding in a
Python 3.12+ virtual environment. Configure the target project using the
[configuration guide](docs/en/configuration.md), including its provider endpoint,
model and profiles.

Local execution requires an activated subscription that permits API-key-only
requests to Gateway for authorization and credit quotas.

The example uses `DOCMETHIS_PROVIDER_API_KEY`, as declared by the `example` API
template. Set the environment variable named by your selected profile and keep
both API keys outside Git:

```bash
FIX_VERSION="<version supplied by DocMeThis>"
FIX_ENV="$HOME/.venvs/docmethis-fix"
python3.12 -m venv "$FIX_ENV"
FIX_PYTHON="$FIX_ENV/bin/python"

"$FIX_PYTHON" -I -m pip install \
  --index-url https://pkg.docmethis.com \
  --extra-index-url https://pypi.org/simple \
  --only-binary=:all: \
  "docmethis-fix==$FIX_VERSION"

TARGET_ROOT=/path/to/project
REPORT="$TARGET_ROOT/check.json"

export DOCMETHIS_FIX_API_KEY_FILE="$HOME/.config/docmethis/fix-api-key"
export DOCMETHIS_PROVIDER_API_KEY="..."
test -s "$DOCMETHIS_FIX_API_KEY_FILE"

"$FIX_PYTHON" -I -m docmethis_check "$TARGET_ROOT" \
  --base-ref main \
  --json-output-file "$REPORT"

"$FIX_PYTHON" -I -m docmethis_fix "$REPORT" \
  --project-root "$TARGET_ROOT" \
  --preview
```

`DOCMETHIS_FIX_API_KEY_FILE` contains the Gateway key; `DOCMETHIS_PROVIDER_API_KEY`
authenticates the inference service in this example. `--preview` generates the
first eligible patch without writing files or committing, but it still contacts
Gateway and the LLM.
Omit `--preview` to apply corrections; add `--no-commit` to leave them
uncommitted.

See the [Fix preview scenario](https://github.com/DocMeThis/docmethis-playground/blob/main/docs/scenarios/fix-preview.md)
and [provider configuration scenario](https://github.com/DocMeThis/docmethis-playground/blob/main/docs/scenarios/fix-provider-config.md).

## Built For Control

- The private Fix release pipeline blocks on Bandit and `pip-audit`.
- Actionlint validates workflow files; Dependabot keeps actions, dependencies
  and image pins current.
- Commercial deployment installs an exact `docmethis-fix` version from
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

## Commercial Onboarding

The public repository contains the integration contract and consumer template;
the private runtime is provisioned during commercial onboarding.

1. [Talk to DocMeThis](https://docmethis.com) about Fix access and supported targets.
2. Install the App from
   `https://github.com/apps/docmethis-fix/installations/new`, with **Only select
   repositories**. The consumer repository stores no App identifier or private
   key.
3. Copy `templates/.github/workflows/docmethis-fix.yml` into the consumer repository.
4. Keep the copied wrapper pinned to the DocMeThis-approved workflow SHA; the
   private runtime version is controlled by that official workflow.
5. Configure the Fix API key and provider credentials in the consumer secret
   store or inference environment.
6. Open a pull request from the same repository: Check runs first and Fix pushes
   the validated correction back to the source branch, where CI and Check run
   again on the new commit.

The template is a thin wrapper: every privileged step lives in the official
reusable workflow
[`.github/workflows/fix.yml`](.github/workflows/fix.yml), pinned by full SHA. The
consumer file keeps its own name, `.github/workflows/docmethis-fix.yml`, and
only declares the call, the permissions and the named secrets. The official
workflow installs the pinned private runtime, runs Check, invokes Fix, and
publishes the report and review patch as artifacts.

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
