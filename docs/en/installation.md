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

The TOML files are optional. Copy them when you need an explicit provider or
policy profile:

```text
templates/config/llm_api.toml.example
  -> .github/docmethis-fix/llm_api.toml

templates/config/llm_policies.toml.example
  -> .github/docmethis-fix/llm_policies.toml
```

The public template is manual-only (`workflow_dispatch`) so it can be tested
safely.

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

1. Open **Actions**, select **DocMeThis Fix**, and choose `workflow_dispatch`.
2. Run it on a trusted branch.
3. Check that `docmethis-fix==0.1.0` installs from `pkg.docmethis.com`.
4. Connect the final `Run Check and private Fix` step to the private runtime
   contract before enabling execution.

The public template installs the pinned wheel and its dependencies with `pip` in
a temporary virtual environment. Its final execution step remains intentionally
reserved for the private runtime contract.

Keep API keys and temporary key files out of Git. Do not run Fix with secrets on
untrusted fork code.

For local execution, see the [README](../../README.md#local-execution).
