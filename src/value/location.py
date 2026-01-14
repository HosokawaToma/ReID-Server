from dataclasses import dataclass
from value.timestamp import ValueTimestamp

@dataclass
class ValueLocation:
    camera_id: int
    view_id: int
    timestamp: ValueTimestamp
