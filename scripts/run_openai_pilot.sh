#!/usr/bin/env bash
set -euo pipefail

: "${OPENAI_API_KEY:?Set OPENAI_API_KEY before running.}"
MODEL="${MODEL:-gpt-4.1}"
LIMIT="${LIMIT:-8}"

mkdir -p outputs analysis casefiles

PYTHONPATH=src python -m redressbench.run_experiment \
  --provider openai \
  --model "$MODEL" \
  --limit "$LIMIT" \
  --conditions baseline guardrailed trace trace_escalation \
  --output "outputs/${MODEL}_pilot_runs.jsonl"

PYTHONPATH=src python -m redressbench.audit_runs \
  --runs "outputs/${MODEL}_pilot_runs.jsonl" \
  --out-dir "analysis/${MODEL}_pilot"
