import pytest

from app.core.exceptions import (
    InvalidSimulatorActionError,
)
from app.models.simulator import (
    PaymentProvider,
    ServiceStatus,
)
from app.simulator.operations_simulator import (
    PAYMENT_SERVICE,
    OperationsSimulator,
)


def test_payment_service_starts_healthy() -> None:
    simulator = OperationsSimulator()

    health = simulator.get_service_health(
        PAYMENT_SERVICE
    )

    assert health.status == ServiceStatus.HEALTHY
    assert health.error_rate == 0.4
    assert (
        health.active_provider
        == PaymentProvider.GLOBALPAY
    )


def test_provider_degradation_changes_health() -> None:
    simulator = OperationsSimulator()

    health = (
        simulator.trigger_provider_degradation()
    )

    assert health.status == ServiceStatus.DEGRADED
    assert health.error_rate == 19.8
    assert health.p95_latency_ms == 5200


def test_provider_degradation_creates_error_logs() -> None:
    simulator = OperationsSimulator()

    simulator.trigger_provider_degradation()

    logs = simulator.get_logs(
        PAYMENT_SERVICE
    )

    messages = [
        log.message
        for log in logs
    ]

    assert any(
        "PaymentProviderTimeout" in message
        for message in messages
    )


def test_provider_failover_recovers_service() -> None:
    simulator = OperationsSimulator()

    simulator.trigger_provider_degradation()

    health = simulator.switch_to_backup_provider()

    assert health.status == ServiceStatus.HEALTHY
    assert health.error_rate == 0.8
    assert (
        health.active_provider
        == PaymentProvider.PAYFLOW
    )


def test_provider_failover_requires_degradation() -> None:
    simulator = OperationsSimulator()

    with pytest.raises(
        InvalidSimulatorActionError
    ):
        simulator.switch_to_backup_provider()