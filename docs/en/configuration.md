# Configuration

The consumer repository owns non-secret Fix configuration. Start from the
examples in `templates/config/` and adapt them to the selected provider.

```toml
[tool.docmethis.fix]
api-profile = "example"
policy-profile = "example"
api-config-file = "config/llm_api.toml"
policy-config-file = "config/llm_policies.toml"
docstring-language = "en"
max-concurrency = 2
include-existing-docstrings = true
scope = "impacted"
```

The provider key is read from the environment variable named by the selected
API profile. Do not put the key in TOML, workflow YAML or an issue.

The private runtime and Gateway contracts determine which profiles and options
are available for a given release. Always use the configuration documented by
the matching release record and pinned runtime SHA.
