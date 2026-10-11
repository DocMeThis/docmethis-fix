# Configuration

Fix configuration is owned by the consumer repository. It has three parts:

1. `pyproject.toml` selects the profiles and controls how Fix chooses and
   writes corrections.
2. `.github/docmethis-fix/llm_api.toml` describes how to reach the selected
   inference provider.
3. `.github/docmethis-fix/llm_policies.toml` selects the model and generation
   limits for the selected policy profile.

The public repository provides examples in `templates/config/`. Copy them into
the consumer repository and adapt them to the provider you use. The profile
names are local table names chosen in these files; the private runtime release
determines which provider protocols, configuration fields, policy values and
models are accepted. Keep all three files aligned with the same release and
runtime SHA.

Authorization is not a project setting. DocMeThis administrators manage the exact
`cf_is_OSS` checkbox and generic owner/repository IDs on the Chargebee subscription.
The checkbox alone selects OSS; IDs are optional outside OSS and constrain only
OSS public access, even if populated on other subscriptions. Removed CF values
project to `NULL`. `organization_workspace` is a capability with expiry: false
allows User only, true and unexpired allows User or Organization. Reservations
skip the GitHub lookup on exact replay or when the pre-read sees an active
capability; the App broker always performs it for every type. If the capability
expires or is revoked before final reserve admission, GitHub facts are missing
and OIDC is present, the API returns retryable `503 UPSTREAM_UNAVAILABLE`, not a
fatal User denial. OSS grants can cover either public
personal or organization projects according to that capability; no plan/coupon,
client `account_type` or `DOCMETHIS_FIX_ACCOUNT_TYPE` controls authorization.
The signed mode remains `paid`/`oss_free`; `paid` does not imply a paid price.
Subscription-scoped workflow policy is optional, including for OSS, and binding
when configured. It is distinct from the globally approved official workflow,
which the App broker always requires.

## Recommended Layout

From the root of the **consumer repository**:

```text
.
├── pyproject.toml
└── .github/
    ├── docmethis-fix/
    │   ├── llm_api.toml
    │   └── llm_policies.toml
    └── workflows/
        └── docmethis-fix.yml
```

The consumer file is a wrapper: it calls the official reusable workflow
`DocMeThis/docmethis-fix/.github/workflows/fix.yml` pinned by full SHA and
contains no executable step.

The paths in `pyproject.toml` are relative to the project root. The configuration
files contain no credentials. Provider and Gateway keys are supplied by the
workflow environment as described in the [installation guide](installation.md).

## Project Settings

Put the shared Fix settings in `[tool.docmethis.fix]`:

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

### `api-profile`

Name of the local table to load from `llm_api.toml`. With the example file,
`api-profile = "example"` selects `[example]`. `example` is not a profile
identifier supplied by the runtime; it is simply the table name used by this
example.

Use a meaningful profile name when a repository has more than one provider or
endpoint. The name must match a table in the file exactly.

### `policy-profile`

Name of the local policy table to load from `llm_policies.toml`. With the
example file, `policy-profile = "example"` selects `[fix.example]`.
`example` is a local name and can be replaced, as long as the setting and table
continue to match.

The API profile and policy profile are independent: one selects the connection
and credentials, while the other selects the model and generation policy.

### `api-config-file`

Path to the API profile file, relative to the project root. The file should
contain endpoints, provider settings and environment-variable names, never
secret values.

Use this setting when the repository keeps configuration outside the default
`.github/docmethis-fix/llm_api.toml` location or when several workflows use
different files.

### `policy-config-file`

Path to the policy profile file, relative to the project root. The file contains
model selection and generation limits, not provider credentials.

### `docstring-language`

Language of generated documentation. Use the language tag supported by the
private runtime, such as `en` for English. This controls the language of the
generated prose; it does not translate existing documentation automatically.

Keep the value consistent with the language and style expected by the project.
If a runtime release supports additional BCP 47 language tags, use the exact
tag documented by that release.

### `max-concurrency`

Maximum number of Fix generations that may be in flight at the same time.

Higher concurrency can reduce runtime for a report with many eligible targets,
but it can also hit provider rate limits faster and consume Gateway quota in a
shorter period. Start with the value supplied by the release documentation and
increase it only when the provider and account quotas allow it.

### `include-existing-docstrings`

Controls whether Fix may target corrections that require replacing an existing
docstring. With the setting disabled, Fix stays limited to the safer set of
eligible corrections that do not require a full existing-docstring replacement.

Enable it only when the repository accepts targeted rewrites of existing
documentation and the generated patch will be reviewed. It does not mean that
Fix rewrites every docstring: the normal behavior remains the smallest useful
correction.

### `scope`

Controls which Check findings Fix may consider:

- `diff`: findings attached to symbols directly selected by the Git diff.
- `impacted`: also consider eligible affected public contracts identified by
  Documentation Impact Analysis (DIA).

Use `diff` for the narrowest and most predictable patch. Use `impacted` when a
private helper change can make an unchanged public API stale and Check provides
the required impact evidence.

## API Profiles

Copy `templates/config/llm_api.toml.example` to
`.github/docmethis-fix/llm_api.toml`. Replace the placeholder endpoint and
profile values with settings supported by the selected private runtime:

```toml
[example]
provider = "openai_compatible"
base_url = "https://api.example.invalid/v1"
api_key_env_var = "DOCMETHIS_PROVIDER_API_KEY"
request_timeout_cap_seconds = 30.0
connect_timeout_seconds = 10.0
read_timeout_seconds = 30.0
pool_timeout_seconds = 10.0
```

