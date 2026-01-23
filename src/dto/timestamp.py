from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class DtoTimestamp:
    timestamp: datetime
