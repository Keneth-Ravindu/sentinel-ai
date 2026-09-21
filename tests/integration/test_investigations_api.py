from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import (
    get_incident_service,
    get_investigation_service,
    get_operations_simulator,
)
from app.main import app
from app.repositories.incident_repository import (
    InMemoryIncidentRepository,
)
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


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
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

    app.dependency_overrides[
        get_incident_service
    ] = lambda: incident_service

    app.dependency_overrides[
        get_operations_simulator
    ] = lambda: simulator

    app.dependency_overrides[
        get_investigation_service
    ] = lambda: investigation_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_investigate_provider_degradation(
    client: TestClient,
) -> None:
    client.post(
        "/api/v1/simulator/scenarios/"
        "provider-degradation"
    )

    create_response = client.post(
        "/api/v1/incidents",
        json={
            "service": "payment-service",
            "severity": "SEV-1",
            "description": (
                "Payment authorization failures "
                "detected during peak traffic."
            ),
            "error_rate": 19.8,
            "p95_latency_ms": 5200,
        },
    )

    incident_id = create_response.json()["id"]

    response = client.post(
        f"/api/v1/incidents/"
        f"{incident_id}/investigations"
    )

    assert response.status_code == 201

    investigation = response.json()

    assert (
        investigation["service"]
        == "payment-service"
    )

    assert (
        investigation["health"]["status"]
        == "degraded"
    )

    assert (
        "payment_provider_timeout_detected"
        in investigation["signals"]
    )

    assert (
        "high_error_rate"
        in investigation["signals"]
    )