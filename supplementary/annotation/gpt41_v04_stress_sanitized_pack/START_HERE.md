# START HERE: RedressBench Sanitized Blinded Annotation Pack v0.4

Use this package for final blinded annotation of the GPT-4.1 v0.4 stress cases.

This pack replaces earlier packs. The case files have been sanitized to remove fields that could reveal or cue the benchmark designer's expected action, including:

- `ground_truth_expected_action`
- scenario title lines
- potential-harm summary lines that sometimes implied validity or wrongness

Annotate only from the visible scenario context, user request, affected party, policies, background records, contest prompt, and agent output.

## Process

1. Open `annotation_template.csv` or your assigned annotator template.
2. For each row, open the matching file in `casefiles/`.
3. Fill all required fields.
4. Record unresolved issues in `issue_log_template.csv`.
5. Return only the completed annotation CSV and issue log.
