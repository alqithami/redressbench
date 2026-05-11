# Supplementary Artifact Plan

For the final paper submission, the anonymous repository should contain enough material for reviewers to understand and reproduce the benchmark without requiring hidden author knowledge.

## Reviewer-facing material

Include:

- benchmark scenarios;
- prompts and output contracts;
- diagnostic scorer;
- smoke-test script;
- model-run scripts;
- annotation rubric;
- blinded annotation protocol;
- diagnostic result summaries;
- final annotation summaries after completion;
- clear explanation that automatic scores are diagnostic.

## Optional reviewer-facing material

Include if anonymity and policy allow:

- raw model trajectories;
- blinded case files;
- adjudicated annotation CSVs;
- inter-annotator agreement reports;
- IRB determination summary with institutional identifiers removed.

## Coordinator-only material

Do not share with annotators. For double-anonymous review, decide carefully whether to include:

- private condition mapping files;
- annotator identities;
- IRB correspondence;
- internal issue logs.

## Paper-to-repository consistency

Every table in the paper should have a corresponding file or command in the repository. Recommended mapping:

| Paper item | Repository source |
|---|---|
| Benchmark domains and counts | `data/*.jsonl` |
| Condition descriptions | `prompts/*.txt`, `prompts/contracts/*.json` |
| Diagnostic results | `analysis/*/condition_summary.csv` |
| Domain diagnostics | `analysis/*/domain_condition_summary.csv` |
| Annotation protocol | `docs/annotation_protocol.md` |
| Human annotation results | `results/final_annotations/` |
| Runtime gate proposal | `docs/runtime_gated_redress.md` |
