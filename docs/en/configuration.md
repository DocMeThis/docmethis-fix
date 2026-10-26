# Configuration

Fix configuration is owned by the consumer repository. It has three parts:

1. `pyproject.toml` selects the profiles and controls how Fix chooses and
   writes corrections.
2. `.github/docmethis-fix/llm_api.toml` describes how to reach the selected
   inference provider.
3. `.github/docmethis-fix/llm_policies.toml` selects the model and generation
   limits for the selected policy profile.

The public repository provides examples in `templates/config/`. Copy them into
the consumer repository and adapt them to the provider you use. Profile names are
local table names chosen in these files. Select the connection and generation
policy explicitly, using your service's API documentation for model IDs and
native request parameters.

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
fatal User denial. OSS grants can cover public personal or organization projects
according to that capability. Gateway evaluates eligibility from the subscription
and verified GitHub context.
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

## Ruff coherence: NumPy only

DocMeThis currently generates NumPy-style docstrings only. When Ruff selects
docstring rules (`D`, `ALL`, etc.), declare the same convention in the Ruff
configuration actually used by the project:

```toml
[tool.ruff.lint.pydocstyle]
convention = "numpy"
```

For standalone `ruff.toml` or `.ruff.toml`, use `[lint.pydocstyle]` instead.
Apply the setting to the existing project configuration and preserve the
project's other selections and ignores.

Fix checks the project and target-directory configurations, their precedence
and explicit `extend` inheritance before LLM preflight, reservations or batch
workers. An incompatible convention, a missing convention with docstring rules
selected, an unreadable configuration or explicit rules conflicting with the
supported rendering causes an immediate configuration error. A private override
inside Fix cannot align a separate Ruff hook or CI job: persist the convention
in the project configuration.

The supplied settings keep only these explicit exclusions:

- `D401`: imperative-mood heuristics are not a reliable multilingual prose contract;
- `COM812`: trailing commas are owned by `ruff format`.

NumPy excludes D203/D213 and D417 by default, so no additional D203/D213 ignores
are needed. Explicit rule selections retain Ruff's precedence; explicitly
selecting D417 still enables its parameter
checks. The JSON document model and Verify checks remain independent of these
Ruff selections.

## Project Settings

### Exception analysis and documentation depths

These shared settings belong in `[tool.docmethis]`, independently of the Fix table:

```toml
[tool.docmethis]
exception_analysis_depth = 2
exception_documentation_depth = 1
```

Both values are strict non-negative integers, with documentation depth no greater
than analysis depth. Zero means local raises only; one also includes exceptions
raised directly by called functions. For A → B → C, documentation depth 1 includes
local raises from A and B, not C. Analysis 4/documentation 0 is supported.

AST facts retain their minimum propagation distance, conditions and provenance.
DIA uses the analysis depth. Documentary generation, Check, Verify, Audit and Fix
use the shared documentary scope for DMT-4001/DMT-4002. A known exception outside
that scope is a deterministic removal candidate; keeping the AST fact does not
authorize documenting it. Delegation to a direct helper remains documentable at
the default depth of 1.

Regenerate the Check report after changing these settings or after applying Fix.
Fix still rejects stale docstring hashes and newly introduced Verify errors.

Put the shared Fix settings in `[tool.docmethis.fix]`:

```toml
[tool.docmethis.fix]
profile = "example"
policy-profile = "example"
api-config-file = ".github/docmethis-fix/llm_api.toml"
policy-config-file = ".github/docmethis-fix/llm_policies.toml"
docstring-quote-style = "double"
docstring-language = "en"
max-concurrency = 2
include-existing-docstrings = true
scope = "impacted"
commit-per-file = false
```

### `profile`

Name of the local table to load from `llm_api.toml`. With the example file,
`profile = "example"` selects `[example]`. `example` is not a profile
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

### `docstring-quote-style`

Use `"double"` or `"single"` for the docstring delimiters. This setting takes
precedence over `[tool.ruff.format].quote-style`; Fix requires one of the two
settings to be declared. Keep the choice consistent with the project's formatter.

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

### `commit-per-file`

Defaults to `false`: a normal Fix invocation applies its patches as one atomic
multi-file session and creates one commit containing the corrected files.

Set `commit-per-file = true`, or pass `--commit-per-file`, to isolate patch
validation, application and commits by file. A local failure in one file preserves
the other validated files and allows later files to be processed and committed.
All supplied patches within a failed file remain unapplied. Snapshot drift in
one candidate excludes its entire file. Files staged outside Fix are not included.

CLI flags override the project setting. `--no-commit-per-file` explicitly selects
the grouped behavior. Explicit batch modes keep their own reservation and recovery
boundaries; grouping applies within each child invocation.

Partial results remain failures: Fix reports the affected paths and all successful
`commit_shas`, including successes after a local commit failure. A commit failure
returns exit code 2 and prevents push/PR publication. Created commits remain local;
recovery preserves their SHAs and commits only the remaining changes, without new
generation or a new reservation. Journal failures and inconsistent recovery hashes
remain global errors. Partial patch results follow the existing whole-reservation
release contract and return a nonzero result.

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
http_max_connections = 10
http_max_keepalive_connections = 5
http_keepalive_expiry_seconds = 30.0
```

### `provider`

Select the API protocol supported by your inference endpoint:

| Value | Generation endpoint relative to `base_url` |
|---|---|
| `openai_compatible` | `/chat/completions` |
| `openai_responses` | `/responses` |
| `anthropic` | `/messages` |
| `gemini` | `/models/{model}:generateContent` |

The protocol is selected explicitly by `provider`, separately from the URL and
model. Consult your service's documentation to choose the protocol and a model
available to your account.

The supplied `responses` API profile uses OpenCode Go at
`https://opencode.ai/inference/go/v1`; pair it with the `responses` policy and a
model documented for that endpoint. Go models served through Chat Completions
need a Chat profile instead. A project TOML file replaces the packaged file:
missing profiles do not fall back to packaged tables, and tables do not inherit
settings from each other.

