from dataclasses import dataclass, field
from value.id import ValueId

@dataclass
class ValuePersonSnapshotAnnotation:
    _person_id: ValueId | None = field(default=None)
    _is_junk: bool = field(default=False)

    @property
    def person_id(self) -> ValueId | None:
        return self._person_id

    @person_id.setter
    def person_id(self, person_id: ValueId) -> None:
        self._person_id = person_id
        self._is_junk = False

    @property
    def is_junk(self) -> bool:
        return self._is_junk

    @is_junk.setter
    def is_junk(self, is_junk: bool) -> None:
        self._is_junk = is_junk
        if is_junk:
            self._person_id = None
