#!/usr/bin/env bash
set -euo pipefail

: "${OPENAI_API_KEY:?Set OPENAI_API_KEY before running.}"
MODEL="${MODEL:-gpt-4.1}"

mkdir -p outputs analysis casefiles

PYTHONPATH=src python -m redressbench.run_experiment \
  --scenarios data/scenarios_v0_4_stress.jsonl \
  --provider openai \
  --model "$MODEL" \
  --conditions baseline guardrailed trace trace_escalation \
  --output "outputs/${MODEL}_v04_stress_runs.jsonl"

PYTHONPATH=src python -m redressbench.audit_runs \
  --runs "outputs/${MODEL}_v04_stress_runs.jsonl" \
  --out-dir "analysis/${MODEL}_v04_stress"

PYTHONPATH=src python -m redressbench.build_blinded_casefiles \
  --runs "outputs/${MODEL}_v04_stress_runs.jsonl" \
  --scenarios data/scenarios_v0_4_stress.jsonl \
  --case-dir "casefiles/${MODEL}_v04_stress_blinded" \
  --annotation-csv "casefiles/${MODEL}_v04_stress_annotation_template.csv" \
  --mapping-csv "casefiles/${MODEL}_v04_stress_private_mapping.csv"
