from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def read_jsonl(path: Path):
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def build_frame(path: Path) -> pd.DataFrame:
    rows = []
    for o in read_jsonl(path):
        score = o.get('score') or {}
        parsed = o.get('parsed_output') or {}
        trace = parsed.get('redress_trace') if isinstance(parsed, dict) else None
        rows.append({
            'run_id': o.get('run_id'),
            'scenario_id': o.get('scenario_id'),
            'domain': o.get('domain'),
            'title': o.get('title'),
            'condition': o.get('condition'),
            'provider': o.get('provider'),
            'model': o.get('model'),
            'backend_error': o.get('backend_error'),
            'parse_ok': score.get('parse_ok'),
            'outcome_label': score.get('outcome_label'),
            'unsafe_action': score.get('unsafe_action'),
            'unsafe_action_proxy': score.get('unsafe_action_proxy'),
            'consequential_action_taken': score.get('consequential_action_taken'),
            'valid_consequential_action': score.get('valid_consequential_action'),
            'redressability_total': score.get('redressability_total'),
            'detectability': score.get('detectability'),
            'traceability': score.get('traceability'),
            'contestability': score.get('contestability'),
            'reversibility': score.get('reversibility'),
            'remedy': score.get('remedy'),
            'recurrence_prevention': score.get('recurrence_prevention'),
            'burden_allocation': score.get('burden_allocation'),
            'value_chain_assignability': score.get('value_chain_assignability'),
            'trace_nonempty': isinstance(trace, dict) and bool(trace),
            'notice': parsed.get('affected_party_notice') if isinstance(parsed, dict) else None,
            'contestability_route_present': bool(parsed.get('contestability_route')) and str(parsed.get('contestability_route')).lower() not in {'none', 'not_applicable'},
            'reversibility_plan_present': bool(parsed.get('reversibility_plan')) and str(parsed.get('reversibility_plan')).lower() not in {'none', 'not_applicable'},
            'remedy_plan_present': bool(parsed.get('remedy_plan')) and str(parsed.get('remedy_plan')).lower() not in {'none', 'not_applicable'},
        })
    return pd.DataFrame(rows)


def main(argv=None):
    p = argparse.ArgumentParser(description='Audit a RedressBench run JSONL file.')
    p.add_argument('--runs', type=Path, required=True)
    p.add_argument('--out-dir', type=Path, required=True)
    args = p.parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    df = build_frame(args.runs)
    df.to_csv(args.out_dir / 'run_level_audit.csv', index=False)
    summary = df.groupby(['provider', 'model', 'condition'], dropna=False).agg(
        n=('run_id', 'count'),
        parse_ok_rate=('parse_ok', 'mean'),
        backend_error_rate=('backend_error', lambda s: s.notna().mean()),
        unsafe_action_rate=('unsafe_action', 'mean'),
        unsafe_action_proxy_rate=('unsafe_action_proxy', 'mean'),
        consequential_action_rate=('consequential_action_taken', 'mean'),
        valid_consequential_rate=('valid_consequential_action', 'mean'),
        redressability_mean=('redressability_total', 'mean'),
        redressability_median=('redressability_total', 'median'),
        trace_nonempty_rate=('trace_nonempty', 'mean'),
        detectability_mean=('detectability', 'mean'),
        traceability_mean=('traceability', 'mean'),
        contestability_mean=('contestability', 'mean'),
        reversibility_mean=('reversibility', 'mean'),
        remedy_mean=('remedy', 'mean'),
        recurrence_mean=('recurrence_prevention', 'mean'),
        burden_mean=('burden_allocation', 'mean'),
        value_chain_mean=('value_chain_assignability', 'mean'),
    ).reset_index()
    summary.to_csv(args.out_dir / 'condition_summary.csv', index=False)
    if 'domain' in df:
        domain_summary = df.groupby(['domain', 'condition'], dropna=False).agg(
            n=('run_id', 'count'),
            parse_ok_rate=('parse_ok', 'mean'),
            unsafe_action_rate=('unsafe_action', 'mean'),
            unsafe_action_proxy_rate=('unsafe_action_proxy', 'mean'),
        consequential_action_rate=('consequential_action_taken', 'mean'),
        valid_consequential_rate=('valid_consequential_action', 'mean'),
            redressability_mean=('redressability_total', 'mean'),
            trace_nonempty_rate=('trace_nonempty', 'mean'),
        ).reset_index()
        domain_summary.to_csv(args.out_dir / 'domain_condition_summary.csv', index=False)
    print(f'Wrote audit outputs to {args.out_dir}')


if __name__ == '__main__':
    raise SystemExit(main())
