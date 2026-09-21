from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import (
    get_operations_simulator,
)
from app.main import app
from app.simulator.operations_simulator import (
    OperationsSimulator,
)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    simulator = OperationsSimulator()

    app.dependency_overrides[
        get_operations_simulator
    ] = lambda: simulator

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_get_payment_service_health(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/simulator/services/"
        "payment-service/health"
    )

    assert response.status_code == 200

    health = response.json()

    assert health["status"] == "healthy"
    assert health["active_provider"] == "GlobalPay"


def test_trigger_provider_degradation(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/simulator/scenarios/"
        "provider-degradation"
    )

    assert response.status_code == 200

    health = response.json()["service_health"]

    assert health["status"] == "degraded"
    assert health["error_rate"] == 19.8


def test_switch_provider_recovers_service(
    client: TestClient,
) -> None:
    client.post(
        "/api/v1/simulator/scenarios/"
        "provider-degradation"
    )

    response = client.post(
        "/api/v1/simulator/actions/"
        "switch-provider"
    )

    assert response.status_code == 200

    health = response.json()["service_health"]

    assert health["status"] == "healthy"
    assert health["active_provider"] == "PayFlow"


def test_switch_provider_while_healthy_returns_conflict(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/simulator/actions/"
        "switch-provider"
    )

    assert response.status_code == 409


def test_reset_restores_initial_state(
    client: TestClient,
) -> None:
    client.post(
        "/api/v1/simulator/scenarios/"
        "provider-degradation"
    )

    client.post(
        "/api/v1/simulator/reset"
    )

    response = client.get(
        "/api/v1/simulator/services/"
        "payment-service/health"
    )

    health = response.json()

    assert health["status"] == "healthy"
    assert health["active_provider"] == "GlobalPay"