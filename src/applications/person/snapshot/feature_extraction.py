from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot.image import RepositoryPersonSnapshotImage
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageFindOneParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneFilters
from repositories.person.snapshot import PersonSnapshotNotFoundError
from repositories.person.snapshot.image import PersonSnapshotImageNotFoundError
from modules.reid.model import ModuleReIDModel
import uuid
from dataclasses import dataclass
from environment import Environment

@dataclass
class ApplicationPersonSnapshotFeatureExtractionParams:
    person_snapshot_id: uuid.UUID

class ApplicationPersonSnapshotFeatureExtractionError(Exception):
    pass

class ApplicationPersonSnapshotNotFoundError(ApplicationPersonSnapshotFeatureExtractionError):
    pass

class ApplicationPersonSnapshotImageNotFoundError(ApplicationPersonSnapshotFeatureExtractionError):
    pass

class ApplicationPersonSnapshotFeatureExtraction:
    def __init__(
        self,
        reid_model: ModuleReIDModel,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_person_snapshot_image: RepositoryPersonSnapshotImage,
    ):
        self.reid_model = reid_model
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_image = repository_person_snapshot_image

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ApplicationPersonSnapshotFeatureExtraction":
        return cls(
            reid_model=ModuleReIDModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
            repository_person_snapshot_image=RepositoryPersonSnapshotImage.create(
                environment),
        )

    def extract(self, params: ApplicationPersonSnapshotFeatureExtractionParams) -> None:
        try:
            person_snapshot = self.repository_person_snapshot.find_first(
                RepositoryPersonSnapshotFindOneParams(
                    filters=RepositoryPersonSnapshotFindOneFilters(
                        ids=[params.person_snapshot_id],
                    ),
                )
            )
            image = self.repository_person_snapshot_image.find_one(
                RepositoryPersonSnapshotImageFindOneParams(
                    id=person_snapshot.image_id,
                ),
            )
            person_snapshots_feature = self.reid_model.extract_feature(
                image.image,
                person_snapshot.camera_id,
                person_snapshot.view_id,
            )
            person_snapshot.feature = person_snapshots_feature
            self.repository_person_snapshot.update(person_snapshot)
        except PersonSnapshotNotFoundError:
            raise ApplicationPersonSnapshotNotFoundError
        except PersonSnapshotImageNotFoundError:
            raise ApplicationPersonSnapshotImageNotFoundError
