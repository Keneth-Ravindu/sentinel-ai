from datetime import UTC, datetime, timedelta

from app.core.exceptions import (
    InvalidSimulatorActionError,
    ServiceNotFoundError,
)
from app.models.simulator import (
    DeploymentRecord,
    LogEntry,
    LogLevel,
    PaymentProvider,
    ServiceHealth,
    ServiceStatus,
)

PAYMENT_SERVICE = "payment-service"


class OperationsSimulator:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        now = datetime.now(UTC)

        self._health = {
            PAYMENT_SERVICE: ServiceHealth(
                service=PAYMENT_SERVICE,
                status=ServiceStatus.HEALTHY,
                cpu_percent=43.2,
                memory_percent=51.8,
                error_rate=0.4,
                p95_latency_ms=380,
                database_latency_ms=36,
                active_provider=PaymentProvider.GLOBALPAY,
            )
        }

        self._logs = {
            PAYMENT_SERVICE: [
                LogEntry(
                    timestamp=now,
                    level=LogLevel.INFO,
                    service=PAYMENT_SERVICE,
                    message=(
                        "Payment service operating normally "
                        "with provider GlobalPay."
                    ),
                )
            ]
        }

        self._deployments = {
            PAYMENT_SERVICE: [
                DeploymentRecord(
                    version="2.8.1",
                    deployed_at=now - timedelta(hours=6),
                    status="successful",
                ),
                DeploymentRecord(
                    version="2.8.0",
                    deployed_at=now - timedelta(days=5),
                    status="successful",
                ),
            ]
        }

    def get_service_health(
        self,
        service: str,
    ) -> ServiceHealth:
        health = self._health.get(service)

        if health is None:
            raise ServiceNotFoundError(service)

        return health.model_copy(deep=True)

    def get_logs(
        self,
        service: str,
    ) -> list[LogEntry]:
        if service not in self._logs:
            raise ServiceNotFoundError(service)

        return [
            log.model_copy(deep=True)
            for log in self._logs[service]
        ]

    def get_deployments(
        self,
        service: str,
    ) -> list[DeploymentRecord]:
        if service not in self._deployments:
            raise ServiceNotFoundError(service)

        return [
            deployment.model_copy(deep=True)
            for deployment in self._deployments[service]
        ]

    def trigger_provider_degradation(
        self,
    ) -> ServiceHealth:
        current = self._health[PAYMENT_SERVICE]

        if current.status == ServiceStatus.DEGRADED:
            return current.model_copy(deep=True)

        degraded_health = current.model_copy(
            update={
                "status": ServiceStatus.DEGRADED,
                "cpu_percent": 45.8,
                "memory_percent": 52.1,
                "error_rate": 19.8,
                "p95_latency_ms": 5200,
                "database_latency_ms": 39,
            }
        )

        self._health[PAYMENT_SERVICE] = degraded_health

        now = datetime.now(UTC)

        self._logs[PAYMENT_SERVICE].extend(
            [
                LogEntry(
                    timestamp=now,
                    level=LogLevel.ERROR,
                    service=PAYMENT_SERVICE,
                    message=(
                        "PaymentProviderTimeout: "
                        "GlobalPay request exceeded "
                        "2000ms timeout."
                    ),
                ),
                LogEntry(
                    timestamp=now,
                    level=LogLevel.ERROR,
                    service=PAYMENT_SERVICE,
                    message=(
                        "PaymentProviderTimeout: "
                        "provider=GlobalPay."
                    ),
                ),
                LogEntry(
                    timestamp=now,
                    level=LogLevel.WARN,
                    service=PAYMENT_SERVICE,
                    message=(
                        "Circuit breaker failure count=37."
                    ),
                ),
            ]
        )

        return degraded_health.model_copy(deep=True)

    def switch_to_backup_provider(
        self,
    ) -> ServiceHealth:
        current = self._health[PAYMENT_SERVICE]

        if current.status != ServiceStatus.DEGRADED:
            raise InvalidSimulatorActionError(
                "Provider failover is only permitted "
                "while the payment service is degraded."
            )

        recovered_health = current.model_copy(
            update={
                "status": ServiceStatus.HEALTHY,
                "cpu_percent": 44.1,
                "memory_percent": 51.4,
                "error_rate": 0.8,
                "p95_latency_ms": 490,
                "database_latency_ms": 37,
                "active_provider": PaymentProvider.PAYFLOW,
            }
        )

        self._health[PAYMENT_SERVICE] = recovered_health

        self._logs[PAYMENT_SERVICE].append(
            LogEntry(
                timestamp=datetime.now(UTC),
                level=LogLevel.INFO,
                service=PAYMENT_SERVICE,
                message=(
                    "Payment traffic switched from "
                    "GlobalPay to PayFlow. "
                    "Service health recovered."
                ),
            )
        )

        return recovered_health.model_copy(deep=True)

# This is the heart of the simulator.