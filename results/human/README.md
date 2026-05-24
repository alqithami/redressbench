# Human Validation Results

This directory contains reviewer-facing validation summaries and a blinded single-validator annotation file for the GPT-4.1 v0.4 stress split.

## Files

- `gpt41_v04_stress_single_validator_annotation_blinded.csv`: blinded validation labels and redressability scores for 96 case files.
- `gpt41_v04_stress_single_validator_issue_log.csv`: validator issue log for case-specific ambiguities, with validator ID anonymized.
- `gpt41_v04_stress_validation_condition_summary.csv`: condition-level validation summary after private coordinator-side merge.
- `gpt41_v04_stress_validation_dimension_summary.csv`: mean dimension scores by condition.
- `gpt41_v04_stress_validation_domain_summary.csv`: domain-level validation summary.
- `gpt41_v04_stress_validation_domain_condition_summary.csv`: domain-by-condition validation summary.
- `gpt41_v04_stress_validation_paired_deltas.csv`: paired redressability deltas by scenario.
- `gpt41_v04_stress_validation_heuristic_human_crosswalk.csv`: crosswalk between diagnostic heuristic flags and validation labels.

## Caution

The included validation pass is single-pass and blinded. It is not an adjudicated multi-rater annotation study. Private condition mappings are intentionally not included.
