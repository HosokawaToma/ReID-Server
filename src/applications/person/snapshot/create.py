from repositories.frame import RepositoryFrame
from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreate
from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreateQueueItem
from entities.frame import EntityFrame
from PIL import Image
from datetime import datetime
from dataclasses import dataclass
from environment import Environment


@dataclass
class ApplicationPersonSnapshotCreateParams:
    image: Image.Image
    camera_id: int
    view_id: int
    timestamp: datetime


class ApplicationPersonSnapshotCreate:
    def __init__(
        self,
        repository_frame: RepositoryFrame,
        repository_queue_person_snapshot_create: RepositoryQueuePersonSnapshotCreate,
    ):
        self.repository_frame = repository_frame
        self.repository_queue_person_snapshot_create = repository_queue_person_snapshot_create

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotCreate":
        return cls(
            repository_frame=RepositoryFrame.create(
                environment),
            repository_queue_person_snapshot_create=RepositoryQueuePersonSnapshotCreate.create(
                environment),
        )

    def save(self, params: ApplicationPersonSnapshotCreateParams) -> None:
        frame = EntityFrame(
            image=params.image,
            camera_id=params.camera_id,
            view_id=params.view_id,
            timestamp=params.timestamp,
        )
        self.repository_frame.save(frame)
        self.repository_queue_person_snapshot_create.push(
            RepositoryQueuePersonSnapshotCreateQueueItem(
                id=frame.id,
            )
        )
