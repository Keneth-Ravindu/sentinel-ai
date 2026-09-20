import pytest

from app.core.exceptions import (
    InvalidIncidentTransitionError,
)
from app.models.incident import (
    IncidentSeverity,
    IncidentStatus,
)
from app.repositories.incident_repository import (
    InMemoryIncidentRepository,
)
from app.schemas.incident import IncidentCreate
from app.services.incident_service import IncidentService


def create_service() -> IncidentService:
    repository = InMemoryIncidentRepository()

    return IncidentService(
        repository=repository
    )


def create_incident_data() -> IncidentCreate:
    return IncidentCreate(
        service="payment-service",
        severity=IncidentSeverity.SEV1,
        description=(
            "Payment authorization failures "
            "detected during peak traffic."
        ),
        error_rate=19.8,
        p95_latency_ms=5200,
    )


def test_create_incident_starts_open() -> None:
    service = create_service()

    incident = service.create_incident(
        create_incident_data()
    )

    assert incident.status == IncidentStatus.OPEN
    assert incident.service == "payment-service"
    assert incident.error_rate == 19.8


def test_valid_status_transition() -> None:
    service = create_service()

    incident = service.create_incident(
        create_incident_data()
    )

    updated_incident = service.update_status(
        incident_id=incident.id,
        target_status=IncidentStatus.INVESTIGATING,
    )

    assert (
        updated_incident.status
        == IncidentStatus.INVESTIGATING
    )


def test_invalid_status_transition_is_rejected() -> None:
    service = create_service()

    incident = service.create_incident(
        create_incident_data()
    )

    with pytest.raises(
        InvalidIncidentTransitionError
    ):
        service.update_status(
            incident_id=incident.id,
            target_status=IncidentStatus.RESOLVED,
        )