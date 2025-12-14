from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreate
from repositories.queue.person_snapshot.create import RepositoryQueuePersonSnapshotCreateError
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtraction
from repositories.queue.person_snapshot.feature_extraction import RepositoryQueuePersonSnapshotFeatureExtractionError
from repositories.frame_image import RepositoryFrameImage
from repositories.frame_image import RepositoryFrameImageFindParams
from repositories.frame_image import RepositoryFrameImageError
from repositories.person.snapshot import RepositoryPersonSnapshot
from environment import Environment
from error import Error
from domain.yolo.detection_model import DomainYoloDetectionModel
from domain.yolo.pose_model import DomainYoloPoseModel
from domain.yolo.segment_model import DomainYoloSegmentModel

class ApplicationPersonSnapshotBackgroundCreateError(Error):
    pass

class ApplicationPersonSnapshotBackgroundCreate:
    def __init__(
        self,
        repository_queue_person_snapshot_create: RepositoryQueuePersonSnapshotCreate,
        repository_frame_image: RepositoryFrameImage,
        detection_model: DomainYoloDetectionModel,
        pose_model: DomainYoloPoseModel,
        segment_model: DomainYoloSegmentModel,
        repository_person_snapshot: RepositoryPersonSnapshot,
        repository_queue_person_snapshot_feature_extraction: RepositoryQueuePersonSnapshotFeatureExtraction,
    ):
        self.repository_queue_person_snapshot_create = repository_queue_person_snapshot_create
        self.repository_frame_image = repository_frame_image
        self.detection_model = detection_model
        self.pose_model = pose_model
        self.segment_model = segment_model
        self.repository_person_snapshot = repository_person_snapshot
        self.repository_queue_person_snapshot_feature_extraction = repository_queue_person_snapshot_feature_extraction

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotBackgroundCreate":
        return cls(
            repository_queue_person_snapshot_create=RepositoryQueuePersonSnapshotCreate.create(
                environment),
            repository_frame_image=RepositoryFrameImage.create(
                environment),
            detection_model=DomainYoloDetectionModel(),
            pose_model=DomainYoloPoseModel(),
            segment_model=DomainYoloSegmentModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            repository_queue_person_snapshot_feature_extraction=RepositoryQueuePersonSnapshotFeatureExtraction.create(
                environment),
        )

    def extract(self) -> None:
        try:
            item = self.repository_queue_person_snapshot_create.dequeue()
            frame_image = self.repository_frame_image.find_first(RepositoryFrameImageFindParams(
                ids=[item.id],
            ))
            person_snapshots = frame_image.crop_person(self.detection_model)
            for person_snapshot in person_snapshots:
                if not person_snapshot.is_full_body(self.pose_model, self.repository_person_snapshot):
                    continue
                if not person_snapshot.is_one_person(self.segment_model, self.repository_person_snapshot):
                    continue
                self.repository_person_snapshot.save(person_snapshot)
            self.repository_frame_image.delete(frame_image)
        except RepositoryQueuePersonSnapshotCreateError as e:
            raise ApplicationPersonSnapshotBackgroundCreateError(e.message)
        except RepositoryFrameImageError as e:
            raise ApplicationPersonSnapshotBackgroundCreateError(e.message)
        except RepositoryQueuePersonSnapshotFeatureExtractionError as e:
            raise ApplicationPersonSnapshotBackgroundCreateError(e.message)
