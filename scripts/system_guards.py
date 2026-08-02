#!/usr/bin/env python3
"""Deterministic guards for closed-evidence investigations and method learning."""
import argparse, hashlib, json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def load(path): return json.loads((ROOT / path).read_text())
def schema(name): return load(Path("schemas") / name)
def validate(record, schema_name):
    return list(Draft202012Validator(schema(schema_name)).iter_errors(record))
def sha(path): return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
def benchmark_result(case):
    return "admit" if all(case[key] for key in ("construction", "data", "self_contained")) else "reject"
def pearson(pairs):
    xs, ys=zip(*pairs); xb=sum(xs)/len(xs); yb=sum(ys)/len(ys)
    den=(sum((x-xb)**2 for x in xs)*sum((y-yb)**2 for y in ys))**.5
    return sum((x-xb)*(y-yb) for x,y in pairs)/den if den else None
def synthetic_artifact_check():
    shared=[1,-1,1,-1]; independent=[1,1,-1,-1]
    naive=pearson(list(zip(shared,[-x for x in shared])))
    cross=pearson(list(zip(independent,[-x for x in shared])))
    return {"naive":naive,"independent":cross,"pass":naive == -1.0 and abs(cross) < 1e-12}
def promotion_allowed(entry):
    gates=entry["selection_quality"],entry["execution_integrity"]
    return all(gate == "pass" for gate in gates)
def check_transaction(path="verification/ecoli-transaction.json"):
    record=load(path); errors=validate(record,"investigation-transaction.schema.json")
    if errors: raise ValueError(errors)
    mismatches=[item["path"] for item in record["files"] if sha(item["path"]) != item["sha256"]]
    if mismatches: raise ValueError(f"checksum mismatch: {mismatches}")
    if validate(load(record["preregistration"]),"preregistration.schema.json"): raise ValueError("invalid preregistration")
    if validate(load(record["result_receipt"]),"investigation-result.schema.json"): raise ValueError("invalid result receipt")
    return {"transaction":"pass","investigation_id":record["investigation_id"]}
def check_benchmark(path="verification/selection-benchmark.json"):
    cases=load(path)["cases"]
    failures=[c["id"] for c in cases if benchmark_result(c)!=c["expected"]]
    return {"benchmark":"pass" if not failures else "fail","cases":len(cases),"failures":failures}
def main():
    p=argparse.ArgumentParser(); p.add_argument("command",choices=["transaction","benchmark","synthetic"]); args=p.parse_args()
    print(json.dumps(check_transaction() if args.command=="transaction" else check_benchmark() if args.command=="benchmark" else synthetic_artifact_check(),sort_keys=True))
if __name__=="__main__": main()
