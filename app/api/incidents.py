from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.core.dependencies import get_incident_service
from app.core.exceptions import (
    IncidentNotFoundError,
    InvalidIncidentTransitionError,
)
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentStatusUpdate,
)
from app.services.incident_service import IncidentService

router = APIRouter(
    prefix="/api/v1/incidents",
    tags=["Incidents"],
)


IncidentServiceDependency = Annotated[
    IncidentService,
    Depends(get_incident_service),
]


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    incident_data: IncidentCreate,
    service: IncidentServiceDependency,
) -> IncidentResponse:
    incident = service.create_incident(
        incident_data
    )

    return IncidentResponse(
        **incident.model_dump()
    )


@router.get(
    "",
    response_model=list[IncidentResponse],
)
def list_incidents(
    service: IncidentServiceDependency,
) -> list[IncidentResponse]:
    incidents = service.list_incidents()

    return [
        IncidentResponse(
            **incident.model_dump()
        )
        for incident in incidents
    ]


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def get_incident(
    incident_id: UUID,
    service: IncidentServiceDependency,
) -> IncidentResponse:
    try:
        incident = service.get_incident(
            incident_id
        )

    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return IncidentResponse(
        **incident.model_dump()
    )


@router.patch(
    "/{incident_id}/status",
    response_model=IncidentResponse,
)
def update_incident_status(
    incident_id: UUID,
    status_update: IncidentStatusUpdate,
    service: IncidentServiceDependency,
) -> IncidentResponse:
    try:
        incident = service.update_status(
            incident_id=incident_id,
            target_status=status_update.status,
        )

    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except InvalidIncidentTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return IncidentResponse(
        **incident.model_dump()
    )