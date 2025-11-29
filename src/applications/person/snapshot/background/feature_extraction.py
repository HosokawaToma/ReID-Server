from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot.image import RepositoryPersonSnapshotImage
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageFindOneParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneFilters
from repositories.person.snapshot import PersonSnapshotNotFoundError
from repositories.person.snapshot.image import PersonSnapshotImageNotFoundError
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtraction
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionError
from modules.reid.model import ModuleReIDModel
from environment import Environment


class ApplicationPersonSnapshotBackgroundFeatureExtractionError(Exception):
    pass


class ApplicationPersonSnapshotNotFoundError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass


class ApplicationPersonSnapshotImageNotFoundError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass


class ApplicationPersonSnapshotBackgroundFeatureExtraction:
    def __init__(
        self,
        repository_queue_person_snapshot_feature_extraction: RepositoryQueuePersonSnapshotFeatureExtraction,
        reid_model: ModuleReIDModel,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_person_snapshot_image: RepositoryPersonSnapshotImage,
    ):
        self.repository_queue_person_snapshot_feature_extraction = repository_queue_person_snapshot_feature_extraction
        self.reid_model = reid_model
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_image = repository_person_snapshot_image

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ApplicationPersonSnapshotBackgroundFeatureExtraction":
        return cls(
            repository_queue_person_snapshot_feature_extraction=RepositoryQueuePersonSnapshotFeatureExtraction.create(
                environment),
            reid_model=ModuleReIDModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            repository_person_snapshot_image=RepositoryPersonSnapshotImage.create(
                environment),
        )

    async def extract(self) -> str:
        try:
            queue_item = await self.repository_queue_person_snapshot_feature_extraction.dequeue()
            person_snapshot = self.repository_person_snapshot.find_first(
                RepositoryPersonSnapshotFindOneParams(
                    filters=RepositoryPersonSnapshotFindOneFilters(
                        ids=[queue_item.id],
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
            return f"person snapshot id: {person_snapshot.id}"
        except RepositoryQueuePersonSnapshotFeatureExtractionError:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError
        except PersonSnapshotNotFoundError:
            raise ApplicationPersonSnapshotNotFoundError
        except PersonSnapshotImageNotFoundError:
            raise ApplicationPersonSnapshotImageNotFoundError
