from typing import Protocol
from uuid import UUID

from app.models.incident import Incident


class IncidentRepository(Protocol):
    def create(
        self,
        incident: Incident,
    ) -> Incident:
        ...

    def get_by_id(
        self,
        incident_id: UUID,
    ) -> Incident | None:
        ...

    def list_all(
        self,
    ) -> list[Incident]:
        ...

    def update(
        self,
        incident: Incident,
    ) -> Incident:
        ...


class InMemoryIncidentRepository:
    def __init__(self) -> None:
        self._incidents: dict[UUID, Incident] = {}

    def create(
        self,
        incident: Incident,
    ) -> Incident:
        self._incidents[incident.id] = incident

        return incident.model_copy(deep=True)

    def get_by_id(
        self,
        incident_id: UUID,
    ) -> Incident | None:
        incident = self._incidents.get(incident_id)

        if incident is None:
            return None

        return incident.model_copy(deep=True)

    def list_all(
        self,
    ) -> list[Incident]:
        incidents = sorted(
            self._incidents.values(),
            key=lambda incident: incident.created_at,
            reverse=True,
        )

        return [
            incident.model_copy(deep=True)
            for incident in incidents
        ]

    def update(
        self,
        incident: Incident,
    ) -> Incident:
        self._incidents[incident.id] = incident

        return incident.model_copy(deep=True)