from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreate
from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreateError
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtraction
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionQueueItem
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionError
from repositories.frame import RepositoryFrame
from repositories.frame import RepositoryFrameFindParams
from repositories.frame import RepositoryFrameError
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from error import Error
from modules.yolo.detection import ModuleYoloDetection
from modules.yolo.pose import ModuleYoloPose
from modules.yolo.segmentation import ModuleYoloSegmentation
from modules.yolo.detection.crop import ModuleYoloDetectionCrop
from modules.yolo.pose.verification import ModuleYoloPoseVerification
from modules.yolo.segmentation.verification import ModuleYoloSegmentationVerification
from entities.person.snapshot import EntityPersonSnapshot

class ApplicationPersonSnapshotBackgroundCreateError(Error):
    pass

class ApplicationPersonSnapshotBackgroundCreate:
    def __init__(
        self,
        repository_queue_person_snapshot_create: RepositoryQueuePersonSnapshotCreate,
        repository_frame: RepositoryFrame,
        yolo_detection: ModuleYoloDetection,
        yolo_pose: ModuleYoloPose,
        yolo_segmentation: ModuleYoloSegmentation,
        yolo_detection_crop: ModuleYoloDetectionCrop,
        yolo_pose_verification: ModuleYoloPoseVerification,
        yolo_segmentation_verification: ModuleYoloSegmentationVerification,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_queue_person_snapshot_feature_extraction: RepositoryQueuePersonSnapshotFeatureExtraction,
    ):
        self.repository_queue_person_snapshot_create = repository_queue_person_snapshot_create
        self.repository_frame = repository_frame
        self.yolo_detection = yolo_detection
        self.yolo_pose = yolo_pose
        self.yolo_segmentation = yolo_segmentation
        self.yolo_detection_crop = yolo_detection_crop
        self.yolo_pose_verification = yolo_pose_verification
        self.yolo_segmentation_verification = yolo_segmentation_verification
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_queue_person_snapshot_feature_extraction = repository_queue_person_snapshot_feature_extraction

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotBackgroundCreate":
        return cls(
            repository_queue_person_snapshot_create=RepositoryQueuePersonSnapshotCreate.create(
                environment),
            repository_frame=RepositoryFrame.create(
                environment),
            yolo_detection=ModuleYoloDetection(),
            yolo_pose=ModuleYoloPose(),
            yolo_segmentation=ModuleYoloSegmentation(),
            yolo_detection_crop=ModuleYoloDetectionCrop(),
            yolo_pose_verification=ModuleYoloPoseVerification(),
            yolo_segmentation_verification=ModuleYoloSegmentationVerification(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            repository_queue_person_snapshot_feature_extraction=RepositoryQueuePersonSnapshotFeatureExtraction.create(
                environment),
        )

    def extract(self) -> None:
        try:
            item = self.repository_queue_person_snapshot_create.dequeue()
            frame = self.repository_frame.find_one(RepositoryFrameFindParams(
                id=item.id,
            ))
            detections = self.yolo_detection.extract(frame.image)
            for detection in detections:
                cropped_image = self.yolo_detection_crop.crop(frame.image, detection)
                yolo_pose = self.yolo_pose.extract(cropped_image)
                yolo_segmentation = self.yolo_segmentation.extract(cropped_image)
                pose_failed = yolo_pose is not None and not self.yolo_pose_verification.verify(yolo_pose)
                segment_failed = not self.yolo_segmentation_verification.verify(yolo_segmentation)
                if pose_failed or segment_failed:
                    continue
                person_snapshot = EntityPersonSnapshot(
                    image_id=frame.id,
                    camera_id=frame.camera_id,
                    view_id=frame.view_id,
                    timestamp=frame.timestamp,
                )
                self.repository_person_snapshot.save(person_snapshot)
                self.repository_queue_person_snapshot_feature_extraction.push(
                    RepositoryQueuePersonSnapshotFeatureExtractionQueueItem(
                        id=person_snapshot.id))
            self.repository_frame.delete(frame)
        except RepositoryQueuePersonSnapshotCreateError as e:
            raise ApplicationPersonSnapshotBackgroundCreateError(e.message)
        except RepositoryFrameError as e:
            raise ApplicationPersonSnapshotBackgroundCreateError(e.message)
        except RepositoryQueuePersonSnapshotFeatureExtractionError as e:
            raise ApplicationPersonSnapshotBackgroundCreateError(e.message)
