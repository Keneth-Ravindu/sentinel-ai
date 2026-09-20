from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.incident import IncidentSeverity, IncidentStatus


class IncidentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    service: str = Field(
        min_length=2,
        max_length=120,
    )

    severity: IncidentSeverity

    description: str = Field(
        min_length=10,
        max_length=2000,
    )

    error_rate: float = Field(
        ge=0,
        le=100,
    )

    p95_latency_ms: float = Field(
        ge=0,
    )


class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus


class IncidentResponse(BaseModel):
    id: UUID
    service: str
    severity: IncidentSeverity
    status: IncidentStatus
    description: str
    error_rate: float
    p95_latency_ms: float
    created_at: datetime
    updated_at: datetime

# Incident = internal domain object
# IncidentCreate = incoming API request
# IncidentStatusUpdate = status-changing request
# IncidentResponse = public API response
# That's healthier than making one model responsible for everything.