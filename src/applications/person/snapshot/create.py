from repositories.frame_image import RepositoryFrameImage
from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreate
from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreateQueueItem
from domain.frame_image import DomainFrameImage
from PIL import Image
from datetime import datetime
from dataclasses import dataclass
from environment import Environment
from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreateError


@dataclass
class ApplicationPersonSnapshotCreateParams:
    image: Image.Image
    camera_id: int
    view_id: int
    timestamp: datetime


class ApplicationPersonSnapshotCreate:
    def __init__(
        self,
        repository_frame_image: RepositoryFrameImage,
        repository_queue_person_snapshot_create: RepositoryQueuePersonSnapshotCreate,
    ):
        self.repository_frame_image = repository_frame_image
        self.repository_queue_person_snapshot_create = repository_queue_person_snapshot_create

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotCreate":
        return cls(
            repository_frame_image=RepositoryFrameImage.create(
                environment),
            repository_queue_person_snapshot_create=RepositoryQueuePersonSnapshotCreate.create(
                environment),
        )

    def save(self, params: ApplicationPersonSnapshotCreateParams) -> None:
        frame_image = DomainFrameImage(
            image=params.image,
            camera_id=params.camera_id,
            view_id=params.view_id,
            timestamp=params.timestamp,
        )
        try:
            self.repository_frame_image.save(frame_image)
            self.repository_queue_person_snapshot_create.push(
                RepositoryQueuePersonSnapshotCreateQueueItem(
                    id=frame_image.id,
                    camera_id=params.camera_id,
                    view_id=params.view_id,
                    timestamp=params.timestamp,
                )
            )
        except RepositoryQueuePersonSnapshotCreateError as e:
            self.repository_frame_image.delete(frame_image)
            raise e
