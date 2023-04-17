from dataclasses import dataclass
import uuid


@dataclass
class Message:
    sensor_name: str
    value: int
    timestamp: float
    id: uuid.UUID

    def __str__(self) -> str:
        return f"{self.id},{self.timestamp},{self.sensor_name},{self.value}"
