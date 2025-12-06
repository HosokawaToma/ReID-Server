from dataclasses import dataclass
from repositories import RepositoryRedis
from environment import Environment
import uuid
from repositories import RepositoryRedisError
from error import Error


@dataclass
class RepositoryQueuePersonSnapshotFeatureExtractionQueueItem:
    id: uuid.UUID


class RepositoryQueuePersonSnapshotFeatureExtractionError(Error):
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
            raise RepositoryQueuePersonSnapshotFeatureExtractionError("repository redis error")

    async def dequeue(self, timeout: int = 0) -> RepositoryQueuePersonSnapshotFeatureExtractionQueueItem:
        try:
            data = await self._dequeue(timeout)
        except RepositoryRedisError as e:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError(str(e))
        if "id" not in data:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError(f"id not found: {data}")
        return RepositoryQueuePersonSnapshotFeatureExtractionQueueItem(
            id=uuid.UUID(data["id"]),
        )
