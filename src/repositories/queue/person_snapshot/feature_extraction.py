from dataclasses import dataclass
from repositories import RepositoryRedis
from environment import Environment
import uuid
from repositories import RepositoryRedisError

@dataclass
class RepositoryQueuePersonSnapshotFeatureExtractionQueueItem:
    id: uuid.UUID


class RepositoryQueuePersonSnapshotFeatureExtractionError(Exception):
    pass


class RepositoryQueuePersonSnapshotFeatureExtraction(RepositoryRedis):
    key = "person_snapshot:feature_extraction"

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryQueuePersonSnapshotFeatureExtraction":
        return cls(environment)

    async def push(self, value: RepositoryQueuePersonSnapshotFeatureExtractionQueueItem) -> None:
        try:
            await self._push({
                    "id": str(value.id),
                })
        except RepositoryRedisError:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError

    async def dequeue(self, timeout: int = 0) -> RepositoryQueuePersonSnapshotFeatureExtractionQueueItem:
        try:
            data = await self._dequeue(timeout)
        except RepositoryRedisError:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError
        if "id" not in data:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError
        return RepositoryQueuePersonSnapshotFeatureExtractionQueueItem(
            id=uuid.UUID(data["id"]),
        )
