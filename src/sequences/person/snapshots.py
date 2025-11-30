from entities.person.snapshot import EntityPersonSnapshot
from entities.person.flow import EntityPersonFlow
from sequences.person.flows import SequencePersonFlows
from datetime import timedelta
import uuid

class SequencePersonSnapshotsError(Exception):
    pass

class SequencePersonSnapshotsPersonIdNotSetError(SequencePersonSnapshotsError):
    pass

class SequencePersonSnapshotsLessThanTwoSnapshotsError(SequencePersonSnapshotsError):
    pass

class SequencePersonSnapshots:
    def __init__(
        self,
        person_snapshots: list[EntityPersonSnapshot],
        person_id: uuid.UUID | None = None,
    ):
        self.person_snapshots = person_snapshots
        self.person_id = person_id

    def group_by_person_id(self) -> list["SequencePersonSnapshots"]:
        person_snapshots_by_person_id: dict[uuid.UUID, list[EntityPersonSnapshot]] = {}
        for person_snapshot in self.person_snapshots:
            if person_snapshot.person_id not in person_snapshots_by_person_id:
                person_snapshots_by_person_id[person_snapshot.person_id] = []
            person_snapshots_by_person_id[person_snapshot.person_id].append(person_snapshot)
        return [
            SequencePersonSnapshots(person_snapshots=person_snapshots, person_id=person_id)
            for person_id, person_snapshots in person_snapshots_by_person_id.items()
        ]

    def sorted_by_timestamp(self) -> "SequencePersonSnapshots":
        return SequencePersonSnapshots(person_snapshots=sorted(self.person_snapshots, key=lambda x: x.timestamp), person_id=self.person_id)
