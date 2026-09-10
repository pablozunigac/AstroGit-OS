#!/usr/bin/env python3
"""
AstroGit-OS --- Proof of Concept 001: Deterministic Lineage State SHA-256 Generator
Standard: Modern Python 3.12+ / Pydantic v2 (2026 Stable Standard)
License: MIT
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict
from ruamel.yaml import YAML


class SubsystemState(BaseModel):
    """Schema model for individual subsystem states."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    entity: str
    active_state: str
    substates: dict[str, Any]


class SiteState(BaseModel):
    """Schema model for site-level metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str
    canonical_state: str


class OperationalStateDeclaration(BaseModel):
    """
    Core AstroGit-OS Declarative State Model.
    Excludes mutable telemetry timestamps during cryptographic hashing.
    """

    model_config = ConfigDict(frozen=True, extra="ignore")

    version: str
    site: SiteState
    subsystems: dict[str, SubsystemState]


def compute_canonical_sha256(state_declaration: OperationalStateDeclaration) -> str:
    """
    Computes a deterministic SHA-256 fingerprint of the operational state.
    Uses JSON canonicalization (sorted keys, no whitespace) to ensure immutability
    across different YAML parsers or key orders.
    """
    raw_dict = state_declaration.model_dump()

    canonical_json = json.dumps(
        raw_dict, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )

    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def process_manifest(file_path: Path) -> str | None:
    """Loads a YAML declarative state file and computes its SHA-256 lineage hash."""
    if not file_path.exists():
        raise FileNotFoundError(f"Manifest not found: {file_path}")

    yaml = YAML(typ="safe")
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.load(f)

    validated_state = OperationalStateDeclaration(**data)
    return compute_canonical_sha256(validated_state)


if __name__ == "__main__":
    manifest_file = (
        Path(__file__).resolve().parent.parent / "manifests" / "instrumentation.yaml"
    )

    try:
        calculated_hash = process_manifest(manifest_file)
        print("=" * 60)
        print(" AstroGit-OS --- Lineage SHA-256 State Verification")
        print("=" * 60)
        print(f" Target File  : {manifest_file.name}")
        print(f" Timestamp    : {datetime.now(timezone.utc).isoformat()}")
        print(f" State SHA-256: {calculated_hash}")
        print("=" * 60)
    except Exception as err:
        print(f"[ERROR] Failed to compute state lineage hash: {err}")
