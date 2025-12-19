from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotNextQueueError
from repositories.person.snapshot import RepositoryPersonSnapshotUpdateError
from repositories.person.snapshot import RepositoryPersonSnapshotPushQueueError
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
            person_snapshot = self.repository_person_snapshot.next_queue(task_name="person_snapshot:feature_extraction")
            person_snapshot.extract_feature(self.reid_model)
            self.repository_person_snapshot.update(person_snapshot)
            self.repository_person_snapshot.push_queue(task_name="person_snapshot:identify", person_snapshot=person_snapshot)
            return person_snapshot
        except RepositoryPersonSnapshotNextQueueError as error:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(error.message) from error
        except RepositoryPersonSnapshotUpdateError as error:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(error.message) from error
        except RepositoryPersonSnapshotPushQueueError as error:
            raise ApplicationPersonSnapshotBackgroundFeatureExtractionError(error.message) from error
