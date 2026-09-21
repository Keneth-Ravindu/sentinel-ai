from datetime import datetime

from pydantic import BaseModel

from app.models.simulator import (
    LogLevel,
    PaymentProvider,
    ServiceStatus,
)


class ServiceHealthResponse(BaseModel):
    service: str
    status: ServiceStatus
    cpu_percent: float
    memory_percent: float
    error_rate: float
    p95_latency_ms: float
    database_latency_ms: float
    active_provider: PaymentProvider


class LogEntryResponse(BaseModel):
    timestamp: datetime
    level: LogLevel
    service: str
    message: str


class DeploymentResponse(BaseModel):
    version: str
    deployed_at: datetime
    status: str


class ScenarioResponse(BaseModel):
    scenario: str
    service_health: ServiceHealthResponse


class ActionResponse(BaseModel):
    action: str
    service_health: ServiceHealthResponse


class ResetResponse(BaseModel):
    message: str