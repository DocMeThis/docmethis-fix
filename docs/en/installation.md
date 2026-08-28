# Installation

DocMeThis Fix is installed by a consumer workflow from an exact private runtime
artifact. This public repository provides the workflow template; it does not
ship the runtime itself.

## Consumer Repository

1. Copy `templates/.github/workflows/docmethis-fix.yml` to `.github/workflows/`.
2. Copy the configuration examples from `templates/config/` when needed.
3. Configure the private distribution and Gateway secrets in the consumer repository.
4. Set the full private runtime commit SHA and matching artifact SHA-256 digest
   supplied during commercial onboarding.
5. Run the workflow manually before enabling it for pushes.

The workflow must install an immutable runtime artifact pinned by hash. It must
never resolve a branch, mutable tag, `latest` reference or shortened SHA.

## Immutable Runtime Pin

Use repository or organization variables for the non-secret pinning data:

- `DOCMETHIS_FIX_RUNTIME_SHA`: the full 40-character runtime commit SHA;
- `DOCMETHIS_FIX_ARTIFACT_SHA256`: the full 64-character artifact digest.

The installer must verify both values before executing the runtime. A semantic
facade release label can identify the matching documentation, but it must not
select what CI executes.

## Required Secret Names

- `DOCMETHIS_FIX_DISTRIBUTION_TOKEN` authorizes access to the private runtime.
- `DOCMETHIS_FIX_API_KEY` authorizes Fix requests to Gateway.
- The provider API key named by the selected `llm_api.toml` profile.

The values belong only in the consumer repository's secret store.
