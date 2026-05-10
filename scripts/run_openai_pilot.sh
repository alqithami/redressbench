#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
: "${OPENAI_API_KEY:?Set OPENAI_API_KEY first}"
MODEL="${MODEL:-gpt-4.1}"
PYTHONPATH=src python -m redressbench.run_experiment \
  --provider openai \
  --model "$MODEL" \
  --limit "${LIMIT:-8}" \
  --sleep "${SLEEP:-0}" \
  --output "outputs/openai_${MODEL//\//_}_pilot_runs.jsonl"
PYTHONPATH=src python -m redressbench.summarize_results \
  --runs "outputs/openai_${MODEL//\//_}_pilot_runs.jsonl" \
  --out-csv "analysis/openai_${MODEL//\//_}_pilot_summary.csv"
PYTHONPATH=src python -m redressbench.build_casefiles \
  --runs "outputs/openai_${MODEL//\//_}_pilot_runs.jsonl" \
  --case-dir "casefiles/openai_${MODEL//\//_}_pilot" \
  --annotation-csv "casefiles/openai_${MODEL//\//_}_pilot_annotation_template.csv"
