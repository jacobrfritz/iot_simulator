from dataclasses import dataclass
import uuid
from datetime import datetime

@dataclass
class Event:
    """
    Holds events
    """
    producer_id: uuid.UUID
    event_time: datetime
    payload:float