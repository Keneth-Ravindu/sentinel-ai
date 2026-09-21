from app.repositories.incident_repository import (
    InMemoryIncidentRepository,
)
from app.services.incident_service import IncidentService
from app.services.investigation_service import (
    InvestigationService,
)
from app.simulator.operations_simulator import OperationsSimulator
from app.tools.deployments_tool import (
    GetRecentDeploymentsTool,
)
from app.tools.logs_tool import GetRecentLogsTool
from app.tools.service_health_tool import (
    GetServiceHealthTool,
)

incident_repository = InMemoryIncidentRepository()

incident_service = IncidentService(
    repository=incident_repository
)


def get_incident_service() -> IncidentService:
    return incident_service


operations_simulator = OperationsSimulator()


def get_operations_simulator() -> OperationsSimulator:
    return operations_simulator

service_health_tool = GetServiceHealthTool(
    simulator=operations_simulator
)

recent_logs_tool = GetRecentLogsTool(
    simulator=operations_simulator
)

recent_deployments_tool = GetRecentDeploymentsTool(
    simulator=operations_simulator
)


investigation_service = InvestigationService(
    incident_service=incident_service,
    health_tool=service_health_tool,
    logs_tool=recent_logs_tool,
    deployments_tool=recent_deployments_tool,
)


def get_investigation_service() -> InvestigationService:
    return investigation_service

