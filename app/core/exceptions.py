from uuid import UUID

from app.models.incident import IncidentStatus


class IncidentNotFoundError(Exception):
    def __init__(self, incident_id: UUID) -> None:
        self.incident_id = incident_id

        super().__init__(
            f"Incident '{incident_id}' was not found."
        )


class InvalidIncidentTransitionError(Exception):
    def __init__(
        self,
        current_status: IncidentStatus,
        target_status: IncidentStatus,
    ) -> None:
        self.current_status = current_status
        self.target_status = target_status

        super().__init__(
            "Invalid incident status transition: "
            f"{current_status.value} -> {target_status.value}"
        )

# This is better than having business logic throw HTTP exceptions.
# Our domain/service layer should not know that FastAPI even exists.

class ServiceNotFoundError(Exception):
    def __init__(self, service: str) -> None:
        self.service = service

        super().__init__(
            f"Service '{service}' was not found."
        )


class InvalidSimulatorActionError(Exception):
    pass


class InvestigationNotAllowedError(Exception):
    def __init__(
        self,
        incident_id: UUID,
        status: str,
    ) -> None:
        self.incident_id = incident_id
        self.status = status

        super().__init__(
            "Investigation cannot be started for "
            f"incident '{incident_id}' while its "
            f"status is '{status}'."
        )