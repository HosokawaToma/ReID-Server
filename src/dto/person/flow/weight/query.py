from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class DtoPersonFlowWeightQuery:
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None
    person_ids: list[uuid.UUID] | None = None
