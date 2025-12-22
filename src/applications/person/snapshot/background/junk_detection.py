from domain.yolo.detection_model import DomainYoloDetectionModel
from domain.yolo.pose_model import DomainYoloPoseModel
from domain.yolo.segment_model import DomainYoloSegmentModel
from error import Error
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot


class ApplicationPersonSnapshotBackgroundJunkDetectionError(Error):
    pass

class ApplicationPersonSnapshotBackgroundJunkDetection:
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        detection_model: DomainYoloDetectionModel,
        pose_model: DomainYoloPoseModel,
        segment_model: DomainYoloSegmentModel,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.detection_model = detection_model
        self.pose_model = pose_model
        self.segment_model = segment_model

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotBackgroundJunkDetection":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            detection_model=DomainYoloDetectionModel(),
            pose_model=DomainYoloPoseModel(),
            segment_model=DomainYoloSegmentModel(),
        )

    def detect(self) -> None:
        try:
            person_snapshot = self.repository_person_snapshot.next_junk_detection()
            person_snapshot.detect_junk(self.pose_model, self.segment_model)
            self.repository_person_snapshot.update(person_snapshot)
            if not person_snapshot.is_junk:
                self.repository_person_snapshot.push_feature_extraction(person_snapshot)
        except Error as error:
            raise ApplicationPersonSnapshotBackgroundJunkDetectionError(error) from error
