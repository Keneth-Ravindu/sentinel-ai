from app.models.simulator import ServiceHealth
from app.simulator.operations_simulator import (
    OperationsSimulator,
)


class GetServiceHealthTool:
    name = "get_service_health"

    description = (
        "Retrieve the current operational health "
        "of a service."
    )

    def __init__(
        self,
        simulator: OperationsSimulator,
    ) -> None:
        self.simulator = simulator

    def execute(
        self,
        service: str,
    ) -> ServiceHealth:
        return self.simulator.get_service_health(
            service
        )