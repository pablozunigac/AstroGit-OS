"""Engine for comparing observed state against desired state baseline."""

from typing import Dict, Any, Tuple


def reconcile_states(observed: Dict[str, Any], desired: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
    """Compares observed vs desired state. Returns (is_synced, diff)."""
    diff = {}
    is_synced = True
    
    # Basic reconciliation logic
    for key, val in desired.items():
        if key not in observed or observed[key] != val:
            is_synced = False
            diff[key] = {"observed": observed.get(key), "desired": val}
            
    return is_synced, diff