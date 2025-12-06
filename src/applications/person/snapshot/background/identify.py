import asyncio
from datetime import datetime

from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentify
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyError
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotOrdering
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

    async def identify(self) -> str:
        try:
            item = await self.repository_queue_person_snapshot_identify.dequeue()
            person_snapshot = await asyncio.to_thread(
                self.repository_person_snapshot.find_first,
                filters=RepositoryPersonSnapshotFilters(
                    ids=[item.id],
                ),
            )
            if person_snapshot.feature is None:
                raise ApplicationPersonSnapshotMissingFeatureError
            nearest_person_snapshot = await asyncio.to_thread(
                self.repository_person_snapshot.find_first,
                filters=RepositoryPersonSnapshotFilters(
                    not_ids=[person_snapshot.id],
                    after_timestamp=datetime.combine(
                        person_snapshot.timestamp.date(), datetime.min.time()
                    ),
                    before_timestamp=person_snapshot.timestamp,
                ),
                ordering=RepositoryPersonSnapshotOrdering(
                    ordering=[
                        person_snapshot.feature,
                        RepositoryPersonSnapshotOrdering.KEY_TIMESTAMP_DESC,
                    ],
                ),
            )
            if nearest_person_snapshot.feature is None:
                return f"person snapshot id: {person_snapshot.id} not identified"
            await asyncio.to_thread(
                self.reid_identifier.guarantee,
                person_snapshot.feature,
                nearest_person_snapshot.feature,
            )
            person_snapshot.person_id = nearest_person_snapshot.person_id
            await asyncio.to_thread(
                self.repository_person_snapshot.update,
                person_snapshot,
                filters=RepositoryPersonSnapshotFilters(
                    ids=[person_snapshot.id],
                ),
            )
            return f"person snapshot id: {person_snapshot.id} identified as person id: {person_snapshot.person_id}"
        except RepositoryQueuePersonSnapshotIdentifyError:
            raise ApplicationPersonSnapshotBackgroundIdentifyError
        except ApplicationPersonSnapshotMissingFeatureError:
            raise ApplicationPersonSnapshotMissingFeatureError
        except PersonSnapshotNotFoundError:
            raise ApplicationPersonSnapshotNotFoundError
        except ReIDIdentifierThresholdError:
            raise ApplicationPersonSnapshotThresholdError
