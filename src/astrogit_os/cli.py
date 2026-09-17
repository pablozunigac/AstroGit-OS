"""Main entry point CLI execution script."""

import sys
from pathlib import Path
import yaml

from astrogit_os.models import InstrumentationSpec
from astrogit_os.hashing import generate_state_hash


def main() -> None:
    manifest_path = Path("manifests/instrumentation.yaml")
    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        raw_data = yaml.safe_load(f)

    # Validate model
    spec = InstrumentationSpec(**raw_data)
    
    # Generate SHA-256 state hash
    state_hash = generate_state_hash(raw_data)
    
    print(f"Site Loaded: {spec.site.id} [{spec.site.canonical_state}]")
    print(f"State Lineage Hash (SHA-256): {state_hash}")


if __name__ == "__main__":
    main()