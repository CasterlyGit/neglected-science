#!/usr/bin/env python3
"""Dependency-light fixed-effect held-block reconstruction for the virus reserve."""
import argparse
import csv
from pathlib import Path

FEATURES = ("best.p", "median.ct", "best.y", "rel.susc")


def solve(matrix, vector):
    a = [row[:] + [value] for row, value in zip(matrix, vector)]
    for col in range(len(vector)):
        pivot = max(range(col, len(vector)), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-12: raise ValueError("singular design")
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]; a[col] = [value / scale for value in a[col]]
        for row in range(len(vector)):
            if row != col:
                factor = a[row][col]; a[row] = [value - factor * base for value, base in zip(a[row], a[col])]
    return [row[-1] for row in a]


def load(path):
    with Path(path).open(newline="") as h: return list(csv.DictReader(h))


def fit(rows):
    x = [[1.0] + [float(r[f]) for f in FEATURES] for r in rows]; y = [float(r["trans.ability"]) for r in rows]
    return solve([[sum(r[i] * r[j] for r in x) for j in range(5)] for i in range(5)], [sum(r[i] * v for r, v in zip(x, y)) for i in range(5)])


def main():
    p = argparse.ArgumentParser(); p.add_argument("--input", required=True); p.add_argument("--holdout-block", required=True); p.add_argument("--allow-evaluation", action="store_true"); a = p.parse_args()
    data = load(a.input); blocks = sorted({r["block"] for r in data})
    if a.holdout_block not in blocks: raise ValueError("unknown block")
    train, test = [r for r in data if r["block"] != a.holdout_block], [r for r in data if r["block"] == a.holdout_block]
    if not a.allow_evaluation:
        print({"blocks": blocks, "holdout": a.holdout_block, "train_rows": len(train), "test_rows": len(test), "outcomes_evaluated": False}); return
    c = fit(train); mae = sum(abs(float(r["trans.ability"]) - sum(v*w for v,w in zip([1.0]+[float(r[f]) for f in FEATURES], c))) for r in test)/len(test)
    print({"holdout": a.holdout_block, "mae": mae, "coefficients": c, "scope":"fixed-effect reconstruction only"})

if __name__ == "__main__": main()
