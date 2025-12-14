from datetime import datetime

from domain.person.snapshot import DomainPersonSnapshot
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentify
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyError
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotOrdering
from repositories.person.snapshot import RepositoryPersonSnapshotError
from environment import Environment
from error import Error
from dataclasses import dataclass
import uuid


@dataclass
class ApplicationPersonSnapshotBackgroundIdentifyParams:
    person_snapshot_id: uuid.UUID


class ApplicationPersonSnapshotBackgroundIdentifyError(Error):
    pass


class ApplicationPersonSnapshotBackgroundIdentify:
    def __init__(
        self,
        repository_queue_person_snapshot_identify: RepositoryQueuePersonSnapshotIdentify,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_queue_person_snapshot_identify = repository_queue_person_snapshot_identify
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotBackgroundIdentify":
        return cls(
            repository_queue_person_snapshot_identify=RepositoryQueuePersonSnapshotIdentify.create(
                environment),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def identify(self) -> DomainPersonSnapshot:
        try:
            item = self.repository_queue_person_snapshot_identify.dequeue()
            person_snapshot = self.repository_person_snapshot.find_first(
                filters=RepositoryPersonSnapshotFilters(ids=[item.id]))
            if person_snapshot is None:
                raise ApplicationPersonSnapshotBackgroundIdentifyError(
                    f"person snapshot not found: {item.id}")
            nearest_person_snapshot = person_snapshot.find_nearest(self.repository_person_snapshot)
            if nearest_person_snapshot is not None:
                person_snapshot.match(nearest_person_snapshot)
                self.repository_person_snapshot.update(person_snapshot)
            return person_snapshot
        except RepositoryQueuePersonSnapshotIdentifyError as e:
            raise ApplicationPersonSnapshotBackgroundIdentifyError(e.message)
        except RepositoryPersonSnapshotError as e:
            raise ApplicationPersonSnapshotBackgroundIdentifyError(e.message)
