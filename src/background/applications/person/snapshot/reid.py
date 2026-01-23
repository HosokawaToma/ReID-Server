from repositories.person.snapshot.reid_queue import RepositoryPersonSnapshotReidQueue
from domain.reid.model import DomainReIDModel
from modules.reid.model import ModuleReIDModel
from environment import Environment
from error import Error
from background.applications.utils import BackgroundApplicationUtilsBase
from repositories.person.snapshot import RepositoryPersonSnapshot
from dto.person.snapshot.person_id import DtoPersonSnapshotPersonId


class BackgroundApplicationPersonSnapshotReidError(Error):
    pass


class BackgroundApplicationPersonSnapshotReid(BackgroundApplicationUtilsBase):
    def __init__(
        self,
        reid_model: DomainReIDModel,
        repository_person_snapshot_reid_queue: RepositoryPersonSnapshotReidQueue,
        repository_person_snapshot: RepositoryPersonSnapshot,
    ):
        self.reid_model = reid_model
        self.repository_person_snapshot_reid_queue = repository_person_snapshot_reid_queue
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "BackgroundApplicationPersonSnapshotReid":
        return cls(
            reid_model=DomainReIDModel(model=ModuleReIDModel()),
            repository_person_snapshot_reid_queue=RepositoryPersonSnapshotReidQueue.create(
                environment),
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment),
        )

    def reid(self) -> DtoPersonSnapshotPersonId:
        try:
            person_snapshot_image = self.repository_person_snapshot_reid_queue.pop()
            person_snapshot_feature = person_snapshot_image.extract_feature(self.reid_model)
            nearest_person_snapshot_feature = self.repository_person_snapshot.find_features_by_nearest(person_snapshot_feature)
            person_snapshot_feature.reid(nearest_person_snapshot_feature)
            return DtoPersonSnapshotPersonId(
                id=person_snapshot_feature.id.id,
                person_id=person_snapshot_feature.person_id.id.id if person_snapshot_feature.person_id.id is not None else None,
                is_junk=person_snapshot_feature.person_id.is_junk,
            )
        except Error as error:
            raise BackgroundApplicationPersonSnapshotReidError(error) from error
