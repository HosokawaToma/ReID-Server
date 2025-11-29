from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentify
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyError
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneFilters
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneOrdering
from repositories.person.snapshot import PersonSnapshotNotFoundError
from modules.reid.identifier import ModuleReIDIdentifier
from modules.reid.identifier import ReIDIdentifierThresholdError
from environment import Environment

from dataclasses import dataclass
import uuid


@dataclass
class ApplicationPersonSnapshotBackgroundIdentifyParams:
    person_snapshot_id: uuid.UUID


class ApplicationPersonSnapshotBackgroundIdentifyError(Exception):
    pass


class ApplicationPersonSnapshotMissingFeatureError(ApplicationPersonSnapshotBackgroundIdentifyError):
    pass


class ApplicationPersonSnapshotNotFoundError(ApplicationPersonSnapshotBackgroundIdentifyError):
    pass


class ApplicationPersonSnapshotThresholdError(ApplicationPersonSnapshotBackgroundIdentifyError):
    pass


class ApplicationPersonSnapshotBackgroundIdentify:
    def __init__(
        self,
        repository_queue_person_snapshot_identify: RepositoryQueuePersonSnapshotIdentify,
        repository_person_snapshot: RepositoryPersonSnapshot,
        reid_identifier: ModuleReIDIdentifier,
    ):
        self.repository_queue_person_snapshot_identify = repository_queue_person_snapshot_identify
        self.repository_person_snapshot = repository_person_snapshot
        self.reid_identifier = reid_identifier

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotBackgroundIdentify":
        return cls(
            repository_queue_person_snapshot_identify=RepositoryQueuePersonSnapshotIdentify.create(
                environment),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            reid_identifier=ModuleReIDIdentifier(threshold=0.895),
        )

    async def identify(self) -> None:
        try:
            item = await self.repository_queue_person_snapshot_identify.dequeue()
            person_snapshot = self.repository_person_snapshot.find_first(
                RepositoryPersonSnapshotFindOneParams(
                    filters=RepositoryPersonSnapshotFindOneFilters(
                        ids=[item.id],
                    ),
                )
            )
            if person_snapshot.feature is None:
                raise ApplicationPersonSnapshotMissingFeatureError
            nearest_person_snapshot = self.repository_person_snapshot.find_first(
                RepositoryPersonSnapshotFindOneParams(
                    ordering=RepositoryPersonSnapshotFindOneOrdering(
                        feature_to_nearest=person_snapshot.feature,
                    ),
                )
            )
            if nearest_person_snapshot.feature is None:
                raise ApplicationPersonSnapshotMissingFeatureError
            self.reid_identifier.guarantee(
                person_snapshot.feature,
                nearest_person_snapshot.feature,
            )
            person_snapshot.person_id = nearest_person_snapshot.person_id
            self.repository_person_snapshot.update(person_snapshot)
        except RepositoryQueuePersonSnapshotIdentifyError:
            raise ApplicationPersonSnapshotBackgroundIdentifyError
        except ApplicationPersonSnapshotMissingFeatureError:
            raise ApplicationPersonSnapshotMissingFeatureError
        except PersonSnapshotNotFoundError:
            raise ApplicationPersonSnapshotNotFoundError
        except ReIDIdentifierThresholdError:
            raise ApplicationPersonSnapshotThresholdError
