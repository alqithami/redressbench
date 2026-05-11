#!/usr/bin/env bash
set -euo pipefail

mkdir -p outputs analysis casefiles

PYTHONPATH=src python -m redressbench.run_experiment \
  --provider scripted \
  --model scripted \
  --limit 2 \
  --conditions baseline guardrailed trace trace_escalation \
  --output outputs/smoke_scripted_runs.jsonl

PYTHONPATH=src python -m redressbench.audit_runs \
  --runs outputs/smoke_scripted_runs.jsonl \
  --out-dir analysis/smoke_scripted

PYTHONPATH=src python -m redressbench.build_blinded_casefiles \
  --runs outputs/smoke_scripted_runs.jsonl \
  --scenarios data/scenarios_v0_2.jsonl \
  --case-dir casefiles/smoke_blinded \
  --annotation-csv casefiles/smoke_annotation_template.csv \
  --mapping-csv casefiles/smoke_private_mapping.csv

PYTHONPATH=src python -m redressbench.validate_annotations \
  --annotations casefiles/smoke_annotation_template.csv \
  --case-dir casefiles/smoke_blinded \
  --allow-empty

echo "Smoke test complete."
