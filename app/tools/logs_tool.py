from app.models.simulator import LogEntry
from app.simulator.operations_simulator import (
    OperationsSimulator,
)


class GetRecentLogsTool:
    name = "get_recent_logs"

    description = (
        "Retrieve recent operational logs "
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
    ) -> list[LogEntry]:
        return self.simulator.get_logs(
            service
        )