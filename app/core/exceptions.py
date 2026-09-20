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