from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .backends import get_backend
from .prompts import CONDITIONS, build_agent_prompt
from .scoring import extract_json_object, score_case

ROOT = Path(__file__).resolve().parents[2]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Run Agent RedressBench v0.2 scenarios.')
    parser.add_argument('--scenarios', type=Path, default=ROOT / 'data' / 'scenarios_v0_2.jsonl')
    parser.add_argument('--provider', choices=['scripted', 'openai', 'ollama'], default='scripted')
    parser.add_argument('--model', default='scripted')
    parser.add_argument('--conditions', nargs='+', choices=CONDITIONS, default=list(CONDITIONS))
    parser.add_argument('--limit', type=int, default=None, help='Limit number of scenarios for pilot runs.')
    parser.add_argument('--scenario-id', action='append', help='Run only one or more scenario IDs.')
    parser.add_argument('--output', type=Path, default=ROOT / 'outputs' / 'runs_v0_2.jsonl')
    parser.add_argument('--sleep', type=float, default=0.0, help='Seconds to sleep between model calls.')
    args = parser.parse_args(argv)

    scenarios = load_jsonl(args.scenarios)
    if args.scenario_id:
        wanted = set(args.scenario_id)
        scenarios = [s for s in scenarios if s['scenario_id'] in wanted]
    if args.limit is not None:
        scenarios = scenarios[:args.limit]

    backend = get_backend(args.provider)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    total = len(scenarios) * len(args.conditions)
    done = 0
    with args.output.open('w', encoding='utf-8') as out:
        for scenario in scenarios:
            for condition in args.conditions:
                done += 1
                prompt = build_agent_prompt(scenario, condition)
                try:
                    raw = backend.complete(prompt, scenario, condition, args.model)
                    parsed, parse_error = extract_json_object(raw)
                    score = score_case(scenario, parsed, parse_error)
                    error = None
                except Exception as exc:
                    raw = ''
                    parsed = None
                    parse_error = str(exc)
                    score = score_case(scenario, None, parse_error)
                    error = str(exc)
                row = {
                    'run_id': f"{scenario['scenario_id']}_{condition}_{args.provider}_{args.model}",
                    'timestamp_utc': utc_now(),
                    'scenario_id': scenario['scenario_id'],
                    'domain': scenario['domain'],
                    'title': scenario['title'],
                    'condition': condition,
                    'provider': args.provider,
                    'model': args.model,
                    'prompt': prompt,
                    'raw_output': raw,
                    'parsed_output': parsed,
                    'score': score,
                    'backend_error': error,
                }
                out.write(json.dumps(row, ensure_ascii=False) + '\n')
                print(f'[{done}/{total}] {scenario["scenario_id"]} {condition}: {score.get("outcome_label")} R={score.get("redressability_total")}', file=sys.stderr)
                if args.sleep:
                    time.sleep(args.sleep)
    print(f'Wrote {args.output}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
