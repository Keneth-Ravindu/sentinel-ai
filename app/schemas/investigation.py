from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.investigation import (
    InvestigationSignal,
)
from app.schemas.simulator import (
    DeploymentResponse,
    LogEntryResponse,
    ServiceHealthResponse,
)


class InvestigationResponse(BaseModel):
    incident_id: UUID
    service: str
    collected_at: datetime
    health: ServiceHealthResponse
    logs: list[LogEntryResponse]
    deployments: list[DeploymentResponse]
    signals: list[InvestigationSignal]