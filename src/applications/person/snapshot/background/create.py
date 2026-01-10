from repositories.frame_image import RepositoryFrameImage
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.frame_image.meta_data import DtoFrameImageMetaData
from environment import Environment
from domain.yolo.detection_model import DomainYoloDetectionModel
from error import Error

class ApplicationPersonSnapshotBackgroundCreateError(Error):
    pass

class ApplicationPersonSnapshotBackgroundCreate:
    def __init__(
        self,
        repository_frame_image: RepositoryFrameImage,
        detection_model: DomainYoloDetectionModel,
        repository_person_snapshot: RepositoryPersonSnapshot,
        is_delete_unnecessary_images: bool,
    ):
        self.repository_frame_image = repository_frame_image
        self.detection_model = detection_model
        self.repository_person_snapshot = repository_person_snapshot
        self.is_delete_unnecessary_images = is_delete_unnecessary_images

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotBackgroundCreate":
        return cls(
            repository_frame_image=RepositoryFrameImage.create(
                environment),
            detection_model=DomainYoloDetectionModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            is_delete_unnecessary_images=environment.is_delete_unnecessary_images,
        )

    def save(self) -> DtoFrameImageMetaData:
        try:
            frame_image = self.repository_frame_image.next_person_snapshot_create()
            person_snapshots = frame_image.crop_person(self.detection_model)
            for person_snapshot in person_snapshots:
                self.repository_person_snapshot.save(person_snapshot)
                self.repository_person_snapshot.push_junk_detection(person_snapshot)
            if self.is_delete_unnecessary_images:
                self.repository_frame_image.delete(frame_image)
            return DtoFrameImageMetaData(
                id=frame_image.id,
                camera_id=frame_image.camera_id,
                view_id=frame_image.view_id,
                timestamp=frame_image.timestamp,
            )
        except Error as error:
            raise ApplicationPersonSnapshotBackgroundCreateError(error) from error
