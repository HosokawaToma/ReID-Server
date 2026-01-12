from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.person_snapshot import DtoPersonSnapshot
from modules.reid.model import ModuleReIDModel
from environment import Environment
from error import Error
from background.applications.utils import BackgroundApplicationUtilsBase


class BackgroundApplicationPersonSnapshotFeatureExtractionError(Error):
    pass


class BackgroundApplicationPersonSnapshotFeatureExtraction(BackgroundApplicationUtilsBase):
    def __init__(
        self,
        reid_model: ModuleReIDModel,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.reid_model = reid_model
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "BackgroundApplicationPersonSnapshotFeatureExtraction":
        return cls(
            reid_model=ModuleReIDModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def extract(self) -> DtoPersonSnapshot:
        try:
            person_snapshot = self.repository_person_snapshot.next_feature_extraction()
            person_snapshot.extract_feature(self.reid_model)
            self.repository_person_snapshot.update(person_snapshot)
            self.repository_person_snapshot.push_identify(person_snapshot)
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
            raise BackgroundApplicationPersonSnapshotFeatureExtractionError(error) from error