### `provider`

Select the provider protocol understood by the runtime. The accepted values
are release-specific. `openai_compatible` in the example means that the
endpoint follows the OpenAI-compatible request protocol; it does not select a
provider account by itself.

### `base_url`

URL of the inference endpoint. `https://api.example.invalid/v1` is only a
placeholder and must be replaced.

Use the endpoint supplied by the provider or organization. Do not put a token,
query-string credential or signed URL in this value.

### `api_key_env_var`

Name of the environment variable from which the runtime reads the provider
key. It is a name, not the key value itself.

For local runs without the facade, set the variable named by the profile.
In the official workflow, the wrapper passes a named `LLM_API_KEY` secret:

```yaml
secrets:
  DOCMETHIS_FIX_API_KEY: ${{ secrets.DOCMETHIS_FIX_API_KEY }}
  LLM_API_KEY: ${{ secrets.DOCMETHIS_PROVIDER_API_KEY }}
```

The supplied wrapper uses `OPENCODE_API_KEY` as its source secret name. Change
that mapping if needed; the official workflow exposes its value only as
`DOCMETHIS_FIX_LLM_API_KEY`, overriding the profile's credential lookup without
changing the provider endpoint or protocol. No executable step or provider `env`
mapping belongs in the consumer wrapper. Endpoint and credential selection are
read from the approved base commit, never from the pull request checkout.

### Timeout settings

The timeout fields bound network operations:

- `request_timeout_cap_seconds`: upper limit for a complete provider request;
- `connect_timeout_seconds`: time allowed to establish the connection;
- `read_timeout_seconds`: time allowed while reading the provider response;
- `pool_timeout_seconds`: time allowed to obtain a client connection.

These values protect a CI job from waiting indefinitely. Keep the release or
provider recommendations unless there is a measured reason to change them.
Timeouts do not increase the provider's model token budget; that belongs in the
policy profile.

The private runtime may support additional connection fields such as pool sizes
or a provider-specific engine. Only use fields documented by the matching
release.

## Policy Profiles

Copy `templates/config/llm_policies.toml.example` to
`.github/docmethis-fix/llm_policies.toml`. A policy profile is a `[fix.<name>]`
table:

```toml
[fix.example]
model = "provider/model"
max_attempts = 3
timeout_seconds = 30.0
token_budget = 8000
prompt_variant = "compact"
structured_output_mode = "guided_json"

[fix.example.generation_options]
temperature = 0.0
max_tokens = 8000
```

### `model`

Model identifier understood by the selected provider and private runtime. The
placeholder `provider/model` is not a usable model. Replace it with a model
approved for the endpoint and release.

The model name does not provide credentials or select the endpoint; those come
from the API profile.

### `max_attempts`

Maximum number of generation attempts for one correction target. More attempts
may recover from a rejected candidate, but they increase latency and provider
usage. Keep this bounded in CI.

### `timeout_seconds`

Policy-level time limit for a generation attempt or policy operation, as defined
by the private runtime release. It is distinct from the API connection timeouts
in `llm_api.toml`.

### `token_budget`

Maximum generation budget allocated to a correction. A larger budget can help
with a complex contract, but costs more and does not guarantee a better patch.
Use the value supported by the selected model and account quota.

### `prompt_variant`

Select the prompt policy used by the runtime. Prompt variants are release
specific; use only names supplied by the matching policy documentation.

### `structured_output_mode`

Select how the model response is constrained before Fix validates it. Keep the
release-provided value unless the runtime documentation says that another mode
is supported.

### `generation_options`

Provider or model-specific generation parameters belong under this nested table.
For example, `temperature` controls sampling and `max_tokens` bounds the
generated response. These settings are not portable across providers; change
them only with the selected model's documentation.

## Secrets And Configuration

Configuration files are committed project policy. Credentials are runtime
inputs and must stay outside Git:

- `DOCMETHIS_FIX_API_KEY_FILE` points to the temporary file containing the
  Gateway key;
- the provider key is provided by the workflow as `DOCMETHIS_FIX_LLM_API_KEY`;
- the private runtime is resolved as a pinned package version from
  `https://pkg.docmethis.com`;
- the publication token is a short-lived GitHub App installation token,
  brokered by Gateway: the App is installed once, and no App credential is
  stored in the consumer repository.

Do not put any of these values in `pyproject.toml`, `llm_api.toml`,
`llm_policies.toml`, workflow YAML or a support request. See the
[installation guide](installation.md) for the GitHub secret setup.

## Safe Starting Point

Before enabling automatic Fix runs, check the following:

1. `api-profile` names a table that exists in `llm_api.toml`.
2. `policy-profile` names a `[fix.<name>]` table that exists in
   `llm_policies.toml`.
3. `base_url` is a real endpoint, not the example placeholder.
4. The wrapper's `LLM_API_KEY` mapping selects the intended provider secret;
   local runs use the profile's `api_key_env_var`.
5. `model` is supported by both the endpoint and the pinned private runtime.
6. The selected `scope` and `include-existing-docstrings` values match the
   level of patch autonomy the repository accepts.
7. No credential appears in the repository or generated logs.

Open a first internal pull request, inspect the generated report and review
patch, and only then rely on the automatic Fix commit for routine changes.
