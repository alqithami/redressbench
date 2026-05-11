from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Iterable

from .scoring import DIMENSIONS

CATEGORICAL_FIELDS = ['human_outcome_label', 'safety_judgment']


def read_by_id(path: Path) -> dict[str, dict[str, str]]:
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    return {row['blind_case_id']: row for row in rows}


def cohen_kappa(pairs: Iterable[tuple[str, str]]) -> float | None:
    pairs = [(a, b) for a, b in pairs if a != '' and b != '']
    if not pairs:
        return None
    n = len(pairs)
    observed = sum(1 for a, b in pairs if a == b) / n
    a_counts = Counter(a for a, _ in pairs)
    b_counts = Counter(b for _, b in pairs)
    labels = set(a_counts) | set(b_counts)
    expected = sum((a_counts[label] / n) * (b_counts[label] / n) for label in labels)
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def weighted_kappa_ordinal(pairs: Iterable[tuple[str, str]], max_score: int = 3) -> float | None:
    clean: list[tuple[int, int]] = []
    for a, b in pairs:
        if a == '' or b == '':
            continue
        try:
            clean.append((int(a), int(b)))
        except ValueError:
            continue
    if not clean:
        return None
    n = len(clean)
    labels = list(range(max_score + 1))
    a_counts = Counter(a for a, _ in clean)
    b_counts = Counter(b for _, b in clean)

    def weight(i: int, j: int) -> float:
        return ((i - j) ** 2) / (max_score ** 2)

    observed_disagreement = sum(weight(a, b) for a, b in clean) / n
    expected_disagreement = 0.0
    for i in labels:
        for j in labels:
            expected_disagreement += weight(i, j) * (a_counts[i] / n) * (b_counts[j] / n)
    if expected_disagreement == 0:
        return 1.0
    return 1 - observed_disagreement / expected_disagreement


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Compute agreement between two RedressBench annotators.')
    parser.add_argument('--a1', type=Path, required=True)
    parser.add_argument('--a2', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    parser.add_argument('--disagreement-threshold', type=int, default=1)
    args = parser.parse_args(argv)

    rows1 = read_by_id(args.a1)
    rows2 = read_by_id(args.a2)
    common_ids = sorted(set(rows1) & set(rows2))
    args.out_dir.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, object]] = []
    disagreement_rows: list[dict[str, object]] = []

    for field in CATEGORICAL_FIELDS:
        pairs = [(rows1[i].get(field, ''), rows2[i].get(field, '')) for i in common_ids]
        exact = mean([1.0 if a == b and a != '' else 0.0 for a, b in pairs])
        summary_rows.append({
            'field': field,
            'n_common': len(common_ids),
            'exact_agreement': exact,
            'cohen_kappa': cohen_kappa(pairs),
            'weighted_kappa': '',
            'mean_absolute_difference': '',
        })
        for case_id, (a, b) in zip(common_ids, pairs):
            if a != b:
                disagreement_rows.append({
                    'blind_case_id': case_id,
                    'field': field,
                    'a1_value': a,
                    'a2_value': b,
                    'difference': '',
                    'case_file': rows1[case_id].get('case_file', rows2[case_id].get('case_file', '')),
                })

    for dim in DIMENSIONS:
        pairs = [(rows1[i].get(dim, ''), rows2[i].get(dim, '')) for i in common_ids]
        numeric_diffs: list[float] = []
        exact_flags: list[float] = []
        for a, b in pairs:
            try:
                ia, ib = int(a), int(b)
            except ValueError:
                continue
            numeric_diffs.append(abs(ia - ib))
            exact_flags.append(1.0 if ia == ib else 0.0)
        summary_rows.append({
            'field': dim,
            'n_common': len(common_ids),
            'exact_agreement': mean(exact_flags),
            'cohen_kappa': '',
            'weighted_kappa': weighted_kappa_ordinal(pairs),
            'mean_absolute_difference': mean(numeric_diffs),
        })
        for case_id, (a, b) in zip(common_ids, pairs):
            try:
                diff = abs(int(a) - int(b))
            except ValueError:
                diff = ''
            if diff == '' or diff > args.disagreement_threshold:
                disagreement_rows.append({
                    'blind_case_id': case_id,
                    'field': dim,
                    'a1_value': a,
                    'a2_value': b,
                    'difference': diff,
                    'case_file': rows1[case_id].get('case_file', rows2[case_id].get('case_file', '')),
                })

    with (args.out_dir / 'agreement_summary.csv').open('w', encoding='utf-8', newline='') as f:
        fieldnames = ['field', 'n_common', 'exact_agreement', 'cohen_kappa', 'weighted_kappa', 'mean_absolute_difference']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    with (args.out_dir / 'disagreements_for_adjudication.csv').open('w', encoding='utf-8', newline='') as f:
        fieldnames = ['blind_case_id', 'case_file', 'field', 'a1_value', 'a2_value', 'difference']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(disagreement_rows)

    print(f'Common cases: {len(common_ids)}')
    print(f'Wrote {args.out_dir / "agreement_summary.csv"}')
    print(f'Wrote {args.out_dir / "disagreements_for_adjudication.csv"}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
