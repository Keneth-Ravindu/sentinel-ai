from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import get_incident_service
from app.main import app
from app.repositories.incident_repository import (
    InMemoryIncidentRepository,
)
from app.services.incident_service import IncidentService


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    repository = InMemoryIncidentRepository()

    service = IncidentService(
        repository=repository
    )

    app.dependency_overrides[
        get_incident_service
    ] = lambda: service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_create_incident(
    client: TestClient,
) -> None:
    response = client.post(
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

    assert response.status_code == 201

    incident = response.json()

    assert incident["service"] == "payment-service"
    assert incident["status"] == "OPEN"
    assert incident["severity"] == "SEV-1"


def test_invalid_error_rate_is_rejected(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/incidents",
        json={
            "service": "payment-service",
            "severity": "SEV-1",
            "description": (
                "Payment authorization failures "
                "detected during peak traffic."
            ),
            "error_rate": 150,
            "p95_latency_ms": 5200,
        },
    )

    assert response.status_code == 422


def test_incident_status_transition(
    client: TestClient,
) -> None:
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

    response = client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={
            "status": "INVESTIGATING",
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "INVESTIGATING"
    )


def test_invalid_status_transition_returns_conflict(
    client: TestClient,
) -> None:
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

    response = client.patch(
        f"/api/v1/incidents/{incident_id}/status",
        json={
            "status": "RESOLVED",
        },
    )

    assert response.status_code == 409