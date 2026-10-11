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

### Updating the approved workflow SHA

DocMeThis approves each official workflow version by full SHA. When a new
version is announced, replace the SHA in the wrapper's `uses:` reference. During
the announced coexistence period, the previous version keeps working; after it
is removed from the approved list, new runs of that version are refused, while
installation tokens already issued simply expire. Never point the wrapper at a
branch or a tag.

## 2. Install the GitHub App

Install the DocMeThis Fix App from its stable link:

```text
https://github.com/apps/docmethis-fix/installations/new
```

- Grant access with **Only select repositories** and select just the
  repositories that will use Fix. Each installation token stays limited to the
  repository attested by the run, even when several repositories are selected.
- On an organization, a GitHub owner may need to approve the installation; Fix
  fails closed with the installation link until it is granted.
- A GitHub owner installs the App through the normal GitHub UI; no service
  account, webhook or user OAuth is required.
- The consumer repository never stores an App ID, an installation ID or a
  private key: the App private key stays inside the DocMeThis Gateway.

## 3. Configure the project

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

## 4. Select the package version

The private runtime is published as the `docmethis-fix` wheel on the PEP 503
index:

```text
https://pkg.docmethis.com
```

The official workflow pins the exact package version through
`DOCMETHIS_FIX_VERSION` in [`.github/workflows/fix.yml`](../../.github/workflows/fix.yml).
Use a published, approved workflow SHA; consumers do not need to maintain a
second runtime version pin or access the private source repository.

Reservations contain two fields (`requested_credits`, `request_fingerprint`).
Saga journals use v4 only, with no v2/v3 reader. When switching from an older
journal format:

1. Stop starting new Fix operations. Using the compatible runtime and Gateway,
   confirm each old operation's accounting state and finish every pending
   Git/push/PR publication. Reconcile uncertain operations first.
2. Archive **all v2/v3 UUID journal files, including terminal ones**, outside each
   active journal directory. Preserve their contents, filenames, batch manifests
   and accounting/publication evidence. Include per-target batch directories and
   any `DOCMETHIS_FIX_JOURNAL_DIR` override.
3. Keep those archives and start v4 with a clean active directory. For example,
   archive project `.docmethis` journals under the sibling
   `.docmethis-archives/pre-v4/`; do not erase `.docmethis` wholesale or edit old
   schema versions to make them appear compatible.

Completing an old operation alone is insufficient: the v4 reader rejects its
file before filtering terminal states. No conversion or backward-compatible
reader is provided. If there are no old journals, no archival step is needed.

## 5. Add GitHub values

For the supplied workflow, create the values at the **repository level**. In
the consumer repository, open:

```text
Settings -> Secrets and variables -> Actions
```

Use the **Secrets** tab and choose **New repository secret** for these values:

| Name | Value |
| --- | --- |
| `DOCMETHIS_FIX_API_KEY` | Fix API key for the DocMeThis Gateway. |
| `OPENCODE_API_KEY` in the supplied wrapper | Provider key forwarded as the official workflow's named `LLM_API_KEY` secret. |

The supplied wrapper maps `LLM_API_KEY: ${{ secrets.OPENCODE_API_KEY }}`. To use
another secret name, change only that named-secret mapping in the wrapper.
The official workflow injects the value as `DOCMETHIS_FIX_LLM_API_KEY`, regardless
of the selected profile's `api_key_env_var`. Do not add executable steps or
provider-specific `env` mappings to the wrapper. Local runs without the facade
use the environment variable named by their profile.

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

### Account prerequisites

The publication rights are validated at run time:

- the App broker always performs the server-side GitHub lookup for every type,
  even with an active capability or after a reservation replay. Reservations skip
  the lookup on exact replay or when the pre-read sees an active capability;
  no client account-type field or Actions variable is accepted as authority;
- `organization_workspace` is a capability: false/expired allows **User only**;
  active and non-expired allows **User or Organization**, not Organization only;
- OSS requires the exact **`subscription.cf_is_OSS`** checkbox, matching generic
  `cf_docmethis_github_owner_id` and `cf_docmethis_github_repository_id` bindings,
  public visibility. Subscription-scoped workflow policy is optional, including
  for OSS, and binding when configured. DocMeThis administrators manage
  these fields on the **subscription**, not the customer; a removed CF projects
  to `NULL`;
- the IDs are optional outside OSS and do not restrict other subscriptions even
  when populated. Neither plan names nor coupons authorize a run;
- an OSS grant may cover a public personal or organization repository according
  to the capability. OSS alone does not require an Organization. The technical
  wire/JWS mode `paid` means non-OSS and can include free access;
- App publication always requires approved official OIDC, the reservation's
  subscription scope and matching repository/SHA, an active installation and a
  token scoped to one repository with `contents: write`.

If the capability expires or is revoked between the reserve pre-read and final
admission, GitHub facts are missing and OIDC is present, the API returns retryable
`503 UPSTREAM_UNAVAILABLE`, not a fatal User denial. The broker's global approved
official workflow guard is mandatory and separate from optional subscription policy.

## 6. Run Fix

1. Open a pull request from a branch of the same repository.
2. The workflow runs Check first; Fix then corrects the eligible findings and
   pushes the commit back to the source branch.
3. CI and Check run again on the new commit; Fix ignores its own bot account to
   avoid loops.
4. Inspect the review patch and the JSON result in the `docmethis-fix-results`
   artifact.

The official workflow `fix.yml`, called by the wrapper, installs the pinned
wheel and its dependencies with `pip` in a temporary virtual environment, then runs
`docmethis_check` and `docmethis_fix` under isolated Python (`-I`). It supplies no
`DOCMETHIS_FIX_ACCOUNT_TYPE`; Gateway applies the server-side GitHub admission
rules, and Fix obtains a short-lived GitHub App installation token from Gateway
for publication only.

Keep API keys and temporary key files out of Git. Do not run Fix with secrets on
untrusted fork code.

For local execution, see the [README](../../README.md#local-execution).
