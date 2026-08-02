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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--partition", choices=("exploration", "validation", "final_holdout"), required=True)
    parser.add_argument("--allow-final", action="store_true")
    args = parser.parse_args()
    if args.partition == "final_holdout" and not args.allow_final:
        raise SystemExit("final holdout locked until validation implementation freeze")
    selected = partition(rows(args.input), args.partition)
    print({"partition": args.partition, "rows": len(selected), "features": FEATURES, "outcome": "amedas", "evaluation_not_implemented": True})


if __name__ == "__main__":
    main()
