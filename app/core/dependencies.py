from app.repositories.incident_repository import (
    InMemoryIncidentRepository,
)
from app.services.incident_service import IncidentService

incident_repository = InMemoryIncidentRepository()

incident_service = IncidentService(
    repository=incident_repository
)


def get_incident_service() -> IncidentService:
    return incident_service