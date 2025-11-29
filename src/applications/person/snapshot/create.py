from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot.image import RepositoryPersonSnapshotImage
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtraction
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionQueueItem
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentify
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyQueueItem
from entities.person.snapshot import EntityPersonSnapshot, EntityPersonSnapshotImage
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
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_person_snapshot_image: RepositoryPersonSnapshotImage,
        repository_queue_person_snapshot_feature_extraction: RepositoryQueuePersonSnapshotFeatureExtraction,
        repository_queue_person_snapshot_identify: RepositoryQueuePersonSnapshotIdentify,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_image = repository_person_snapshot_image
        self.repository_queue_person_snapshot_feature_extraction = repository_queue_person_snapshot_feature_extraction
        self.repository_queue_person_snapshot_identify = repository_queue_person_snapshot_identify

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotCreate":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            repository_person_snapshot_image=RepositoryPersonSnapshotImage.create(
                environment),
            repository_queue_person_snapshot_feature_extraction=RepositoryQueuePersonSnapshotFeatureExtraction.create(
                environment),
            repository_queue_person_snapshot_identify=RepositoryQueuePersonSnapshotIdentify.create(
                environment),
        )

    async def save(self, params: ApplicationPersonSnapshotCreateParams) -> None:
        image = EntityPersonSnapshotImage(
            image=params.image,
        )
        self.repository_person_snapshot_image.save(image)
        person_snapshot = EntityPersonSnapshot(
            image_id=image.id,
            camera_id=params.camera_id,
            view_id=params.view_id,
            timestamp=params.timestamp,
        )
        self.repository_person_snapshot.save(person_snapshot)
        await self.repository_queue_person_snapshot_feature_extraction.push(
            RepositoryQueuePersonSnapshotFeatureExtractionQueueItem(
                id=person_snapshot.id,
            )
        )
        await self.repository_queue_person_snapshot_identify.push(
            RepositoryQueuePersonSnapshotIdentifyQueueItem(
                id=person_snapshot.id,
            )
        )
