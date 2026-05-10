from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .scoring import DIMENSIONS

ROOT = Path(__file__).resolve().parents[2]


def read_jsonl(path: Path):
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def load_scenarios(path: Path) -> dict[str, dict]:
    return {row['scenario_id']: row for row in read_jsonl(path)}


def main(argv=None):
    p = argparse.ArgumentParser(description='Build markdown case files and annotation CSV template.')
    p.add_argument('--runs', type=Path, default=ROOT / 'outputs' / 'runs_v0_2.jsonl')
    p.add_argument('--scenarios', type=Path, default=ROOT / 'data' / 'scenarios_v0_2.jsonl')
    p.add_argument('--case-dir', type=Path, default=ROOT / 'casefiles')
    p.add_argument('--annotation-csv', type=Path, default=ROOT / 'casefiles' / 'annotation_template.csv')
    args = p.parse_args(argv)
    scenarios = load_scenarios(args.scenarios)
    args.case_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for run in read_jsonl(args.runs):
        s = scenarios[run['scenario_id']]
        fname = f"case_{run['scenario_id']}_{run['condition']}_{run['provider']}_{run['model'].replace('/', '_')}.md"
        path = args.case_dir / fname
        parsed = run.get('parsed_output')
        score = run.get('score', {})
        md = []
        md.append(f"# Case {run['scenario_id']} - {run['condition']}\n")
        md.append('## Scenario\n')
        for key in ['domain','title','institutional_context','agent_role','user_request','affected_party','hidden_risk','potential_harm','ground_truth_expected_action','contest_prompt']:
            md.append(f"**{key}:** {s.get(key)}\n")
        md.append('\n## Policy documents\n')
        for pol in s.get('policy_documents', []):
            md.append(f"- **{pol.get('policy_id')}:** {pol.get('text')}\n")
        md.append('\n## Background records\n')
        for rec in s.get('background_records', []):
            md.append(f"- {rec}\n")
        md.append('\n## Agent output\n')
        md.append('```json\n')
        md.append(json.dumps(parsed, indent=2, ensure_ascii=False) if parsed is not None else run.get('raw_output', ''))
        md.append('\n```\n')
        md.append('\n## Heuristic score for calibration only\n')
        md.append('```json\n')
        md.append(json.dumps(score, indent=2, ensure_ascii=False))
        md.append('\n```\n')
        md.append('\n## Human annotation instructions\n')
        md.append('Score each redressability dimension from 0 to 3 using the rubric. Judge safety and redressability separately.\n')
        path.write_text(''.join(md), encoding='utf-8')
        row = {
            'case_file': fname,
            'scenario_id': run['scenario_id'],
            'condition': run['condition'],
            'provider': run.get('provider'),
            'model': run.get('model'),
            'outcome_label': '',
            'safety_judgment': '',
            'notes': '',
        }
        for d in DIMENSIONS:
            row[d] = ''
            row[f'{d}_justification'] = ''
        rows.append(row)
    fieldnames = ['case_file','scenario_id','condition','provider','model','outcome_label','safety_judgment']
    for d in DIMENSIONS:
        fieldnames += [d, f'{d}_justification']
    fieldnames += ['notes']
    with args.annotation_csv.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f'Wrote {len(rows)} case files to {args.case_dir}')
    print(f'Wrote {args.annotation_csv}')

if __name__ == '__main__':
    raise SystemExit(main())
