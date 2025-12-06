from repositories.person.snapshot import RepositoryPersonSnapshot
from entities.person.snapshot import EntityPersonSnapshot
from repositories.person.snapshot.image import RepositoryPersonSnapshotImage
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageFindOneParams
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import PersonSnapshotNotFoundError
from repositories.person.snapshot.image import PersonSnapshotImageNotFoundError
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtraction
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionError
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentify
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyQueueItem
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyError
from modules.reid.model import ModuleReIDModel
from modules.yolo.pose import ModuleYoloPose
from modules.yolo.pose.verification import ModuleYoloPoseVerification
from modules.yolo.segmentation import ModuleYoloSegmentation
from modules.yolo.segmentation.verification import ModuleYoloSegmentationVerification
from environment import Environment


class ApplicationPersonSnapshotBackgroundFeatureExtractionError(Exception):
    pass


class ApplicationPersonSnapshotNotFoundError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass


class ApplicationPersonSnapshotImageNotFoundError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass

class ApplicationPersonSnapshotYoloPoseNotFoundError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass

class ApplicationPersonSnapshotYoloPoseVerificationError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass

class ApplicationPersonSnapshotYoloSegmentationNotFoundError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass

class ApplicationPersonSnapshotYoloSegmentationVerificationError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass

class ApplicationPersonSnapshotIdentifyQueueError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass

class ApplicationPersonSnapshotRepositoryError(ApplicationPersonSnapshotBackgroundFeatureExtractionError):
    pass

class ApplicationPersonSnapshotBackgroundFeatureExtraction:
    def __init__(
        self,
        yolo_pose_model: ModuleYoloPose,
        yolo_segmentation_model: ModuleYoloSegmentation,
        yolo_pose_verification: ModuleYoloPoseVerification,
        yolo_segmentation_verification: ModuleYoloSegmentationVerification,
        repository_queue_person_snapshot_feature_extraction: RepositoryQueuePersonSnapshotFeatureExtraction,
        repository_queue_person_snapshot_identify: RepositoryQueuePersonSnapshotIdentify,
        reid_model: ModuleReIDModel,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_person_snapshot_image: RepositoryPersonSnapshotImage,
    ):
        self.yolo_pose_model = yolo_pose_model
        self.yolo_segmentation_model = yolo_segmentation_model
        self.yolo_pose_verification = yolo_pose_verification
        self.yolo_segmentation_verification = yolo_segmentation_verification
        self.repository_queue_person_snapshot_feature_extraction = repository_queue_person_snapshot_feature_extraction
        self.repository_queue_person_snapshot_identify = repository_queue_person_snapshot_identify
        self.reid_model = reid_model
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_person_snapshot_image = repository_person_snapshot_image

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ApplicationPersonSnapshotBackgroundFeatureExtraction":
        return cls(
            yolo_pose_model=ModuleYoloPose(),
            yolo_segmentation_model=ModuleYoloSegmentation(),
            yolo_pose_verification=ModuleYoloPoseVerification(),
            yolo_segmentation_verification=ModuleYoloSegmentationVerification(),
            repository_queue_person_snapshot_feature_extraction=RepositoryQueuePersonSnapshotFeatureExtraction.create(
                environment),
            repository_queue_person_snapshot_identify=RepositoryQueuePersonSnapshotIdentify.create(
                environment),
            reid_model=ModuleReIDModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            repository_person_snapshot_image=RepositoryPersonSnapshotImage.create(
                environment),
        )

    async def extract(self) -> EntityPersonSnapshot:
        try:
            queue_item = await self.repository_queue_person_snapshot_feature_extraction.dequeue()
            person_snapshot = self.repository_person_snapshot.find_first(
                filters=RepositoryPersonSnapshotFilters(
                    ids=[queue_item.id],
                )
            )
            image = self.repository_person_snapshot_image.find_one(
                RepositoryPersonSnapshotImageFindOneParams(
                    id=person_snapshot.image_id,
                )
            )
            yolo_pose = self.yolo_pose_model.extract(
                image.image,
            )
            yolo_segmentation = self.yolo_segmentation_model.extract(
                image.image,
            )
            if yolo_pose is None:
                self.repository_person_snapshot.delete(
                    filters=RepositoryPersonSnapshotFilters(
                        ids=[person_snapshot.id],
                    ),
                )
                raise ApplicationPersonSnapshotYoloPoseNotFoundError
            if not self.yolo_pose_verification.verify(
                yolo_pose,
            ):
                self.repository_person_snapshot.delete(
                    filters=RepositoryPersonSnapshotFilters(
                        ids=[person_snapshot.id],
                    ),
                )
                raise ApplicationPersonSnapshotYoloPoseVerificationError
            if yolo_segmentation is None:
                self.repository_person_snapshot.delete(
                    filters=RepositoryPersonSnapshotFilters(
                        ids=[person_snapshot.id],
                    ),
                )
                raise ApplicationPersonSnapshotYoloSegmentationNotFoundError
            if not self.yolo_segmentation_verification.verify(
                yolo_segmentation,
            ):
                self.repository_person_snapshot.delete(
                    filters=RepositoryPersonSnapshotFilters(
                        ids=[person_snapshot.id],
                    )
                )
                raise ApplicationPersonSnapshotYoloSegmentationVerificationError
            person_snapshots_feature = self.reid_model.extract_feature(
                image.image,
                person_snapshot.camera_id,
                person_snapshot.view_id,
            )
            person_snapshot.feature = person_snapshots_feature
            self.repository_person_snapshot.update(
                person_snapshot,
                filters=RepositoryPersonSnapshotFilters(
                    ids=[person_snapshot.id],
                ),
            )
            await self.repository_queue_person_snapshot_identify.push(
                RepositoryQueuePersonSnapshotIdentifyQueueItem(
                    id=person_snapshot.id,
                )
            )
            return person_snapshot
        except RepositoryQueuePersonSnapshotFeatureExtractionError:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError
        except PersonSnapshotNotFoundError:
            raise ApplicationPersonSnapshotNotFoundError
        except PersonSnapshotImageNotFoundError:
            raise ApplicationPersonSnapshotImageNotFoundError
        except ApplicationPersonSnapshotYoloPoseNotFoundError:
            raise ApplicationPersonSnapshotYoloPoseNotFoundError
        except ApplicationPersonSnapshotYoloPoseVerificationError:
            raise ApplicationPersonSnapshotYoloPoseVerificationError
        except ApplicationPersonSnapshotYoloSegmentationNotFoundError:
            raise ApplicationPersonSnapshotYoloSegmentationNotFoundError
        except ApplicationPersonSnapshotYoloSegmentationVerificationError:
            raise ApplicationPersonSnapshotYoloSegmentationVerificationError
        except RepositoryQueuePersonSnapshotIdentifyError:
            raise ApplicationPersonSnapshotIdentifyQueueError
