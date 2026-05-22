# RedressBench repository audit and update plan

## Audit summary

The repository is close to submission-ready as an anonymous artifact, but it needs a final cleanup before being linked from a double-anonymous paper. The current repository already contains the core benchmark structure: scenario data, prompts, schemas, rubrics, scripts, source code, documentation, interim results, and human-validation summaries. The most important correction is to replace the current blinded-case builder with a sanitized version and to add a clean supplementary annotation package.

## Current strengths

- Repository root includes the expected benchmark directories: `data/`, `prompts/`, `schemas/`, `rubrics/`, `src/redressbench/`, `scripts/`, `docs/`, `tests/`, and `results/`.
- Scenario data includes seed, stress, and combined splits.
- Source code includes runners, scoring/audit code, case-file building, annotation validation, and agreement utilities.
- `results/human/` already includes aggregate single-pass validation summaries for the GPT-4.1 stress split.
- `docs/` already contains annotation, ethics, reproducibility, runtime-gate, and anonymization materials.

## Required corrections before submission

1. Replace `src/redressbench/build_blinded_casefiles.py`.
   - The current version writes `title`, `potential_harm`, and `ground_truth_expected_action` into annotator-facing case files.
   - These fields break strict blinding and should be excluded by default.
   - The replacement builder in the update package generates sanitized case files and stores private fields only in the private mapping CSV.

2. Replace `README.md`.
   - The current README is usable but still says annotation is in progress and has internal/status language.
   - The replacement README presents the artifact as a reviewer-facing repository and includes the validation supplement.

3. Add supplementary annotation materials.
   - Add `supplementary/annotation/gpt41_v04_stress_sanitized_pack/`.
   - Add a blinded single-validator annotation file and issue log under `results/human/`.
   - Add `docs/human_validation_supplement.md` and `docs/sanitized_annotation_pack.md`.

4. Remove stale generated/private files from version control.
   - Remove committed `__pycache__` files.
   - Remove or carefully replace tracked `casefiles/`, `outputs/`, and `analysis/` directories unless they are intentionally released and sanitized.
   - Do not publish private mapping files.

5. Rename deadline/status documents.
   - Remove `docs/README_deadline_validation_update.md` and `docs/gpt41_v04_stress_deadline_validation_status.md`, or leave them unlinked.
   - Use the cleaner `docs/gpt41_v04_stress_validation_status.md` in the update package.

## Package contents

The update package contains:

- `README.md` replacement;
- `.gitignore` replacement/addition;
- `REVIEWER_GUIDE.md`;
- `GITHUB_UPDATE_INSTRUCTIONS.md`;
- `APPLY_REPOSITORY_UPDATE.sh`;
- sanitized `src/redressbench/build_blinded_casefiles.py` replacement;
- `docs/human_validation_supplement.md`;
- `docs/sanitized_annotation_pack.md`;
- `docs/anonymous_artifact_checklist.md`;
- clean validation status document;
- `results/human/` validation summaries and blinded validation CSV;
- sanitized annotation pack under `supplementary/annotation/gpt41_v04_stress_sanitized_pack/`;
- convenience script `scripts/build_gpt41_v04_sanitized_annotation_pack.sh`.

## Validation checks performed

- The blinded validation CSV has 96 rows.
- All required annotation columns are present.
- No duplicate blinded case IDs were detected.
- All referenced case files exist in the sanitized supplementary pack.
- Outcome labels and safety labels are valid.
- All redressability scores are in `{0,1,2,3}`.
- All safety and dimension justifications are non-empty.
- Sanitized case files contain no detected `ground_truth`, `expected_action`, `potential_harm`, `model_draft`, heuristic-score, or condition-label fields.
- The replacement case-file builder passes Python syntax compilation.

## Recommended commit message

```text
Finalize anonymous artifact and validation supplement
```
