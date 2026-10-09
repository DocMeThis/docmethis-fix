# Installation

This guide adds DocMeThis Fix to a consumer repository through GitHub Actions.

You need an activated [DocMeThis CI Fix](https://docmethis.fr/en/ci-fix/start)
subscription and the private runtime package version supplied during onboarding.
The public repository contains the workflow and configuration templates, not the
executable runtime itself.

## 1. Copy the files

In the consumer repository, copy the workflow:

```text
templates/.github/workflows/docmethis-fix.yml
  -> .github/workflows/docmethis-fix.yml
```

The copied file keeps the name `docmethis-fix.yml`: it is the consumer wrapper.
It calls the official reusable workflow
`DocMeThis/docmethis-fix/.github/workflows/fix.yml`, pinned by full SHA, which
contains every privileged step.

The TOML files are optional. Copy them when you need an explicit provider or
policy profile:

```text
templates/config/llm_api.toml.example
  -> .github/docmethis-fix/llm_api.toml

templates/config/llm_policies.toml.example
  -> .github/docmethis-fix/llm_policies.toml
```

The template runs on internal pull requests (`opened`, `reopened`,
`synchronize`) and only calls the official reusable workflow pinned by full SHA.
That workflow checks out the source branch, runs Check, invokes Fix and pushes
the validated correction back to that branch, where CI and Check run again.
Pull requests from forks are excluded.

## 2. Configure the project

Add the Fix settings to the consumer repository's `pyproject.toml`:

```toml
[tool.docmethis.fix]
api-profile = "example"
policy-profile = "example"
api-config-file = ".github/docmethis-fix/llm_api.toml"
policy-config-file = ".github/docmethis-fix/llm_policies.toml"
docstring-language = "en"
max-concurrency = 2
include-existing-docstrings = true
scope = "impacted"
```

In the copied files:

- replace the example provider endpoint in `llm_api.toml`;
- replace `provider/model` in `llm_policies.toml` with a supported model;
- keep `api-profile` and `policy-profile` synchronized with the table names.

In the official workflow, the API profile, the API config file and its
overrides — which carry the endpoint and the credential selection — are read
from the **approved base commit** of the pull request, never from the PR
checkout. Merge the Fix configuration into the base branch before enabling the
workflow, including for the first installation.

See [Configuration](configuration.md) for the available settings and provider
profile format.

## 3. Select the package version

The private runtime is published as the `docmethis-fix` wheel on the PEP 503
index:

```text
https://pkg.docmethis.com
```

The current package version is `0.1.0`. Use the exact version supplied by
DocMeThis. The consumer does not access the private source repository or a
GitHub Release to install the wheel.

## 4. Add GitHub values

For the supplied workflow, create the values at the **repository level**. In
the consumer repository, open:

```text
Settings -> Secrets and variables -> Actions
```

Use the **Secrets** tab and choose **New repository secret** for these values:

| Name | Value |
| --- | --- |
| `DOCMETHIS_FIX_API_KEY` | Fix API key for the DocMeThis Gateway. |
| Name from `api_key_env_var` | The provider API key, stored as an Actions secret under that exact name. |

For the example API profile, `api_key_env_var` is set to
`DOCMETHIS_PROVIDER_API_KEY`. Create an Actions secret with that name and put
the actual provider API key in its value. A different profile may require a
name such as `ANTHROPIC_API_KEY`. The name is configuration; only the value is
secret. The supplied workflow exposes `OPENROUTER_API_KEY` and
`OPENCODE_API_KEY`; add a corresponding `env` mapping when the selected profile
uses another name.

Package installation from `pkg.docmethis.com` does not use a GitHub token or a
client-side artifact digest.

### Which GitHub scope should you use?

- **Repository**: use this for the installation described here. The values are
  available to this repository's workflows and require no extra workflow
  change.
- **Organization**: use this only when the same values must be shared by
  several repositories. Create them under the organization's **Settings ->
  Secrets and variables -> Actions**, then grant access to this repository.
- **Environment**: use this only when the job declares the matching
  `environment:`. The supplied workflow does not declare an environment, so
  environment-level values are not available to it by default.

Do not create these secrets as environment variables on the runner. The workflow
reads them through the GitHub `secrets` context.

## 5. Run Fix

1. Open a pull request from a branch of the same repository.
2. The workflow runs Check first; Fix then corrects the eligible findings and
   pushes the commit back to the source branch.
3. CI and Check run again on the new commit; Fix ignores its own bot account to
   avoid loops.
4. Inspect the review patch and the JSON result in the `docmethis-fix-results`
   artifact.

The official workflow `fix.yml`, called by the wrapper, installs the pinned
wheel and its dependencies with `pip` in a temporary virtual environment, then runs
`docmethis_check` and `docmethis_fix`. It forwards
`github.event.pull_request.base.repo.owner.type` so Gateway can apply the
Organization workspace rule to the owning account, and Fix obtains a short-lived
GitHub App installation token from Gateway for the push only.

Keep API keys and temporary key files out of Git. Do not run Fix with secrets on
untrusted fork code.

For local execution, see the [README](../../README.md#local-execution).
