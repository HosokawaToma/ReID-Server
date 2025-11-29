from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot.image import RepositoryPersonSnapshotImage
from entities.person.snapshot import PersonSnapshot, PersonSnapshotImage
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
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_image = repository_person_snapshot_image

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotCreate":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
            repository_person_snapshot_image=RepositoryPersonSnapshotImage.create(environment),
        )

    def save(self, params: ApplicationPersonSnapshotCreateParams) -> PersonSnapshot:
        image = PersonSnapshotImage(
            image=params.image,
        )
        self.repository_person_snapshot_image.save(image)
        person_snapshot = PersonSnapshot(
            image_id=image.id,
            camera_id=params.camera_id,
            view_id=params.view_id,
            timestamp=params.timestamp,
        )
        self.repository_person_snapshot.save(person_snapshot)
        return person_snapshot
