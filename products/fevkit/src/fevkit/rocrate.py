from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .audit import audit_bundle
from .io import bundle_root, canonical_json, load_document, safe_path

RO_CRATE_CONTEXT = "https://w3id.org/ro/crate/1.1/context"
PROCESS_RUN_PROFILE = "https://w3id.org/ro/wfrun/process/0.5"


def export_rocrate(path: str | Path, output: str | Path) -> Path:
    root = bundle_root(path)
    document = load_document(root)
    report = audit_bundle(root)
    destination = Path(output).expanduser().resolve()
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)

    run = document["run"]
    graph: list[dict[str, Any]] = [
        {"@id": "ro-crate-metadata.json", "@type": "CreativeWork", "about": {"@id": "./"}, "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"}},
        {"@id": "./", "@type": "Dataset", "name": run.get("title", run.get("id", "FEVKit run")), "description": run.get("objective", ""), "conformsTo": [{"@id": "https://w3id.org/ro/crate/1.1"}, {"@id": PROCESS_RUN_PROFILE}], "hasPart": [], "fevkit:computedStage": report.computed_stage, "fevkit:qualifiers": report.qualifiers},
    ]
    root_node = graph[1]

    for collection in ("inputs", "artifacts"):
        for item in run.get(collection, []):
            relative = item["path"]
            source = safe_path(root, relative)
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            root_node["hasPart"].append({"@id": relative})
            graph.append({"@id": relative, "@type": "File", "name": item.get("id", Path(relative).name), "encodingFormat": item.get("media_type"), "sha256": item.get("sha256")})

    shutil.copy2(root / "run.json", destination / "run.json")
    root_node["hasPart"].append({"@id": "run.json"})
    graph.append({"@id": "run.json", "@type": "File", "name": "FEVKit run manifest", "encodingFormat": "application/json"})

    software_ids = []
    for step in run.get("steps", []):
        tool = step.get("tool")
        if not isinstance(tool, dict) or not tool.get("name"):
            continue
        software_id = f"#tool-{step['id']}"
        software_ids.append({"@id": software_id})
        graph.append({"@id": software_id, "@type": "SoftwareApplication", "name": tool["name"], "softwareVersion": tool.get("version")})

    graph.append({"@id": "#run", "@type": "CreateAction", "name": run.get("title", run.get("id")), "startTime": run.get("started_at"), "endTime": run.get("completed_at"), "instrument": software_ids, "object": [{"@id": item["path"]} for item in run.get("inputs", [])], "result": [{"@id": item["path"]} for item in run.get("artifacts", [])], "actionStatus": "http://schema.org/CompletedActionStatus" if run.get("status") == "completed" else "http://schema.org/PotentialActionStatus"})

    metadata = {"@context": [RO_CRATE_CONTEXT, {"fevkit": "https://fevkit.vercel.app/ns#", "sha256": "https://w3id.org/ro/terms/sha256"}], "@graph": graph}
    (destination / "ro-crate-metadata.json").write_text(canonical_json(metadata), encoding="utf-8")
    (destination / "fevkit-audit.json").write_text(canonical_json(report.to_dict()), encoding="utf-8")
    return destination
