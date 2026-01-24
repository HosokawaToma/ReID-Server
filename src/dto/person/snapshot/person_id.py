from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class DtoPersonSnapshotPersonId:
    id: uuid.UUID
    person_id: uuid.UUID | None
    is_junk: bool
