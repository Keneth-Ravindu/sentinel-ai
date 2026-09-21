from datetime import UTC, datetime, timedelta
from uuid import UUID

from app.core.exceptions import (
    InvestigationNotAllowedError,
)
from app.models.incident import IncidentStatus
from app.models.investigation import (
    Investigation,
    InvestigationSignal,
)
from app.models.simulator import (
    DeploymentRecord,
    LogEntry,
    ServiceHealth,
)
from app.services.incident_service import IncidentService
from app.tools.deployments_tool import (
    GetRecentDeploymentsTool,
)
from app.tools.logs_tool import GetRecentLogsTool
from app.tools.service_health_tool import (
    GetServiceHealthTool,
)


class InvestigationService:
    def __init__(
        self,
        incident_service: IncidentService,
        health_tool: GetServiceHealthTool,
        logs_tool: GetRecentLogsTool,
        deployments_tool: GetRecentDeploymentsTool,
    ) -> None:
        self.incident_service = incident_service
        self.health_tool = health_tool
        self.logs_tool = logs_tool
        self.deployments_tool = deployments_tool

    def investigate(
        self,
        incident_id: UUID,
    ) -> Investigation:
        incident = self.incident_service.get_incident(
            incident_id
        )

        if incident.status == IncidentStatus.OPEN:
            incident = (
                self.incident_service.update_status(
                    incident_id=incident.id,
                    target_status=(
                        IncidentStatus.INVESTIGATING
                    ),
                )
            )

        elif (
            incident.status
            != IncidentStatus.INVESTIGATING
        ):
            raise InvestigationNotAllowedError(
                incident_id=incident.id,
                status=incident.status.value,
            )

        health = self.health_tool.execute(
            incident.service
        )

        logs = self.logs_tool.execute(
            incident.service
        )

        deployments = self.deployments_tool.execute(
            incident.service
        )

        signals = self._extract_signals(
            health=health,
            logs=logs,
            deployments=deployments,
        )

        return Investigation(
            incident_id=incident.id,
            service=incident.service,
            collected_at=datetime.now(
                UTC
            ),
            health=health,
            logs=logs,
            deployments=deployments,
            signals=signals,
        )

    def _extract_signals(
        self,
        health: ServiceHealth,
        logs: list[LogEntry],
        deployments: list[DeploymentRecord],
    ) -> list[InvestigationSignal]:
        signals: list[InvestigationSignal] = []

        if health.error_rate >= 5:
            signals.append(
                InvestigationSignal.HIGH_ERROR_RATE
            )

        if health.p95_latency_ms >= 2000:
            signals.append(
                InvestigationSignal.HIGH_P95_LATENCY
            )

        if health.cpu_percent < 80:
            signals.append(
                InvestigationSignal.CPU_WITHIN_NORMAL_RANGE
            )

        if health.memory_percent < 80:
            signals.append(
                InvestigationSignal.MEMORY_WITHIN_NORMAL_RANGE
            )

        if health.database_latency_ms < 100:
            signals.append(
                InvestigationSignal.
                DATABASE_LATENCY_WITHIN_NORMAL_RANGE
            )

        messages = [
            log.message.lower()
            for log in logs
        ]

        if any(
            "paymentprovidertimeout" in message
            for message in messages
        ):
            signals.append(
                InvestigationSignal.
                PAYMENT_PROVIDER_TIMEOUT_DETECTED
            )

        if any(
            "circuit breaker" in message
            for message in messages
        ):
            signals.append(
                InvestigationSignal.
                CIRCUIT_BREAKER_WARNING_DETECTED
            )

        recent_threshold = (
            datetime.now(UTC)
            - timedelta(hours=24)
        )

        if any(
            deployment.deployed_at
            >= recent_threshold
            for deployment in deployments
        ):
            signals.append(
                InvestigationSignal.
                RECENT_DEPLOYMENT_DETECTED
            )

        return signals