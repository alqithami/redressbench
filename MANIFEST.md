# Files to Replace or Add

This repository snapshot is intended to replace the current scaffold with a cleaner anonymous artifact.

## Replace

- `README.md`
- `README_v0_4_stress.md`
- `pyproject.toml`
- `requirements.txt`
- `scripts/run_scripted_demo.sh`
- `scripts/run_openai_pilot.sh`
- source files under `src/redressbench/` if your current repository has older versions

## Add

- `.gitignore`
- `ARTIFACT_CHECKLIST.md`
- `docs/annotator_quickstart.md`
- `docs/annotation_protocol.md`
- `docs/irb_ethics_note.md`
- `docs/reproducibility.md`
- `docs/anonymization_checklist.md`
- `docs/runtime_gated_redress.md`
- `docs/results_status.md`
- `docs/repository_manifest.md`
- `docs/artifact_appendix_plan.md`
- `src/redressbench/validate_annotations.py`
- `src/redressbench/annotation_agreement.py`
- `scripts/run_smoke_test.sh`
- `scripts/run_gpt41_v04_stress.sh`
- `scripts/run_ollama_v03_full.sh`
- `tests/test_smoke.py`
- `results/interim/README.md`
- `results/interim/*.csv`

## Suggested copy command

From outside the repository:

```bash
rsync -av redressbench_repository_v09/ /path/to/redressbench/
```

Then run:

```bash
cd /path/to/redressbench
bash scripts/run_smoke_test.sh
```
