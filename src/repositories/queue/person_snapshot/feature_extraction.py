from dataclasses import dataclass
from repositories import RepositoryRedis
from environment import Environment
import uuid

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

    def push(self, value: RepositoryQueuePersonSnapshotFeatureExtractionQueueItem) -> None:
        self._push({
            "id": str(value.id),
        })

    async def dequeue(self, timeout: int = 0) -> RepositoryQueuePersonSnapshotFeatureExtractionQueueItem:
        data = await self._dequeue(timeout)
        if "id" not in data:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError
        return RepositoryQueuePersonSnapshotFeatureExtractionQueueItem(
            id=uuid.UUID(data["id"]),
        )
