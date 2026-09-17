"""AstroGit-OS: Declarative architecture and operational lineage for astronomical instrumentation."""

__version__ = "0.2.0"

from .hashing import generate_state_hash
from .models import InstrumentationSpec
from .reconciliation import reconcile_states

__all__ = ["InstrumentationSpec", "generate_state_hash", "reconcile_states"]
