from domain.yolo.pose_model import DomainYoloPoseModel
from domain.yolo.segment_model import DomainYoloSegmentModel
from error import Error
from environment import Environment
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.person_snapshot import DtoPersonSnapshot
from background.application.utils import BackgroundApplicationUtilsBase

class BackgroundApplicationPersonSnapshotJunkDetectionError(Error):
    pass

class BackgroundApplicationPersonSnapshotJunkDetection(BackgroundApplicationUtilsBase):
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        pose_model: DomainYoloPoseModel,
        segment_model: DomainYoloSegmentModel,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.pose_model = pose_model
        self.segment_model = segment_model

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundApplicationPersonSnapshotJunkDetection":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
            pose_model=DomainYoloPoseModel(),
            segment_model=DomainYoloSegmentModel(),
        )

    def detect(self) -> DtoPersonSnapshot:
        try:
            person_snapshot = self.repository_person_snapshot.next_junk_detection()
            person_snapshot.detect_junk(self.pose_model, self.segment_model)
            self.repository_person_snapshot.update(person_snapshot)
            if not person_snapshot.is_junk:
                self.repository_person_snapshot.push_feature_extraction(person_snapshot)
            return DtoPersonSnapshot(
                id=person_snapshot.id,
                camera_id=person_snapshot.camera_id,
                view_id=person_snapshot.view_id,
                timestamp=person_snapshot.timestamp,
                is_junk=person_snapshot.is_junk,
                person_id=person_snapshot.person_id,
                feature=person_snapshot.feature,
            )
        except Error as error:
            raise BackgroundApplicationPersonSnapshotJunkDetectionError(error) from error
