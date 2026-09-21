from app.models.simulator import DeploymentRecord
from app.simulator.operations_simulator import (
    OperationsSimulator,
)


class GetRecentDeploymentsTool:
    name = "get_recent_deployments"

    description = (
        "Retrieve recent deployment history "
        "for a service."
    )

    def __init__(
        self,
        simulator: OperationsSimulator,
    ) -> None:
        self.simulator = simulator

    def execute(
        self,
        service: str,
    ) -> list[DeploymentRecord]:
        return self.simulator.get_deployments(
            service
        )