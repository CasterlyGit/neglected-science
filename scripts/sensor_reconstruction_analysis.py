#!/usr/bin/env python3
"""Frozen linear reconstruction; final holdout is intentionally locked."""
import argparse
import csv
from datetime import datetime
from pathlib import Path

FEATURES = ("ek", "solar", "humid", "azimuth", "altitude")


def rows(path):
    with Path(path).open(newline="") as handle:
        data = list(csv.DictReader(handle))
    data.sort(key=lambda row: datetime.fromisoformat(row["datetime"]))
    return data


def partition(data, name):
    n = len(data); cuts = {"exploration": (0, .5), "validation": (.5, .7), "final_holdout": (.7, 1)}
    start, end = cuts[name]
    return data[int(n * start):int(n * end)]


def solve(matrix, vector):
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    for column in range(len(vector)):
        pivot = max(range(column, len(vector)), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("singular calibration design")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(len(vector)):
            if row != column:
                factor = augmented[row][column]
                augmented[row] = [value - factor * base for value, base in zip(augmented[row], augmented[column])]
    return [row[-1] for row in augmented]


def fit(data):
    design = [[1.0] + [float(row[name]) for name in FEATURES] for row in data]
    outcome = [float(row["amedas"]) for row in data]
    return solve([[sum(row[i] * row[j] for row in design) for j in range(6)] for i in range(6)], [sum(row[i] * value for row, value in zip(design, outcome)) for i in range(6)])


def mae(data, coefficients, raw=False):
    return sum(abs(float(row["amedas"]) - (float(row["ek"]) if raw else sum(value * coefficient for value, coefficient in zip([1.0] + [float(row[name]) for name in FEATURES], coefficients)))) for row in data) / len(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--partition", choices=("exploration", "validation", "final_holdout"), required=True)
    parser.add_argument("--allow-final", action="store_true")
    args = parser.parse_args()
    if args.partition == "final_holdout" and not args.allow_final:
        raise SystemExit("final holdout locked until validation implementation freeze")
    data = rows(args.input)
    selected = partition(data, args.partition)
    if args.partition == "exploration":
        print({"partition": args.partition, "rows": len(selected), "features": FEATURES, "outcome": "amedas", "evaluation_not_implemented": True})
        return
    coefficients = fit(partition(data, "exploration"))
    print({"partition": args.partition, "rows": len(selected), "linear_mae": mae(selected, coefficients), "raw_ek_mae": mae(selected, coefficients, raw=True), "coefficients": coefficients})


if __name__ == "__main__":
    main()
