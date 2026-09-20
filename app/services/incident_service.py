from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.core.exceptions import (
    IncidentNotFoundError,
    InvalidIncidentTransitionError,
)
from app.models.incident import Incident, IncidentStatus
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate

ALLOWED_STATUS_TRANSITIONS: dict[
    IncidentStatus,
    set[IncidentStatus],
] = {
    IncidentStatus.OPEN: {
        IncidentStatus.INVESTIGATING,
    },
    IncidentStatus.INVESTIGATING: {
        IncidentStatus.MITIGATING,
        IncidentStatus.RESOLVED,
    },
    IncidentStatus.MITIGATING: {
        IncidentStatus.RESOLVED,
    },
    IncidentStatus.RESOLVED: set(),
}


class IncidentService:
    def __init__(
        self,
        repository: IncidentRepository,
    ) -> None:
        self.repository = repository

    def create_incident(
        self,
        incident_data: IncidentCreate,
    ) -> Incident:
        now = datetime.now(UTC)

        incident = Incident(
            id=uuid4(),
            service=incident_data.service,
            severity=incident_data.severity,
            status=IncidentStatus.OPEN,
            description=incident_data.description,
            error_rate=incident_data.error_rate,
            p95_latency_ms=incident_data.p95_latency_ms,
            created_at=now,
            updated_at=now,
        )

        return self.repository.create(incident)

    def get_incident(
        self,
        incident_id: UUID,
    ) -> Incident:
        incident = self.repository.get_by_id(
            incident_id
        )

        if incident is None:
            raise IncidentNotFoundError(
                incident_id
            )

        return incident

    def list_incidents(
        self,
    ) -> list[Incident]:
        return self.repository.list_all()

    def update_status(
        self,
        incident_id: UUID,
        target_status: IncidentStatus,
    ) -> Incident:
        incident = self.get_incident(
            incident_id
        )

        if incident.status == target_status:
            return incident

        allowed_transitions = (
            ALLOWED_STATUS_TRANSITIONS[
                incident.status
            ]
        )

        if target_status not in allowed_transitions:
            raise InvalidIncidentTransitionError(
                current_status=incident.status,
                target_status=target_status,
            )

        updated_incident = incident.model_copy(
            update={
                "status": target_status,
                "updated_at": datetime.now(
                    UTC
                ),
            }
        )

        return self.repository.update(
            updated_incident
        )