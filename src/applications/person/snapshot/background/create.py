from repositories.frame_image import RepositoryFrameImage
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.frame_image import RepositoryFrameImageNextQueueError
from repositories.person.snapshot import RepositoryPersonSnapshotSaveError
from repositories.person.snapshot import RepositoryPersonSnapshotPushQueueError
from repositories.frame_image import RepositoryFrameImageDeleteError
from environment import Environment
from domain.yolo.detection_model import DomainYoloDetectionModel
from domain.yolo.pose_model import DomainYoloPoseModel
from domain.yolo.segment_model import DomainYoloSegmentModel
from error import Error

class ApplicationPersonSnapshotBackgroundCreateError(Error):
    pass

class ApplicationPersonSnapshotBackgroundCreate:
    def __init__(
        self,
        repository_frame_image: RepositoryFrameImage,
        detection_model: DomainYoloDetectionModel,
        pose_model: DomainYoloPoseModel,
        segment_model: DomainYoloSegmentModel,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.repository_frame_image = repository_frame_image
        self.detection_model = detection_model
        self.pose_model = pose_model
        self.segment_model = segment_model
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotBackgroundCreate":
        return cls(
            repository_frame_image=RepositoryFrameImage.create(
                environment),
            detection_model=DomainYoloDetectionModel(),
            pose_model=DomainYoloPoseModel(),
            segment_model=DomainYoloSegmentModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def save(self) -> None:
        try:
            frame_image = self.repository_frame_image.next_queue(queue_name="frame_image:person_snapshot_create")
            person_snapshots = frame_image.crop_person(self.detection_model)
            for person_snapshot in person_snapshots:
                if not person_snapshot.is_full_body(self.pose_model):
                    continue
                if not person_snapshot.is_one_person(self.segment_model):
                    continue
                self.repository_person_snapshot.save(person_snapshot)
                self.repository_person_snapshot.push_queue(task_name="person_snapshot:feature_extraction", person_snapshot=person_snapshot)
            self.repository_frame_image.delete(frame_image)
        except RepositoryFrameImageNextQueueError as error:
            raise ApplicationPersonSnapshotBackgroundCreateError(error.message) from error
        except RepositoryPersonSnapshotSaveError as error:
            raise ApplicationPersonSnapshotBackgroundCreateError(error.message) from error
        except RepositoryPersonSnapshotPushQueueError as error:
            raise ApplicationPersonSnapshotBackgroundCreateError(error.message) from error
        except RepositoryFrameImageDeleteError as error:
            raise ApplicationPersonSnapshotBackgroundCreateError(error.message) from error
