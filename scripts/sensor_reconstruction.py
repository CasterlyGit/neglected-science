#!/usr/bin/env python3
"""No-outcome structural gate for the sensor temporal-transfer reconstruction."""
import argparse
import csv
from datetime import datetime
from pathlib import Path

REQUIRED = ("datetime", "amedas", "ek", "humid", "solar", "wind", "azimuth", "altitude")


def structural_receipt(path):
    with Path(path).open(newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != REQUIRED:
            raise ValueError("unexpected sensor schema")
        timestamps = [datetime.fromisoformat(row["datetime"]) for row in reader]
    if len(timestamps) < 20 or timestamps != sorted(timestamps):
        raise ValueError("timestamps must be sufficient and ordered")
    split = timestamps[int(len(timestamps) * 0.7)]
    return {"rows": len(timestamps), "first": timestamps[0].isoformat(), "last": timestamps[-1].isoformat(), "chronological_split": split.isoformat(), "outcome_values_read": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--structural-input", required=True)
    args = parser.parse_args()
    print(structural_receipt(args.structural_input))


if __name__ == "__main__":
    main()
