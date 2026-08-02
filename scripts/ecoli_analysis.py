#!/usr/bin/env python3
"""Partition-safe E. coli robustness analysis for preregistration v1."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PARTITIONS = {
    "exploration": ({"1", "2"}, [("1", "2"), ("2", "1")]),
    "validation": ({"1", "2", "3"}, [("1", "3"), ("2", "3")]),
    "final": ({"1", "2", "4"}, [("1", "4"), ("2", "4")]),
}


def read_rows(path: Path):
    with path.open(newline="") as handle:
        return list(csv.DictReader((line for line in handle if not line.startswith("#")), delimiter="\t"))


def pearson(pairs):
    if len(pairs) < 3:
        return None
    xs, ys = zip(*pairs)
    xbar, ybar = sum(xs) / len(xs), sum(ys) / len(ys)
    numerator = sum((x - xbar) * (y - ybar) for x, y in pairs)
    denominator = math.sqrt(sum((x - xbar) ** 2 for x in xs) * sum((y - ybar) ** 2 for y in ys))
    return None if denominator == 0 else numerator / denominator


def fisher_mean(correlations):
    usable = [value for value in correlations if value is not None and abs(value) < 1]
    if not usable:
        return None
    return math.tanh(sum(math.atanh(value) for value in usable) / len(usable))


def anc_initial_by_block(rows, blocks):
    values = defaultdict(list)
    for row in rows:
        if row["block"] in blocks:
            key = (row["strain"], row["env"], row["mut"], row["block"])
            values[key].append(float(row["corrected.r"]) + float(row["r.anc.strain"]) - 1)
    return {key: sum(group) / len(group) for key, group in values.items()}


def published_style(rows, blocks):
    grouped = defaultdict(list)
    for row in rows:
        if row["block"] in blocks:
            key = (row["strain"], row["env"], row["mut"], row["rep"])
            grouped[key].append(row)
    comparisons = defaultdict(list)
    for (strain, env, _mut, _rep), group in grouped.items():
        comparisons[(strain, env)].append((
            sum(float(row["r.anc.strain"]) for row in group) / len(group),
            sum(float(row["r.change"]) for row in group) / len(group),
        ))
    return {f"{strain}:{env}": pearson(pairs) for (strain, env), pairs in sorted(comparisons.items())}


def cross_fitted(ancestor_rows, evolved_rows, x_block, y_block):
    ancestor = anc_initial_by_block(ancestor_rows, {x_block, y_block})
    comparisons = defaultdict(list)
    for row in evolved_rows:
        if row["block"] != y_block:
            continue
        base = (row["strain"], row["env"], row["mut"])
        x = ancestor.get(base + (x_block,))
        y_ancestor = ancestor.get(base + (y_block,))
        if x is None or y_ancestor is None:
            continue
        gain = float(row["corrected.r"]) - y_ancestor
        comparisons[(row["strain"], row["env"])].append((x, gain))
    return {f"{strain}:{env}": pearson(pairs) for (strain, env), pairs in sorted(comparisons.items())}


def summarise_cross_fit(ancestor_rows, evolved_rows, pairs):
    estimates = {f"{x}_to_{y}": cross_fitted(ancestor_rows, evolved_rows, x, y) for x, y in pairs}
    combined = {
        key: fisher_mean([estimate.get(key) for estimate in estimates.values()])
        for key in sorted(set().union(*(set(estimate) for estimate in estimates.values())))
    }
    return estimates, combined


def analysis(partition):
    ancestor_rows = read_rows(RAW / "data_set-full.anc.txt")
    evolved_rows = read_rows(RAW / "data_set-full.ev.change.txt")
    blocks, pairs = PARTITIONS[partition]
    baseline = published_style(evolved_rows, blocks)
    estimates, combined = summarise_cross_fit(ancestor_rows, evolved_rows, pairs)
    return {
        "partition": partition,
        "blocks": sorted(blocks),
        "published_style_correlations": baseline,
        "published_style_mean": fisher_mean(list(baseline.values())),
        "cross_fit_estimates": estimates,
        "cross_fit_mean": fisher_mean(list(combined.values())),
        "eligible_comparisons": sum(value is not None for value in combined.values()),
        "excluded_comparisons": sorted(key for key, value in combined.items() if value is None),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--partition", required=True, choices=["exploration", "validation", "final"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analysis(args.partition)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
