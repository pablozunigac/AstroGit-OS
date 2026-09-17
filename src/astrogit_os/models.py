"""Data models for validating declarative state manifests."""

from typing import Any

from pydantic import BaseModel


class SubstateSpec(BaseModel):
    """Substates of a subsystem."""

    model_config = {"extra": "allow"}


class SubsystemSpec(BaseModel):
    """Subsystem status specification."""

    entity: str
    active_state: str
    substates: dict[str, Any]


class SiteSpec(BaseModel):
    """Observatory site specification."""

    id: str
    canonical_state: str


class InstrumentationSpec(BaseModel):
    """Root model for instrumentation.yaml."""

    version: str
    timestamp: str
    site: SiteSpec
    subsystems: dict[str, SubsystemSpec]
