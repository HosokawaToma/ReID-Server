from database import Database
from error import Error
from database.query.person_snapshot import DatabaseQueryPersonSnapshot
from dto.person.snapshot.meta_data import DtoPersonSnapshotMetaData
from migration.models.person_snapshots import MigrationModelPersonSnapshot
import uuid
from datetime import datetime
from environment import Environment

class DaoPersonSnapshotMetaDataError(Error):
    pass

class DaoPersonSnapshotMetaDataOpenError(DaoPersonSnapshotMetaDataError):
    pass

class DaoPersonSnapshotMetaDataCommitError(DaoPersonSnapshotMetaDataError):
    pass

class DaoPersonSnapshotMetaDataCloseError(DaoPersonSnapshotMetaDataError):
    pass

class DaoPersonSnapshotMetaData:
    def __init__(self, database: Database):
        self.database = database

    @classmethod
    def create(cls, environment: Environment) -> "DaoPersonSnapshotMetaData":
        return cls(
            database=Database.create(environment),
        )

    def _model_to_dto(self, model: MigrationModelPersonSnapshot) -> DtoPersonSnapshotMetaData:
        return DtoPersonSnapshotMetaData(
            id=uuid.UUID(str(model.id)),
            camera_id=int(str(model.camera_id)),
            view_id=int(str(model.view_id)),
            timestamp=datetime.fromisoformat(str(model.timestamp)),
            is_junk=bool(model.is_junk),
            person_id=uuid.UUID(str(model.person_id)) if model.person_id is not None else None,
        )

    def find(self, query: DatabaseQueryPersonSnapshot) -> list[DtoPersonSnapshotMetaData]:
        try:
            with self.database as session:
                session_query = session.query(MigrationModelPersonSnapshot)
                session_query = query.build(session_query)
                models = session_query.all()
                return [self._model_to_dto(model) for model in models]
        except Error as error:
            raise DaoPersonSnapshotMetaDataError(error) from error
