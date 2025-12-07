from repositories.person.snapshot import RepositoryPersonSnapshot
from entities.person.snapshot import EntityPersonSnapshot
from repositories.person.snapshot.image import RepositoryPersonSnapshotImage
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageFindOneParams
from repositories.person.snapshot.image import RepositoryPersonSnapshotImageDeleteParams
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
from modules.yolo.pose.verification import ModuleYoloPoseVerification
from modules.yolo.segmentation import ModuleYoloSegmentation
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

    def extract(self) -> EntityPersonSnapshot:
        try:
            queue_item = self.repository_queue_person_snapshot_feature_extraction.dequeue()
            person_snapshot = self.repository_person_snapshot.find_first(
                filters=RepositoryPersonSnapshotFilters(ids=[queue_item.id]))
            if person_snapshot is None:
                raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(
                    f"person snapshot not found: {queue_item.id}")
            image = self.repository_person_snapshot_image.find_one(
                RepositoryPersonSnapshotImageFindOneParams(id=person_snapshot.image_id))
            yolo_pose = self.yolo_pose_model.extract(image.image)
            yolo_segmentation = self.yolo_segmentation_model.extract(image.image)
            pose_failed = yolo_pose is not None and not self.yolo_pose_verification.verify(yolo_pose)
            segment_failed = not self.yolo_segmentation_verification.verify(yolo_segmentation)
            if pose_failed or segment_failed:
                self.repository_person_snapshot.delete(
                    RepositoryPersonSnapshotFilters(ids=[person_snapshot.id]))
                self.repository_person_snapshot_image.delete(
                    RepositoryPersonSnapshotImageDeleteParams(id=person_snapshot.image_id))
            if pose_failed:
                raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(
                    "yolo pose verification failed")
            if segment_failed:
                raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(
                    "yolo segmentation verification failed")
            person_snapshots_feature = self.reid_model.extract_feature(
                image.image,
                person_snapshot.camera_id,
                person_snapshot.view_id)
            person_snapshot.feature = person_snapshots_feature
            self.repository_person_snapshot.update(person_snapshot)
            self.repository_queue_person_snapshot_identify.push(
                RepositoryQueuePersonSnapshotIdentifyQueueItem(id=person_snapshot.id))
            return person_snapshot
        except RepositoryQueuePersonSnapshotFeatureExtractionError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except RepositoryPersonSnapshotError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except RepositoryPersonSnapshotImageError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
        except RepositoryQueuePersonSnapshotIdentifyError as e:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(e.message)
