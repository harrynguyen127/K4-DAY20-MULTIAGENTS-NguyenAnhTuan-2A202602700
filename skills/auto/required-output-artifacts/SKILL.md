---
name: required-output-artifacts
description: Use when a task asks for an output file, report, dataset, or structured deliverable rather than only code changes.
---
- Extract every required output path, filename, and format from the task before analysis.
- Create the parent directory if missing and write the artifact to the exact expected location.
- Include every required top-level field, metadata block, header row, and column.
- Use the specified units and representations; convert values during generation, not in prose.
- Apply required canonicalization: spelling, case, separators, and abbreviations.
- Apply required ordering and filtering to the output data.
- After writing, programmatically load the artifact and assert it exists, parses, and has expected keys/columns.
- Check aggregate counts or totals against the source data to catch dropped or duplicated records.
- Remove temporary helper scripts and scratch outputs unless the task allows them.
- Before finalizing, list each requested artifact and confirm it is present and valid.