from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.core.dependencies import get_operations_simulator
from app.core.exceptions import (
    InvalidSimulatorActionError,
    ServiceNotFoundError,
)
from app.schemas.simulator import (
    ActionResponse,
    DeploymentResponse,
    LogEntryResponse,
    ResetResponse,
    ScenarioResponse,
    ServiceHealthResponse,
)
from app.simulator.operations_simulator import OperationsSimulator

router = APIRouter(
    prefix="/api/v1/simulator",
    tags=["Operations Simulator"],
)


SimulatorDependency = Annotated[
    OperationsSimulator,
    Depends(get_operations_simulator),
]


@router.get(
    "/services/{service}/health",
    response_model=ServiceHealthResponse,
)
def get_service_health(
    service: str,
    simulator: SimulatorDependency,
) -> ServiceHealthResponse:
    try:
        health = simulator.get_service_health(service)

    except ServiceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return ServiceHealthResponse(
        **health.model_dump()
    )


@router.get(
    "/services/{service}/logs",
    response_model=list[LogEntryResponse],
)
def get_service_logs(
    service: str,
    simulator: SimulatorDependency,
) -> list[LogEntryResponse]:
    try:
        logs = simulator.get_logs(service)

    except ServiceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return [
        LogEntryResponse(**log.model_dump())
        for log in logs
    ]


@router.get(
    "/services/{service}/deployments",
    response_model=list[DeploymentResponse],
)
def get_service_deployments(
    service: str,
    simulator: SimulatorDependency,
) -> list[DeploymentResponse]:
    try:
        deployments = simulator.get_deployments(
            service
        )

    except ServiceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return [
        DeploymentResponse(
            **deployment.model_dump()
        )
        for deployment in deployments
    ]


@router.post(
    "/scenarios/provider-degradation",
    response_model=ScenarioResponse,
)
def trigger_provider_degradation(
    simulator: SimulatorDependency,
) -> ScenarioResponse:
    health = (
        simulator.trigger_provider_degradation()
    )

    return ScenarioResponse(
        scenario="provider-degradation",
        service_health=ServiceHealthResponse(
            **health.model_dump()
        ),
    )


@router.post(
    "/actions/switch-provider",
    response_model=ActionResponse,
)
def switch_provider(
    simulator: SimulatorDependency,
) -> ActionResponse:
    try:
        health = simulator.switch_to_backup_provider()

    except InvalidSimulatorActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return ActionResponse(
        action="switch-payment-provider",
        service_health=ServiceHealthResponse(
            **health.model_dump()
        ),
    )


@router.post(
    "/reset",
    response_model=ResetResponse,
)
def reset_simulator(
    simulator: SimulatorDependency,
) -> ResetResponse:
    simulator.reset()

    return ResetResponse(
        message="Operations simulator reset successfully."
    )