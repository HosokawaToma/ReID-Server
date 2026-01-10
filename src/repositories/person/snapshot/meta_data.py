from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from migration.models.person_snapshots import MigrationModelPersonSnapshot
from domain.person.snapshot.meta_data import DomainPersonSnapshotMetaData
from domain.person.snapshot.meta_data_sequence import DomainPersonSnapshotMetaDataSequence
from environment import Environment
from error import Error

class RepositoryPersonSnapshotMetaDataError(Error):
    pass

class RepositoryPersonSnapshotMetaDataFindError(RepositoryPersonSnapshotMetaDataError):
    pass

class RepositoryPersonSnapshotMetaData:
    def __init__(self, database: RepositoryUtilDatabase):
        self.database = database

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotMetaData":
        return cls(
            database=RepositoryUtilDatabase.create(environment),
        )

    def _model_to_domain(self, model: MigrationModelPersonSnapshot) -> DomainPersonSnapshotMetaData:
        return DomainPersonSnapshotMetaData(
            id=model.id,
            camera_id=model.camera_id,
            view_id=model.view_id,
            timestamp=model.timestamp,
            is_junk=model.is_junk,
            person_id=model.person_id,
        )

    def find(self, query: RepositoryUtilDatabaseQueryPersonSnapshot | None = None) -> DomainPersonSnapshotMetaDataSequence:
        try:
            with self.database as session:
                session_query = session.query(MigrationModelPersonSnapshot)
                if query is not None:
                    session_query = query.build(session_query)
                models = session_query.all()
                return DomainPersonSnapshotMetaDataSequence(
                    meta_data_list=[self._model_to_domain(model) for model in models],
                )
        except Error as error:
            raise RepositoryPersonSnapshotMetaDataFindError(error) from error
