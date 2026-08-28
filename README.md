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
    <img src="branding/cta-fix.png" alt="Subscribe to DocMeThis Fix or test with 250 free credits">
  </a>
</p>

## Private By Architecture

DocMeThis does not perform inference and does not receive your source code,
prompts or provider credentials. Fix runs in your CI and sends them directly to
the inference endpoint you choose. With local or private inference, they remain
in your environment; with a hosted provider, that provider's data policy applies.

The DocMeThis Gateway only authorizes the account and validates or reserves
credit quotas. It receives no source or prompt. The Fix API key authenticates
that call. Approved OSS workflows may additionally present GitHub OIDC, only to
prove eligibility.

## Free For Eligible OSS

Eligible public open-source projects can use Fix at no charge after validation
and activation. The repository
must meet the OSS conditions, including public visibility, and every run remains
subject to the approved workflow and OSS credit quota. Private and commercial
repositories use the commercial entitlement and its quota rules.

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
    <img src="branding/cta-fix.png" alt="Subscribe to DocMeThis Fix or test with 250 free credits">
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
    <img src="branding/cta-fix.png" alt="Subscribe to DocMeThis Fix or test with 250 free credits">
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

## Built For Control

- The private Fix release pipeline blocks on Bandit and `pip-audit`.
- Actionlint validates workflow files; Dependabot keeps actions, dependencies
  and image pins current.
- Commercial deployment must pin a full runtime commit SHA and matching artifact
  SHA-256 digest, never a branch, mutable tag, `latest` or short SHA.
- Gateway authorization is signed and scoped to the account, request and quota.
- Idempotent credit reservations distinguish consume from release, including
  failed or uncertain runs.
- API keys and provider credentials stay in the appropriate secret store or
  configured endpoint; they are never committed here.

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-fix.png" alt="Subscribe to DocMeThis Fix or test with 250 free credits">
  </a>
</p>

## Commercial Onboarding

The public repository contains the integration contract and consumer template;
the private runtime is provisioned during commercial onboarding.

1. [Talk to DocMeThis](https://docmethis.com) about Fix access and supported targets.
2. Copy `templates/.github/workflows/docmethis-fix.yml` into the consumer repository.
3. Pin `DOCMETHIS_FIX_RUNTIME_SHA` and `DOCMETHIS_FIX_ARTIFACT_SHA256` to the
   supplied runtime commit and artifact digest.
4. Configure the distribution token, Fix API key and provider credentials in
   the consumer secret store or inference environment.
5. Run manually, inspect the patch and let normal CI decide whether to merge.

The public workflow is a safe skeleton until the private distribution channel
and commercial runtime contract are configured.

Operational guides:

- [Installation](docs/en/installation.md)
- [Configuration](docs/en/configuration.md)
- [Troubleshooting](docs/en/troubleshooting.md)

## Support

Use the [issue templates](.github/ISSUE_TEMPLATE/) for documentation,
configuration and facade questions. Never include secrets, prompts, customer
source code or unredacted Fix reports. Security issues belong in the private
process described by [SECURITY.md](SECURITY.md).

<p align="center">
  <a href="https://docmethis.com/fr/pricing/#ci-fix">
    <img src="branding/cta-fix.png" alt="Subscribe to DocMeThis Fix or test with 250 free credits">
  </a>
</p>

## Commercial Terms

DocMeThis Fix is proprietary commercial software and material. This repository
does not grant an open-source license. Access, use, copying, modification,
redistribution and production deployment require the applicable written
DocMeThis agreement.
