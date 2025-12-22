from datetime import datetime

from domain.person.snapshot import DomainPersonSnapshot
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

    def identify(self) -> DomainPersonSnapshot:
        try:
            person_snapshot = self.repository_person_snapshot.next_identify()
            nearest_person_snapshot = self.repository_person_snapshot.find_first(
                filters=RepositoryPersonSnapshotFilters(
                    not_ids=[person_snapshot.id],
                    timestamp_after=datetime.combine(
                        person_snapshot.timestamp.date(), datetime.min.time()),
                    timestamp_before=person_snapshot.timestamp,
                    is_junk=False,
                    ),
                ordering=RepositoryPersonSnapshotOrdering([
                    person_snapshot.feature, # type: ignore
                    RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_DESC]),
            )
            if nearest_person_snapshot is not None:
                person_snapshot.person_reid(nearest_person_snapshot)
                self.repository_person_snapshot.update(person_snapshot)
            return person_snapshot
        except Error as error:
            raise ApplicationPersonSnapshotBackgroundIdentifyError(error) from error
