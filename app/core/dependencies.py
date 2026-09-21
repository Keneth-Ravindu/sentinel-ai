from app.repositories.incident_repository import (
    InMemoryIncidentRepository,
)
from app.services.incident_service import IncidentService
from app.simulator.operations_simulator import OperationsSimulator

incident_repository = InMemoryIncidentRepository()

incident_service = IncidentService(
    repository=incident_repository
)


def get_incident_service() -> IncidentService:
    return incident_service


operations_simulator = OperationsSimulator()


def get_operations_simulator() -> OperationsSimulator:
    return operations_simulator

