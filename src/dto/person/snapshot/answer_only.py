from dataclasses import dataclass
import uuid

@dataclass
class DtoPersonSnapshotAnswerOnly:
    id: uuid.UUID
    person_id: uuid.UUID | None
    is_junk: bool
