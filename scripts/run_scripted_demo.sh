#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=src python -m redressbench.run_experiment \
  --provider scripted \
  --model scripted \
  --limit 8 \
  --output outputs/scripted_demo_runs.jsonl
PYTHONPATH=src python -m redressbench.summarize_results \
  --runs outputs/scripted_demo_runs.jsonl \
  --out-csv analysis/scripted_demo_summary.csv
PYTHONPATH=src python -m redressbench.build_casefiles \
  --runs outputs/scripted_demo_runs.jsonl \
  --case-dir casefiles/scripted_demo \
  --annotation-csv casefiles/scripted_demo_annotation_template.csv