Without project TOML files, select the packaged API and policy explicitly:

```toml
[tool.docmethis.fix]
profile = "opencode_responses"
policy-profile = "responses"
```

The packaged `[fix.responses]` policy uses the OpenCode Go model `gpt-6-luna`
and `max_output_tokens = 2000`. Confirm model
availability for your account or override `model`. API and policy profiles are
independent: selecting `opencode_responses` alone leaves the default policy
selected; it does not convert the default Qwen/Chat settings. If you supply a
policy TOML, define its `[fix.responses]` table or select another matching policy.

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

The pool fields are `http_max_connections`, `http_max_keepalive_connections` and
`http_keepalive_expiry_seconds`. Extra HTTP headers belong in a profile's
`extra_headers` table. `{session_id}` expands once per gateway instance; use it
for OpenCode Go's `x-opencode-session`. Authentication and transport headers are
reserved; DocMeThis supplies its own User-Agent.

### Inference-server diagnostics

The runtime records provider/server warnings and errors in
`.docmethis/inference-server-diags.jsonl`. Use `--diagnostics-file <path>` to
choose another destination.

The log is reset for each invocation and can be empty when server calls succeed.
Local precondition, Verify and Ruff-safe failures are reported in Fix's JSON
result instead. Only existing, non-empty logs are announced on stderr or listed
in the result's `diagnostics_file`/`diagnostics_files` fields; these fields are
`null` when no corresponding log contains events.

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
structured_output_mode = "json_prompted"

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

Budget checked against the input and output token counts returned by the service.
It is distinct from a provider's native output limit and is not translated into
one. Set that limit in `generation_options` using the API's exact field name.

### `prompt_variant`

Select the prompt policy used by the runtime. Prompt variants are release
specific; use only names supplied by the matching policy documentation.

### `structured_output_mode`

Fix defaults to `json_prompted`: the prompt requests JSON and Fix strictly
validates the response locally. No native structured-output schema is sent.

Opt in to `guided_json` when your endpoint/model combination reliably supports
native JSON Schema constraints. It constrains generation at the provider and
uses the same local validation afterwards. Enable it in your policy profile:

```toml
[fix.example]
# Keep the other required policy fields from the example above.
structured_output_mode = "guided_json"
```

Or override the selected policy from `pyproject.toml`:

```toml
[tool.docmethis.fix.policy]
structured-output-mode = "guided_json"
```

Existing explicit mode selections remain authoritative. If guided output is
explicitly unsupported, Fix can fall back to `json_prompted`; an invalid schema
or an opaque HTTP 400 does not authorize that fallback. Diagnostics record the
requested mode, effective mode and fallback reason.

### `generation_options`

This is the single catch-all table for native JSON request parameters. Names,
case, values and nested objects are sent unchanged. Consult your service's API
and model documentation: it accepts or rejects the options. DocMeThis checks
JSON validity, not provider-specific ranges or a whitelist of generation knobs.
Unsupported options are not silently omitted, renamed or retried with different
parameters.

The templates include complete, separate Chat, Responses, Anthropic and Gemini
policies. Their native output limits are respectively `max_tokens`,
`max_output_tokens`, `max_tokens` and `generationConfig.maxOutputTokens`.
For example, these are options for a Responses policy:

```toml
[fix.responses.generation_options]
max_output_tokens = 2000

[fix.responses.generation_options.reasoning]
effort = "low"

[fix.responses.generation_options.text]
verbosity = "low"
```

Use parameter names and structures from your service's API reference. In
pyproject overrides, outer configuration fields may use dashes, but keys inside
`generation-options` retain their exact native spelling.

DocMeThis owns the model, canonical prompt, non-streaming execution and structured
output schema. These paths cannot appear in `generation_options`, even when the
corresponding runtime field is absent:

| Protocol | Reserved paths (in addition to `model` for every protocol) |
|---|---|
| Chat Completions | `messages`, `stream`, `response_format` |
| Responses | `input`, `stream`, `background`, `text.format` |
| Anthropic | `messages`, `stream`, `output_config.format` |
| Gemini | `contents`, `generationConfig.responseMimeType`, `generationConfig.responseSchema`, `generationConfig.responseJsonSchema` |

Objects merge by distinct keys without replacing values; lists are indivisible.
A reserved path, replacement of its parent, or value collision fails before the
network call. Neighboring fields such as `text.verbosity` remain available.
Native output limits are user options, not reserved fields. Structured-output
fallback remains controlled by DocMeThis; an ordinary invalid option does not
trigger a fallback to another protocol, model or endpoint.

A schema validation error (for example `invalid_json_schema`) is reported as an
error, not as a missing capability. JSON-prompted fallback requires an explicit
structured-output incompatibility; the words `invalid` and `json_schema` in an
error message are not sufficient.

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

1. `profile` names a table that exists in `llm_api.toml`.
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
