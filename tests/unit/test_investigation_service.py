from app.models.incident import (
    IncidentSeverity,
    IncidentStatus,
)
from app.models.investigation import (
    InvestigationSignal,
)
from app.repositories.incident_repository import (
    InMemoryIncidentRepository,
)
from app.schemas.incident import IncidentCreate
from app.services.incident_service import (
    IncidentService,
)
from app.services.investigation_service import (
    InvestigationService,
)
from app.simulator.operations_simulator import (
    OperationsSimulator,
)
from app.tools.deployments_tool import (
    GetRecentDeploymentsTool,
)
from app.tools.logs_tool import GetRecentLogsTool
from app.tools.service_health_tool import (
    GetServiceHealthTool,
)


def build_investigation_service() -> tuple[
    InvestigationService,
    IncidentService,
    OperationsSimulator,
]:
    repository = InMemoryIncidentRepository()

    incident_service = IncidentService(
        repository=repository
    )

    simulator = OperationsSimulator()

    investigation_service = InvestigationService(
        incident_service=incident_service,
        health_tool=GetServiceHealthTool(
            simulator
        ),
        logs_tool=GetRecentLogsTool(
            simulator
        ),
        deployments_tool=(
            GetRecentDeploymentsTool(
                simulator
            )
        ),
    )

    return (
        investigation_service,
        incident_service,
        simulator,
    )


def test_investigation_collects_failure_evidence() -> None:
    (
        investigation_service,
        incident_service,
        simulator,
    ) = build_investigation_service()

    simulator.trigger_provider_degradation()

    incident = incident_service.create_incident(
        IncidentCreate(
            service="payment-service",
            severity=IncidentSeverity.SEV1,
            description=(
                "Payment authorization failures "
                "detected during peak traffic."
            ),
            error_rate=19.8,
            p95_latency_ms=5200,
        )
    )

    investigation = (
        investigation_service.investigate(
            incident.id
        )
    )

    assert (
        InvestigationSignal.HIGH_ERROR_RATE
        in investigation.signals
    )

    assert (
        InvestigationSignal.
        PAYMENT_PROVIDER_TIMEOUT_DETECTED
        in investigation.signals
    )

    assert (
        InvestigationSignal.
        DATABASE_LATENCY_WITHIN_NORMAL_RANGE
        in investigation.signals
    )


def test_investigation_changes_open_incident_status() -> None:
    (
        investigation_service,
        incident_service,
        simulator,
    ) = build_investigation_service()

    simulator.trigger_provider_degradation()

    incident = incident_service.create_incident(
        IncidentCreate(
            service="payment-service",
            severity=IncidentSeverity.SEV1,
            description=(
                "Payment authorization failures "
                "detected during peak traffic."
            ),
            error_rate=19.8,
            p95_latency_ms=5200,
        )
    )

    investigation_service.investigate(
        incident.id
    )

    updated_incident = (
        incident_service.get_incident(
            incident.id
        )
    )

    assert (
        updated_incident.status
        == IncidentStatus.INVESTIGATING
    )