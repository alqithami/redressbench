# Repository Update Instructions

This package contains replacement and supplementary files for `redressbench`.

## Apply the update

From a local clone of the repository:

```bash
unzip redressbench_submission_update_v22.zip -d /tmp/redressbench_update
rsync -av /tmp/redressbench_update/redressbench_submission_update_v22/ /path/to/redressbench/
cd /path/to/redressbench
```

## Remove stale or risky files

The current repository contains generated directories and a Python `__pycache__` directory. Remove them from version control unless intentionally releasing checked and sanitized contents:

```bash
git rm -r --cached src/redressbench/__pycache__ || true
git rm -r --cached casefiles || true
git rm -r --cached outputs || true
git rm -r --cached analysis || true
```

Do not remove `results/`, `data/`, `prompts/`, `schemas/`, `rubrics/`, `scripts/`, or `supplementary/annotation/`.

The older files below use deadline/status naming and should be removed or left unlinked. The update package replaces them with cleaner names:

```bash
git rm --cached docs/README_deadline_validation_update.md || true
git rm --cached docs/gpt41_v04_stress_deadline_validation_status.md || true
```

## Add updated files

```bash
git add README.md .gitignore REVIEWER_GUIDE.md \
  docs/human_validation_supplement.md \
  docs/sanitized_annotation_pack.md \
  docs/anonymous_artifact_checklist.md \
  docs/gpt41_v04_stress_validation_status.md \
  results/human/ \
  supplementary/annotation/gpt41_v04_stress_sanitized_pack/ \
  scripts/build_gpt41_v04_sanitized_annotation_pack.sh \
  src/redressbench/build_blinded_casefiles.py

git status
```

## Final checks before push

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
bash scripts/run_smoke_test.sh
PYTHONPATH=src python -m redressbench.validate_annotations \
  --annotations results/human/gpt41_v04_stress_single_validator_annotation_blinded.csv \
  --case-dir supplementary/annotation/gpt41_v04_stress_sanitized_pack/casefiles
```

Then commit and push:

```bash
git commit -m "Finalize anonymous artifact and validation supplement"
git push
```

## Important anonymity warning

Do not link a public repository owned by a named account from a double-anonymous submission. Mirror the same files to the anonymous repository used in the paper link, or use an anonymizing service. The public repository can remain a working copy, but the submitted link should not identify authors.
