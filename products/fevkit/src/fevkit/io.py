from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class BundleError(ValueError):
    """Raised when a bundle path or document is unsafe or unreadable."""


def bundle_root(path: str | Path) -> Path:
    root = Path(path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise BundleError(f"Bundle directory does not exist: {root}")
    return root


def manifest_path(root: Path) -> Path:
    candidate = root / "run.json"
    if not candidate.is_file():
        raise BundleError(f"Bundle does not contain run.json: {root}")
    return candidate


def load_document(root: Path) -> dict[str, Any]:
    try:
        value = json.loads(manifest_path(root).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise BundleError(f"run.json is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise BundleError("run.json must contain a JSON object")
    return value


def safe_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise BundleError("Declared path must be a non-empty string")
    declared = Path(relative)
    if declared.is_absolute():
        raise BundleError(f"Absolute paths are not allowed: {relative}")
    resolved = (root / declared).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise BundleError(f"Path escapes bundle root: {relative}") from exc
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
