#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict
from ruamel.yaml import YAML


class SubsystemState(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    entity: str
    active_state: str
    substates: dict[str, Any]


class SiteState(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    canonical_state: str


class OperationalStateDeclaration(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    version: str
    timestamp: str
    site: SiteState
    subsystems: dict[str, SubsystemState]


def compute_canonical_sha256(
    state: OperationalStateDeclaration,
) -> str:
    data = state.model_dump(exclude={"timestamp"})
    canonical = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def process_manifest(file_path: Path) -> Optional[str]:
    if not file_path.is_file():
        raise FileNotFoundError(f"Manifest not found: {file_path}")

    yaml = YAML(typ="safe")

    with file_path.open("r", encoding="utf-8") as file:
        data = yaml.load(file)

    state = OperationalStateDeclaration.model_validate(data)

    return compute_canonical_sha256(state)


def main() -> int:
    manifest_file = (
        Path(__file__).resolve().parent.parent / "manifests" / "instrumentation.yaml"
    )

    try:
        sha256_hash = process_manifest(manifest_file)

        print("=" * 60)
        print(" AstroGit-OS — Lineage SHA-256 State Verification")
        print("=" * 60)
        print(f" Target File  : {manifest_file.name}")
        print(f" Schema       : {sha256_hash}")
        print(f" State SHA-256: {sha256_hash}")
        print("=" * 60)

        return 0

    except Exception as err:
        print(f"[ERROR] Failed to compute state lineage hash: {err}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
