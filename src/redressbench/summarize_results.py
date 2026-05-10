from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict, Counter
from pathlib import Path

from .scoring import DIMENSIONS

ROOT = Path(__file__).resolve().parents[2]


def read_jsonl(path: Path):
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def mean(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    return sum(vals) / len(vals) if vals else None


def main(argv=None):
    p = argparse.ArgumentParser(description='Summarize Agent RedressBench run JSONL.')
    p.add_argument('--runs', type=Path, default=ROOT / 'outputs' / 'runs_v0_2.jsonl')
    p.add_argument('--out-csv', type=Path, default=ROOT / 'analysis' / 'summary_by_condition.csv')
    args = p.parse_args(argv)

    rows = list(read_jsonl(args.runs))
    groups = defaultdict(list)
    for row in rows:
        groups[(row['condition'], row.get('model', ''), row.get('provider', ''))].append(row)

    fields = ['condition', 'model', 'provider', 'n', 'parse_ok_rate', 'unsafe_action_rate', 'mean_redressability_total'] + [f'mean_{d}' for d in DIMENSIONS] + ['outcome_counts']
    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_rows = []
    for (condition, model, provider), g in sorted(groups.items()):
        scores = [r.get('score', {}) for r in g]
        n = len(g)
        parse_ok_rate = mean([1 if s.get('parse_ok') else 0 for s in scores])
        unsafe_action_rate = mean([1 if s.get('unsafe_action') else 0 for s in scores if s.get('unsafe_action') is not None])
        total = mean([s.get('redressability_total') for s in scores])
        row = {
            'condition': condition,
            'model': model,
            'provider': provider,
            'n': n,
            'parse_ok_rate': parse_ok_rate,
            'unsafe_action_rate': unsafe_action_rate,
            'mean_redressability_total': total,
            'outcome_counts': json.dumps(Counter(s.get('outcome_label') for s in scores), sort_keys=True),
        }
        for d in DIMENSIONS:
            row[f'mean_{d}'] = mean([s.get(d) for s in scores])
        out_rows.append(row)

    with args.out_csv.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    # Console table
    print('condition\tprovider\tmodel\tn\tunsafe_rate\tmean_R')
    for r in out_rows:
        print(f"{r['condition']}\t{r['provider']}\t{r['model']}\t{r['n']}\t{r['unsafe_action_rate']:.3f}\t{r['mean_redressability_total']:.2f}")
    print(f'Wrote {args.out_csv}')

if __name__ == '__main__':
    raise SystemExit(main())
