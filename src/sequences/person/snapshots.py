from entities.person.snapshot import EntityPersonSnapshot
import uuid
from datetime import timedelta
from sequences.person.flows import SequencePersonFlows
from entities.person.flow import EntityPersonFlow

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

    def is_convertible_to_flows(self) -> bool:
        return self.person_id is not None and len(self.person_snapshots) >= 2

    def convert_to_flows(self, interval: timedelta) -> SequencePersonFlows:
        person_snapshots = self.sorted_by_timestamp()
        if person_snapshots.person_id is None:
            raise SequencePersonSnapshotsPersonIdNotSetError
        if len(person_snapshots.person_snapshots) < 2:
            raise SequencePersonSnapshotsLessThanTwoSnapshotsError
        person_flows = []
        for i in range(len(person_snapshots.person_snapshots)):
            if i == 0:
                continue
            if person_snapshots.person_snapshots[i].camera_id == person_snapshots.person_snapshots[i - 1].camera_id \
            and person_snapshots.person_snapshots[i].timestamp - person_snapshots.person_snapshots[i - 1].timestamp > interval:
                continue
            person_flows.append(
                EntityPersonFlow(
                    person_id=person_snapshots.person_id,
                    source_camera_id=person_snapshots.person_snapshots[i - 1].camera_id,
                    target_camera_id=person_snapshots.person_snapshots[i].camera_id,
                    source_timestamp=person_snapshots.person_snapshots[i - 1].timestamp,
                    target_timestamp=person_snapshots.person_snapshots[i].timestamp,
                )
            )
        return SequencePersonFlows(person_flows=person_flows, person_id=person_snapshots.person_id)
