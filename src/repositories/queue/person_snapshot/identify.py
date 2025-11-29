from repositories import RepositoryRedis
from environment import Environment
from dataclasses import dataclass
import uuid
from repositories import RepositoryRedisError

@dataclass
class RepositoryQueuePersonSnapshotIdentifyQueueItem:
    id: uuid.UUID


class RepositoryQueuePersonSnapshotIdentifyError(Exception):
    pass


class RepositoryQueuePersonSnapshotIdentify(RepositoryRedis):
    key = "person_snapshot:identify"

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryQueuePersonSnapshotIdentify":
        return cls(environment)

    async def push(self, value: RepositoryQueuePersonSnapshotIdentifyQueueItem) -> None:
        try:
            await self._push({
                "id": str(value.id),
            })
        except RepositoryRedisError:
            raise RepositoryQueuePersonSnapshotIdentifyError

    async def dequeue(self, timeout: int = 0) -> RepositoryQueuePersonSnapshotIdentifyQueueItem:
        try:
            data = await self._dequeue(timeout)
        except RepositoryRedisError:
            raise RepositoryQueuePersonSnapshotIdentifyError
        if "id" not in data:
            raise RepositoryQueuePersonSnapshotIdentifyError
        return RepositoryQueuePersonSnapshotIdentifyQueueItem(
            id=uuid.UUID(data["id"]),
        )
