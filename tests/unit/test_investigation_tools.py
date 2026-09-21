from app.simulator.operations_simulator import (
    PAYMENT_SERVICE,
    OperationsSimulator,
)
from app.tools.deployments_tool import (
    GetRecentDeploymentsTool,
)
from app.tools.logs_tool import GetRecentLogsTool
from app.tools.service_health_tool import (
    GetServiceHealthTool,
)


def test_health_tool_returns_service_health() -> None:
    simulator = OperationsSimulator()

    tool = GetServiceHealthTool(
        simulator
    )

    health = tool.execute(
        PAYMENT_SERVICE
    )

    assert health.service == PAYMENT_SERVICE
    assert health.status == "healthy"


def test_logs_tool_returns_service_logs() -> None:
    simulator = OperationsSimulator()

    tool = GetRecentLogsTool(
        simulator
    )

    logs = tool.execute(
        PAYMENT_SERVICE
    )

    assert len(logs) >= 1

    assert logs[0].service == PAYMENT_SERVICE


def test_deployments_tool_returns_history() -> None:
    simulator = OperationsSimulator()

    tool = GetRecentDeploymentsTool(
        simulator
    )

    deployments = tool.execute(
        PAYMENT_SERVICE
    )

    assert len(deployments) >= 1
    assert deployments[0].status == "successful"