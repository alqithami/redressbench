#!/usr/bin/env bash
set -euo pipefail

RUNS="${1:-outputs/gpt-4.1_v04_stress_runs.jsonl}"
SCENARIOS="${2:-data/scenarios_v0_4_stress.jsonl}"
OUT_DIR="${3:-casefiles/gpt41_v04_stress_sanitized}"
ANNOTATION_CSV="${4:-casefiles/gpt41_v04_stress_annotation_template.csv}"
MAPPING_CSV="${5:-casefiles/gpt41_v04_stress_private_mapping.csv}"

PYTHONPATH=src python -m redressbench.build_blinded_casefiles \
  --runs "$RUNS" \
  --scenarios "$SCENARIOS" \
  --case-dir "$OUT_DIR" \
  --annotation-csv "$ANNOTATION_CSV" \
  --mapping-csv "$MAPPING_CSV"

echo "Sanitized case files written to $OUT_DIR"
echo "Annotation template written to $ANNOTATION_CSV"
echo "Private mapping written to $MAPPING_CSV -- do not share this file with annotators."
