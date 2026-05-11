# Artifact Checklist

Use this checklist before submission.

## Code

- [ ] `bash scripts/run_smoke_test.sh` succeeds.
- [ ] `python -m redressbench.run_experiment --help` succeeds with `PYTHONPATH=src`.
- [ ] `python -m redressbench.audit_runs --help` succeeds.
- [ ] `python -m redressbench.build_blinded_casefiles --help` succeeds.
- [ ] `python -m redressbench.validate_annotations --help` succeeds.
- [ ] `python -m redressbench.annotation_agreement --help` succeeds.

## Data

- [ ] Seed scenarios present.
- [ ] Stress scenarios present.
- [ ] Combined scenarios present.
- [ ] Scenario schema present.
- [ ] Redress trace schema present.

## Annotation

- [ ] Rubric present.
- [ ] Annotator quickstart present.
- [ ] Annotation protocol present.
- [ ] Calibration plan documented.
- [ ] IRB/ethics status documented accurately.

## Anonymity

- [ ] No author names or affiliations.
- [ ] No identifying repository owner in text.
- [ ] No private paths, API keys, or tokens.
- [ ] No annotator names.
- [ ] Private mapping files handled deliberately.

## Paper consistency

- [ ] README version matches paper version.
- [ ] Reported model names and splits match paper.
- [ ] Results in paper match CSV summaries.
- [ ] Human annotation status matches paper.
