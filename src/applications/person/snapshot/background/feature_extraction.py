from repositories.person.snapshot import RepositoryPersonSnapshot
from entities.person.snapshot import EntityPersonSnapshot
from repositories.person.snapshot.image import RepositoryPersonSnapshotImage
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageFindOneParams
from repositories.person.snapshot import RepositoryPersonSnapshotFilters
from repositories.person.snapshot import RepositoryPersonSnapshotError
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageError
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtraction
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionError
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentify
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyQueueItem
from repositories.queue.person_snapshot.identify import RepositoryQueuePersonSnapshotIdentifyError
from modules.reid.model import ModuleReIDModel
from modules.yolo.pose import ModuleYoloPose
from modules.yolo.pose import ModuleYoloPoseError
from modules.yolo.pose.verification import ModuleYoloPoseVerification
from modules.yolo.segmentation import ModuleYoloSegmentation
from modules.yolo.segmentation import ModuleYoloSegmentationError
from modules.yolo.segmentation.verification import ModuleYoloSegmentationVerification
from environment import Environment
from error import Error


class ApplicationPersonSnapshotBackgroundFeatureExtractionError(Error):
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
            if not self.yolo_pose_verification.verify(yolo_pose):
                self.repository_person_snapshot.delete(
                    filters=RepositoryPersonSnapshotFilters(
                        ids=[person_snapshot.id],
                    ),
                )
                raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(
                    "yolo pose verification failed"
                )
            if not self.yolo_segmentation_verification.verify(yolo_segmentation):
                self.repository_person_snapshot.delete(
                    filters=RepositoryPersonSnapshotFilters(
                        ids=[person_snapshot.id],
                    ),
                )
                raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(
                    "yolo segmentation verification failed"
                )
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
        except RepositoryQueuePersonSnapshotFeatureExtractionError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except RepositoryPersonSnapshotError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except RepositoryPersonSnapshotImageError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except ModuleYoloPoseError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except ModuleYoloSegmentationError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except RepositoryQueuePersonSnapshotIdentifyError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
