from repositories import RepositoryRedis
from environment import Environment
from dataclasses import dataclass
import uuid
from repositories import RepositoryRedisError
from error import Error

@dataclass
class RepositoryQueuePersonSnapshotIdentifyQueueItem:
    id: uuid.UUID


class RepositoryQueuePersonSnapshotIdentifyError(Error):
    pass


class RepositoryQueuePersonSnapshotIdentify(RepositoryRedis):
    key = "person_snapshot:identify"

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryQueuePersonSnapshotIdentify":
        return cls(environment)

    def push(self, value: RepositoryQueuePersonSnapshotIdentifyQueueItem) -> None:
        try:
            self._push({
                "id": str(value.id),
            })
        except RepositoryRedisError as e:
            raise RepositoryQueuePersonSnapshotIdentifyError(e.message)

    def dequeue(self, timeout: int = 0) -> RepositoryQueuePersonSnapshotIdentifyQueueItem:
        try:
            data = self._dequeue(timeout)
        except RepositoryRedisError as e:
            raise RepositoryQueuePersonSnapshotIdentifyError(e.message)
        if "id" not in data:
            raise RepositoryQueuePersonSnapshotIdentifyError("id not found")
        return RepositoryQueuePersonSnapshotIdentifyQueueItem(
            id=uuid.UUID(data["id"]),
        )
