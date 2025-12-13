from repositories import RepositoryRedis
from repositories import RepositoryRedisError
from error import Error
from dataclasses import dataclass
import uuid
from environment import Environment

@dataclass
class RepositoryQueuePersonSnapshotCreateQueueItem:
    id: uuid.UUID

class RepositoryQueuePersonSnapshotCreateError(Error):
    pass

class RepositoryQueuePersonSnapshotCreate(RepositoryRedis):
    key = "person_snapshot:create"

    def __init__(
        self,
        environment: Environment,
    ):
        super().__init__(environment)

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryQueuePersonSnapshotCreate":
        return cls(
            environment=environment,
        )

    def push(self, value: RepositoryQueuePersonSnapshotCreateQueueItem) -> None:
        try:
            self._push({
                "id": str(value.id),
            })
        except RepositoryRedisError as e:
            raise RepositoryQueuePersonSnapshotCreateError(e.message)

    def dequeue(self, timeout: int = 0) -> RepositoryQueuePersonSnapshotCreateQueueItem:
        try:
            data = self._dequeue(timeout)
        except RepositoryRedisError as e:
            raise RepositoryQueuePersonSnapshotCreateError(e.message)
        if "id" not in data:
            raise RepositoryQueuePersonSnapshotCreateError(f"id not found: {data}")
        return RepositoryQueuePersonSnapshotCreateQueueItem(
            id=uuid.UUID(data["id"]),
        )
