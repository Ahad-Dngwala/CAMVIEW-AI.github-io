from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import uuid

@dataclass
class Event:
    """
    Standard Logic Event Schema for the Traffic Safety System.
    """
    event_type: str  # e.g., "WRONG_SIDE", "POTHOLE", "EMERGENCY_VEHICLE"
    camera_id: str
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    severity: str = "INFO"  # INFO, WARNING, CRITICAL
    metadata: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def time_str(self) -> str:
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.event_id,
            "type": self.event_type,
            "camera": self.camera_id,
            "time": self.timestamp,
            "time_fmt": self.time_str,
            "severity": self.severity,
            "metadata": self.metadata
        }
