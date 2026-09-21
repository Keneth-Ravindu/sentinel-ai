from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.core.dependencies import (
    get_investigation_service,
)
from app.core.exceptions import (
    IncidentNotFoundError,
    InvestigationNotAllowedError,
    ServiceNotFoundError,
)
from app.schemas.investigation import (
    InvestigationResponse,
)
from app.services.investigation_service import (
    InvestigationService,
)

router = APIRouter(
    prefix="/api/v1/incidents",
    tags=["Investigations"],
)


InvestigationServiceDependency = Annotated[
    InvestigationService,
    Depends(get_investigation_service),
]


@router.post(
    "/{incident_id}/investigations",
    response_model=InvestigationResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_investigation(
    incident_id: UUID,
    service: InvestigationServiceDependency,
) -> InvestigationResponse:
    try:
        investigation = service.investigate(
            incident_id
        )

    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except InvestigationNotAllowedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    except ServiceNotFoundError as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_424_FAILED_DEPENDENCY
            ),
            detail=str(exc),
        ) from exc

    return InvestigationResponse(
        **investigation.model_dump()
    )