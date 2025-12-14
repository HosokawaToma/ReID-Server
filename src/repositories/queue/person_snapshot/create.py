from repositories import RepositoryRedis
from repositories import RepositoryRedisError
from error import Error
from dataclasses import dataclass
import uuid
from environment import Environment
from datetime import datetime
@dataclass
class RepositoryQueuePersonSnapshotCreateQueueItem:
    id: uuid.UUID
    camera_id: int
    view_id: int
    timestamp: datetime

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
                "camera_id": str(value.camera_id),
                "view_id": str(value.view_id),
                "timestamp": value.timestamp.isoformat(),
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
        if "camera_id" not in data:
            raise RepositoryQueuePersonSnapshotCreateError(f"camera_id not found: {data}")
        if "view_id" not in data:
            raise RepositoryQueuePersonSnapshotCreateError(f"view_id not found: {data}")
        if "timestamp" not in data:
            raise RepositoryQueuePersonSnapshotCreateError(f"timestamp not found: {data}")
        return RepositoryQueuePersonSnapshotCreateQueueItem(
            id=uuid.UUID(data["id"]),
            camera_id=int(data["camera_id"]),
            view_id=int(data["view_id"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
