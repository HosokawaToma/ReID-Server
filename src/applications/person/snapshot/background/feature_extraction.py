from repositories.person.snapshot import RepositoryPersonSnapshot
from domain.person.snapshot import DomainPersonSnapshot
from modules.reid.model import ModuleReIDModel
from environment import Environment
from error import Error


class ApplicationPersonSnapshotBackgroundFeatureExtractionError(Error):
    pass


class ApplicationPersonSnapshotBackgroundFeatureExtraction:
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
    ) -> "ApplicationPersonSnapshotBackgroundFeatureExtraction":
        return cls(
            reid_model=ModuleReIDModel(),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def extract(self) -> DomainPersonSnapshot:
        try:
            person_snapshot = self.repository_person_snapshot.next_feature_extraction()
            person_snapshot.extract_feature(self.reid_model)
            self.repository_person_snapshot.update(person_snapshot)
            self.repository_person_snapshot.push_identify(person_snapshot)
            return person_snapshot
        except Error as error:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(error) from error
