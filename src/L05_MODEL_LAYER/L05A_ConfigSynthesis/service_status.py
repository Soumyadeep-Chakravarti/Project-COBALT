# L05_MODEL_LAYER/L05A_ConfigSynthesis/service_status.py

from typing import Dict

from pydantic import BaseModel, Field


class ServiceStatus(BaseModel):
    """
    Standardized health and readiness check for all COBALT microservices.
    Used by L03B Gateway for system health monitoring.
    """

    service_name: str = Field(
        ...,
        description="The unique name of the service (e.g., L02A_HostExecutionCore).",
    )
    health_status: str = Field(
        ..., description="Overall health: OK, DEGRADED, or CRITICAL."
    )
    last_check: str = Field(
        ..., description="Timestamp of the last check (ISO format)."
    )
    details: Dict[str, str] = Field(
        default={},
        description="Optional metrics or details (e.g., Uptime, Memory Usage).",
    )
