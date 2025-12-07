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

    def push(self, value: RepositoryQueuePersonSnapshotFeatureExtractionQueueItem) -> None:
        try:
            self._push({
                "id": str(value.id),
            })
        except RepositoryRedisError as e:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError(e.message)

    def dequeue(self, timeout: int = 0) -> RepositoryQueuePersonSnapshotFeatureExtractionQueueItem:
        try:
            data = self._dequeue(timeout)
        except RepositoryRedisError as e:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError(e.message)
        if "id" not in data:
            raise RepositoryQueuePersonSnapshotFeatureExtractionError(f"id not found: {data}")
        return RepositoryQueuePersonSnapshotFeatureExtractionQueueItem(
            id=uuid.UUID(data["id"]),
        )
