from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneParams
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneFilters
from repositories.person.snapshot import RepositoryPersonSnapshotFindOneOrdering
from repositories.person.snapshot import PersonSnapshotNotFoundError
from modules.reid.identifier import ModuleReIDIdentifier
from modules.reid.identifier import ReIDIdentifierThresholdError
from environment import Environment

from dataclasses import dataclass
import uuid

@dataclass
class ApplicationPersonSnapshotIdentifyParams:
    person_snapshot_id: uuid.UUID

class ApplicationPersonSnapshotIdentifyError(Exception):
    pass

class ApplicationPersonSnapshotMissingFeatureError(ApplicationPersonSnapshotIdentifyError):
    pass

class ApplicationPersonSnapshotNotFoundError(ApplicationPersonSnapshotIdentifyError):
    pass

class ApplicationPersonSnapshotThresholdError(ApplicationPersonSnapshotIdentifyError):
    pass

class ApplicationPersonSnapshotIdentify:
    def __init__(
        self,
        repository_person_snapshot: RepositoryPersonSnapshot,
        reid_identifier: ModuleReIDIdentifier,
    ):
        self.repository_person_snapshot = repository_person_snapshot
        self.reid_identifier = reid_identifier

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotIdentify":
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(environment),
            reid_identifier=ModuleReIDIdentifier(threshold=0.895),
        )

    def identify(self, params: ApplicationPersonSnapshotIdentifyParams) -> None:
        try:
            person_snapshot = self.repository_person_snapshot.find_first(
                RepositoryPersonSnapshotFindOneParams(
                    filters=RepositoryPersonSnapshotFindOneFilters(
                        ids=[params.person_snapshot_id],
                    ),
                )
            )
            if person_snapshot.feature is None:
                raise ApplicationPersonSnapshotMissingFeatureError
            nearest_person_snapshot = self.repository_person_snapshot.find_first(
                RepositoryPersonSnapshotFindOneParams(
                    ordering=RepositoryPersonSnapshotFindOneOrdering(
                        feature_to_nearest=person_snapshot.feature,
                    ),
                )
            )
            if nearest_person_snapshot.feature is None:
                raise ApplicationPersonSnapshotMissingFeatureError
            self.reid_identifier.guarantee(
                person_snapshot.feature,
                nearest_person_snapshot.feature,
            )
            person_snapshot.person_id = nearest_person_snapshot.person_id
            self.repository_person_snapshot.update(person_snapshot)
        except ApplicationPersonSnapshotMissingFeatureError:
            raise ApplicationPersonSnapshotMissingFeatureError
        except PersonSnapshotNotFoundError:
            raise ApplicationPersonSnapshotNotFoundError
        except ReIDIdentifierThresholdError:
            raise ApplicationPersonSnapshotThresholdError
