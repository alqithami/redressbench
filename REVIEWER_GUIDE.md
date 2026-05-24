# Reviewer Guide

This repository is organized to support anonymous review of Agent RedressBench.

## Recommended reading path

1. `README.md` for the artifact overview and quickstart.
2. `docs/human_validation_supplement.md` for the validation annotation procedure and interpretation.
3. `data/scenarios_v0_4_stress.jsonl` for the stress split used in the GPT-4.1 validation analysis.
4. `prompts/` for the condition-specific instructions and output contracts.
5. `src/redressbench/` for experiment runners, diagnostic scoring, audit scripts, and sanitized case-file generation.
6. `results/human/` for aggregate validation summaries and the blinded single-validator annotation file.
7. `supplementary/annotation/gpt41_v04_stress_sanitized_pack/` for the case files that were safe to show a validator.

## What is intentionally excluded

Private condition-mapping files, API keys, local environment files, and author-identifying metadata are excluded. Generated model trajectories can be regenerated using the documented commands. If raw model trajectories are released later, they should be placed under an archival release after confirming that they contain no secrets or author-identifying paths.

## Validation status

The included validation material is a single-pass blinded validation over the 96 GPT-4.1 v0.4 stress cases. It is appropriate for inspecting the redressability scoring procedure and the paper's validation analysis. It is not a substitute for fully adjudicated multi-rater evidence.
