"""Crypto logic for operational state SHA-256 generation."""

import hashlib
import json
from typing import Any


def generate_state_hash(data: dict[str, Any]) -> str:
    """Generates a deterministic SHA-256 hash from a dictionary representation."""
    canonical_bytes = json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical_bytes).hexdigest()