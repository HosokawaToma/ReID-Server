from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class DtoPersonFlowQuery:
    person_id: uuid.UUID
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
