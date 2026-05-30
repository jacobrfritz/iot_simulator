from dataclasses import dataclass
import uuid
from datetime import datetime
import json


@dataclass
class Event:
    """
    Holds events
    """

    producer_id: uuid.UUID
    event_time: datetime
    payload: float
    def to_json(self)->str:
        out = {
            "producer_id":str(self.producer_id),
            "event_time":self.event_time.isoformat(),
            "payload":str(self.payload)
        }
        return json.dumps(out)
