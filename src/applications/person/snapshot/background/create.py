from repositories.frame_image import RepositoryFrameImage
from repositories.person.snapshot import RepositoryPersonSnapshot
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
        is_delete_unnecessary_images: bool,
    ):
        self.repository_frame_image = repository_frame_image
        self.detection_model = detection_model
        self.pose_model = pose_model
        self.segment_model = segment_model
        self.repository_person_snapshot = repository_person_snapshot
        self.is_delete_unnecessary_images = is_delete_unnecessary_images

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
            is_delete_unnecessary_images=environment.is_delete_unnecessary_images,
        )

    def save(self) -> None:
        try:
            frame_image = self.repository_frame_image.next_person_snapshot_create()
            person_snapshots = frame_image.crop_person(self.detection_model)
            for person_snapshot in person_snapshots:
                if not person_snapshot.is_full_body(self.pose_model):
                    if not self.is_delete_unnecessary_images:
                        self.repository_frame_image.save(frame_image)
                    continue
                if not person_snapshot.is_one_person(self.segment_model):
                    if not self.is_delete_unnecessary_images:
                        self.repository_frame_image.save(frame_image)
                    continue
                self.repository_person_snapshot.save(person_snapshot)
                self.repository_person_snapshot.push_feature_extraction(person_snapshot)
            if self.is_delete_unnecessary_images:
                self.repository_frame_image.delete(frame_image)
        except Error as error:
            raise ApplicationPersonSnapshotBackgroundCreateError(error) from error
