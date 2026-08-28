# Troubleshooting

## Runtime Download Fails

Check that `DOCMETHIS_FIX_DISTRIBUTION_TOKEN` is configured, the requested
runtime SHA and artifact SHA-256 match the release record, and the private
artifact is available to the distribution channel.

## Gateway Authentication Fails

Check that `DOCMETHIS_FIX_API_KEY` is present in the consumer secret store. Do
not paste its value into an issue. Confirm that the Gateway contract version
matches the private runtime release.

## No Corrections Are Produced

Inspect the Check JSON summary first. A clean report, unsupported diagnostic,
missing provider profile or policy refusal can all result in zero patches.
Attach the sanitized summary and the facade/runtime versions to a support issue.

## A Generated Patch Fails CI

Keep the patch for review, rerun Check on the resulting commit, and report the
Check code, facade revision and runtime SHA. Do not upload private prompts or
complete source files.
