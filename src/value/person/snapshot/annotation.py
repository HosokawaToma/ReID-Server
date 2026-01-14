from dataclasses import dataclass
from value.id import ValueId

@dataclass
class ValuePersonSnapshotAnnotation:
    person_id: ValueId | None
    is_junk: bool

    @classmethod
    def new_id(cls) -> "ValuePersonSnapshotAnnotation":
        return cls(
            person_id=ValueId(),
            is_junk=False,
        )
