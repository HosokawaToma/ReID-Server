from datetime import datetime

from dto.person_snapshot import DtoPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotOrdering
from environment import Environment
from error import Error


class ApplicationPersonSnapshotBackgroundIdentifyError(Error):
    pass

class ApplicationPersonSnapshotBackgroundIdentify:
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotBackgroundIdentify":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def identify(self) -> DtoPersonSnapshot:
        try:
            person_snapshot = self.repository_person_snapshot.next_identify()
            nearest_person_snapshot = self.repository_person_snapshot.find_first(
                filters=RepositoryPersonSnapshotFilters(
                    not_ids=[person_snapshot.id],
                    timestamp_after=datetime.combine(
                        person_snapshot.timestamp.date(), datetime.min.time()),
                    timestamp_before=person_snapshot.timestamp,
                    is_junk=False,
                    has_person_id=True,
                    has_feature=True,
                    ),
                ordering=RepositoryPersonSnapshotOrdering([
                    person_snapshot.feature, # type: ignore
                    RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_DESC]),
            )
            person_snapshot.person_reid(nearest_person_snapshot)
            self.repository_person_snapshot.update(person_snapshot)
            return DtoPersonSnapshot(
                id=person_snapshot.id,
                camera_id=person_snapshot.camera_id,
                view_id=person_snapshot.view_id,
                timestamp=person_snapshot.timestamp,
                is_junk=person_snapshot.is_junk,
                person_id=person_snapshot.person_id,
                feature=person_snapshot.feature,
            )
        except Error as error:
            raise ApplicationPersonSnapshotBackgroundIdentifyError(error) from error
